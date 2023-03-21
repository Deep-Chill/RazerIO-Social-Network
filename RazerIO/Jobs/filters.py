import django_filters
from .models import JobListing
from django_filters import DateFilter

class JobFilter(django_filters.FilterSet):
    Date_Posted = DateFilter(lookup_expr='gte')

    class Meta:
        model = JobListing
        fields = ['Company', 'Category', 'Experience_Level', 'OtherInfo', 'Location', 'Date_Posted']
