from __future__ import unicode_literals
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


def generate_id():
    return uuid4().hex[:28]


@python_2_unicode_compatible
class RazorpayTransaction(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    email = models.EmailField(null=True, blank=True)
    txnid = models.CharField(
        max_length=32, db_index=True, default=generate_id
    )
    basket_id = models.CharField(
        max_length=12, null=True, blank=True, db_index=True
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                 blank=True)
    currency = models.CharField(max_length=8, null=True, blank=True)

    # TODO: Make sure razorpay's status strings match these.
    INITIATED, CAPTURED, AUTHORIZED, CAPTURE_FAILED, AUTH_FAILED = (
        "initiated", "captured", "authorized", "capfailed", "authfailed"
    )
    status = models.CharField(max_length=32)

    rz_id = models.CharField(
        max_length=32, null=True, blank=True, db_index=True
    )

    error_code = models.CharField(max_length=32, null=True, blank=True)
    error_message = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ('-date_created',)
        app_label = 'rzpay'

    @property
    def is_successful(self):
        return self.status == self.CAPTURED

    @property
    def is_pending(self):
        return self.status == self.AUTHORIZED

    @property
    def is_failed(self):
        # TODO: Probably mark abandoned transactions as failed in batch
        return self.status not in (
            self.CAPTURED, self.AUTHORIZED, self.INITIATED
        )

    def __str__(self):
        return 'razorpay payment: %s' % self.rz_id
