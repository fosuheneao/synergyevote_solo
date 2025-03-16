from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema View for API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Synergy Evote - GoVote API",
        default_version="v1",
        description="API documentation for the GoVote electronic voting system.",
        terms_of_service="https://www.yourwebsite.com/terms/",
        contact=openapi.Contact(email="support@yourwebsite.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
