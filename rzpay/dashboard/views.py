from django.views import generic

from .. import models


class TransactionListView(generic.ListView):
    model = models.RazorpayTransaction
    template_name = 'rzpay/dashboard/transaction_list.html'
    context_object_name = 'transactions'


class TransactionDetailView(generic.DetailView):
    model = models.RazorpayTransaction
    template_name = 'rzpay/dashboard/transaction_detail.html'
    context_object_name = 'txn'
