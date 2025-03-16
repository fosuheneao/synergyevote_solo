import csv
import io
from django.utils.timezone import now
from django.urls import path
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django import forms
from django.db.models import Count
from django.db.models import Q
from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.http import HttpResponse
from .models import *


class CreatedByMixin:
    #Mixin to automatically set 'created_by' on model save."""
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class CustomAdminSite(admin.AdminSite):
    #Custom Admin Panel with Dashboard & CSV Upload."""
    site_header = "Synergy Evote Admin Dashboard"
    site_title = "Synergy Evote Admin"
    index_title = "Live Voting Statistics"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("admin-dashboard/", self.admin_view(self.admin_dashboard), name="admin-dashboard"),
            path("upload-voter-csv/", self.admin_view(upload_voters_csv), name="upload-voter-csv"),
        ]
        return custom_urls + urls

    def admin_dashboard(self, request):
        elections = Election.objects.all()
        return TemplateResponse(request, "admin/dashboard.html", {"elections": elections})
admin_site = CustomAdminSite(name="custom_admin")

# Customize the admin site headers
admin.site.site_header = "Synergy Evote - Govote Admin Panel"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Synergy Evote Admin Portal"

def upload_voters_csv(request):
    #Handles bulk CSV upload for voters."""
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        if not csv_file:
            messages.error(request, "No file selected.")
            return redirect("admin:upload-voter-csv")

        decoded_file = csv_file.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)

        for row in reader:
            Voter.objects.create(
                voter_id=row[0],
                firstname=row[1],
                lastname=row[2],
                email=row[3],
                tel=row[4],
            )

        messages.success(request, "Voters uploaded successfully!")
        return redirect("admin:app_voter_changelist")

    return render(request, "admin/upload_voter_csv.html")




class YesNoOptionInline(admin.StackedInline):
    #Inline model for Yes/No voting options."""
    model = YesNoOption
    extra = 2  # Display both Yes and No options by default
    max_num = 2
    can_delete = True


class PositionAdminForm(forms.ModelForm):
    #Custom form to validate max_vote based on vote_type."""
    class Meta:
        model = Position
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        vote_type = cleaned_data.get("vote_type")
        max_vote = cleaned_data.get("max_vote")

        if vote_type == "multiple" and max_vote <= 1:
            raise forms.ValidationError("For multiple candidate selection, max_vote must be greater than 1.")

        return cleaned_data
    
# class PositionAdminForm(forms.ModelForm):
#     #Custom form to validate max_vote based on vote_type."""
#     class Meta:
#         model = Position
#         fields = "__all__"

#     def clean(self):
#         cleaned_data = super().clean()
#         vote_type = cleaned_data.get("vote_type")
#         max_vote = cleaned_data.get("max_vote")

#         # Ensure multiple selections have a max_vote greater than 1
#         if vote_type == "multiple" and max_vote <= 1:
#             raise forms.ValidationError("For multiple candidate selection, max_vote must be greater than 1.")

#         return cleaned_data
    
# class CustomAdminSite(admin.AdminSite):
#     # site_header = "Synergy Evote Admin Panel"
#     # site_title = "Synergy Evote"
#     # index_title = "Welcome to Synergy Evote"

#     def each_context(self, request):
#         context = super().each_context(request)
#         context["custom_css"] = "govote_admin/styles.css"  # Link the custom CSS file
#         return context

# # Register the custom admin site
# admin_site = CustomAdminSite(name="custom_admin")
    
# admin.site.register(Country)
class CountryModelAdmin(admin.ModelAdmin):
    # Exclude the 'created_by' field from the admin form
    exclude = ('created_at',)
    
    list_display = ('name', 'code','latitude', 'longitude', 'flag')  # Fields to display in list view
    list_filter = ('name', 'code',) # Filter sidebar options
    search_fields = ('name', 'code',)  # Searchable fields
    ordering = ('name', 'code',)  # Default ordering
    autocomplete_fields = ["created_by"]
    
    class Media:
         css = {
             'all': ('admin/css/custom_admin.css',)  # Path to your custom CSS
         }
        
    def save_model(self, request, obj, form, change):
        # Set the current user as 'created_by' only when the object is newly created
        if not change:  # 'change' is False when adding a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(Country, CountryModelAdmin)


