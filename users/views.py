from django.shortcuts import render,redirect, get_object_or_404,HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import Post,User,Profile,FriendRequest
from .forms import PostForm,RegisterForm,LoginForm,ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings



def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"{username} Welcome")
                return redirect('home')
            else:
                messages.error(request, "No user available with these credentials")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'login_form': form})


@login_required(login_url='login')
def profile(request, id):
    user = get_object_or_404(User, pk=id)
    user_profile = get_object_or_404(Profile, id=id)
    friends = user_profile.friends.all()
    allusers = User.objects.exclude(id=user.id).exclude(profile__in=friends)
    pending_requests = FriendRequest.objects.filter(to_user=request.user, status="Pending")
    posts = Post.objects.filter(author=request.user)
    for post in posts:
        post.total_likes=post.likes.count()
    context = {'user': user, 'allusers': allusers, 'friends': friends, 'pending_requests': pending_requests, 'posts':posts}
    return render(request, 'users/profile.html', context)



def sign_out(request):
    logout(request)
    return redirect('login')




@login_required(login_url='login')
def home(request):
    posts = Post.objects.all()
    for post in posts:
        post.total_likes=post.likes.count()
    context = {'posts': posts,}
    return render(request,'users/home.html', context)  

#---------------------Posts Functions---------------------#
@login_required(login_url='login')
def posts(request):
    posts=Post.objects.all()
    context={'posts':posts}
    return render(request, 'users/posts.html', context)

#likepost
@login_required(login_url='login')
def like_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('home')


@login_required(login_url='login')
def create_post(request):
    if request.method == 'GET':
        form = PostForm()
    elif request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('home')
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'users/post_create.html', context)      
    
@login_required(login_url='login')  
def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('posts')
        else:
            messages.error(request, 'Please correct the following errors:')
    else:
        form = PostForm(instance=post)

    return render(request, 'users/edit_post.html', {'form': form, 'post': post})

@login_required(login_url='login')
def delete_post(request, id):
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, pk=id)
    context = {'post': post}    
    if request.method == 'GET':
        return render(request, 'users/post_delete.html',context)
    elif request.method == 'POST':
        post.delete()
        messages.success(request,  'The post has been deleted successfully.')
        return redirect('posts')   
 

#-----------Friend Request Functions---------------------#
    
@login_required(login_url='login')
def send_friend_request(request, id):
    user_to_send_request = User.objects.get(pk=id)
    current_user = request.user

    if current_user == user_to_send_request:
        return redirect('profile', id=user_to_send_request.id, request_error='Cannot send request to yourself')

    existing_request = FriendRequest.objects.filter(from_user=current_user, to_user=user_to_send_request).exists()
    if existing_request:
        # Inform the user that the request was not sent due to an existing request
        messages.info(request, 'Friend request already sent to this user.')
    else:
        # Create and save the friend request
        friend_request = FriendRequest.objects.create(from_user=current_user, to_user=user_to_send_request)
        # Redirect to the profile of the recipient user
        return redirect('profile', id=user_to_send_request.id)

    # Redirect to the profile page of the user to whom the request was sent
    return redirect('profile', id=id)


@login_required(login_url='login')
def received_friend_requests(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'profile.html', {'pending_requests': pending_requests}) 

@login_required(login_url='login')
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(pk=request_id)
    if friend_request.to_user == request.user and friend_request.status == 'Pending':
        friend_request.status = 'Accepted'
        friend_request.save()
        friend_request.to_user.profile.friends.add(friend_request.from_user.profile)
        friend_request.from_user.profile.friends.add(friend_request.to_user.profile)
        return redirect('profile', id=request.user.id)
    else:
        return redirect('profile', id=friend_request.from_user.id)





@login_required(login_url='login')
def reject_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(pk=request_id)
    if friend_request.to_user == request.user and friend_request.status == 'Pending':
        friend_request.status = 'Rejected'
        friend_request.save()
        return redirect('profile', id=friend_request.from_user.id, request_rejected=True)
    else:
        return redirect('profile')