from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ElectionViewSet, PositionViewSet, CandidateViewSet, VoteView,
    VoterLoginView, VoterSecondAuthView, ElectionListView
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from .docs import schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="API Docs",
        default_version="v1",
    ),
    public=True,
)


# Router for ViewSets
router = DefaultRouter()
router.register(r'elections', ElectionViewSet, basename='election')
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'candidates', CandidateViewSet, basename='candidate')

# API Endpoints
urlpatterns = [
    path("", include(router.urls)),

    # Voter Authentication
    path("voter/login/", VoterLoginView.as_view(), name="voter-login"),
    path("voter/authenticate/", VoterSecondAuthView.as_view(), name="voter-authenticate"),

    # Elections
    path("elections/", ElectionListView.as_view(), name="elections-list"),
    path("vote/", VoteView.as_view(), name="cast-vote"),

    # Swagger & ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    
    # path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    # path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),

]
