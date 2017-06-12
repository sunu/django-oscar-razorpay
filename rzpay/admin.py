from django.contrib import admin
from . import models


class RazorpayTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'currency', 'txnid', 'status',
                    'rz_id', 'error_code', 'error_message', 'date_created',
                    'basket_id', 'email']
    readonly_fields = [
        'user',
        'amount',
        'currency',
        'txnid',
        'rz_id',
        'error_code',
        'error_message',
        'date_created',
        'basket_id',
        'email'
    ]

admin.site.register(models.RazorpayTransaction, RazorpayTransactionAdmin)
