from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="ArabClub API Documentation",
        default_version="v1",
        description="""
        This is just a project to apply an idea
        that might one day be a pride for all Arab developers 😊.
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="islam.kamel@agr.svu.edu.eg"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

api_version = "api/v1/"

urlpatterns = [
    path(f"{api_version}posts/", include("newsfeed.urls"), name="home"),
    path("admin/", admin.site.urls),
    path(f"{api_version}account/", include("users.urls")),
    path(
        f"{api_version}token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        f"{api_version}token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    re_path(
        r"^$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
