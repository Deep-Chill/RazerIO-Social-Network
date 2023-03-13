import django_filters
from .models import JobListing

class JobFilter(django_filters.FilterSet):
    company = django_filters.CharFilter(field_name='Company', lookup_expr='icontains')
    job_title = django_filters.CharFilter(lookup_expr='icontains')
    experience_level = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte')

    class Meta:
        model = JobListing
        fields = ['company', 'job_title', 'experience_level', 'category', 'location', 'salary_min', 'salary_max']
