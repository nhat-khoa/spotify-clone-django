from email import message
from rest_framework import permissions

class IsArtistUser(permissions.BasePermission):
    """
    Custom permission để kiểm tra user có phải là artist không
    """
    message = "You must be an artist to perform this action."
    
    def has_permission(self, request, view):
        # Kiểm tra xem user có đăng nhập và có role là artist không
        return request.user and request.user.is_authenticated and hasattr(request.user, 'artist_profile')

class IsTrackOwner(permissions.BasePermission):
    """
    Custom permission để kiểm tra user có phải là chủ sở hữu của track không
    """
    message = "You are not the owner of this track."
    
    def has_object_permission(self, request, view, obj):
        return obj.artist == request.user.artist_profile
    
    def has_permission(self, request, view, *args, **kwargs):     
        # For object-specific actions, let has_object_permission handle it
        return True