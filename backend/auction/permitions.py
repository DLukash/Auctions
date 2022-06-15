from datetime import datetime, timezone, timedelta
from rest_framework import permissions
from auction.models import Bid

class IsAuthor(permissions.BasePermission):
    """ 
    Permition for authors
    : also permit SAFE_METHODS for testing perrios

    """

    def has_object_permission(self, request, view, obj):
        print('Check permitions data')
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class NoAuctionAuthor(permissions.BasePermission):
    """
    Permition for not being an author of an Auction
    Use to prevent author from making bids
    : also permit SAFE_METHODS for testing perrios

    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or not isinstance(obj, Bid):
            return True
        return not obj.auction.author == request.user


class LessThenFiveMinPass(permissions.BasePermission):
    """
    Permition for deleting bids
    Bid only can be deleted within 5 min after it made
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or not isinstance(obj, Bid):
            return True
        
        time_diff = timedelta(minutes=5)
        return (datetime.now(timezone.utc) - obj.bid_time) < time_diff


class PermissionPolicyMixin:
    """
    Class to add per-method permissions capability to ViewSets
    """

    def check_permissions(self, request):
        try:
            # This line is heavily inspired from `APIView.dispatch`.
            # It returns the method associated with an endpoint.
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
            handler
            and self.permission_classes_per_method
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(handler.__name__)

        super().check_permissions(request)


