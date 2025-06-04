from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    class AdvertisementFilter(django_filters.FilterSet):
        created_at = DateFromToRangeFilter()

        class Meta:
            model = Advertisement
            fields = {
                'status': ['exact'],
                'created_at': ['exact'],
            }

