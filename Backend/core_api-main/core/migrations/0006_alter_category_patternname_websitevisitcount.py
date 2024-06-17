# Generated by Django 4.1 on 2024-01-08 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_website_baseurl_entrycount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='patternName',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.CreateModel(
            name='WebsiteVisitCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('month', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField(default=0)),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.website')),
            ],
            options={
                'unique_together': {('website', 'year', 'month')},
            },
        ),
    ]
