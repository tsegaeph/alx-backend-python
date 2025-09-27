import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from django.http import JsonResponse


# Configure logger
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Deny access if outside 6 AM - 9 PM
        if current_hour < 6 or current_hour > 21:
            return HttpResponseForbidden("Chat access is only allowed between 6 AM and 9 PM.")
        
        response = self.get_response(request)
        return response    


class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of messages a user can send per minute based on IP address.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Store IP: [timestamps of POST requests]
        self.ip_request_log = {}

    def __call__(self, request):
        # Only limit POST requests (assume these are message sends)
        if request.method == "POST" and request.path.startswith("/api/conversations/"):
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60  # 1 minute
            limit = 5    # max 5 messages per minute

            timestamps = self.ip_request_log.get(ip, [])
            # Remove timestamps older than window
            timestamps = [ts for ts in timestamps if now - ts < window]

            if len(timestamps) >= limit:
                return JsonResponse(
                    {"detail": "Message rate limit exceeded. Try again later."}, 
                    status=429
                )

            # Add current timestamp
            timestamps.append(now)
            self.ip_request_log[ip] = timestamps

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """
        Get client IP from request headers
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class RolePermissionMiddleware:
    """
    Middleware to enforce role-based permissions for chat access.
    Only users with role 'admin' or 'moderator' can perform certain actions.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Assume user must be authenticated
        user = getattr(request, "user", None)

        # Skip if user is anonymous
        if user is not None and user.is_authenticated:
            allowed_roles = ["admin", "moderator"]

            # Check if user has role attribute (custom User model) 
            user_role = getattr(user, "role", None)
            if user_role not in allowed_roles:
                return JsonResponse(
                    {"detail": "You do not have permission to perform this action."},
                    status=403
                )

        response = self.get_response(request)
        return response