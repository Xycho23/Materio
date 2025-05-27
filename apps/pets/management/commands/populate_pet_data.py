from django.core.management.base import BaseCommand
from apps.pets.models import Location, Shelter, Pet, Adoption
from django.utils import timezone
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate database with sample pet adoption data'

    def handle(self, *args, **kwargs):
        # Create locations
        locations = [
            Location.objects.create(city='Manila', region='NCR'),
            Location.objects.create(city='Quezon City', region='NCR'),
            Location.objects.create(city='Cebu City', region='Visayas'),
            Location.objects.create(city='Davao City', region='Mindanao'),
            Location.objects.create(city='Baguio', region='Luzon'),
            Location.objects.create(city='Makati', region='NCR'),
            Location.objects.create(city='Taguig', region='NCR'),
            Location.objects.create(city='Iloilo', region='Visayas'),
        ]

        # Create shelters with more details
        shelters = []
        shelter_names = [
            'Pawfect Haven', 'Second Chance Sanctuary', 'Happy Tails', 
            'Pet Paradise', 'Animal Haven', 'Furry Friends Rescue',
            'PAWS Philippines', 'Hope Animal Shelter'
        ]
        
        for i, name in enumerate(shelter_names):
            shelter = Shelter.objects.create(
                name=name,
                location=locations[i],
                pet_count=random.randint(15, 45)
            )
            shelters.append(shelter)

        # More detailed pet types and breeds
        pet_types = {
            'Dog': ['Aspin', 'Shih Tzu', 'Golden Retriever', 'Beagle', 'Poodle', 'Labrador', 'Husky'],
            'Cat': ['Puspin', 'Persian', 'Siamese', 'Maine Coon', 'Russian Blue'],
            'Bird': ['Parrot', 'Lovebird', 'Cockatiel', 'Budgie'],
            'Rabbit': ['Holland Lop', 'Netherland Dwarf', 'Mini Rex']
        }

        pet_names = [
            'Lucky', 'Max', 'Luna', 'Charlie', 'Bella', 'Oreo', 'Simba', 
            'Nemo', 'Rocky', 'Coco', 'Milo', 'Tiger', 'Shadow', 'Angel',
            'Princess', 'Zeus', 'Leo', 'Loki', 'Nova', 'Pepper'
        ]

        # Create pets with more variety
        pets = []
        for _ in range(100):  # Create 100 pets
            pet_type = random.choice(list(pet_types.keys()))
            pet = Pet.objects.create(
                name=random.choice(pet_names),
                type=pet_type,
                breed=random.choice(pet_types[pet_type]),
                shelter=random.choice(shelters),
                status=random.choices(['available', 'adopted', 'treatment'], weights=[0.5, 0.3, 0.2])[0]
            )
            pets.append(pet)

        # Create adoption records
        adopter_names = [
            'Juan Dela Cruz', 'Maria Santos', 'Pedro Reyes', 'Ana Gonzales',
            'Mike Torres', 'Sarah Garcia', 'James Lim', 'Emma Cruz',
            'David Tan', 'Sofia Reyes', 'Marcus Santos', 'Isabella Cruz'
        ]

        # Generate adoptions over the last 6 months
        now = timezone.now()
        for pet in pets:
            if pet.status == 'adopted':
                adoption_date = now - timedelta(days=random.randint(1, 180))
                Adoption.objects.create(
                    pet=pet,
                    adopter_name=random.choice(adopter_names),
                    adopter_phone=f'09{random.randint(100000000, 999999999)}',
                    application_date=adoption_date - timedelta(days=random.randint(1, 7)),
                    status='approved',
                    approved_date=adoption_date
                )

        # Create some pending applications
        available_pets = Pet.objects.filter(status='available')
        for _ in range(10):
            application_date = now - timedelta(days=random.randint(1, 14))
            Adoption.objects.create(
                pet=random.choice(available_pets),
                adopter_name=random.choice(adopter_names),
                adopter_phone=f'09{random.randint(100000000, 999999999)}',
                application_date=application_date,
                status='pending'
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with enhanced data'))
