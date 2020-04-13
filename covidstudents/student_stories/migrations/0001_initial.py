# Generated by Django 3.0.3 on 2020-04-13 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('school', models.CharField(max_length=50)),
                ('major', models.CharField(max_length=75)),
                ('year', models.CharField(choices=[('HS', 'high school'), ('FR', 'freshman'), ('SO', 'sophomore'), ('JR', 'junior'), ('SR', 'senior+'), ('GR', 'graduate')], max_length=2)),
                ('state', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50, null=True)),
                ('worryFinancial', models.CharField(choices=[('NW', 'not worried'), ('SW', 'somewhat worried'), ('VW', 'very worried'), ('NA', 'prefer not to share')], max_length=2)),
                ('worryHousing', models.CharField(choices=[('NW', 'not worried'), ('SW', 'somewhat worried'), ('VW', 'very worried'), ('NA', 'prefer not to share')], max_length=2)),
                ('worryAcademic', models.CharField(choices=[('NW', 'not worried'), ('SW', 'somewhat worried'), ('VW', 'very worried'), ('NA', 'prefer not to share')], max_length=2)),
                ('worryGovernment', models.CharField(choices=[('NW', 'not worried'), ('SW', 'somewhat worried'), ('VW', 'very worried'), ('NA', 'prefer not to share')], max_length=2)),
                ('worryPhysical', models.CharField(choices=[('NW', 'not worried'), ('SW', 'somewhat worried'), ('VW', 'very worried'), ('NA', 'prefer not to share')], max_length=2)),
                ('worryMental', models.CharField(choices=[('NW', 'not worried'), ('SW', 'somewhat worried'), ('VW', 'very worried'), ('NA', 'prefer not to share')], max_length=2)),
                ('responseCommunity', models.TextField(null=True)),
                ('responseAffected', models.TextField(null=True)),
                ('responseElse', models.TextField(null=True)),
                ('comfortablePublish', models.CharField(choices=[('Y', 'yes'), ('N', 'no'), ('X', 'prefer not to share')], max_length=1)),
                ('knowPositive', models.CharField(choices=[('Y', 'yes'), ('N', 'no'), ('X', 'prefer not to share')], max_length=1)),
                ('currentLocation', models.CharField(max_length=50)),
                ('responseDoneDifferently', models.TextField(null=True)),
                ('mediaLinks', models.TextField(null=True)),
                ('artCredit', models.CharField(max_length=50, null=True)),
                ('reactLove', models.IntegerField(default=0)),
                ('reactSad', models.IntegerField(default=0)),
                ('reactUp', models.IntegerField(default=0)),
                ('reactAngry', models.IntegerField(default=0)),
                ('reactTotal', models.IntegerField(default=0)),
                ('approvalState', models.CharField(choices=[('approved', 'approved'), ('rejected', 'rejected'), ('undecided', 'undecided')], default='undecided', max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50)),
                ('charcount', models.IntegerField(default=1)),
            ],
        ),
    ]
