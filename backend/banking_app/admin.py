from django.contrib import admin

from banking_app.models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "account_number", "holders", "balance", "account_type", "created")
    search_fields = (
        "account_number",
        "balance",
        "account_type",
    )
    list_filter = ("account_type",)
    ordering = ("-created",)

    def holders(self, obj):
        return ', '.join([str(item) for item in obj.holder.all()])

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "source", "destination", "amount", "transaction_type")
    search_fields = (
        "id",
        "source__id",
        "destination__id",
        "source__account_number",
        "destination__account_number",
        "amount",
        "transaction_type",
        "created",
        "updated"
    )
    raw_id_fields = ("source", "destination")
    ordering = ("-created",)

    def date(self, obj):
        return obj.created.strftime("%Y-%m-%d %H:%M:%S.%f")

    