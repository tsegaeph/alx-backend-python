import logging
from datetime import datetime
from django.http import HttpResponseForbidden


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