# admin.site.register(Region)
class RegionModelAdmin(admin.ModelAdmin):
    # Exclude the 'created_by' field from the admin form
    exclude = ('created_at',)
    
    list_display = ('name', 'code','country', 'latitude', 'longitude')  # Fields to display in list view
    list_filter = ('name', 'code','country') # Filter sidebar options
    search_fields = ('name','country',)  # Searchable fields
    ordering = ('name', 'code','country',)  # Default ordering
    autocomplete_fields = ["created_by"]
    
    class Media:
         css = {
             'all': ('admin/css/custom_admin.css',)  # Path to your custom CSS
         }
         
    def save_model(self, request, obj, form, change):
        # Set the current user as 'created_by' only when the object is newly created
        if not change:  # 'change' is False when adding a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(Region, RegionModelAdmin)

# admin.site.register(District)
class DistrictModelAdmin(admin.ModelAdmin):
    # Exclude the 'created_by' field from the admin form
    exclude = ('created_at',)
    
    list_display = ('name', 'code','region', 'latitude', 'longitude')  # Fields to display in list view
    list_filter = ('name', 'code','region') # Filter sidebar options
    search_fields = ('name','region',)  # Searchable fields
    ordering = ('name', 'code','region',)  # Default ordering
    autocomplete_fields = ["created_by"]
    
    class Media:
         css = {
             'all': ('admin/css/custom_admin.css',)  # Path to your custom CSS
         }
         
    def save_model(self, request, obj, form, change):
        # Set the current user as 'created_by' only when the object is newly created
        if not change:  # 'change' is False when adding a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(District, DistrictModelAdmin)

#admin.site.register(City)
class CityModelAdmin(admin.ModelAdmin):
    # Exclude the 'created_by' field from the admin form
    exclude = ('created_at',)
    
    list_display = ('name', 'code','district', 'latitude', 'longitude',)  # Fields to display in list view
    list_filter = ('name', 'code','district') # Filter sidebar options
    search_fields = ('name','district',)  # Searchable fields
    ordering = ('name', 'code','district',)  # Default ordering
    autocomplete_fields = ["created_by"]
    
    # list_display = ('name', 'show_map')

    def show_map(self, obj):
        # Creates a clickable link with city name that opens a modal
        return format_html(
            '<a href="#" class="show-map" data-lat="{}" data-lng="{}">View Map</a>',
            obj.latitude, obj.longitude
        )
    show_map.short_description = "City Map"
    
    class Media:
         css = {
             'all': ('admin/css/custom_admin.css',)  # Path to your custom CSS
         }
         
    def created_at_date(self, obj):
        return obj.created_at.date()  # Extract only the date part

    created_at_date.short_description = 'Created At'  # Change column name in the list view
    
    def save_model(self, request, obj, form, change):
        # Set the current user as 'created_by' only when the object is newly created
        if not change:  # 'change' is False when adding a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(City, CityModelAdmin)

class TitleModelAdmin(admin.ModelAdmin):
    # Exclude the 'created_by' field from the admin form
    exclude = ('created_by',)
    
    list_display = ('name', 'code', 'description', 'active')  # Fields to display in list view
    list_filter = ('name', 'code', 'description', 'active',)  # Filter sidebar options
    search_fields = ('name', 'code', 'active')  # Searchable fields
    ordering = ('name', 'code', 'active')  # Default ordering
    autocomplete_fields = ["created_by"]
    
    class Media:
         css = {'all': ('admin/css/custom_admin.css',)  }
         
    def save_model(self, request, obj, form, change):
        if not change:  # 'change' is False when adding a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(Title, TitleModelAdmin)

class DesignationModelAdmin(admin.ModelAdmin):
    # Exclude the 'created_by' field from the admin form
    exclude = ('created_by',)
    
    list_display = ('name', 'code', 'description', 'active')  # Fields to display in list view
    list_filter = ('name', 'code', 'description', 'active',)  # Filter sidebar options
    search_fields = ('name', 'code', 'active')  # Searchable fields
    ordering = ('name', 'code', 'active')  # Default ordering
    autocomplete_fields = ["created_by"]
    
    class Media:
         css = {'all': ('admin/css/custom_admin.css',)  }
         
    def save_model(self, request, obj, form, change):
        if not change:  # 'change' is False when adding a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(Designation, DesignationModelAdmin)

