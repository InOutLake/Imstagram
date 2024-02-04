from .models import Client, Scope
from .forms import AuthorisationForm

def get_client_by_id(client_id):
    try:
        return Client.objects.get(client_id=int(client_id))
    except Client.DoesNotExist:
        return None

def create_context(client, scope_name):
    return {
        'scope_info': Scope.objects.get(scope_name=scope_name).scope_info,
        'form': AuthorisationForm()
    }