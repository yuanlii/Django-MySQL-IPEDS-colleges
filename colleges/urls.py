from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),

    path('institutions/', views.InstitutionListView.as_view(), name='institution'),
    path('institutions/search/', views.InstitutionFilterView.as_view(), name='institution_search'),
    path('institutions/<int:pk>/', views.InstitutionDetailView.as_view(), name='institution_detail'),

    path('institutions/new/', views.InstitutionCreateView.as_view(), name='institution_new'),
    path('institutions/<int:pk>/delete/', views.InstitutionDeleteView.as_view(), name='institution_delete'),
    path('institutions/<int:pk>/update/', views.InstitutionUpdateView.as_view(), name='institution_update'),
    
    path('filters/', views.InstitutionFilterView.as_view(), name = 'filters')

]




