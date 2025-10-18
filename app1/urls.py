from django.urls import path
from . import views
urlpatterns=[
    path('signup/',views.create_officer,name='signup'),
    path('login/',views.login_view,name='login'),
    path('Home/',views.home,name='home'),
    path('socity/<str:name>/',views.socity_page,name='socity_page'),
    path('post/<str:id>/',views.post_detail,name='post_detail'),
    path('dashboard/<str:name>/', views.society_dashboard, name='society_dashboard'),
    path('dashboard/<str:name>/create-post/',views.create_post,name='create_post'),
    path('dashboard/<str:name>/edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('dashboard/<str:name>/delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('Branch_officers',views.Branch_officer_view,name='branch_officer'),



]
