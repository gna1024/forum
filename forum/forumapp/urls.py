from django.urls import path
from . import views

urlpatterns = [
    path("", views.forum, name="Forum"),
    path("discussion/<int:myid>/", views.discussion, name="Discussions"),
    path("register/", views.UserRegister, name="Register"),
    path("login/", views.UserLogin, name="Login"),
    path("logout/", views.UserLogout, name="Logout"),
    path("myprofile/", views.myprofile, name="Myprofile"),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'), 
    path('get-post-content/<int:post_id>/', views.get_post_content, name='get_post_content'),
    path("edit-post/<int:post_id>/", views.edit_post, name="edit_post"),

]
