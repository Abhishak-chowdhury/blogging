from django.urls import path
from myapp import views
urlpatterns = [
    path('',views.Home,name='home'),
   
    path('blogs',views.blog,name='blogs'), 
    path('single-blog/<slug:blog>',views.SingleBlog,name='single-blog'),
    path('about',views.About,name='about'),
    path('contact-us',views.Contact,name='contact-us'),
    path('category/<str:name>',views.category_wise_blog,name='category_wise_blog'),
    path('crediantial',views.Crediantial,name='crediantial'),
    path('signup',views.Signup,name='signup'),
    path('signin',views.Signin,name='signin'),
    path('logout',views.logout,name='logout'),
    path('comment',views.comment,name='comment'),
    path('ajax_value',views.ajax_value,name='ajax_value'),
    path('search',views.Search,name='search'),
    path('change-password',views.changepass,name='change-password'),
]