from django.contrib import admin
from .models import Location, Shelter, Pet, Adoption

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'region')
    search_fields = ('city', 'region')

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'get_pet_count')
    list_filter = ('location__region',)
    search_fields = ('name',)

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'breed', 'status', 'shelter')
    list_filter = ('status', 'type', 'shelter')
    search_fields = ('name', 'breed')

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ('pet', 'adopter_name', 'status', 'application_date')
    list_filter = ('status',)
    search_fields = ('adopter_name', 'pet__name')
