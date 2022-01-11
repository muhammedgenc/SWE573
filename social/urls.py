from django.urls import path
from . import views

urlpatterns = [
    path('service', views.ServiceListView.as_view(), name='service-list'),
    path('service/<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    path('service/create/', views.ServiceCreateView.as_view(), name='service-create'),
    path('service/edit/<int:pk>/', views.ServiceEditView.as_view(), name='service-edit'),
    path('service/delete/<int:pk>/', views.ServiceDeleteView.as_view(), name='service-delete'),
    path('service/<int:service_pk>/application/delete/<int:pk>/', views.ServiceApplicationDeleteView.as_view(), name='application-delete'),
    path('service/<int:service_pk>/application/approve/<int:pk>/', views.ServiceApplicationApproveView.as_view(), name='application-approve'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', views.ProfileEditView.as_view(), name='profile-edit'),
    path('event', views.EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('event/create/', views.EventCreateView.as_view(), name='event-create'),
    path('event/edit/<int:pk>/', views.EventEditView.as_view(), name='event-edit'),
    path('event/delete/<int:pk>/', views.EventDeleteView.as_view(), name='event-delete'),
    path('event/<int:event_pk>/eventapplication/delete/<int:pk>/', views.EventApplicationDeleteView.as_view(), name='eventapplication-delete'),

]