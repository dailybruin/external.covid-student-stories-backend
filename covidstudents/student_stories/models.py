from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=50)
    charcount = models.IntegerField(default=1)


class Coordinates(models.Model):
    coordquery = models.CharField(max_length=150, blank=True)

    longitude = models.FloatField()
    latitude = models.FloatField()


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

    APPROVAL_STATES = [
        ('approved', 'approved'),
        ('rejected', 'rejected'),
        ('undecided', 'undecided')
    ]

    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    school = models.CharField(max_length=100, blank=True)
    major = models.CharField(max_length=75, blank=True)
    year = models.CharField(
        max_length=2, choices=YEAR_IN_SCHOOL_CHOICES, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    worryFinancial = models.CharField(
        max_length=2, choices=FEELINGS, blank=True)
    worryHousing = models.CharField(max_length=2, choices=FEELINGS, blank=True)
    worryAcademic = models.CharField(
        max_length=2, choices=FEELINGS, blank=True)
    worryGovernment = models.CharField(
        max_length=2, choices=FEELINGS, blank=True)
    worryPhysical = models.CharField(
        max_length=2, choices=FEELINGS, blank=True)
    worryMental = models.CharField(max_length=2, choices=FEELINGS, blank=True)
    responseCommunity = models.TextField(null=True, blank=True)
    responseAffected = models.TextField(null=True, blank=True)
    responseElse = models.TextField(null=True, blank=True)
    comfortablePublish = models.CharField(
        max_length=1, choices=YES_OR_NO, blank=True)
    knowPositive = models.CharField(
        max_length=1, choices=YES_OR_NO, blank=True)
    currentLocation = models.CharField(max_length=50, blank=True)
    responseDoneDifferently = models.TextField(null=True, blank=True)
    artCredit = models.TextField(null=True, blank=True)
    reactLove = models.IntegerField(default=0, blank=True)
    reactSad = models.IntegerField(default=0, blank=True)
    reactUp = models.IntegerField(default=0, blank=True)
    reactAngry = models.IntegerField(default=0, blank=True)
    reactTotal = models.IntegerField(default=0, blank=True)
    approvalState = models.CharField(
        max_length=9, choices=APPROVAL_STATES, default='undecided', blank=True)
