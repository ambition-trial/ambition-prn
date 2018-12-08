from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_managers.historical_records import HistoricalRecords
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_visit_tracking.managers import VisitModelManager, CrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin
from edc_visit_tracking.model_mixins.visit_model_mixin.visit_model_mixin import VisitModelMixin


class SubjectVisit(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class Week2(BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)
