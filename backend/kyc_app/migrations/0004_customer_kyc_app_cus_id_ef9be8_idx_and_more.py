# Generated by Django 4.2 on 2023-06-25 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kyc_app', '0003_alter_kycdocuments_address_proof_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['id'], name='kyc_app_cus_id_ef9be8_idx'),
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['first_name', 'middle_name', 'last_name'], name='kyc_app_cus_first_n_45b646_idx'),
        ),
        migrations.AddIndex(
            model_name='customeraddress',
            index=models.Index(fields=['id'], name='kyc_app_cus_id_508d87_idx'),
        ),
        migrations.AddIndex(
            model_name='customeraddress',
            index=models.Index(fields=['customer'], name='kyc_app_cus_custome_c0718c_idx'),
        ),
        migrations.AddIndex(
            model_name='knowyourcustomer',
            index=models.Index(fields=['id'], name='kyc_app_kno_id_de7734_idx'),
        ),
        migrations.AddIndex(
            model_name='knowyourcustomer',
            index=models.Index(fields=['customer'], name='kyc_app_kno_custome_bd50f4_idx'),
        ),
        migrations.AddIndex(
            model_name='knowyourcustomer',
            index=models.Index(fields=['id_proof_value', 'address_proof_value'], name='kyc_app_kno_id_proo_e7e04b_idx'),
        ),
        migrations.AddIndex(
            model_name='kycdocuments',
            index=models.Index(fields=['id'], name='kyc_app_kyc_id_461692_idx'),
        ),
        migrations.AddIndex(
            model_name='kycdocuments',
            index=models.Index(fields=['customer'], name='kyc_app_kyc_custome_bc6dac_idx'),
        ),
    ]
