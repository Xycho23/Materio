from django.core.management.base import BaseCommand
from apps.pets.models import Location, Shelter, Pet, Adoption
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Loads sample data for pets app'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Location.objects.all().delete()
        
        # Sample locations
        locations = [
            ('Manila', 'NCR'),
            ('Quezon City', 'NCR'),
            ('Makati', 'NCR'),
            ('Baguio', 'North Luzon'),
            ('Cebu', 'Visayas'),
            ('Davao', 'Mindanao'),
        ]
        
        for city, region in locations:
            Location.objects.create(city=city, region=region)
            
        # Sample shelters
        shelter_names = [
            'Happy Paws Sanctuary',
            'Second Chance Animal Shelter',
            'Pet Haven',
            'Furry Friends Rescue',
            'Pawsitive Care Center',
        ]
        
        for name in shelter_names:
            location = random.choice(Location.objects.all())
            Shelter.objects.create(name=name, location=location)
            
        # Sample pets
        pet_types = ['Dog', 'Cat', 'Bird', 'Rabbit']
        dog_breeds = ['Aspin', 'Shih Tzu', 'Beagle', 'Golden Retriever', 'Pomeranian']
        cat_breeds = ['Puspin', 'Persian', 'Siamese', 'American Shorthair']
        bird_breeds = ['Parrot', 'Lovebird', 'Cockatiel']
        rabbit_breeds = ['Holland Lop', 'Lionhead', 'Dutch']
        
        pet_names = [
            'Max', 'Luna', 'Charlie', 'Bella', 'Rocky',
            'Lucy', 'Milo', 'Nala', 'Leo', 'Lily',
            'Simba', 'Coco', 'Zeus', 'Daisy', 'Oliver'
        ]
        
        statuses = ['available', 'adopted', 'treatment']
        
        for _ in range(30):  # Create 30 pets
            pet_type = random.choice(pet_types)
            if pet_type == 'Dog':
                breed = random.choice(dog_breeds)
            elif pet_type == 'Cat':
                breed = random.choice(cat_breeds)
            elif pet_type == 'Bird':
                breed = random.choice(bird_breeds)
            else:
                breed = random.choice(rabbit_breeds)
                
            Pet.objects.create(
                name=random.choice(pet_names),
                type=pet_type,
                breed=breed,
                shelter=random.choice(Shelter.objects.all()),
                status=random.choice(statuses)
            )
            
        # Sample adoptions
        adopter_names = [
            'Juan Dela Cruz', 'Maria Santos', 'Pedro Reyes',
            'Ana Gonzales', 'Jose Garcia', 'Sofia Rodriguez'
        ]
        
        for pet in Pet.objects.filter(status='adopted'):
            Adoption.objects.create(
                pet=pet,
                adopter_name=random.choice(adopter_names),
                adopter_phone=f'09{random.randint(100000000, 999999999)}',
                status='approved',
                approved_date=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data'))
