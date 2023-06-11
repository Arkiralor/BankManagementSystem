# Generated by Django 4.2 on 2023-06-10 12:19

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=16)),
                ('middle_name', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=16), blank=True, null=True, size=7)),
                ('last_name', models.CharField(max_length=16)),
                ('regnal_suffix', models.CharField(help_text='I, II, Jr., Sr., etc', max_length=10)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male'), ('Other', 'Other')], max_length=16)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='KYCDocuments',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='media/custdocuments/photo', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg', 'png'))])),
                ('id_proof_type', models.CharField(choices=[('PAN Card', 'PAN Card'), ('Aadhar Card', 'Aadhar Card'), ('Voter ID', 'Voter ID'), ('Passport', 'Passport'), ('Driving License', 'Driving License')], max_length=25)),
                ('id_proof', models.ImageField(blank=True, null=True, upload_to='media/custdocuments/id_proof', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg', 'png'))])),
                ('address_proof_type', models.CharField(choices=[('Aadhar Card', 'Aadhar Card'), ('Voter ID', 'Voter ID'), ('Electricity Bill', 'Electricity Bill'), ('Passport', 'Passport'), ('Driving License', 'Driving License')], max_length=25)),
                ('address_proof', models.ImageField(blank=True, null=True, upload_to='media/custdocuments/address_proof', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg', 'png'))])),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kyc_app.customer')),
            ],
            options={
                'verbose_name': 'KYC Document',
                'verbose_name_plural': 'KYC Documents',
            },
        ),
        migrations.CreateModel(
            name='KnowYourCustomer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id_proof_value', models.CharField(max_length=128)),
                ('address_proof_value', models.CharField(max_length=128)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kyc_app.customer')),
            ],
            options={
                'verbose_name': 'Know Your Customer',
                'verbose_name_plural': 'Know Your Customers',
            },
        ),
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('line_1', models.CharField(blank=True, max_length=128, null=True)),
                ('line_2', models.CharField(blank=True, max_length=128, null=True)),
                ('city', models.CharField(blank=True, max_length=64, null=True)),
                ('district', models.CharField(blank=True, max_length=64, null=True)),
                ('state', models.CharField(blank=True, max_length=64, null=True)),
                ('country', models.CharField(blank=True, max_length=64, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=7, null=True, validators=[django.core.validators.RegexValidator(regex=re.compile('^([1-9]{1})([0-9]{5})'))])),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kyc_app.customer')),
            ],
            options={
                'verbose_name': 'Customer Address',
                'verbose_name_plural': 'Customer Addresses',
            },
        ),
    ]