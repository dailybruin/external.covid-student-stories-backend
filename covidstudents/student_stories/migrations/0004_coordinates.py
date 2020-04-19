# Generated by Django 3.0.3 on 2020-04-19 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_stories', '0003_auto_20200413_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordquery', models.CharField(blank=True, max_length=150)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
            ],
        ),
    ]
