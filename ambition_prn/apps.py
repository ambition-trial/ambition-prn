from django.apps import AppConfig as DjangoApponfig
from django.conf import settings


class AppConfig(DjangoApponfig):
    name = 'ambition_prn'
    verbose_name = 'Ambition Subject PRN Forms'
    has_exportable_data = True

    def ready(self):
        from .signals import study_termination_conclusion_on_post_save
        pass


if settings.APP_NAME == 'ambition_prn':

    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU

    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = 'botswana'
        definitions = {
            '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                                 slots=[100, 100, 100, 100, 100, 100, 100]),
            '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                                 slots=[100, 100, 100, 100, 100])}
