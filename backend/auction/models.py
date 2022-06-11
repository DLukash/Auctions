from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator
from rest_framework.serializers import ValidationError
from django.core.validators import RegexValidator

# Create your models here.

class UserManager(BaseUserManager):
    """ Model manager to handle custom User model"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """ Custom ORM model for user"""

    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField()

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []



class Region(models.Model):
    """ ORM model to hold regions """

    name = models.CharField(max_length=25)


class Auction(models.Model):
    """ ORM model to hold auctions """

    photo = models.ImageField(blank=True)
    cadnumber = models.CharField(max_length=23, validators=[RegexValidator(
            regex=r'\d{10}:\d{2}:\d{3}:\d{4}',
            message='The cadaster number should be the 0000000000:00:000:0000 format'
        )])
    size = models.FloatField()
    duration = models.IntegerField(validators=[MinValueValidator(1)])             #How long, in hours, auction should last
    #current_price = models.FloatField(default=0.0)
    
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def last_bid(self):
        """
        Return the last bid acording to bid_time.
        Return None if there is no such bid
        """
        if self.bid_set.exists():
            return self.bid_set.latest('bid_time')
        else:
            return None
    
    @property
    def current_price(self):
        """
        Return the last price acording to bid was made
        Return 0.0 if there are no bids at all
        """
        if self.bid_set.exists():
            return self.bid_set.latest('bid_time').price
        else:
            return 0.0


class Bid(models.Model):
    """ ORM model to hold bids"""

    #previous_bid = models.ForeignKey('self', on_delete=models.DO_NOTHING)
    previous_bid = models.OneToOneField('self', on_delete=models.DO_NOTHING, blank=True, null=True, primary_key=False)
    price = models.FloatField(validators=[MinValueValidator(0)])
    bid_time = models.DateTimeField(default=datetime.now, editable=False)

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)


    def clean(self) -> None:
        
        #Check if bider is not an author of the lot
        if self.author == self.auction.author:
            raise ValidationError("Author of the lot can't bid")

        # Populate the previous bid if there are none of
        if not self.previous_bid:
            self.previous_bid = self.auction.last_bid

        #Check if last bid don't have the same author
        if self.previous_bid:
            if self.previous_bid.author == self.author:
                raise ValidationError ("The same author can't make two bids in a row")

        return super().clean()

    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        """
        Redefind to invoce madel.clean() method during every save 
        to inforce some additional madel level validation
        """
        self.clean()
        return super().save(force_insert, force_update, using, update_fields)

    
    def delete(self, using=None, keep_parents=False):

        """
        In case of bid is deleting change all forward bids if there was some
        """
        later_bids = self.auction.bid_set.filter(bid_time__gte = self.bid_time).order_by('bid_time')
        previous_bid = self.previous_bid
        for bid in later_bids:
            bid.previous_bid = previous_bid
            previous_bid = bid
            bid.save()

        return super().delete(using, keep_parents)

    

    
