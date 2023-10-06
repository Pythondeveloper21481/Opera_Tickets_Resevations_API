"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from tickets import views


from rest_framework.routers import DefaultRouter

router = DefaultRouter()  #for viewsets
router.register('guest', views.UserViewSet_guest)
router.register('opera', views.UserViewSet_opera)
router.register('resevation', views.UserViewSet_reservation)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('django/jsnomodel', views.no_rest_no_model),
    path('django/jsfrmodel', views.no_rest_from_model),
    path('rest/fbv_list', views.fbv_list),
    path('rest/fbv_pk/<int:pk>', views.fbv_pk),
    path('rest/CBV_list', views.CBV_list.as_view() ),
    path('rest/CBV_pk/<int:pk>', views.CBV_pk.as_view() ), # don't use pk in a real work!
    path('rest/mixins_list', views.mixins_list.as_view()),
    path('rest/mixins_pk/<int:pk>', views.mixins_pk.as_view()),
    path('rest/generics_list', views.generics_list.as_view()),
    path('rest/generics_pk/<int:pk>', views.generics_pk.as_view()),
    path('rest/UserViewSet_guest/', include(router.urls)),
    path('rest/UserViewSet_opera/', include(router.urls)),
    path('rest/UserViewSet_reservation/', include(router.urls)),
    path('search/Search_opera/', views.Search_opera),# use Postman app to search 
    path('search/new_reservation/', views.new_reservation),

]#there is no security in this urls !
#this work is only for education!