class AreaModelAdmin(admin.ModelAdmin):
    # Exclude the 'created_by' field from the admin form
    exclude = ('created_by',)
    
    list_display = ('name', 'code', 'description', 'active')  # Fields to display in list view
    list_filter = ('name', 'code', 'description', 'active',)  # Filter sidebar options
    search_fields = ('name', 'code', 'active')  # Searchable fields
    ordering = ('name', 'code', 'active')  # Default ordering
    autocomplete_fields = ["created_by"]
    
    class Media:
         css = {'all': ('admin/css/custom_admin.css',)  }
         
    def save_model(self, request, obj, form, change):
        if not change:  # 'change' is False when adding a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(Area, AreaModelAdmin)

# class VoterModelAdmin(admin.ModelAdmin):
#     # Exclude the 'created_by' field from the admin form
#     exclude = ('created_by','created_at',)
    
#     list_display = ('voter_id', 'firstname', 'lastname', 'email', 'tel','country','region','district','area','designation','can_vote','electco', 'active')  # Fields to display in list view
#     list_filter = ('voter_id', 'firstname', 'lastname', 'email', 'tel','country', 'active',)  # Filter sidebar options
#     search_fields = ('voter_id', 'firstname', 'lastname', 'email', 'tel','country', 'active')  # Searchable fields
#     ordering = ('voter_id', 'firstname', 'lastname', 'email', 'tel','country', 'active')  # Default ordering
#     autocomplete_fields = ["created_by"]
    
#     class Media:
#          css = {'all': ('admin/css/custom_admin.css',)  }
         
#     def save_model(self, request, obj, form, change):
#         if not change:  # 'change' is False when adding a new object
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)
# admin.site.register(Voter, VoterModelAdmin)

##################33 ALLOWS FOR CSV UPLOAD#############################################


# class VoterModelAdmin(admin.ModelAdmin):
#     #Admin panel customization for Voter model with CSV upload."""
#     exclude = ('created_by', 'created_at')
#     list_display = ('voter_id', 'firstname', 'lastname', 'email', 'upload_csv_button')

#     def upload_csv_button(self, obj=None):
#         url = reverse('admin:upload-voter-csv')
#         return format_html('<a class="button" href="{}">Upload CSV</a>', url)

#     upload_csv_button.short_description = "Upload Voters via CSV"


# admin.site.register(Voter, VoterModelAdmin)


class VoterModelAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'firstname', 'lastname', 'email', 'tel')

    def get_urls(self):
        """Add custom admin URL for CSV upload."""
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.admin_site.admin_view(self.upload_csv), name="admin_upload_voter_csv"),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        """Handle CSV upload."""
        if request.method == "POST":
            csv_file = request.FILES.get("csv_file")
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "File must be a CSV!")
                return redirect("..")

            try:
                data_set = csv_file.read().decode("utf-8")
                io_string = io.StringIO(data_set)
                reader = csv.reader(io_string, delimiter=",")
                next(reader)  # Skip header row
                
                created_count = 0
                for row in reader:
                    country = Country.objects.filter(name=row[5]).first() if row[5] else None
                    region = Region.objects.filter(name=row[6]).first() if row[6] else None
                    district = District.objects.filter(name=row[7]).first() if row[7] else None
                    area = Area.objects.filter(name=row[8]).first() if row[8] else None
                    designation = Designation.objects.filter(name=row[9]).first() if row[9] else None

                    voter, created = Voter.objects.update_or_create(
                        voter_id=row[0],
                        defaults={
                            "firstname": row[1],
                            "lastname": row[2],
                            "email": row[3],
                            "tel": row[4],
                            "country": country,
                            "region": region,
                            "district": district,
                            "area": area,
                            "designation": designation,
                            "can_vote": row[10].lower() == "true",
                            "electco": int(row[11]) if row[11] else 0,
                            "created_by": request.user
                        }
                    )
                    if created:
                        created_count += 1
                
                messages.success(request, f"Successfully uploaded {created_count} voters.")
                return redirect("..")
            
            except Exception as e:
                messages.error(request, f"Error processing CSV: {str(e)}")
                return redirect("..")

        return render(request, "admin/csv_upload.html", {})

admin.site.register(Voter, VoterModelAdmin)

# class VoterModelAdmin(admin.ModelAdmin):
#     #Admin panel customization for Voter model with bulk CSV upload support."""
    
#     exclude = ('created_by', 'created_at')
    
