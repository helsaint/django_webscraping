from django.urls import path
from .views import web_scrape_api_home, web_scrape_api

urlpatterns = [
    path('', web_scrape_api_home, name='web_scrape_api_home'),
    path('web_scrape_api/', web_scrape_api, name='web_scrape_api'),
]