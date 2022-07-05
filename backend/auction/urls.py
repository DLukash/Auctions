
#Django & DRF
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

#Views
from auction.views import RegionViewSet, AuctionViewSet, BidViewSet, AuctionAuditView, StatisticView


#Auctions
urlpatterns = [
    path('auction/',AuctionViewSet.as_view({'get':'list',
                                      'post':'create'}), name = 'auction-list'),
    path('auction/<int:pk>', AuctionViewSet.as_view({'get':'retrieve', 
                                                'patch':'partial_update', 
                                                'delete':'destroy'}), name = 'auction-detail'),
    path('auction/audit', AuctionAuditView.as_view(), name = 'auction-audit'),
    path('auction/statistic', StatisticView.as_view(), name = 'auction-statistics'),
]

#Regions
region_router = DefaultRouter()
region_router.register('region', RegionViewSet, basename='region')
urlpatterns += region_router.urls

#Bids
urlpatterns +=[
    path('bid/', BidViewSet.as_view({'get':'list',
                                'post':'create'}), name = 'bid-list'),
    path('bid/<int:pk>', BidViewSet.as_view({'get':'retrieve', 
                                        'delete':'destroy'}), name = 'bid-detail')
]

#Staticfiles & mediafiles
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
