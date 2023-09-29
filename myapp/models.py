from django.db import models
import uuid
from django.utils.text import slugify
import random
import string
from django.contrib.auth.models import User
# Create your models here.
RAT = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    
)

class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True

class Profile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    image=models.ImageField(upload_to='profile')
    bio=models.TextField()
    address=models.CharField(max_length=250)

class Category(BaseModel):
    category_name=models.CharField(max_length=100)
    def __str__(self):
        return self.category_name

class Blog(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_user')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category_blog')
    title=models.CharField(max_length=200)
    blog_slug=models.SlugField(verbose_name='auto_generated_slug',unique=True,editable=False,blank=True,default='')
    image=models.ImageField(upload_to='blog_img')
    description=models.TextField()
    def save(self, *args, **kwargs):
        if not self.blog_slug:
            self.blog_slug = slugify(self.title)
            k=Blog.objects.filter(blog_slug=self.blog_slug).exists()
            if k:
                N = 7
                res = ''.join(random.choices(string.ascii_letters, k=N))
                self.blog_slug=self.blog_slug+"_"+res
        super().save(*args, **kwargs)
class BlogSubImg(BaseModel):
    blog=models.OneToOneField(Blog,on_delete=models.CASCADE,related_name='sub_blog')
    sub_img1=models.ImageField(upload_to='sub_blog_img',blank=True)
    sub_img2=models.ImageField(upload_to='sub_blog_img',blank=True)
    sub_img3=models.ImageField(upload_to='sub_blog_img',blank=True)

class CommentUser(BaseModel):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comment_blog')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='c_user',null=True)
    img=models.ImageField(upload_to='comment_user_img',null=True)
    desc=models.TextField()
    

class Likes(BaseModel):
    user=models.ManyToManyField(User,related_name='like_user')
    blog=models.OneToOneField(Blog,on_delete=models.SET_NULL,related_name='blog_likes',null=True)
    like_count=models.IntegerField(default=0)
    def total_likes(self):
        return self.user.count()

