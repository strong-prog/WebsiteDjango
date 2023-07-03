# Generated by Django 3.0.14 on 2022-09-28 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20220926_1702'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name': 'Налог', 'verbose_name_plural': 'Налоги'},
        ),
        migrations.AddField(
            model_name='orders',
            name='tax',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='payment.Tax', verbose_name='Налог'),
        ),
        migrations.AddField(
            model_name='tax',
            name='tax',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Налог'),
        ),
        migrations.AddField(
            model_name='tax',
            name='user_id',
            field=models.IntegerField(default=1, verbose_name='id пользователя'),
        ),
    ]
