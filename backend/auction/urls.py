
#Django & DRF
from django.urls import path
from rest_framework.routers import DefaultRouter

#Views
from auction.views import RegionViewSet, AuctionViewSet, BidViewSet



#Auctions
urlpatterns = [
    path('auction/',AuctionViewSet.as_view({'get':'list',
                                      'post':'create'})),
    path('auction/<int:pk>', AuctionViewSet.as_view({'get':'retrieve', 
                                                'patch':'partial_update', 
                                                'delete':'destroy'}))   
]

#Regions
region_router = DefaultRouter()
region_router.register('region', RegionViewSet, basename='region')
urlpatterns += region_router.urls

#Bids
urlpatterns +=[
    path('bid/', BidViewSet.as_view({'get':'list',
                                'post':'create'})),
    path('bid/<int:pk>', BidViewSet.as_view({'get':'retrieve', 
                                        'delete':'destroy'}))
]

