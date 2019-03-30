from ambition_ae.constants import AE_INITIAL_ACTION, AE_FOLLOWUP_ACTION
from ambition_subject.constants import BLOOD_RESULTS_ACTION
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.safestring import mark_safe
from edc_action_item import ActionWithNotification, HIGH_PRIORITY, site_action_items
from edc_constants.constants import CLOSED

from .constants import DEATH_REPORT_ACTION, DEATH_REPORT_TMG_ACTION
from .constants import PROTOCOL_DEVIATION_VIOLATION_ACTION
from .constants import STUDY_TERMINATION_CONCLUSION_ACTION
from .constants import STUDY_TERMINATION_CONCLUSION_ACTION_W10


class ProtocolDeviationViolationAction(ActionWithNotification):
    name = PROTOCOL_DEVIATION_VIOLATION_ACTION
    display_name = "Submit Protocol Deviation/Violation Report"
    notification_display_name = "Protocol Deviation/Violation Report"
    parent_action_names = []
    reference_model = "ambition_prn.protocoldeviationviolation"
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "ambition_prn_admin"
    priority = HIGH_PRIORITY

    def close_action_item_on_save(self):
        return self.reference_obj.report_status == CLOSED


class StudyTerminationConclusionAction(ActionWithNotification):
    name = STUDY_TERMINATION_CONCLUSION_ACTION
    display_name = "Submit Study Termination/Conclusion Report"
    notification_display_name = "Study Termination/Conclusion Report"
    parent_action_names = [
        BLOOD_RESULTS_ACTION,
        DEATH_REPORT_ACTION,
        AE_FOLLOWUP_ACTION,
    ]
    reference_model = "ambition_prn.studyterminationconclusion"
    show_link_to_changelist = True
    admin_site_name = "ambition_prn_admin"
    priority = HIGH_PRIORITY


class StudyTerminationConclusionW10Action(ActionWithNotification):
    name = STUDY_TERMINATION_CONCLUSION_ACTION_W10
    display_name = "Submit W10 Study Termination/Conclusion Report"
    notification_display_name = "W10 Study Termination/Conclusion Report"
    parent_action_names = [DEATH_REPORT_ACTION]
    reference_model = "ambition_prn.studyterminationconclusionw10"
    show_link_to_changelist = True
    admin_site_name = "ambition_prn_admin"
    priority = HIGH_PRIORITY


class DeathReportAction(ActionWithNotification):
    name = DEATH_REPORT_ACTION
    display_name = "Submit Death Report"
    notification_display_name = "Death Report"
    reference_model = "ambition_prn.deathreport"
    parent_action_names = [AE_INITIAL_ACTION, AE_FOLLOWUP_ACTION]
    show_link_to_changelist = True
    show_link_to_add = True
    admin_site_name = "ambition_prn_admin"
    priority = HIGH_PRIORITY
    singleton = True
    dirty_fields = ["cause_of_death"]

    def get_next_actions(self):
        """Adds 1 DEATHReportTMG if not yet created and
        STUDY_TERMINATION_CONCLUSION if required.
        """
        # DEATH_REPORT_TMG_ACTION
        try:
            self.action_item_model_cls().objects.get(
                parent_action_item=self.reference_obj.action_item,
                related_action_item=self.reference_obj.action_item,
                action_type__name=DEATH_REPORT_TMG_ACTION,
            )
        except ObjectDoesNotExist:
            next_actions = [DEATH_REPORT_TMG_ACTION]
        else:
            next_actions = []

        # STUDY_TERMINATION_CONCLUSION_ACTION
        on_schedule_w10_model_cls = django_apps.get_model(
            "ambition_prn.onschedulew10")
        off_schedule_w10_cls = django_apps.get_model(
            "ambition_prn.studyterminationconclusionw10"
        )
        off_schedule_cls = django_apps.get_model(
            "ambition_prn.studyterminationconclusion"
        )
        try:
            on_schedule_w10_model_cls.objects.get(
                subject_identifier=self.subject_identifier
            )
        except ObjectDoesNotExist:
            try:
                off_schedule_cls.objects.get(
                    subject_identifier=self.subject_identifier)
            except ObjectDoesNotExist:
                next_actions.append(STUDY_TERMINATION_CONCLUSION_ACTION)
        else:
            try:
                off_schedule_w10_cls.objects.get(
                    subject_identifier=self.subject_identifier
                )
            except ObjectDoesNotExist:
                next_actions.append(STUDY_TERMINATION_CONCLUSION_ACTION_W10)
        return next_actions


class DeathReportTmgAction(ActionWithNotification):
    name = DEATH_REPORT_TMG_ACTION
    display_name = "TMG Death Report pending"
    notification_display_name = "TMG Death Report"
    parent_action_names = [DEATH_REPORT_ACTION, DEATH_REPORT_TMG_ACTION]
    reference_model = "ambition_prn.deathreporttmg"
    related_reference_model = "ambition_prn.deathreport"
    related_reference_fk_attr = "death_report"
    priority = HIGH_PRIORITY
    create_by_user = False
    color_style = "info"
    show_link_to_changelist = True
    admin_site_name = "ambition_prn_admin"
    instructions = mark_safe(
        f"This report is to be completed by the TMG only.")
    #     try:
    #         email_recipients = [settings.EMAIL_CONTACTS.get('tmg')]
    #     except AttributeError:
    #         email_recipients = []

    def close_action_item_on_save(self):
        if (
            self.reference_obj.death_report.cause_of_death
            == self.reference_obj.cause_of_death
        ):
            self.delete_children_if_new(parent_action_item=self.action_item)
        return self.reference_obj.report_status == CLOSED

    def get_next_actions(self):
        """Returns an second DeathReportTmgAction if the
        submitted report does not match the cause of death
        of the original death report.

        Also, no more than two DeathReportTmgAction can exist.
        """
        next_actions = []
        try:
            self.action_item_model_cls().objects.get(
                parent_action_item=self.related_action_item,
                related_action_item=self.related_action_item,
                action_type__name=self.name,
            )
        except ObjectDoesNotExist:
            pass
        except MultipleObjectsReturned:
            # because more than one action item has the same
            # parent_action_item and related_action_item. this
            # only occurs for older data.
            pass
        else:
            if (
                self.action_item_model_cls()
                .objects.filter(
                    related_action_item=self.related_action_item,
                    action_type__name=self.name,
                )
                .count()
                < 2
            ):
                if (
                    self.reference_obj.cause_of_death
                    != self.related_action_item.reference_obj.cause_of_death
                ):
                    next_actions = ["self"]
        return next_actions


site_action_items.register(DeathReportAction)
site_action_items.register(DeathReportTmgAction)
site_action_items.register(ProtocolDeviationViolationAction)
site_action_items.register(StudyTerminationConclusionAction)
site_action_items.register(StudyTerminationConclusionW10Action)
