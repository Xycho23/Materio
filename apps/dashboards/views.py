from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.pets.models import Pet, Adoption, Shelter, Location
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta


class DashboardsView(TemplateView):
    template_name = 'dashboard_analytics.html'

    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month = month_start - timedelta(days=30)

        # Calculate adoption rate and monthly data
        current_month_adoptions = Adoption.objects.filter(application_date__gte=month_start).count()
        last_month_adoptions = Adoption.objects.filter(
            application_date__gte=last_month,
            application_date__lt=month_start
        ).count()

        adoption_rate = 0
        if last_month_adoptions > 0:
            adoption_rate = ((current_month_adoptions - last_month_adoptions) / last_month_adoptions) * 100

        # Get regional pet counts
        region_pets = {
            'ncr_pets': Pet.objects.filter(shelter__location__region='NCR').count(),
            'luzon_pets': Pet.objects.filter(shelter__location__region__icontains='Luzon').count(),
            'visayas_pets': Pet.objects.filter(shelter__location__region__icontains='Visayas').count(),
            'mindanao_pets': Pet.objects.filter(shelter__location__region__icontains='Mindanao').count(),
        }

        # Monthly adoptions data
        monthly_adoptions = []
        for i in range(12, 0, -1):
            month_start = now.replace(day=1) - timedelta(days=30 * (i - 1))
            month_end = (month_start + timedelta(days=32)).replace(day=1)
            count = Adoption.objects.filter(
                application_date__gte=month_start,
                application_date__lt=month_end
            ).count()
            monthly_adoptions.append(count)

        # Update context with all required data
        context.update({
            'location_stats': Location.objects.annotate(
                shelter_count=Count('shelter'),
                pet_count=Count('shelter__pet')
            ).values('region', 'shelter_count', 'pet_count'),

            'shelter_stats': Shelter.objects.annotate(
                available_pets=Count('pet', filter=Q(pet__status='available')),
                adopted_pets=Count('pet', filter=Q(pet__status='adopted')),
                total_pets=Count('pet')
            ).select_related('location').all(),

            'pet_stats': {
                'by_type': Pet.objects.values('type').annotate(count=Count('id')),
                'by_breed': Pet.objects.values('breed').annotate(count=Count('id'))[:10],
                'by_status': Pet.objects.values('status').annotate(count=Count('id')),
            },

            'adoption_stats': {
                'total': Adoption.objects.count(),
                'approved': Adoption.objects.filter(status='approved').count(),
                'pending': Adoption.objects.filter(status='pending').count(),
                'this_month': Adoption.objects.filter(application_date__gte=month_start).count(),
            },

            'recent_adoptions': Adoption.objects.select_related('pet', 'pet__shelter').order_by('-application_date')[:5],

            'recent_applications': Adoption.objects.select_related('pet').order_by('-application_date')[:10],
            'adoption_rate': round(adoption_rate, 2),
            'monthly_adoptions': monthly_adoptions,
            'total_adoptions': Adoption.objects.count(),
            'pet_types': Pet.objects.values('type').annotate(count=Count('id')),
            'local_shelters': Shelter.objects.annotate(
                total_pet_count=Count('pet')
            ).select_related('location').values(
                'name', 'location__city', 'location__region', 'total_pet_count'
            )[:5],

            **region_pets
        })

        return context
