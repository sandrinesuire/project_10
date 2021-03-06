# Generated by Django 2.2.4 on 2019-08-29 16:59

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='The BarCode from openfoodfact api.', max_length=100)),
                ('nutrition_grades', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], help_text='The nutrition grade of article from openfoodfact api.', max_length=1)),
                ('id_api', models.CharField(help_text='The store id from openfoodfact api.', max_length=400)),
                ('product_name', models.CharField(help_text='The article name from openfoodfact api.', max_length=200)),
                ('image_url', models.URLField(help_text='The url article image from openfoodfact api.', null=True)),
                ('nutriments', django.contrib.postgres.fields.jsonb.JSONField(default=list, help_text='List of article nutriments from openfoodfact api.', null=True)),
                ('url', models.URLField(help_text='The url article from openfoodfact api.', null=True)),
                ('ingredients', django.contrib.postgres.fields.jsonb.JSONField(default=list, help_text='List of article ingredients from openfoodfact api.', null=True)),
                ('keywords', django.contrib.postgres.fields.jsonb.JSONField(default=list, help_text='List of article _keywords from openfoodfact api.', null=True)),
                ('delete', models.CharField(help_text='Internal field for working.', max_length=20, null=True)),
                ('my_grade', models.PositiveIntegerField(help_text='Internal field for working.', null=True)),
                ('keywords_number', models.PositiveIntegerField(help_text='Internal field for working.', null=True)),
                ('ingredients_number', models.PositiveIntegerField(help_text='Internal field for working.', null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The category name from openfoodfact api.', max_length=200)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The store name from openfoodfact api.', max_length=200)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Substitute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(help_text='the relation with Article model', on_delete=django.db.models.deletion.CASCADE, related_name='substitutes', to='substitute.Article')),
                ('profile', models.ForeignKey(help_text='the relation with Profile model', on_delete=django.db.models.deletion.CASCADE, related_name='substitutes', to='substitute.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(help_text='the relation with category model', related_name='articles', to='substitute.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='stores',
            field=models.ManyToManyField(help_text='the relation with store model', related_name='articles', to='substitute.Store'),
        ),
    ]
