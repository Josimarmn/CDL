# Generated by Django 5.1.6 on 2025-03-14 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='total_curso01',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='total_curso02',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='total_curso03',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='total_curso04',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='total_curso05',
            field=models.IntegerField(null=True),
        ),
    ]
