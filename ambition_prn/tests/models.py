from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_visit_tracking.model_mixins import VisitModelMixin


class SubjectConsent(models.Model):

    screening_identifier = models.CharField(max_length=50)

    subject_identifier = models.CharField(max_length=50)


class SubjectVisit(VisitModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50)

    class Meta(VisitModelMixin.Meta):
        pass


class PatientHistory(BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    first_arv_regimen = models.CharField(
        max_length=50)
