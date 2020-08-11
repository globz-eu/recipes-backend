from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from recipes import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/<int:pk>', views.recipe_detail, name='recipe_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
