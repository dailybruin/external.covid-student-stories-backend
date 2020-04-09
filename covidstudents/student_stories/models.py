from django.db import models


class Story(models.Model):
    YEAR_IN_SCHOOL_CHOICES = [
        ('HS', 'high school'),
        ('FR', 'freshman'),
        ('SO', 'sophomore'),
        ('JR', 'junior'),
        ('SR', 'senior+'),
        ('GR', 'graduate'),
    ]

    FEELINGS = [
        ('NW', 'not worried'),
        ('SW', 'somewhat worried'),
        ('VW', 'very worried'),
        ('NA', 'prefer not to share')
    ]

    YES_OR_NO = [
        ('Y', 'yes'),
        ('N', 'no'),
        ('X', 'prefer not to share')
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    school = models.CharField(max_length=50)
    major = models.CharField(max_length=75)
    year = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    ethnicity = models.CharField(max_length=50)
    hometown = models.CharField(max_length=50)
    worryFinancial = models.CharField(max_length=2, choices=FEELINGS)
    worryHousing = models.CharField(max_length=2, choices=FEELINGS)
    worryAcademic = models.CharField(max_length=2, choices=FEELINGS)
    worryGovernment = models.CharField(max_length=2, choices=FEELINGS)
    worryPhysical = models.CharField(max_length=2, choices=FEELINGS)
    worryMental = models.CharField(max_length=2, choices=FEELINGS)
    responseCommunity = models.TextField(null=True)
    responseAffected = models.TextField(null=True)
    responseElse = models.TextField(null=True)
    comfortablePublish = models.CharField(max_length=1, choices=YES_OR_NO)
    knowPositive = models.CharField(max_length=1, choices=YES_OR_NO)
    currentLocation = models.CharField(max_length=50)
    responseDoneDifferently = models.TextField(null=True)
    mediaLinks = models.TextField(null=True)
    artCredit = models.CharField(max_length=50, null=True)
    reactLove = models.IntegerField(default=0)
    reactSad = models.IntegerField(default=0)
    reactUp = models.IntegerField(default=0)
    reactAngry = models.IntegerField(default=0)
    reactTotal = models.IntegerField(default=0)
