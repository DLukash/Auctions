#Django & DRF
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase

#Models
from auction.models import User, Auction, Bid, Region

#Other
from os import path


class AuctionTestCase(APITestCase):

    fixtures = [
        'auction_fixtures.json',
        'region_fixtures.json',
        'user_fixtures.json',
        'bid_fixtures.json'
    ]

    def setUp(self) -> None:
        self.user_one = User.objects.get(pk=1)
        self.user_two = User.objects.get(pk=2)
    
    def test_create_create_auction_shorter_hour(self):
        url = reverse('auction-list')
        self.client.force_authenticate(user = self.user_one)
        response = self.client.post(url, data={
            "photo": "",
            "cadnumber": "0000000000:000:00:0000",
            "size": 2.0,
            "duration": 0,
            "region": 1
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_create_auction_wrong_cadnumber(self):
        url = reverse('auction-list')
        self.client.force_authenticate(user = self.user_two)
        response = self.client.post(url, data={
            "photo": "",
            "cadnumber": "0000000000000000000",
            "size": 2.0,
            "duration": 0,
            "region": 1
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_create_auction_without_authentication(self):
        url = reverse('auction-list')
        self.client.force_authenticate(user = None)
        response = self.client.post(url, data={
            "photo": "",
            "cadnumber": "0000000000:000:00:0000",
            "size": 2.0,
            "duration": 1,
            "region": 1
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_create_auction_with_auth(self):
        url = reverse('auction-list')
        self.client.force_authenticate(user = self.user_one)
        response = self.client.post(url, data={
            "photo": "",
            "cadnumber": "0000000000:00:000:0000",
            "size": 2.0,
            "duration": 1,
            "region": 1
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
    
    



    