from email import message
from rest_framework import permissions

class IsPlaylistOwnerOrInCollaborators(permissions.BasePermission):
    """
    Custom permission to only allow owners of a playlist or users in the collaborators list to edit it.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Allow read-only access for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For write operations, check if the user is the owner or in the collaborators list
        playlist = view.get_object()
        return playlist.user == request.user or request.user.id in playlist.collaborators