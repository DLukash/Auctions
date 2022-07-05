#Django & DRF
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase

#Models
from auction.models import User, Auction, Bid, Region

#Other
from datetime import datetime, datetime, timezone, timedelta


class BaseTestCase(APITestCase):
    fixtures = [
        'auction_fixtures.json',
        'region_fixtures.json',
        'user_fixtures.json',
        'bid_fixtures.json'
    ]

    def setUp(self) -> None:
        self.user_one = User.objects.get(pk=1)
        self.user_two = User.objects.get(pk=2)


class AuctionTestCase(BaseTestCase):
    
    def test_create_create_auction_shorter_hour(self):
        url = reverse('auction-list')
        self.client.force_authenticate(user = self.user_one)
        response = self.client.post(url, data={
            "photo": "",
            "cadnumber": "0000000000:00:000:0000",
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
            "cadnumber": "0000000000:00:000:0000",
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

    def test_create_delete_auction_by_author(self):
        url = reverse('auction-detail', args=[1])
        self.client.force_authenticate(user = self.user_one)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_delete_auction_not_by_author(self):
        url = reverse('auction-detail', args=[2])
        self.client.force_authenticate(user = self.user_one)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BidTestCase(BaseTestCase):
    
    def setUp(self) -> None:
        #Up to date Auction
        super().setUp()

        #Normal auction
        Auction.objects.create(
            pk = 1001,
            cadnumber = "0000000000:00:000:0000",
            size = 1,
            duration = 1,
            start_date = datetime.now(timezone.utc),
            author = self.user_one,
            region = Region.objects.get(pk=1),
        )

        #Outdated auction
        Auction.objects.create(
            pk = 1002,
            cadnumber = "0000000000:00:000:0000",
            size = 1,
            duration = 1,
            start_date = datetime.now(timezone.utc) - timedelta(hours=2),
            author = self.user_one,
            region = Region.objects.get(pk=1),
        )

    def test_bid_by_auction_author(self):
        url = reverse('bid-list')
        self.client.force_authenticate(user = self.user_one)
        response = self.client.post(url, data={
                "price": 100,
                "auction": 1001
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bid_not_by_auction_author(self):
        url = reverse('bid-list')
        self.client.force_authenticate(user = self.user_two)
        response = self.client.post(url, data={
                "price": 100,
                "auction": 1001
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_bid_on_outdated_auction(self):
        url = reverse('bid-list')
        self.client.force_authenticate(user = self.user_two)
        response = self.client.post(url, data={
                "price": 100,
                "auction": 1002
        })
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bid_two_times_in_a_raw(self):
        url = reverse('bid-list')
        self.client.force_authenticate(user = self.user_two)
        self.client.post(url, data={
                "price": 100,
                "auction": 1001
        })
        response1 = self.client.post(url, data={
                "price": 100,
                "auction": 1001
        })
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)



    

    



    