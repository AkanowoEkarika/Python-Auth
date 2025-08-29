from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from users.views import home_redirect

urlpatterns = [
	path("admin/", admin.site.urls),
	path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
	path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
	path("api/auth/", include("users.urls")),
    	path('', home_redirect, name='home'),

]
