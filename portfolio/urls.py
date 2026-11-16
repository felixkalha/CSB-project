from django.urls import path

from . import views

app_name = 'portfolio'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:project_id>/', views.detail, name='detail'),
    path('<int:project_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment')
] 