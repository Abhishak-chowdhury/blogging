from django.shortcuts import render,redirect
from myapp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth import authenticate,login as login_details,logout as logout_details
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
# Create your views here.

def Home(request):
    cat_obj=Category.objects.all()
    blog_obj_travel_2=Blog.objects.filter(category=1).order_by('-id')[0:2]
    blog_obj_travel_1_to_3=Blog.objects.filter(category=1).order_by('-id')[0:3]
    blog_obj_travel_3_to_5=Blog.objects.filter(category=1).order_by('-id')[3:5]
    blog_obj_sports_1=Blog.objects.filter(category=2).order_by('-id')[0]
    blog_obj_sports_3_to_5=Blog.objects.filter(category=2).order_by('-id')[3:5]
    blog_obj_sports_1_to_3=Blog.objects.filter(category=2).order_by('-id')[0:3]
    blog_obj_education_2=Blog.objects.filter(category=3).order_by('-id')[0:2]
    blog_obj_education_1_to_6=Blog.objects.filter(category=3).order_by('-id')[0:6]
    blog_obj_business_1=Blog.objects.filter(category=4).order_by('-id')[0]
    blog_obj_business_2_to_4=Blog.objects.filter(category=4).order_by('-id')[1:3]
    blog_obj_business_5=Blog.objects.filter(category=4).order_by('-id')[3]
    contex={
        'category_obj':cat_obj,
        'blog_obj_travel_2':blog_obj_travel_2,
        'blog_obj_sports_1':blog_obj_sports_1,
        'blog_obj_education_2':blog_obj_education_2,
        'blog_obj_travel_3_to_5':blog_obj_travel_3_to_5,
        'blog_obj_travel_1_to_3':blog_obj_travel_1_to_3,
        'blog_obj_sports_3_to_5':blog_obj_sports_3_to_5,
        'blog_obj_sports_1_to_3':blog_obj_sports_1_to_3,
        'blog_obj_education_1_to_6':blog_obj_education_1_to_6,
        'blog_obj_business_1':blog_obj_business_1,
        'blog_obj_business_2_to_4':blog_obj_business_2_to_4,
        'blog_obj_business_5':blog_obj_business_5,
    }
    return render(request,'index.html',contex)
def category_wise_blog(request,name):
    cat_obj=Category.objects.all()
    single_cat=Category.objects.get(category_name=name)
    user=request.user
    popular_blog=Likes.objects.alias(num_comments=Count('user')).order_by('-num_comments')[:3]
    blog_obj=Blog.objects.filter(category=single_cat)
    cats_obj=Category.objects.all()
    paginator = Paginator(blog_obj, 3)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    total=page_obj.paginator.num_pages
    contex={
        'single_cat':single_cat,
        'blog_objs':blog_obj,
        'category_obj':cat_obj,
        'page_obj': page_obj,
        'cats_obj':cats_obj,
        'popular_blog':popular_blog,
        'total':[n+1 for n in range(total)],
    }
    return render(request,'category.html',contex)
def blog(request):
    cat_obj=Category.objects.all()
    blogs=Blog.objects.all()
    popular_blog=Likes.objects.alias(num_comments=Count('user')).order_by('-num_comments')[:3]
    paginator = Paginator(blogs, 2)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    total=page_obj.paginator.num_pages
    
    contex={
        'blogs':blogs,
        "page_obj": page_obj,
        'category_obj':cat_obj,
        'total':[n+1 for n in range(total)],
        'popular_blog':popular_blog,
        
    }
    return render(request,'blog.html',contex)
def SingleBlog(request,blog):
    user1=request.user
    print(user1)
    single_cat=Blog.objects.get(blog_slug=blog)
    user=single_cat.user
    profile_obj=Profile.objects.get(user=user)
    comment_user_obj=CommentUser.objects.filter(blog=single_cat)
    user_obj=None
    try:
        user_obj=User.objects.get(username=user1)
    except Exception as e:
        print(e)
    comment=CommentUser.objects.filter(blog=single_cat).count
    cats_obj=Category.objects.all()
    blog_obj_1_to_4=Blog.objects.exclude(blog_slug=blog).order_by('-id')[0:4]
    popular_blog=Likes.objects.alias(num_comments=Count('user')).order_by('-num_comments')[:3]
    is_liked=None
    try:
        is_liked=Likes.objects.get(user=request.user,blog=single_cat)
    except Exception as e:
        print(e)
    contex={
        'single_cat':single_cat,
        'profile_obj':profile_obj, 
        'comment_user_obj':comment_user_obj,
        'user_obj':user_obj,
        'comment':comment,
        'cats_obj':cats_obj,
        'category_obj':cats_obj,
        'blog_obj_1_to_4':blog_obj_1_to_4,
        'is_liked':is_liked,
        'popular_blog':popular_blog
    }
    return render(request,'single.html',contex)
