from django.utils import timezone
from .models import Token

class TokenCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            token_value = request.headers.get('token', None) # TODO Have to move tokens to header prbbl
        finally:
            if not token_value:
                response = self.get_response(request)
                return response
        # TODO CBTTL Bad decision since it tripples amount of DB querries, but for now I cannot come up with better idea
        token_value = str(token_value)
        Token.objects.filter(token_body=token_value, expires_at__lt=timezone.now()).delete()
        Token.objects.filter(token_body=token_value, authorization_code_expires_at__lt=timezone.now()).delete()
        response = self.get_response(request)
        return response