from ambition_rando.tests import AmbitionTestCaseMixin
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE, DEAD
from edc_list_data import site_list_data
from edc_registration.models import RegisteredSubject

from ..constants import CONSENT_WITHDRAWAL
from ..form_validators import StudyTerminationConclusionFormValidator
from ..models import DeathReport


class TestStudyTerminationConclusionFormValidator(AmbitionTestCaseMixin, TestCase):

    @classmethod
    def setUpClass(cls):
        site_list_data.autodiscover()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):

        self.subject_identifier = '12345'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier)

    def test_termination_reason_death_no_death_form_invalid(self):

        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'termination_reason': DEAD,
                        'death_date': get_utcnow().date()}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('termination_reason', form_validator._errors)

    def test_yes_discharged_after_initial_admission_none_date_discharged(self):
        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'discharged_after_initial_admission': YES,
                        'initial_discharge_date': None}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('initial_discharge_date', form_validator._errors)

    def test_no_discharged_after_initial_admission_with_date_discharged(self):
        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'discharged_after_initial_admission': NO,
                        'initial_discharge_date': get_utcnow}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('initial_discharge_date', form_validator._errors)

    def test_no_discharged_after_initial_admission_readmission_invalid(self):
        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'discharged_after_initial_admission': NO,
                        'initial_discharge_date': None,
                        'readmission_after_initial_discharge': YES}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(
            'readmission_after_initial_discharge', form_validator._errors)

    def ttest_no_discharged_after_initial_admission_no_readmission_valid(self):
        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'discharged_after_initial_admission': NO,
                        'initial_discharge_date': None,
                        'readmission_after_initial_discharge': NOT_APPLICABLE}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_yes_readmission_none_readmission_date(self):
        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'readmission_after_initial_discharge': YES,
                        'readmission_date': None}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('readmission_date', form_validator._errors)

    def test_no_readmission_with_readmission_date(self):
        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'readmission_after_initial_discharge': NO,
                        'readmission_date': get_utcnow}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('readmission_date', form_validator._errors)

    def test_died_no_death_date_invalid(self):
        DeathReport.objects.create(
            subject_identifier=self.subject_identifier,
            death_datetime=get_utcnow(),
            study_day=1)

        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'termination_reason': DEAD,
                        'death_date': None}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('death_date', form_validator._errors)

    def test_died_death_date_mismatch(self):
        DeathReport.objects.create(
            subject_identifier=self.subject_identifier,
            death_datetime=get_utcnow(),
            study_day=1)

        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'termination_reason': DEAD,
                        'death_date': date(2011, 1, 1)}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('death_date', form_validator._errors)

    def test_died_death_date_ok(self):
        dte = get_utcnow()
        DeathReport.objects.create(
            subject_identifier=self.subject_identifier,
            death_datetime=get_utcnow(),
            study_day=1)

        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'termination_reason': DEAD,
                        'death_date': dte.date()}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_died_death_date_change(self):
        dte = get_utcnow()
        DeathReport.objects.create(
            subject_identifier=self.subject_identifier,
            death_datetime=get_utcnow(),
            study_day=1)

        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'termination_reason': DEAD,
                        'death_date': dte.date()}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_twilling_to_complete_10w_withdrawal_of_consent(self):
        """ Asserts willing_to_complete_10w when termination reason
            is consent_withdrawn.
        """
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'termination_reason': 'consent_withdrawn',
            'consent_withdrawal_reason': 'Reason',
            'willing_to_complete_10w': NOT_APPLICABLE}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('willing_to_complete_10w', form_validator._errors)

    def test_centre_care_transfer_willing_to_complete_in_centre_given(self):
        """ Asserts willing_to_complete_centre when termination reason
            is care_transferred_to_another_institution.
        """
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'termination_reason': 'care_transferred_to_another_institution',
            'willing_to_complete_centre': NOT_APPLICABLE}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('willing_to_complete_centre', form_validator._errors)

        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'termination_reason': 'care_transferred_to_another_institution',
            'willing_to_complete_centre': NO}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_yes_willing_to_complete_willing_to_complete_date(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'willing_to_complete_10w': YES,
            'willing_to_complete_date': None}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('willing_to_complete_date', form_validator._errors)

    def test_no_willing_tocomplete_10WFU_with_date_to_complete(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'willing_to_complete_10w': NO,
            'willing_to_complete_date': get_utcnow()}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('willing_to_complete_date', form_validator._errors)

    def test_yes_willing_to_complete_centre_none_date_to_complete(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'willing_to_complete_centre': YES,
            'willing_to_complete_date': None}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('willing_to_complete_date', form_validator._errors)

    def test_no_willing_to_complete_centre_none_date_to_complete(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'willing_to_complete_centre': NO,
            'willing_to_complete_date': None}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_no_willing_to_complete_centreU_with_date_to_complete(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'willing_to_complete_centre': NO,
            'willing_to_complete_date': get_utcnow()}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('willing_to_complete_date', form_validator._errors)

    def test_included_in_error_reason_date_provided(self):
        """ Asserts included_in_error_date when termination reason
            is error_description.
        """
        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'termination_reason': 'included_in_error',
                        'included_in_error': 'blah blah blah blah',
                        'included_in_error_date': None}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('included_in_error_date', form_validator._errors)

        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'termination_reason': 'included_in_error',
                        'included_in_error': 'blah blah blah blah',
                        'included_in_error_date': get_utcnow()}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_included_in_error_reason_narrative_provided(self):
        """ Asserts included_in_error_date when termination reason
            is included_in_error.
        """
        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'termination_reason': 'included_in_error',
                        'included_in_error_date': get_utcnow(),
                        'included_in_error': None}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('included_in_error', form_validator._errors)

        cleaned_data = {'subject_identifier': self.subject_identifier,
                        'termination_reason': 'included_in_error',
                        'included_in_error_date': get_utcnow(),
                        'included_in_error': 'blah blah blah blah'}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_other_late_protocol_exclusion_none_date_to_complete(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'first_line_regimen': OTHER,
            'first_line_regimen_other': None}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('first_line_regimen_other', form_validator._errors)

    def test_other_second_line_regimen_none_second_line_regime_other(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'second_line_regimen': OTHER,
            'second_line_regimen_other': None}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('second_line_regimen_other', form_validator._errors)

    def test_consent_withdrawal_reason_invalid(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'termination_reason': CONSENT_WITHDRAWAL,
            'consent_withdrawal_reason': None}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('consent_withdrawal_reason', form_validator._errors)

    def test_consent_withdrawal_reason_valid(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'termination_reason': CONSENT_WITHDRAWAL,
            'consent_withdrawal_reason': 'Reason'}
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
