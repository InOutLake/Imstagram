from django.utils import timezone
from .models import Token

class TokenCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            auth_header = request.headers.get('token', None) # Have to move tokens to header prbbl
        except:
            return response
        token_value = auth_header.split(' ')
        # CBTTL Bad decision since it tripples amount of DB querries, but for now I use sqlite that cannot handle this internally
        # or can, but I did'n figuret out that yet 
        Token.objects.filter(token_body=token_value, expires_at__lt=timezone.now()).delete()
        Token.objects.filter(token_body=token_value, authorization_code_expires_at__lt=timezone.now()).delete()
        response = self.get_response(request)
        return response