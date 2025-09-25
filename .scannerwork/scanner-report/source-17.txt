from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('keys/', views.keys_page, name='keys'),
    path('generate-keys/', views.generate_keys_api, name='generate_keys_api'),
    path('crypt/', views.crypt_page, name='crypt'),
    path('decrypt/', views.decrypt_page, name='decrypt'),
    path('public-key/', views.public_key_api, name='public_key'),
    path('decrypt-api/', views.decrypt_api, name='decrypt_api'),
    path('private-key/', views.private_key_api, name='private_key_api'),
]
