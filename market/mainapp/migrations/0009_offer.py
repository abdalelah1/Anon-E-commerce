# Generated by Django 4.0.4 on 2023-04-07 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_product_product_date_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
                ('offer_description', models.CharField(max_length=1000)),
                ('offer_discount', models.FloatField()),
                ('offer_start_date', models.DateField()),
                ('offer_end_date', models.DateField()),
                ('offer_product_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product')),
            ],
        ),
    ]
