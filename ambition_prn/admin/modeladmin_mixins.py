from django.conf import settings
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminAuditFieldsMixin,
    ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin,
)
from edc_notification import NotificationModelAdminMixin
from edc_sites.admin import ModelAdminSiteMixin
from edc_subject_dashboard import ModelAdminSubjectDashboardMixin


class ModelAdminMixin(
    ModelAdminNextUrlRedirectMixin,
    NotificationModelAdminMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,
    ModelAdminAuditFieldsMixin,
    ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin,
    ModelAdminSubjectDashboardMixin,
    ModelAdminSiteMixin,
):

    list_per_page = 10
    date_hierarchy = "modified"
    empty_value_display = "-"
    subject_dashboard_url = "subject_dashboard_url"

    post_url_on_delete_name = settings.DASHBOARD_URL_NAMES.get(subject_dashboard_url)

    def post_url_on_delete_kwargs(self, request, obj):
        return dict(subject_identifier=obj.subject_identifier)
