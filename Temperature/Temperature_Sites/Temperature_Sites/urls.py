"""Temperature_Sites URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from django.conf.urls import url
from .views import Views

v = Views()

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', v.res_empty),
    url(r'^index.html$', v.res_index_html),
    url(r'^locations$', v.res_locations),
    url(r'^locations.json$', v.res_locations_json),
    url(r'^search-locations/([a-z]{0,10})$', v.res_search_locations),
    url(r'^plot$', v.res_plot),
]
