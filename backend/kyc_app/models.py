from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import (EmailValidator, FileExtensionValidator,
                                    RegexValidator)
from django.db import models

from core.boilerplate.model_template import TemplateModel
from kyc_app.constants import FormatRegex
from kyc_app.model_choices import CustomerChoice


class Customer(TemplateModel):
    first_name = models.CharField(max_length=16)
    middle_name = ArrayField(
        models.CharField(max_length=16),
        size=7,
        blank=True,
        null=True
    )
    last_name = models.CharField(max_length=16)
    regnal_suffix = models.CharField(
        max_length=10, help_text="I, II, Jr., Sr., etc")
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=16, choices=CustomerChoice.GENDER_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        self.middle_name = [name.title() for name in self.middle_name]
        self.last_name = self.last_name.title()
        self.regnal_suffix = self.regnal_suffix.upper()

        super(Customer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class KnowYourCustomer(TemplateModel):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    id_proof_value = models.CharField(max_length=128)
    address_proof_value = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Know Your Customer"
        verbose_name_plural = "Know Your Customers"


class KYCDocuments(TemplateModel):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to="media/custdocuments/photo",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=CustomerChoice.ALLOWED_FILE_EXTENSIONS)
        ]
    )
    id_proof_type = models.CharField(
        max_length=25, choices=CustomerChoice.ID_PROOF_CHOICES)
    id_proof = models.ImageField(
        upload_to="media/custdocuments/id_proof",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=CustomerChoice.ALLOWED_FILE_EXTENSIONS)
        ]
    )
    address_proof_type = models.CharField(
        max_length=25, choices=CustomerChoice.ADDRESS_PROOF_CHOICES)
    address_proof = models.ImageField(
        upload_to="media/custdocuments/address_proof",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=CustomerChoice.ALLOWED_FILE_EXTENSIONS)
        ]
    )

    def __str__(self):
        return f"{self.pk}"

    def save(self, *args, **kwargs):

        super(KYCDocuments, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "KYC Document"
        verbose_name_plural = "KYC Documents"


class CustomerAddress(TemplateModel):
    """
    Model to hold addresses of Customers
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    line_1 = models.CharField(max_length=128, blank=True, null=True)
    line_2 = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    district = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    pin_code = models.CharField(
        validators=[RegexValidator(regex=FormatRegex.PIN_REGEX)],
        max_length=7,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.pk

    def save(self, *args, **kwargs):
        is_true = (
            self.line_1 or self.line_2 or self.city or self.district or self.state or self.country)
        if is_true and not self.pin_code:
            raise ValidationError("The PIN code is mandatory.")

        self.city = self.city.title() if self.city else None
        self.district = self.district.title() if self.district else None
        self.state = self.state.title() if self.state else None
        self.country = self.country.title() if self.country else None

        super(CustomerAddress, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Customer Address"
        verbose_name_plural = "Customer Addresses"
