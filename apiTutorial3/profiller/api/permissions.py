from rest_framework import permissions


class KendiProfiliOrReadOnly(permissions.IsAdminUser):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS :
            return True
        else:
            return obj.user == request.user 
        

class DurumSahibiOrReadOnly(permissions.IsAdminUser):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS :
            return True
        else:
            return obj.user_profil == request.user.profil
        