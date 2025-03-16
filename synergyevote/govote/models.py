from django.contrib.auth.models import AbstractUser, User, Group
from django.db import models, transaction
from django.forms import ValidationError
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum, F, Value, Subquery, OuterRef, Count
from django.db.models.functions import Coalesce
from geopy.distance import geodesic  # type: ignore # For proximity calculation
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
import random
import string



class ActiveStatusModel(models.Model):
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Country(ActiveStatusModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    flag = models.ImageField(upload_to='country/flag/', null=True, blank=True, verbose_name="Attach Country Flag") 
    description = models.TextField(default="", null=True, blank=True)   
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_countries')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Country'
        
    def __str__(self):
        return self.name 
    
# Model for Region linked to Country
class Region(ActiveStatusModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)  # ISO country code, e.g., "GR" for Greater Accra
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(default="", null=True, blank=True)  
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_regions')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Regions'
        
    def __str__(self):
        return self.name 
    
# Model for District linked to Region
class District(ActiveStatusModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True, default="")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(default="", null=True, blank=True)     
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_districts')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Districts'
        
    def __str__(self):
        return self.name 
    
# Model for City linked to District
class City(ActiveStatusModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True, default="")
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(default="", null=True, blank=True)     
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_cities')
    created_at = models.DateTimeField(default=timezone.now)
        
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'City'
        
    def __str__(self):
        return self.name 
    
# Model for City linked to District
class Title(ActiveStatusModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True, default="")
    description = models.TextField(default="", null=True, blank=True)   
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_titles')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Titles'
        
    def __str__(self):
        return self.name 
    
# Model for City linked to District
class Designation(ActiveStatusModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True, default="")
    description = models.TextField(default="", null=True, blank=True)     
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_designations')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Designations'
        
    def __str__(self):
        return self.name 
    
# Model for District linked to Region
class Area(ActiveStatusModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True, default="")
    description = models.TextField(default="", null=True, blank=True)     
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_areas')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Areas'
        
    def __str__(self):
        return self.name 
    
class Voter(ActiveStatusModel):
    voter_id = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)  # Hashed
    vpass = models.CharField(max_length=255)  # Second-layer authentication
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=True, blank=True)
    tel = models.CharField(max_length=27, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    can_vote = models.BooleanField(default=True)
    electco = models.IntegerField(default=0)    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_voters')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Voter List'
        
    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.voter_id})"
     
    
 
class AdminUser(AbstractUser):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('admin', 'System User'),
        ('electoralCommissioner', 'Electoral Commissioner'),
        ('pollingOfficer', 'Polling Officer'),
    ]
    groups = models.ManyToManyField("auth.Group",related_name="admin_users",blank=True, )
    user_permissions = models.ManyToManyField("auth.Permission", related_name="admin_users", blank=True,)
    role = models.CharField(max_length=25, choices=ROLE_CHOICES)
    
class Election(ActiveStatusModel):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("pending", "Pending Approval"),
    ]
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()    
    max_vote = models.IntegerField(default=1)  # Default to 1 (for single candidate selection)
    golive = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    instructions =  models.TextField(null=True, blank=True, default="")    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_elections')
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_elections')
    modified_at = models.DateTimeField(null=True, blank=True)  # Remove default=""  
    # active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Elections'
        
    def __str__(self):
        return f"{self.name} {self.start_date} - {self.end_date}"

class Position(ActiveStatusModel):
    VOTE_TYPE_CHOICES = [
        ("single", "Single Candidate Selection"),
        ("multiple", "Multiple Candidate Selection"),
        ("yes_no", "Yes/No Vote"),
    ]
    election = models.ForeignKey("Election", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    max_vote = models.IntegerField(default=1)
    priority = models.IntegerField(default=0)
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPE_CHOICES, default="single")
    instructions = models.CharField(max_length=255, default="", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_created_position')
    created_at = models.DateTimeField(default=now)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_position')
    modified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Election Positions'

    def __str__(self):
        return f"{self.description} - {self.election.name}"

    def save(self, *args, **kwargs):
        #Ensure exactly two `YesNoOption` instances exist for `yes_no` vote type."""
        super().save(*args, **kwargs)
        if self.vote_type == "yes_no":
            self.ensure_yes_no_options()

    def ensure_yes_no_options(self):
        #Create 'Yes' and 'No' options if missing."""
        existing_options = YesNoOption.objects.filter(position=self)
        existing_choices = existing_options.values_list("vote_yn", flat=True)

        if "Yes" not in existing_choices:
            YesNoOption.objects.create(position=self, vote_yn="Yes", created_by=self.created_by)
        if "No" not in existing_choices:
            YesNoOption.objects.create(position=self, vote_yn="No", created_by=self.created_by)

class YesNoOption(models.Model):
    VOTE_YN_CHOICES = [("Yes", "Yes"), ("No", "No")]
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="yes_no_options")    
    vote_yn = models.CharField(max_length=3, choices=VOTE_YN_CHOICES)
    photo = models.ImageField(upload_to="position/YesNoOption/", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_created_ynoption")
    created_at = models.DateTimeField(default=now)
       
        
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Election Position YesNoOption'
        constraints = [
            models.UniqueConstraint(fields=["position", "vote_yn"], name="unique_yes_no_option")
        ]

    def __str__(self):
        return f"{self.vote_yn} - {self.position.description}"
    
class Candidate(ActiveStatusModel):
    position = models.ForeignKey(Position, on_delete=models.CASCADE , null=True, blank=True, related_name="candidates")
    title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    profile = models.TextField(default="", null=True, blank=True)  
    photo = models.ImageField(upload_to='candidates/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_positions')
    created_at = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_positions')
    modified_at = models.DateTimeField() 
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Election Candidates'
        
    def __str__(self):
        return f"{self.position.election.name} - {self.title.name} {self.firstname} {self.lastname}"

class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voteVal = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name_plural = 'Election Votes'
        
    def __str__(self):
        return f"Vote by {self.voter.voter_id} for {self.candidate.firstname} {self.candidate.lastname}"
    
    
    
class Subscription(ActiveStatusModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50, choices=[('free', 'Free'), ('pro', 'Pro')])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Subscriptions'
        
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.plan}"
    
