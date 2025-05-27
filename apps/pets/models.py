from django.db import models

class Location(models.Model):
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.city}, {self.region}"

class Shelter(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    def get_pet_count(self):
        return self.pet_set.count()
    get_pet_count.short_description = 'Pet Count'
    
    def __str__(self):
        return self.name

class Pet(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('adopted', 'Adopted'),
        ('treatment', 'In Treatment')
    ])
    
    def __str__(self):
        return self.name

class Adoption(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adopter_name = models.CharField(max_length=100)
    adopter_phone = models.CharField(max_length=20)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ])
    approved_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.adopter_name} - {self.pet.name}"
