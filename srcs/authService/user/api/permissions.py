from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class ApiRequestPermission(permissions.BasePermission):

	def has_permission(self, request, view):
		origin = request.META.get('HTTP_ORIGIN', 'Unknown origin')
		referer = request.META.get('HTTP_REFERER', 'Unknown referer')
		allowed_origins = ['https://alp.com.tr']
		allowed_referers = ['https://alp.com.tr/login', 
					        'https://alp.com.tr/logout', 
					        'https://alp.com.tr/register']
		if origin not in allowed_origins or referer not in allowed_referers:
			raise PermissionDenied(f"You do not have permission to access this resource.")
		return True

class SelfProfilOrReadOnly(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS :
            return True
        else:
            return obj.user == request.user 
        

# class SelfCommentOrReadOnly(permissions.IsAdminUser):

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS :
#             return True
#         else:
#             return obj.user_profil == request.user.profil