# Generated by Django 2.2.4 on 2019-09-17 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0003_auto_20190910_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='id_api',
            field=models.CharField(help_text='The store id from openfoodfact api.', max_length=600),
        ),
        migrations.AlterField(
            model_name='article',
            name='image_url',
            field=models.URLField(help_text='The url article image from openfoodfact api.', max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='product_name',
            field=models.CharField(help_text='The article name from openfoodfact api.', max_length=600),
        ),
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.URLField(help_text='The url article from openfoodfact api.', max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='The category name from openfoodfact api.', max_length=600),
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(help_text='The store name from openfoodfact api.', max_length=600),
        ),
    ]
