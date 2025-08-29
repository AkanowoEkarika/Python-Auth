from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ForgotPasswordView, ResetPasswordView, home_redirect

urlpatterns = [
	path("register/", RegisterView.as_view(), name="register"),
	path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
	path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
	path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
	path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    # path('users/', include('users.urls')),

]
