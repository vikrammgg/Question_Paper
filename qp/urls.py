from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/',views.add, name='add'),
    # path('qp_t/', views.qp_t, name ='qp_t'),
    path('create-paper/', views.create_question_paper, name='create_question_paper'),
]