from django.contrib import admin

from ledger_app.models import EmployeeLedger


@admin.register(EmployeeLedger)
class EmployeeLedgerAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'title', 'created', 'updated')
    raw_id_fields = ('employee',)
    search_fields = (
        'employee__id',
        'employee__username',
        'employee__email',
        'employee__first_name',
        'employee__last_name',
        'title',
        'body'
    )
    ordering = ('-created',)
    list_filter = ('created',)
