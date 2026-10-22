"""
URL configuration for the TicketsAnywhere API.

- /health          liveness probe for containers / load balancers
- /admin/          Django admin
- /api/            REST API (see ticketapp/urls.py)
- /api/token/...   SimpleJWT token endpoints
- /api-auth/       DRF browsable-API login
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.views.decorators.http import require_safe
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@require_safe
def health(request):
    """Lightweight liveness check; does not touch the database."""
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('health', health, name='health'),
    path('health/', health),
    path('admin/', admin.site.urls),
    path('api/', include('ticketapp.urls')),
    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Built-in login
    path('api-auth/', include('rest_framework.urls')),
]
