from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Categories(models.Model):
    categories=models.TextField(("Kategori adı"),null=True,blank=True)

class Post(models.Model):
    user=models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    categories=models.ForeignKey(Categories, verbose_name=("Kategori"), on_delete=models.CASCADE)
    post_text=models.TextField(("Post"),null=True,blank=True)
    post_img=models.ImageField(("Post-Fotoğrafı"), upload_to="image",blank=True, null=True)
    likes=models.ManyToManyField(User,related_name='likes',blank=True, verbose_name='Beğen')
    

    
    def total_likes(self):
        return self.likes.all().count()

    
    
class Comment(models.Model):
    user=models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=('Post'),on_delete=models.CASCADE)
    comment=models.TextField(("Yorum"))
    date_now =models.DateTimeField(('Yorum-tarihi'),auto_now_add=True, blank=True, null=True)
    
class Profil(models.Model):
    user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    profil_img=models.ImageField(("profil-fotoğrafı"), upload_to="image", blank=True, null=True, default='img/default-profile-img.png')
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.user.username