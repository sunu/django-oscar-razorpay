from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from apps.app import application
from rzpay.dashboard.app import application as razorpay_dashboard

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += i18n_patterns(
    # Razorpay integration...
    url(r'^checkout/razorpay/', include('rzpay.urls')),
    # Dashboard views for Razorpay
    url(r'^dashboard/razorpay/', include(razorpay_dashboard.urls)),
    url(r'', include(application.urls)),
)
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
