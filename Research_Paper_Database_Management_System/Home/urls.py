from django.contrib import admin
from django.urls import path
from Home import views


urlpatterns = [
    path('', views.index, name="index_page"),
    path('users/', views.show_users, name="show_users"),
    path('research_paper/', views.show_research, name="show_research"),
    path('insert/', views.insert_research, name="insert_research"),
    path('research_paper/Edit/<int:id>',views.Editresearch,name="Editresearch"),
    path('Update/<int:id>',views.updateresearch,name="updateresearch"),
    path('research_paper/Delete/<int:id>',views.Delres,name="Delres"),
]