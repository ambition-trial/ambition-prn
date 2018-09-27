from ambition_rando.tests import AmbitionTestCaseMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.test import TestCase, tag
from edc_action_item.models.action_item import ActionItem
from edc_base.utils import get_utcnow
from edc_constants.constants import CLOSED, NEW, NO
from edc_facility.import_holidays import import_holidays
from edc_registration.models import RegisteredSubject
from model_mommy import mommy

from ..action_items import DeathReportAction, DEATH_REPORT_TMG_ACTION
from ..constants import CRYTOCOCCAL_MENINGITIS, MALIGNANCY


class TestDeathReport(AmbitionTestCaseMixin, TestCase):

    def setUp(self):
        super().setUp()
        import_holidays()
        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier)

    def test_add_death_report_action(self):
        """Note, death report action is a "singleton" action.
        """
        action = DeathReportAction(subject_identifier=self.subject_identifier)
        self.assertEqual(ActionItem.objects.all().count(), 1)
        action_item = ActionItem.objects.get(
            action_identifier=action.action_identifier)

        # fill on death report
        death_report = mommy.make_recipe(
            'ambition_prn.deathreport',
            subject_identifier=self.subject_identifier)
        self.assertEqual(action.action_identifier,
                         death_report.action_identifier)

        # attempt to create a new action
        action = DeathReportAction(subject_identifier=self.subject_identifier)
        # show it just picks up existing action
        self.assertEqual(action.action_identifier,
                         action_item.action_identifier)

        # try to fill in another death report, raises IntegrityError
        self.assertRaises(
            IntegrityError,
            mommy.make_recipe,
            'ambition_prn.deathreport',
            subject_identifier=self.subject_identifier)

    def test_death_report_action_urls(self):

        action = DeathReportAction(subject_identifier=self.subject_identifier)
        action_item = ActionItem.objects.get(
            action_identifier=action.action_identifier)
        self.assertEqual(
            action.reference_url(
                action_item=action_item, reference_obj=None),
            f'/admin/ambition_prn/deathreport/add/')

        death_report = mommy.make_recipe(
            'ambition_prn.deathreport',
            subject_identifier=self.subject_identifier)

        action = DeathReportAction(
            subject_identifier=self.subject_identifier)

        self.assertEqual(
            action.reference_url(
                action_item=action_item, reference_obj=death_report),
            f'/admin/ambition_prn/deathreport/{str(death_report.pk)}/change/')

    def test_death_report_action_creates_next_actions(self):
        DeathReportAction(subject_identifier=self.subject_identifier)
        mommy.make_recipe(
            'ambition_prn.deathreport',
            subject_identifier=self.subject_identifier)
        names = [
            obj.action_type.name for obj in ActionItem.objects.filter(status=NEW)]
        names.sort()
        self.assertEqual(
            names, ['submit-death-report-tmg', 'submit-study-termination-conclusion'])

    def test_death_report_closes_action(self):
        DeathReportAction(subject_identifier=self.subject_identifier)
        death_report = mommy.make_recipe(
            'ambition_prn.deathreport',
            subject_identifier=self.subject_identifier)
        obj = ActionItem.objects.get(
            action_identifier=death_report.action_identifier)
        self.assertEqual(obj.status, CLOSED)

    def test_add_tmg_death_report_action_cause_matches(self):

        death_report_action = DeathReportAction(
            subject_identifier=self.subject_identifier)
        death_report = mommy.make_recipe(
            'ambition_prn.deathreport',
            subject_identifier=self.subject_identifier,
            cause_of_death=CRYTOCOCCAL_MENINGITIS)
        self.assertEqual(death_report_action.action_identifier,
                         death_report.action_identifier)

        # assert death report creates one TMG Death Report Action
        self.assertEqual(ActionItem.objects.filter(
            action_type__name=DEATH_REPORT_TMG_ACTION).count(), 1)

        # fill in TMG report with matching cause of death
        death_report_tmg = mommy.make_recipe(
            'ambition_prn.deathreporttmg',
            subject_identifier=self.subject_identifier,
            death_report=death_report,
            cause_of_death=CRYTOCOCCAL_MENINGITIS,
            related_reference_identifier=death_report_action.action_identifier,
            parent_reference_identifier=death_report_action.action_identifier
        )
        self.assertEqual(
            death_report_tmg.parent_reference_identifier,
            death_report.action_identifier)

        self.assertEqual(
            death_report_tmg.related_reference_identifier,
            death_report.action_identifier)

        # assert a second TMG Death Report Action is NOT created
        # because the cause of death matches
        self.assertEqual(ActionItem.objects.filter(
            action_type__name=DEATH_REPORT_TMG_ACTION).count(), 1)

    def test_add_two_tmg_death_report_action_cause_not_matching(self):

        death_report_action = DeathReportAction(
            subject_identifier=self.subject_identifier)
        death_report = mommy.make_recipe(
            'ambition_prn.deathreport',
            subject_identifier=self.subject_identifier,
            cause_of_death=CRYTOCOCCAL_MENINGITIS)

        # assert death report creates one TMG Death Report Action
        try:
            action_item = ActionItem.objects.get(
                action_type__name=DEATH_REPORT_TMG_ACTION)
        except ObjectDoesNotExist:
            self.fail('Action item unexpectedly does not exist')

        self.assertEqual(ActionItem.objects.filter(
            action_type__name=DEATH_REPORT_TMG_ACTION).count(), 1)

        # fill in TMG report with non-matching cause of death
        death_report_tmg1 = mommy.make_recipe(
            'ambition_prn.deathreporttmg',
            subject_identifier=self.subject_identifier,
            death_report=death_report,
            cause_of_death=MALIGNANCY,
            cause_of_death_agreed=NO,
            report_status=CLOSED,
            report_closed_datetime=get_utcnow(),
            action_identifier=action_item.action_identifier,
            related_reference_identifier=death_report.action_identifier,
            parent_reference_identifier=death_report.action_identifier)

        action_item = ActionItem.objects.get(
            action_identifier=death_report_tmg1.action_identifier,
            action_type__name=DEATH_REPORT_TMG_ACTION)

        # assert a second TMG Death Report Action is created
        # by death_report_tmg because the cause of death matches
        self.assertEqual(ActionItem.objects.filter(
            related_reference_identifier=death_report.action_identifier,
            action_type__name=DEATH_REPORT_TMG_ACTION,
            status=CLOSED).count(), 1)
        self.assertEqual(ActionItem.objects.filter(
            related_reference_identifier=death_report.action_identifier,
            action_type__name=DEATH_REPORT_TMG_ACTION,
            status=NEW).count(), 1)
        self.assertEqual(ActionItem.objects.filter(
            action_type__name=DEATH_REPORT_TMG_ACTION).count(), 2)

        # resave
        death_report_tmg1.save()

        # still 2
        self.assertEqual(ActionItem.objects.filter(
            action_type__name=DEATH_REPORT_TMG_ACTION).count(), 2)

        # fill in second TMG report with any cause of death
        death_report_tmg2 = mommy.make_recipe(
            'ambition_prn.deathreporttmg',
            subject_identifier=self.subject_identifier,
            death_report=death_report,
            cause_of_death=MALIGNANCY,
            related_reference_identifier=death_report_action.action_identifier,
            parent_reference_identifier=death_report_tmg1.action_identifier)

        # still 2
        self.assertEqual(ActionItem.objects.filter(
            action_type__name=DEATH_REPORT_TMG_ACTION).count(), 2)

        death_report_tmg2.save()

        # still 2
        self.assertEqual(ActionItem.objects.filter(
            action_type__name=DEATH_REPORT_TMG_ACTION).count(), 2)

        # resave
        death_report.save()

        # still 2
        self.assertEqual(ActionItem.objects.filter(
            action_type__name=DEATH_REPORT_TMG_ACTION).count(), 2)

        # resave
        death_report_tmg1.save()

        # still 2
        self.assertEqual(ActionItem.objects.filter(
            action_type__name=DEATH_REPORT_TMG_ACTION).count(), 2)
