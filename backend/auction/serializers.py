from rest_framework import serializers
from auction.models import Auction, Region, Bid


class AuctionSerializer(serializers.ModelSerializer):

    """ Auction model class serializer"""
    
    class Meta:
        model = Auction
        fields = '__all__'
        extra_kwargs = {'author': {'required': False}} 


class RegionSerializer(serializers.ModelSerializer):

    """ Region model class serializer"""

    class Meta:
        model = Region
        fields = '__all__'
        

class BidSerializer(serializers.ModelSerializer):

    """ Bid model serializer"""

    class Meta:
        model = Bid
        fields = '__all__'

        extra_kwargs = {'author': {'required': False},
                    'previous_bid': {'required': False},
                    'bid_time':{'required': False}
                        }

    
    def save(self, **kwargs):
        super().save(**kwargs)
        pass
    
