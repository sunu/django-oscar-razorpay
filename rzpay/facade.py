"""
Responsible for briding between Oscar and the Razorpay gateway
"""
from __future__ import unicode_literals
from uuid import uuid4
import logging

from django.conf import settings

from .models import RazorpayTransaction as Transaction
from .exceptions import RazorpayError

import razorpay

rz_client = razorpay.Client(
    auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)
)

logger = logging.getLogger('razorpay')


def start_razorpay_txn(basket, amount, user=None, email=None):
    """
    Record the start of a transaction and calculate costs etc.
    """
    if basket.currency:
        currency = basket.currency
    else:
        currency = getattr(settings, 'RAZORPAY_CURRENCY', 'INR')
    transaction = Transaction(
        user=user, amount=amount, currency=currency, status="initiated",
        basket_id=basket.id, txnid=uuid4().hex[:28], email=email
    )
    transaction.save()
    return transaction


def update_transaction_details(rz_id, txn_id):
    """
    Fetch the completed details about the Razorpay transaction and update our
    tranaction model.
    """
    try:
        payment = rz_client.payment.fetch(rz_id)
    except Exception as e:
        logger.warning(
            "Unable to fetch transaction details for rz txn %s: %s",
            rz_id, e)
        raise RazorpayError
    try:
        txn = Transaction.objects.get(txnid=txn_id)
    except Transaction.DoesNotExist as e:
        logger.warning(
            "Unable to find transaction details for txnid %s: %s",
            txn_id, e)
        raise RazorpayError
    if (int(txn.amount*100) != payment["amount"] or
            txn.currency != payment["currency"]):
        logger.warning(
            "Payment details mismatch for txn %s and %s",
            txn, payment
        )
        raise RazorpayError
    txn.status = payment["status"]
    txn.rz_id = rz_id
    txn.save()
    return txn


def capture_transaction(rz_id):
    """
    capture the payment
    """
    try:
        txn = Transaction.objects.get(rz_id=rz_id)
        rz_client.payment.capture(rz_id, int(txn.amount*100))
        txn.status = "captured"
        txn.save()
    except Exception as e:
        logger.warning(
            "Couldn't capture payment for txn %s: %s",
            txn, e
        )
        raise RazorpayError
    return txn


def refund_transaction(rz_id, amount, currency):
    try:
        txn = Transaction.objects.get(rz_id)
        assert amount <= int(txn.amount*100)
        assert currency == txn.currency
        rz_client.payment.refund(rz_id, amount)
    except Exception as e:
        logger.warning(
            "Couldn't refund txn %s: %s",
            txn, e
        )
