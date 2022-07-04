
#Django & DRF
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

#Views
from auction.views import RegionViewSet, AuctionViewSet, BidViewSet, AuctionAudit



#Auctions
urlpatterns = [
    path('auction/',AuctionViewSet.as_view({'get':'list',
                                      'post':'create'})),
    path('auction/<int:pk>', AuctionViewSet.as_view({'get':'retrieve', 
                                                'patch':'partial_update', 
                                                'delete':'destroy'})),
    path('auction/audit', AuctionAudit.as_view())  
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

#Staticfiles & mediafiles
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)