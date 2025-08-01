
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ItemDetailView
from .views import ExchangeRequestsView

urlpatterns = [
    path('', views.index, name='Home'),
    path('my_items', views.my, name='MyItems'),
    path('register', views.register, name='Registration'),
    path('login', views.user_login, name='Login'),
    path('create', views.create, name='Create'),
    path('detali/<int:pk>/', ItemDetailView.as_view(), name='ItemDetali'),
    path('exchange-requests/', ExchangeRequestsView.as_view(), name='ExchangeRequests'),

   
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)