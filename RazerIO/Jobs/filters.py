import django_filters
from .models import JobListing
from django_filters import DateFilter

class JobFilter(django_filters.FilterSet):
    Date_Posted = DateFilter(lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte')
    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')

    class Meta:
        model = JobListing
        fields = ['Company', 'Experience_Level', 'salary_min', 'salary_max',
                  'Date_Posted']
