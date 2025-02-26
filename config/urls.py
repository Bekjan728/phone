from django.contrib import admin 
from django.urls import path, include 
from rest_framework import permissions 
from drf_yasg.views import get_schema_view 
from drf_yasg  import openapi 
 
 
schema_view = get_schema_view( 
    openapi.Info( 
        title='Store API', 
        default_version='v1', 
        description='This is a store API', 
        terms_of_service='http://google.com/policies/terms', 
        contact=openapi.Contact(email='contact@snippets.local'), 
        license=openapi.License(name='BSD License') 
    ), 
    public=True, 
    permission_classes=[permissions.AllowAny] 
) 
 
 
 
urlpatterns = [ 
    path('', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'), 
    path('admin/', admin.site.urls), 
    path('api/phones/', include('apps.phone.urls')), 
    path('api/account/', include('apps.account.urls')), 
    path('api/review/', include('apps.review.urls'))
]