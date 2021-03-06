# Generated by Django 3.1.4 on 2020-12-31 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='mod_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='number_of_comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='entry',
            name='number_of_pingbacks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='entry',
            name='pub_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
