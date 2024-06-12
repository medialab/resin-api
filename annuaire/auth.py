from datetime import timedelta

from django.utils import timezone
from rest_framework.authentication import TokenAuthentication


class TokenExpirationAuthentication(TokenAuthentication):
    def get_model(self):
        model = super().get_model()
        model.objects.filter(created__lt=timezone.now() - timedelta(days=1)).delete()
        return model
