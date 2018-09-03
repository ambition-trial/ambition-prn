from django.conf import settings
from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import ambition_prn_admin

app_name = 'ambition_prn'

urlpatterns = [
    path('admin/', ambition_prn_admin.urls),
    path('', RedirectView.as_view(url='/ambition_prn/admin/'), name='home_url'),
]


if settings.APP_NAME == 'ambition_prn':
    from django.contrib import admin

    urlpatterns += [
        path('admin/', admin.site.urls),
    ]
