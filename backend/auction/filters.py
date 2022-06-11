from django_filters import rest_framework as filters

from auction.models import Region, Auction

class AuctionFilter(filters.FilterSet):
    """
    Filter depends on size and region
    """
    min_size = filters.NumberFilter(field_name='size', lookup_expr='gte')
    max_size = filters.NumberFilter(field_name='size', lookup_expr='lte')
    region = filters.ModelChoiceFilter(queryset=Region.objects.all())

    class Meta:
        model=Auction
        fields=['region', 'min_size', 'max_size']