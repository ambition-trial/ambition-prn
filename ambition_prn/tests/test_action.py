from ambition_rando.tests import AmbitionTestCaseMixin
from django.test import TestCase, tag
from edc_action_item import SingletonActionItemError
from edc_action_item.models.action_item import ActionItem
from edc_constants.constants import CLOSED, NEW
from edc_facility.import_holidays import import_holidays
from edc_registration.models import RegisteredSubject
from model_mommy import mommy

from ..action_items import DeathReportAction
from django.db.utils import IntegrityError


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
