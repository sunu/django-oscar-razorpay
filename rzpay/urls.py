from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^preview/(?P<basket_id>\d+)/$',
        views.SuccessResponseView.as_view(),
        name='razorpay-success-response'),
    url(r'^cancel/(?P<basket_id>\d+)/$', views.CancelResponseView.as_view(),
        name='razorpay-cancel-response'),
    url(r'^payment/', views.PaymentView.as_view(),
        name='razorpay-direct-payment'),
]
