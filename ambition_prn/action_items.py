from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
        self.delete_if_new(action_cls=DeathReportTmgAction)
        next_actions = [DeathReportTmgAction]
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

    def close_action_item_on_save(self):
        self.delete_if_new(action_cls=self)
        return self.reference_obj.report_status == CLOSED

    def get_next_actions(self):
        next_actions = []
        self.delete_if_new(action_cls=self)
        try:
            self.reference_model_cls().objects.get(
                death_report=self.reference_obj.death_report)
        except MultipleObjectsReturned:
            pass
        else:
            if self.reference_obj.report_status == CLOSED:
                if (self.reference_obj.death_report.cause_of_death
                        != self.reference_obj.cause_of_death):
                    next_actions = [self]
        return next_actions


site_action_items.register(DeathReportAction)
site_action_items.register(DeathReportTmgAction)
site_action_items.register(ProtocolDeviationViolationAction)
site_action_items.register(StudyTerminationConclusionAction)
site_action_items.register(StudyTerminationConclusionW10Action)
