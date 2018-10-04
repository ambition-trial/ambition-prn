from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from edc_action_item import Action, HIGH_PRIORITY, site_action_items
from edc_constants.constants import CLOSED


DEATH_REPORT_ACTION = 'submit-death-report'
DEATH_REPORT_TMG_ACTION = 'submit-death-report-tmg'
PROTOCOL_DEVIATION_VIOLATION_ACTION = 'submit-protocol-deviation-violation'
STUDY_TERMINATION_CONCLUSION_ACTION = 'submit-study-termination-conclusion'
STUDY_TERMINATION_CONCLUSION_ACTION_W10 = 'submit-w10-study-termination-conclusion'


class ProtocolDeviationViolationAction(Action):
    name = PROTOCOL_DEVIATION_VIOLATION_ACTION
    display_name = 'Submit Protocol Deviation/Violation Report'
    reference_model = 'ambition_prn.protocoldeviationviolation'
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = 'ambition_prn_admin'
    priority = HIGH_PRIORITY

    def close_action_item_on_save(self):
        return self.reference_obj.report_status == CLOSED


class StudyTerminationConclusionAction(Action):
    name = STUDY_TERMINATION_CONCLUSION_ACTION
    display_name = 'Submit Study Termination/Conclusion Report'
    reference_model = 'ambition_prn.studyterminationconclusion'
    show_link_to_changelist = True
    admin_site_name = 'ambition_prn_admin'
    priority = HIGH_PRIORITY


class StudyTerminationConclusionW10Action(Action):
    name = STUDY_TERMINATION_CONCLUSION_ACTION_W10
    display_name = 'Submit W10 Study Termination/Conclusion Report'
    reference_model = 'ambition_prn.studyterminationconclusionw10'
    show_link_to_changelist = True
    admin_site_name = 'ambition_prn_admin'
    priority = HIGH_PRIORITY


class DeathReportAction(Action):
    name = DEATH_REPORT_ACTION
    display_name = 'Submit Death Report'
    reference_model = 'ambition_prn.deathreport'
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = 'ambition_prn_admin'
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        """Adds 1 DEATHReportTMG if not yet created.
        """
        try:
            self.action_item_model_cls().objects.get(
                parent_action_identifier=self.reference_obj.action_identifier,
                related_action_identifier=self.reference_obj.action_identifier,
                action_type__name=DeathReportTmgAction.name)
        except ObjectDoesNotExist:
            next_actions = [DeathReportTmgAction]
        else:
            next_actions = []

        on_schedule_w10_model_cls = django_apps.get_model(
            'ambition_prn.onschedulew10')
        try:
            on_schedule_w10_model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            next_actions.append(StudyTerminationConclusionAction)
        else:
            next_actions.append(StudyTerminationConclusionW10Action)
        return next_actions


class DeathReportTmgAction(Action):
    name = DEATH_REPORT_TMG_ACTION
    display_name = 'TMG Death Report pending'
    reference_model = 'ambition_prn.deathreporttmg'
    related_reference_model = 'ambition_prn.deathreport'
    related_reference_fk_attr = 'death_report'
    priority = HIGH_PRIORITY
    create_by_user = False
    color_style = 'info'
    show_link_to_changelist = True
    admin_site_name = 'ambition_prn_admin'
    instructions = mark_safe(
        f'This report is to be completed by the TMG only.')
    try:
        email_recipients = [settings.EMAIL_CONTACTS.get('tmg')]
    except AttributeError:
        email_recipients = []

    def close_action_item_on_save(self):
        if (self.reference_obj.death_report.cause_of_death
                == self.reference_obj.cause_of_death):
            self.delete_children_if_new(
                parent_action_identifier=self.action_identifier)
        return self.reference_obj.report_status == CLOSED

    def get_next_actions(self):
        """Returns an second DeathReportTmgAction if the
        submitted report does not match the cause of death
        of the original death report.

        Also, no more than two DeathReportTmgAction can exist.
        """
        next_actions = []
        related_reference_obj = self.related_reference_model_cls().objects.get(
            action_identifier=self.related_action_identifier)
        related_action_identifier = related_reference_obj.action_identifier
        try:
            self.action_item_model_cls().objects.get(
                parent_action_identifier=related_action_identifier,
                related_action_identifier=related_action_identifier,
                action_type__name=self.name)
        except ObjectDoesNotExist:
            pass
        else:
            if (self.action_item_model_cls().objects.filter(
                related_action_identifier=related_action_identifier,
                    action_type__name=self.name).count() < 2):
                if (self.reference_obj.cause_of_death
                        != related_reference_obj.cause_of_death):
                    next_actions = [self]
        return next_actions


site_action_items.register(DeathReportAction)
site_action_items.register(DeathReportTmgAction)
site_action_items.register(ProtocolDeviationViolationAction)
site_action_items.register(StudyTerminationConclusionAction)
site_action_items.register(StudyTerminationConclusionW10Action)