@login_required(login_url='crediantial')
def comment(request):
    if request.method == 'POST':
        user_obj=request.POST.get("user_obj")
        blo_obj=request.POST.get("blo_obj")
        txt=request.POST.get("txt")
        s_slug=request.POST.get("s_slug")
        b_obj=Blog.objects.get(id=blo_obj)
        u_obj=User.objects.get(id=user_obj)
            
        CommentUser.objects.create(blog=b_obj,user=request.user,desc=txt)
        
        
        # if u_obj:
        # CommentUser.objects.create(user=u_obj)
        # CommentUser.objects.create(desc=txt)
        # print(user_obj)
        # print(blo_obj)
        # print(txt)

        return redirect('single-blog',blog=s_slug)
@login_required(login_url='crediantial')
def Search(request):
    
    if request.method == 'POST':
        search=request.POST.get('search')
        searching_blog=Blog.objects.filter(title__icontains=search)
        print(search)
        contex={
            'searching_blog':searching_blog
        }
    return render(request,'search.html',contex)

def About(request):
    return render(request,'about.html')
def Contact(request):
    return render(request,'contact.html')

def Crediantial(request):
    return render(request,'login.html')

def Signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Email = request.POST.get('email')
        Password = request.POST.get('password')
        Confirm_Password = request.POST.get('re-password')
        try:
            if User.objects.filter(email = Email).first():
                messages.warning(request, "Email is already exists,please go to signin")
                return redirect('crediantial')
            
            if Password != Confirm_Password:
                messages.warning(request, "please check your confirm password")
                return redirect('crediantial')
            str_characters = string.ascii_lowercase + string.digits
            username = ''.join(random.choices(str_characters, k=5))  
            user_obj=User(username=name+'_'+username,first_name=name,email=Email,)
            user_obj.set_password(Password)
            print(user_obj)
            user_obj.save()
            messages.success(request, "sucessfully registered and continue to sign in process")
            return redirect('home')
            
        except Exception as e:
            print(e)
    return render('crediantial')

def Signin(request):
    if request.method == 'POST':
        Email = request.POST.get('email')
        Password = request.POST.get('password')
        try:
            obj = User.objects.get(email=Email)
        
            username=obj.username
            print(username)
            user = authenticate(request,email = Email ,password = Password,username=username)
            print(user)
            if user is not None:
                login_details(request, user)
                messages.success(request,f"sucessfully registered {Email}")
                return redirect('home')
            else:
                messages.warning(request,"password is incorrect")
                return redirect('crediantial')
        except Exception as e:
            print(e)
            messages.warning(request,"login details are incorrect")
            return redirect('crediantial')
    return redirect('home')
@login_required(login_url='crediantial')
def logout(request):
    logout_details(request)
    messages.success(request,'thank you for spending some moment')
    return redirect('home')
@login_required(login_url='crediantial')
def ajax_value(request):
    if request.method == 'POST':
        b_id=request.POST.get('blog_id')
        u_id=request.POST.get('user_id')
        blog_obj=request.POST.get('blog_obj')
        numberOfLikes=request.POST.get('numberOfLikes')
        user_object=User.objects.get(id=u_id)
        blog_object=Blog.objects.get(id=b_id)
        print(blog_obj)
        try:
            l_obj=Likes.objects.get(blog=blog_object)
            if l_obj:
                l_obj.user.add(request.user)
                return JsonResponse({"status":"Save"})
        except Exception as e:
            instance=Likes.objects.create(blog=blog_object)
            instance.user.add(request.user)
            instance.save()
            return JsonResponse({"status":"Save"})
        

def changepass(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        oldpassword=request.POST.get('oldpassword')
        newpassword=request.POST.get('newpassword')
        try:
                user_obj=User.objects.get(email=email)
            
                match_password=check_password(oldpassword,user_obj.password)
                if not match_password:
                    messages.warning(request,'old password is not matched')
                    return redirect('change-password')
                else:
                    user_obj.set_password(newpassword)
                    user_obj.save()
                    messages.success(request,'password changed sucessfully')
                    return redirect('change-password')
        except Exception as e:
           
            messages.warning(request,'email does not exists')
            return redirect('change-password')
    return render(request,'changepassword.html')