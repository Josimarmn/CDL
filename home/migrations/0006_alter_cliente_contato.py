# Generated by Django 5.1.7 on 2025-03-19 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_cliente_contato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='contato',
            field=models.CharField(help_text='(DDD) + 9 + contato', max_length=20, verbose_name='Contato'),
        ),
    ]
