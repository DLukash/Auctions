from datetime import datetime, timedelta, timezone

#Django & DRF
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from django.db.models import Max, ExpressionWrapper, fields, F

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
        serializer.save(author = self.request.user, duration_timedelta = timedelta(hours=serializer.validated_data['duration']))
    
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


class AuctionAudit(APIView):
    """
    To GET itterate over all open auction (closed = False) and check if it is run of time.
    If so -> make close = True.
    Return number of closed and remaining auctions.
    """
    
    def get(self, request):

        """
        Retrieve all outdated auctions (start_date+duration_timedelta < now)
        Set "closed" to all quaryset
        """

        duration = ExpressionWrapper(F('start_date') + F('duration_timedelta'), 
                                output_field=fields.DateTimeField())
        auctions = Auction.objects.annotate(finish = duration).filter(finish__lt =  datetime.now(timezone.utc))
        auctions.update(closed = True)

        return Response(data={"closed":len(auctions)}, status= status.HTTP_200_OK)