#     list_display = ('voter_id', 'firstname', 'lastname', 'email', 'upload_csv_button')
    
#     def upload_csv_button(self, obj):
#         #Returns a button linking to the CSV upload page."""
#         url = reverse('admin:upload-voter-csv')  # Ensure correct admin URL
#         return format_html('<a class="button" href="{}">Upload CSV</a>', url)

#     upload_csv_button.short_description = "Bulk Upload"
#     upload_csv_button.allow_tags = True  # Allow HTML rendering
    
#     #list_display = ('voter_id', 'firstname', 'lastname', 'email', 'tel', 'country', 'region', 'district', 'area', 'designation', 'can_vote', 'electco', 'active')
#     list_filter = ('country', 'region', 'district', 'can_vote', 'active')
#     search_fields = ('voter_id', 'firstname', 'lastname', 'email', 'tel')
#     ordering = ('voter_id', 'firstname', 'lastname')
#     autocomplete_fields = ["created_by"]
    
#     class Media:
#         css = {'all': ('admin/css/custom_admin.css',)}

#     def save_model(self, request, obj, form, change):
#         #Set created_by field automatically."""
#         if not change:
#             obj.created_by = request.user
#         super().save_model(request, obj, form, change)

#     def get_urls(self):
#         #Add a custom admin URL for CSV upload."""
#         from django.urls import path
#         urls = super().get_urls()
#         custom_urls = [
#             path('upload-csv/', self.admin_site.admin_view(self.upload_csv), name="upload-voter-csv"),
#         ]
#         return custom_urls + urls

#     # def upload_csv_button(self, obj):
#     #     #Button for uploading CSV"""
#     #     return format_html('<a class="button" href="upload-csv/">Upload CSV</a>')
    
#     def upload_csv(self, request):
#         #Handle CSV file upload and create Voter objects."""
#         if request.method == "POST":
#             csv_file = request.FILES.get("csv_file")
#             if not csv_file.name.endswith('.csv'):
#                 messages.error(request, "File must be a CSV!")
#                 return redirect("..")

#             try:
#                 data_set = csv_file.read().decode("utf-8")
#                 io_string = io.StringIO(data_set)
#                 reader = csv.reader(io_string, delimiter=",")
#                 next(reader)  # Skip header row
                
#                 created_count = 0
#                 for row in reader:
#                     if len(row) < 7:  # Ensure required columns exist
#                         messages.warning(request, "Skipping invalid row: " + str(row))
#                         continue

#                     # Retrieve related objects
#                     country = Country.objects.filter(name=row[5]).first() if row[5] else None
#                     region = Region.objects.filter(name=row[6]).first() if row[6] else None
#                     district = District.objects.filter(name=row[7]).first() if row[7] else None
#                     area = Area.objects.filter(name=row[8]).first() if row[8] else None
#                     designation = Designation.objects.filter(name=row[9]).first() if row[9] else None

#                     # Create voter entry
#                     voter, created = Voter.objects.update_or_create(
#                         voter_id=row[0],
#                         defaults={
#                             "firstname": row[1],
#                             "lastname": row[2],
#                             "email": row[3],
#                             "tel": row[4],
#                             "country": country,
#                             "region": region,
#                             "district": district,
#                             "area": area,
#                             "designation": designation,
#                             "can_vote": row[10].lower() == "true",
#                             "electco": int(row[11]) if row[11] else 0,
#                             "created_by": request.user
#                         }
#                     )
#                     if created:
#                         created_count += 1
                
#                 messages.success(request, f"Successfully uploaded {created_count} voters.")
#                 return redirect("..")
            
#             except Exception as e:
#                 messages.error(request, f"Error processing CSV: {str(e)}")
#                 return redirect("..")

#         return render(request, "admin/csv_upload.html", {})

#     actions = [upload_csv_button]
    
# admin.site.register(Voter, VoterModelAdmin)


class YesNoOptionModelAdmin(admin.ModelAdmin):
    # Exclude the 'created_by' field from the admin form
    exclude = ('created_by','created_at',)
    
    list_display = ('position', 'vote_yn',  'photo',)  # Fields to display in list view
    list_filter = ('position', 'vote_yn', 'photo',)  # Filter sidebar options
    search_fields = ('position', 'vote_yn','photo',)  # Searchable fields
    ordering = ('position', 'vote_yn', 'photo',)  # Default ordering
    autocomplete_fields = ["created_by"]
    
    class Media:
         css = {'all': ('admin/css/custom_admin.css',)  }
         
    def save_model(self, request, obj, form, change):
        if not change:  # 'change' is False when adding a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(YesNoOption, YesNoOptionModelAdmin)

