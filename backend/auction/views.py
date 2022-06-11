
#Django & DRF
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

#Models
from auction.models import Auction, Region, Bid

#Serializers
from auction.serializers import AuctionSerializer, RegionSerializer, BidSerializer

#Custome permition
from auction.permitions import IsAuthor, PermissionPolicyMixin, LessThenFiveMinPass


class AuctionViewSet(PermissionPolicyMixin,
                mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

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

    # TODO Change CREATE method store current user as an author
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


class RegionViewSet(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):

    """
    ViewSet to handle CRUD for Region class
    """
    
    serializer_class = RegionSerializer
    queryset = Region.objects.all()

    permission_classes = [IsAuthenticated]
    

class BidViewSet(PermissionPolicyMixin,
                mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):

    """
    ViewSet to handle CRUD for Bid class
    """
    
    serializer_class = BidSerializer
    queryset = Bid.objects.all()

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

    