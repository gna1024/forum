from django.shortcuts import render, redirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_GET
from django.shortcuts import render
from .models import Post, Reply, Profile


def forum(request):
    profile = Profile.objects.all()
    if request.method == "POST":
        user = request.user
        image = request.user.profile.image
        content = request.POST.get('content', '')
        post = Post(user1=user, post_content=content, image=image)
        post.save()
        alert = True
        posts = Post.objects.filter().order_by('-timestamp')  # Retrieve the posts again
        return redirect('Forum')
    posts = Post.objects.filter().order_by('-timestamp')
    return render(request, "forum.html", {'posts': posts})



def discussion(request, myid):
    post = Post.objects.filter(id=myid).first()
    replies = Reply.objects.filter(post=post)
    if request.method == "POST":
        user = request.user
        if hasattr(user, 'profile'):
            image = user.profile.image
        else:
            image = "/path/to/default/image.png"  # Provide a default image URL
        desc = request.POST.get('desc', '')
        reply = Reply(user=user, reply_content=desc, post=post, image=image)
        reply.save()
        alert = True
        return redirect(request.path)
    return render(request, "discussion.html", {'post': post, 'replies': replies})


def UserRegister(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters.")
            return redirect('/register')
        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers.")
            return redirect('/register')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')
    return render(request, "register.html")

def UserLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/myprofile")
        else:
            messages.error(request, "Invalid Credentials")
        alert = True
        return render(request, 'login.html', {'alert': alert})
    return render(request, "login.html")

def UserLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')

@login_required(login_url='/login')
def myprofile(request):
    user = request.user

    # Check if the profile already exists for the user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, "profile.html", {'obj': obj})
        else:
            return render(request, "profile.html", {'form': form})
    else:
        form = ProfileForm(instance=profile)
        return render(request, "profile.html", {'form': form})



@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user has permission to delete the post (e.g., user is the author or an admin)
    if request.user.is_authenticated and (request.user == post.user1 or request.user.is_staff):
        post.delete()
        # Return a JSON response indicating the success of the deletion
        return JsonResponse({'message': 'Post deleted successfully'})
    else:
        # Return a JSON response with an error message if the user doesn't have permission to delete the post
        return JsonResponse({'error': 'You do not have permission to delete this post'}, status=403)
    

@require_GET
def get_post_content(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user.is_authenticated and (request.user == post.user1 or request.user.is_staff):
        data = {
            'post_content': post.post_content
        }
        return JsonResponse(data)
    else:
        return HttpResponseForbidden('You do not have permission to access this post')


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the user has permission to edit the post (e.g., user is the author or an admin)
    if request.user.is_authenticated and (request.user == post.user1 or request.user.is_staff):
        if request.method == "POST":
            post_content = request.POST.get('edit_content', '')
            post.post_content = post_content
            post.save()
            return redirect('Forum')  # Replace 'Forum' with the appropriate URL name of the forum page
        else:
            return render(request, 'edit_post.html', {'post': post})
    else:
        return HttpResponseForbidden('You do not have permission to edit this post')