class PositionModelAdmin(admin.ModelAdmin):
    #Customized Django Admin for Position model with dynamic Yes/No option handling."""
    
    exclude = ("created_by", "modified_by", "modified_at")  # Fields to exclude in admin form
    
    list_display = ("description", "election", "max_vote", "priority", "vote_type", "active")  # List view fields
    list_filter = ("description", "election", "max_vote", "priority", "vote_type", "active")  # Filter sidebar options
    search_fields = ("description", "election__name", "vote_type")  # Searchable fields
    ordering = ("description", "election", "max_vote", "priority", "vote_type", "active")  # Default ordering
    autocomplete_fields = ["created_by"]
    
    form = PositionAdminForm  # Attach the custom form

    class Media:
        #Include custom CSS for admin styling."""
        css = {"all": ("admin/css/custom_admin.css",)}

    def get_inlines(self, request, obj=None):
        #Dynamically show YesNoOptionInline only when vote_type is 'yes_no'."""
        if obj and obj.vote_type == "yes_no":
            return [YesNoOptionInline]
        return []

    def save_model(self, request, obj, form, change):
        #Set `created_by` on creation and update `modified_by` & `modified_at` on modification."""
        if change:  
            obj.modified_by = request.user
            obj.modified_at = now()  # Set current timestamp only when modified
        else:
            obj.created_by = request.user  
        super().save_model(request, obj, form, change)

# Register the updated Position model in Django Admin
admin.site.register(Position, PositionModelAdmin)

class ElectionModelAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by', 'modified_at')

    list_display = ('name','start_date','end_date', 'start_time','end_time','max_vote','golive','priority','status','active')  
    list_filter = ('name','start_date','end_date', 'start_time','end_time','max_vote','golive','priority','status','active',)  
    search_fields = ('name','start_date','end_date', 'start_time','end_time','max_vote','golive','priority','status','active')  
    ordering = ('name','start_date','end_date', 'start_time','end_time','max_vote','golive','priority','status','active')  
    autocomplete_fields = ["created_by"]

    class Media:
         css = {'all': ('admin/css/custom_admin.css',)}

    def save_model(self, request, obj, form, change):
        if change:  
            obj.modified_by = request.user
            obj.modified_at = now()  # Set current timestamp only when modified
        else:
            obj.created_by = request.user  
        super().save_model(request, obj, form, change)

admin.site.register(Election, ElectionModelAdmin)

class CandidateModelAdmin(admin.ModelAdmin):
    # Exclude the 'created_by' field from the admin form
    exclude = ('created_by',)
    
    list_display = ('position','title','firstname', 'lastname','photo','active')  # Fields to display in list view
    list_filter = ('position','title','firstname', 'lastname','photo', 'active',)  # Filter sidebar options
    search_fields = ('position','title','firstname', 'lastname','photo','active')  # Searchable fields
    ordering = ('position','title','firstname', 'lastname','photo', 'active')  # Default ordering
    autocomplete_fields = ["created_by"]
    
    class Media:
         css = {'all': ('admin/css/custom_admin.css',)  }
         
    def save_model(self, request, obj, form, change):
        if not change:  # 'change' is False when adding a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(Candidate, CandidateModelAdmin)



class VoteModelAdmin(admin.ModelAdmin):
    # Exclude the 'created_by' field from the admin form
      
    list_display = ('voter','candidate','position', 'election', 'voteVal','timestamp',)  # Fields to display in list view
    list_filter = ('voter','candidate', 'position', 'election', 'voteVal','timestamp',)  # Filter sidebar options
    search_fields = ('voter','candidate', 'position', 'election', 'voteVal','timestamp',)  # Searchable fields
    ordering = ('voter','candidate', 'position', 'election', 'voteVal','timestamp',)  # Default ordering
    
    
    class Media:
         css = {'all': ('admin/css/custom_admin.css',)  }
         
    def save_model(self, request, obj, form, change):
        if not change:  # 'change' is False when adding a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(Vote, VoteModelAdmin)
