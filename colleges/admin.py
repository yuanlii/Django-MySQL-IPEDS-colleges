from django.contrib import admin
import colleges.models as models


# Register your models here.
@admin.register(models.AcademicDomain)
class AcademicDomainAdmin(admin.ModelAdmin):
    fields = ['cipcode', 'ciptitle']
    list_display = ['cipcode', 'ciptitle']
    ordering = ['cipcode', 'ciptitle']

@admin.register(models.GraduationRaceType)
class GraduationRaceTypeAdmin(admin.ModelAdmin):
    fields = ['race_category_name']
    list_display = ['race_category_name']
    ordering = ['race_category_name']

@admin.register(models.LibraryCollectionCategory)
class LibraryCollectionCategoryAdmin(admin.ModelAdmin):
    fields = ['collection_category_name']
    list_display = ['collection_category_name']
    ordering = ['collection_category_name']


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    fields = ['city_id','city_name']
    list_display = ['city_id','city_name']
    ordering = ['city_id','city_name']

@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    fields = ['state_id','state_name']
    list_display = ['state_id','state_name']
    ordering = ['state_id','state_name']


@admin.register(models.PeerComparison)
class PeerComparisonAdmin(admin.ModelAdmin):
    fields = ['institution','comparison_institution']
    list_display = ['institution','comparison_institution']
    ordering = ['institution']


@admin.register(models.Institution)
class InstitutionAdmin(admin.ModelAdmin):

    fields = ['unitid',
                'institution_name',
                'city',
                'state',
                'zip_code',
                'student_faculty_ratio',
                'percent_admitted']

    list_display = ['unitid','institution_name','survey_year','city','state','zip_code','student_faculty_ratio','percent_admitted']
    ordering = ['institution_name']




