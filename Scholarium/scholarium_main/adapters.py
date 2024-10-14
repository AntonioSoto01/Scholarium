from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from django.http import HttpResponse


class RestrictedAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
            raise ImmediateHttpResponse(HttpResponse('Registrations are closed.', status=403))
class RestrictedSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        raise ImmediateHttpResponse(HttpResponse('Registrations are closed.', status=403))