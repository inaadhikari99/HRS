"""hrs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from App import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('home/page/<int:page_number>', views.home, name='homepage'),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('upload_dataset/', views.upload_dataset, name="upload dataset"),
    path('user_favorites/', views.get_user_favorites),
    path('add_to_favorite/<int:id>', views.add_to_favorite),
    path('remove_from_favorites/<int:id>', views.remove_from_favorites),
    path('hotels/<int:id>', views.get_hotel_info),
    path('khalti-request/<int:id>', views.KhaltiReq, name="khaltirequest"),
    path("khalti-verify/", views.KhaltiVerify, name="khaltiverify")

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
