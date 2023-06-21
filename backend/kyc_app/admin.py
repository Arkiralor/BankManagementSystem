from django.contrib import admin

from kyc_app.models import Customer, KnowYourCustomer, KYCDocuments, CustomerAddress

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "middle_name", "last_name", "regnal_suffix", "gender", "age")
    search_fields = (
        "id",
        "first_name",
        "last_name",
        "middle_name",
        "regnal_suffix",
    )
    ordering = ("-created",)

    def age(self, obj):
        return obj.age
    
    def middle_name(self, obj):
        return ' '.join([item for item in obj.middle_name])


@admin.register(KnowYourCustomer)
class KnowYourCustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "id_proof_value", "address_proof_value")
    search_fields = (
        "id",
        "customer__id",
        "customer__first_name",
        "customer__last_name",
        "id_proof_value",
        "address_proof_value",
    )
    raw_id_fields = ("customer",)
    ordering = ("-created",)


@admin.register(KYCDocuments)
class KYCDocumentsAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "photo", "id_proof", "address_proof")
    search_fields = (
        "id",
        "customer__id",
        "customer__first_name",
        "customer__last_name",
        "id_proof",
        "address_proof",
    )
    raw_id_fields = ("customer",)
    ordering = ("-created",)


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "line_1", "line_2", "city", "district", "state", "country", "pin_code")
    search_fields = (
        "id",
        "customer__id",
        "customer__first_name",
        "customer__last_name",
        "line_1",
        "line_2",
        "city",
        "district",
        "state",
        "country",
        "pin_code"
    )
    raw_id_fields = ("customer",)
    ordering = ("-created",)