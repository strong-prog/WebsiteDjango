# Generated by Django 3.0.14 on 2022-09-24 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField()),
                ('discounted_price', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]