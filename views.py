'''
Description:
This Django code implements a basic social networking application with features such as user authentication, 
post creation, post editing, following users, and viewing user profiles. 

The code includes various views and functions to handle different aspects of the application:

1. The `index` view retrieves all posts from the database, paginates them, and renders them on the index page.

2. The `login_view` function handles user authentication. It attempts to authenticate a user based on the provided 
username and password.

3. The `logout_view` function logs out the current user.

4. The `register` function allows users to register for the application.

5. The `new_post` function allows authenticated users to create new posts.

6. The `all_posts` view displays all posts in the application.

7. The `following_posts` view displays posts from users followed by the current user.

8. The `profile` view displays the profile of a user, including their posts, follower count, following count, and follow status.

9. The `toggle_follow` view toggles the follow status between the logged-in user and the requested user.

10. The `edit_post` view allows users to edit their own posts.

This code provides a foundation for building a social networking platform using Django, offering essential 
features for user interaction and content management.
'''

# Import necessary modules and functions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Post, User, Profile
from django.contrib import messages

# Define views and functions

# Index view
def index(request):
    # Retrieve all posts ordered by timestamp
    posts = Post.objects.all().order_by('-timestamp')

    # Paginate the posts
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass paginated posts to the template context
    return render(request, "network/index.html", {'page_obj': page_obj})

# Login view
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "network/login.html")

# Logout view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Register view
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {"message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# New post view
@csrf_exempt
@login_required
def new_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        try:
            if content:
                post = Post.objects.create(content=content, author=request.user)
                return JsonResponse({'success': True, 'post': {'author': post.author.username, 'content': post.content, 'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M:%S')}})
        except Exception as e:
            print("Exception:", e)  
            return JsonResponse({'success': False, 'error': str(e)})  
    return JsonResponse({'success': False, 'error': 'Invalid data'})

# All posts view
@login_required
def all_posts(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/all_posts.html', {'page_obj': page_obj})

# Following posts view
@login_required
def following_posts(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/following_posts.html', {'page_obj': page_obj})

# Profile view
@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-timestamp')

    # Paginator for posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Count followers and following
    follower_count = profile_user.followers.count()
    following_count = profile_user.following.count()

    # Check if the current user follows the profile user
    is_following = request.user.is_authenticated and request.user != profile_user and request.user.following.filter(pk=profile_user.pk).exists()

    context = {
        'profile_user': profile_user,
        'page_obj': page_obj,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_following': is_following,
    }
    return render(request, 'network/profile.html', context)

# Toggle follow view
@login_required
def toggle_follow(request, username):
    profile_user = get_object_or_404(User, username=username)
    if request.user != profile_user:
        profile, created = Profile.objects.get_or_create(user=request.user)
        if request.user.profile.following.filter(id=profile_user.id).exists():
            request.user.profile.following.remove(profile_user)
        else:
            request.user.profile.following.add(profile_user)
        return redirect('profile', username=username)
    else:
        messages.warning(request, "You cannot follow yourself.")
        return redirect('profile', username=username)

# Edit post view
@login_required
def edit_post(request, post_id):
    # Retrieve the post object to edit
    post = get_object_or_404(Post, pk=post_id)

    # Check if the current user is the author of the post
    if request.user == post.author:
        if request.method == 'POST':
            # Update the post content with the new content
            new_content = request.POST.get('content')
            if new_content:
                post.content = new_content
                post.save()
                return redirect('index')
        else:
            # Pre-fill the form with the current post content
            return render(request, 'network/edit_post.html', {'post': post})
    else:
        # If the current user is not the author, display an error message or handle it appropriately
        return HttpResponse("You are not authorized to edit this post.")

from django.http import JsonResponse
from .models import Post

@login_required
@csrf_exempt
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)

        # Check if the user has already liked the post
        if post.likes.filter(pk=request.user.pk).exists():
            # If the user has already liked the post, unlike it
            post.likes.remove(request.user)
            action = 'unlike'
        else:
            # If the user hasn't liked the post, like it
            post.likes.add(request.user)
            action = 'like'

        # Return updated like count
        like_count = post.likes.count()
        return JsonResponse({'likes': like_count, 'action': action})
    else:
        # If request method is not POST, return an error response
        return JsonResponse({'error': 'Invalid request method'}, status=400)
