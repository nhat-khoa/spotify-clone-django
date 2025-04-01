from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, ExpiredTokenError
from apps.users.models import User


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = AnonymousUser()  # Đặt user mặc định là AnonymousUser
        request.token = None  # Đặt token mặc định là None
        
        # Lấy token từ header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header is None or auth_header.strip() == '':
            return None

        header_parts = auth_header.split()
        if header_parts[0] != 'Bearer':
            return None
        
        if len(header_parts) != 2:
            return self.unauthorized_response("Authorization header must contain two space-delimited values")
        
        try:
            # Tách token từ header
            raw_token = header_parts[1]

            # Xác thực token
            validated_token = AccessToken(raw_token)
            
            # Lấy user ID từ token
            user_id = validated_token['user_id']

            # Tìm user trong database
            user = User.objects.get(id=user_id)
            # Kiểm tra is_active
            if not user.is_active:
                return self.unauthorized_response("User account is not active.")

            # Gán user vào request để sử dụng trong views
            request.user = user
            request.token = validated_token

            return None

        except (InvalidToken, TokenError, ExpiredTokenError):
            return self.unauthorized_response("Token is invalid or expired.")

        except User.DoesNotExist:
            return self.unauthorized_response("User not found.")

        except Exception as e:
            return self.unauthorized_response(str(e))

    def unauthorized_response(self, message):
        return JsonResponse({
            'error': message
        }, status=401)
