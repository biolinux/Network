'''
Description:
This Django code defines the URL patterns for routing requests to different views within the social networking application.

1. The empty path ("") directs to the index view, which displays all posts.
2. The path "login" directs to the login_view for user authentication.
3. The path "logout" directs to the logout_view for logging out the current user.
4. The path "register" directs to the register view for user registration.
5. The path "new_post/" directs to the new_post view for creating a new post.
6. Another empty path ("") directs to the all_posts view, displaying all posts.
7. The path "profile/<str:username>/" directs to the profile view for displaying a user's profile.
8. The path "toggle_follow/<str:username>/" directs to the toggle_follow view for toggling follow status.
9. The path "edit-post/<int:post_id>/" directs to the edit_post view for editing a post.

These URL patterns define the endpoints for accessing different functionalities of the social networking application.
'''

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('new_post/', views.new_post, name='new_post'),
    path('', views.all_posts, name='all_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('toggle_follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post')
]

