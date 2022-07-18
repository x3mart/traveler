"""traveler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from accounts.views import MyTokenObtainPairView, PasswordRecovery, PasswordRecoveryConfirm
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.i18n import i18n_patterns
import debug_toolbar
from accounts.views import RedirectSocial


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('retailrocket/', make_retailrocket_yml),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    # Djoser Beta extension for social_django
    path('api/auth/social/', include('djoser.social.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/jwt/create/', MyTokenObtainPairView.as_view(), name='token_create'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path to my app's endpoints
    path('api/', include('accounts.urls')),
    path('api/', include('tours.urls')),
    path('api/', include('languages.urls')),
    path('api/', include('geoplaces.urls')),
    path('api/', include('currencies.urls')),
    path('api/', include('currencies.urls')),
    path('api/', include('docs.urls')),
    path('api/', include('bankdetails.urls')),
    path('api/', include('verificationrequests.urls')),
    path('api/', include('tgbots.urls')),
    path('api/', include('chats.urls')),
    path('api/', include('articles.urls')),
    path('api/', include('supports.urls')),
    path('api/', include('orders.urls')),
    # test google-oauth2
    path('account/profile/', RedirectSocial.as_view()),
    # temporary password recovery Must be deleted on production
    path('password/passwordrecovery/', PasswordRecovery.as_view(), name='admin_password_reset'),
    path('password/reset/confirm/<str:uid>/<str:token>', PasswordRecoveryConfirm.as_view()),
]

urlpatterns += i18n_patterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    schema_view = get_schema_view(
        openapi.Info(
            title="Snippets API",
            default_version='v1',
            description="Test description",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@snippets.local"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns += [
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('__debug__/', include(debug_toolbar.urls)),
    ]
urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
