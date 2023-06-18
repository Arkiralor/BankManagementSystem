from os import sep, path, makedirs

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import (EmailValidator, FileExtensionValidator,
                                    RegexValidator)
from django.db import models

from core.boilerplate.model_template import TemplateModel
from kyc_app.constants import FormatRegex
from kyc_app.model_choices import CustomerChoice

from kyc_app import logger


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
        max_length=10, help_text="I, II, Jr., Sr., etc", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=16, choices=CustomerChoice.GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        if self.middle_name:
            self.middle_name = [name.title() for name in self.middle_name]
        self.last_name = self.last_name.title()
        if self.regnal_suffix:
            self.regnal_suffix = self.regnal_suffix.upper()

        super(Customer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class KnowYourCustomer(TemplateModel):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    id_proof_value = models.CharField(max_length=128, blank=True, null=True)
    address_proof_value = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Know Your Customer"
        verbose_name_plural = "Know Your Customers"


class KYCDocuments(TemplateModel):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to="custdocuments/photo",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=CustomerChoice.ALLOWED_FILE_EXTENSIONS)
        ]
    )
    id_proof_type = models.CharField(
        max_length=25, choices=CustomerChoice.ID_PROOF_CHOICES, blank=True, null=True)
    id_proof = models.ImageField(
        upload_to="custdocuments/id_proof",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=CustomerChoice.ALLOWED_FILE_EXTENSIONS)
        ]
    )
    address_proof_type = models.CharField(
        max_length=25, choices=CustomerChoice.ADDRESS_PROOF_CHOICES, blank=True, null=True)
    address_proof = models.ImageField(
        upload_to="custdocuments/address_proof",
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

    ## TODO (prithoo): Will deal with this later.
    # def fix_file_names(self, *args, **kwargs):
    #     if self.photo:
    #         logger.info(f"Fixing photo name for customer {self.customer.id}")
    #         self.photo.name = f"{self.id_proof.name.split(sep)[:-1:]}{sep}{self.customer.id}-photo.{self.photo.name.split('.')[-1]}"
    #         logger.info(self.photo.name)
    #     if self.id_proof:
    #         logger.info(f"Fixing id_proof name for customer {self.customer.id}")
    #         self.id_proof.name = f"{self.id_proof.name.split(sep)[:-1:]}{sep}{self.customer.id}-id.{self.id_proof.name.split('.')[-1]}"
    #         logger.info(self.id_proof.name)
    #     if self.address_proof:
    #         logger.info(f"Fixing address_proof name for customer {self.customer.id}")
    #         self.address_proof.name = f"{self.id_proof.name.split(sep)[:-1:]}{sep}{self.customer.id}-address.{self.address_proof.name.split('.')[-1]}"
    #         logger.info(self.address_proof.name)

    #     self.save()

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
        return f"{self.pk}"

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
