from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,aauthenticate
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone



def create_officer(request):
    if request.method == 'POST':
        form = CreateOfficerForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                print(f"User created successfully: {user.email}")  
                return redirect('home')
            except Exception as e:
         
                return render(request, 'signup.html', {
                    'form': form, 
                    'error': f'Error creating user: {str(e)}'
                })
        else:
            
            print("Form errors:", form.errors)  
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Please correct the errors below.'
            })
    else:
        form = CreateOfficerForm()
    
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = Login_Form(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
        
            messages.error(request, 'Email or password is incorrect')
    else:
        form = Login_Form()
    
    return render(request, 'login.html', {'form': form})

def home(request):
    
    societies = Socity.objects.all()  
    today = timezone.now()
    one_month_ago = today - timedelta(days=30)
    recent_posts = Post.objects.filter(Posting_Date__gte=one_month_ago).order_by('-Posting_Date')
    
    branch_officers = branch_officer.objects.all()
    
    context = {
        'context': societies,  
        'branch_officer': branch_officers,
        'Post_In_Home':recent_posts
    }
    return render(request, 'home.html', context)

def socity_page(request, name):
    society = get_object_or_404(Socity, name=name)
    posts = Post.objects.filter(socity=society).order_by('-Posting_Date')
    officers = Socity_officer.objects.filter(socity=society) 
    
    context = {
        'society': society,
        'posts': posts,
        'officers': officers 
    }
    return render(request, 'Socity_Page.html', context)

def post_detail(request, id):

    post = get_object_or_404(Post, id=id)
    if not post.socity:
        messages.error(request, "This post is not associated with any society.")
        return redirect('home')
    context = {
        'post': post  
    }
    return render(request, 'post_detail.html', context)

def society_member_required(view_func):
    def wrapper(request, name, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first')
            return redirect('login')
        
        if not request.user.is_active:
            messages.error(request, 'Your account is not active yet. Please contact administrator')
            return redirect('home')
        
        
        society = get_object_or_404(Socity, name=name)
        
        if request.user.socity != society:
            messages.error(request, f'You are not a member of {society.name}')
            return redirect('home')
        
        return view_func(request, name, *args, **kwargs)
    return wrapper


@login_required
@society_member_required
def society_dashboard(request, name):
    
    society = get_object_or_404(Socity, name=name)
    
    
    posts = Post.objects.filter(socity=society)
    
    context = {
        'society': society,
        'posts': posts,
        'user': request.user
    }
    return render(request, 'society_dashboard.html', context)

@login_required
@society_member_required
def create_post(request, name):
    society = get_object_or_404(Socity, name=name)

    if request.method == 'POST':
        print("=" * 60)
        print(" CREATE POST - DEBUG START")
        print("=" * 60)
        
        
        print(f" POST data: {request.POST}")
        print(f" FILES data: {request.FILES}")
        
        
        if 'img' in request.FILES:
            image_file = request.FILES['img']
            print(f" Image found: {image_file.name}")
            print(f" Image size: {image_file.size}")
            print(f" Image type: {image_file.content_type}")
        else:
            print(" NO IMAGE IN FILES")
        
        form = CreatePostForm(request.POST, request.FILES)
        print(f" Form valid: {form.is_valid()}")
        
        if form.is_valid():
            print(" FORM IS VALID - SAVING...")
            
            
            post = form.save(commit=False)
            print(f" Post title: {post.title}")
            print(f" Post image before save: {post.img}")
            
        
            post.socity = society
            
            
            post.save()
            print(f" POST SAVED TO DATABASE")
            print(f" Post image after save: {post.img}")
            print(f" Image URL: {post.img.url if post.img else 'No image'}")
            
            
            from django.db import connection
            print(f"Total posts in DB: {Post.objects.count()}")
            
            latest_post = Post.objects.latest('id')
            print(f" Latest post image: {latest_post.img}")
            
            messages.success(request, 'Post created successfully!')
            return redirect('society_dashboard', name=name)
        else:
            print(" FORM INVALID")
            print(f" Form errors: {form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CreatePostForm()
    
    context = {
        'form': form,
        'society': society
    }
    return render(request, 'create_post.html', context)

@login_required
@society_member_required
def edit_post(request, name, post_id):
    society = get_object_or_404(Socity, name=name)
    post = get_object_or_404(Post, id=post_id, socity=society)
    
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('society_dashboard', name=name)
    else:
        form = CreatePostForm(instance=post)
    
    context = {
        'form': form,
        'society': society,
        'post': post,
        'action': 'Edit'  
    }
    return render(request, 'create_post.html', context)


@login_required
@society_member_required
def delete_post(request, name, post_id):
    society = get_object_or_404(Socity, name=name)
    post = get_object_or_404(Post, id=post_id, socity=society)
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Post "{post_title}" deleted successfully!')
        return redirect('society_dashboard', name=name)
    
    
    context = {
        'society': society,
        'post': post
    }
    return render(request, 'confirm_delete.html', context)

def Branch_officer_view(request):
    Branch_officers = branch_officer.objects.all()
    context = {
        'branch_officer': Branch_officers
    }
    return render(request, 'home.html', context)
