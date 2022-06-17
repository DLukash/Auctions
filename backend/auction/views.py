
#Django & DRF
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.db.models import Max

#Models
from auction.models import Auction, Region, Bid

#Serializers
from auction.serializers import AuctionSerializer, RegionSerializer, BidSerializer

#Custome permition
from auction.permitions import IsAuthor, PermissionPolicyMixin, LessThenFiveMinPass

#Custom filter
from auction.filters import AuctionFilter, BidFilter


class AuctionViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):
    """ 
    ViewSet of actions for Auction class:
    - Creating (POST)
    - View as a list (GET)
    - View as entity (GET wiht <int:pk>)
    - Modifying (PATCH with <int:pk>)
    - Deleting (DELETE with wiht <int:pk>)
    """
    
    serializer_class = AuctionSerializer
    queryset = Auction.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AuctionFilter

    permission_classes = [IsAuthenticated]

    permission_classes_per_method = {
        "destroy": [IsAuthenticated&IsAuthor&IsAuthenticated],
        "partial_update": [IsAuthenticated&IsAuthor&IsAuthenticated]
    }
   
    def perform_create(self, serializer):
        """
        Overwrited method
        Store authorised user as an author of the auction
        """
        serializer.save(author = self.request.user)
    
    
    def get_queryset(self):
        query_set = super().get_queryset()

        """
        Implementing aditional filtering depends on the last bid
        """

        if 'min_price' in self.request.GET:
            query_set = query_set.annotate(c_price=Max('bid__price')).filter(c_price__gt = self.request.GET['min_price'])

        if 'max_price' in self.request.GET:
            query_set = query_set.annotate(c_price=Max('bid__price')).filter(c_price__lt = self.request.GET['max_price'])
       
        return query_set


class RegionViewSet(viewsets.ModelViewSet):

    """
    ViewSet to handle CRUD for Region class
    """
    
    serializer_class = RegionSerializer
    queryset = Region.objects.all()

    permission_classes = [IsAuthenticated]
    

class BidViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):

    """
    ViewSet to handle CRUD for Bid class
    """
    
    serializer_class = BidSerializer
    queryset = Bid.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BidFilter

    permission_classes = [IsAuthenticated]

    permission_classes_per_method = {
        "destroy": [IsAuthenticated&IsAuthor&LessThenFiveMinPass],
    }

    
    def perform_create(self, serializer):
        """
        Overwrited method
        Store authorised user as an author of the auction
        """
        serializer.save(author = self.request.user)

