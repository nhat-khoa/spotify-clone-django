from rest_framework import permissions

class IsArtistUser(permissions.BasePermission):
    """
    Custom permission để kiểm tra user có phải là artist không
    """
    def has_permission(self, request, view):
        # Kiểm tra xem user có đăng nhập và có role là artist không
        return request.user and request.user.is_authenticated and hasattr(request.user, 'artist_profile')

class IsTrackOwner(permissions.BasePermission):
    """
    Custom permission để kiểm tra user có phải là chủ sở hữu của track không
    """
    def has_object_permission(self, request, view, obj):
        # Kiểm tra xem user hiện tại có phải là artist sở hữu track này không
        return obj.artist.user == request.user