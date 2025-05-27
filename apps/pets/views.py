from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Pet, Adoption, Shelter, Location
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard(request):
    # Location statistics
    location_stats = Location.objects.annotate(
        shelter_count=Count('shelter'),
        pet_count=Count('shelter__pet')
    ).values('region', 'shelter_count', 'pet_count')

    # Shelter statistics
    shelter_stats = Shelter.objects.annotate(
        available_pets=Count('pet', filter=Q(pet__status='available')),
        adopted_pets=Count('pet', filter=Q(pet__status='adopted')),
        total_pets=Count('pet')
    ).select_related('location').all()

    # Pet statistics by type and status
    pet_stats = {
        'by_type': Pet.objects.values('type').annotate(count=Count('id')),
        'by_breed': Pet.objects.values('breed').annotate(count=Count('id'))[:10],
        'by_status': Pet.objects.values('status').annotate(count=Count('id')),
    }

    # Adoption statistics
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    adoption_stats = {
        'total': Adoption.objects.count(),
        'approved': Adoption.objects.filter(status='approved').count(),
        'pending': Adoption.objects.filter(status='pending').count(),
        'this_month': Adoption.objects.filter(
            application_date__gte=month_start
        ).count(),
    }

    # Get recent applications
    recent_applications = Adoption.objects.select_related('pet').order_by('-application_date')[:10]

    # Add status color mapping to Adoption model instances
    for application in recent_applications:
        application.get_status_color = {
            'pending': 'warning',
            'approved': 'success',
            'rejected': 'danger'
        }.get(application.status, 'primary')

    # Get regional pet counts
    region_pets = {
        'ncr_pets': Pet.objects.filter(shelter__location__region='NCR').count(),
        'luzon_pets': Pet.objects.filter(shelter__location__region__icontains='Luzon').count(),
        'visayas_pets': Pet.objects.filter(shelter__location__region__icontains='Visayas').count(),
        'mindanao_pets': Pet.objects.filter(shelter__location__region__icontains='Mindanao').count(),
    }

    # Get local shelters with pet count
    local_shelters = Shelter.objects.annotate(
        pet_count=Count('pet')
    ).select_related('location').values(
        'name', 'location__city', 'location__region', 'pet_count'
    )[:5]

    # Get pet types for chart
    pet_types = Pet.objects.values('type').annotate(count=Count('id'))

    # Calculate adoption rate
    last_month = month_start - timedelta(days=30)
    current_month_adoptions = Adoption.objects.filter(
        application_date__gte=month_start
    ).count()
    last_month_adoptions = Adoption.objects.filter(
        application_date__gte=last_month,
        application_date__lt=month_start
    ).count()
    
    adoption_rate = 0
    if last_month_adoptions > 0:
        adoption_rate = ((current_month_adoptions - last_month_adoptions) / last_month_adoptions) * 100

    # Monthly adoptions for the chart (last 12 months)
    monthly_adoptions = []
    for i in range(12, 0, -1):
        month_start = now.replace(day=1) - timedelta(days=30 * (i-1))
        month_end = (month_start + timedelta(days=32)).replace(day=1)
        count = Adoption.objects.filter(
            application_date__gte=month_start,
            application_date__lt=month_end
        ).count()
        monthly_adoptions.append(count)

    context = {
        'layout_path': 'layouts/content.html',  # Add this line
        'location_stats': location_stats,
        'shelter_stats': shelter_stats,
        'pet_stats': pet_stats,
        'adoption_stats': adoption_stats,
        'recent_adoptions': Adoption.objects.select_related(
            'pet', 'pet__shelter'
        ).order_by('-application_date')[:5],
        'recent_applications': recent_applications,
        **region_pets,
        'local_shelters': local_shelters,
        'pet_types': pet_types,
        'total_adoptions': adoption_stats['total'],
        'adoption_rate': round(adoption_rate, 2),
        'monthly_adoptions': monthly_adoptions,
    }
    
    # Debug prints
    print("Location statistics:", list(location_stats))
    print("Shelter statistics:", list(shelter_stats))
    print("Pet statistics:", pet_stats)
    print("Adoption statistics:", adoption_stats)
    print("Recent adoptions:", list(context['recent_adoptions']))
    
    return render(request, 'templates/dashboard_analytics.html', context)

def pet_list(request):
    pets = Pet.objects.filter(status='available')
    return render(request, 'pets/pet_list.html', {'pets': pets})
