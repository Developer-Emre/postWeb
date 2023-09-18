
from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
    users=User.objects.all().order_by("?")
    post_random=Post.objects.all().order_by("?")
    categorys=Categories.objects.all()
    profil=Profil.objects.all()
        
    """Ara"""
    query = request.GET.get('q')
    if query:
        post_random = post_random.filter(
            Q(post_text__icontains=query)|
            Q(categories__categories__icontains=query)
        ).distinct

    
    """Giris yap"""
    
    if request.method == "POST" and "giris" in request.POST:
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            
            messages.error(request,'E-posta veya şifre bilginiz hatalı. Bilgilerinizi kontrol ediniz.')
            return redirect('/')
        else:
      
            messages.error(request,'E-posta veya şifre bilginiz hatalı. Bilgilerinizi kontrol ediniz.')
            return redirect ('/')
    
    """Kayit-Ol"""

    
    if request.method == "POST" and "kayit" in request.POST:
        name=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        password=request.POST['password']
        password_1=request.POST['password-1']

        
        if password==password_1:
            if  User.objects.filter(username=name).exists():
                context={
                "bildirim":"İsim kullanılıyor. Farklı bir isim girerek tekrar deneyebilirsiniz."
            }
                return redirect(request,'index.html',context=context)
            if  User.objects.filter(email=email).exists():
                context={
                "bildirim":"E-mail adresiniz kullanılıyor."
            }
                return redirect(request,'index.html',context=context)
                
            else:   
                user=User.objects.create_user(username=name, password=password, first_name=name, last_name=lastname, email=email)
                
                user.save()
                
            return render(request,'index.html',{"successfull":"Kayıt işleminiz tamamlandı. Bilgilerinizle giriş yapabilirsiniz."})
        else:
            context={
                "bildirim":"Parolanız eşleşmiyor"
            }
        
            return redirect(request,'index.html',context=context)
         
    
    
    if request.method == "POST":
        if "follow" in request.POST:
            # Kullanıcının takip etmek istediği kişi
            to_follow_username = request.POST["follow"]
            to_follow = User.objects.get(username=to_follow_username)
            # Kullanıcıyı takip et
            request.user.profil.followers.add(to_follow)
        elif "unfollow" in request.POST:
            # Kullanıcının takibi bırakmak istediği kişi
            to_unfollow_username = request.POST["unfollow"]
            to_unfollow = User.objects.get(username=to_unfollow_username)
            # Kullanıcının takibini bırak
            request.user.profil.followers.remove(to_unfollow)

    context={
            "post_random":post_random,
            "categorys":categorys,
            "users":users,
            "profil":profil,

        }
    return render(request,'index.html',context)


def logoutUser(request):
    logout(request)
    return redirect('/')


def detail(request,id):
    post= Post.objects.get(id=id)
    comments = Comment.objects.filter(post=post)
    profil=Profil.objects.all()
    users=User.objects.all().order_by("?")
    

        
    if request.method=="POST" and "comment-submit" in request.POST:
        comment=request.POST["comment"]
        comm=Comment(comment=comment,post=post,user=request.user)
        comm.save()
            
        return HttpResponseRedirect('/detail/'+id)

    context = {
        "post":post,
        "comments":comments,
        "profil":profil,
        "users":users,
        "user_profile_pic": request.user.profil.profil_img.url if request.user.is_authenticated else None

    }
    return render(request,'detail.html',context)

@login_required(login_url="/")
def profil(request):
    liked_posts = Post.objects.filter(likes=request.user)

    """"Profil bilgileri giriş"""
    
    user_profile = None  # varsayılan değer None olarak tanımlandı
    if request.user.is_authenticated:
        user_profile = Profil.objects.get(user=request.user)
        

    if request.method == 'POST' and "image" in request.POST:
        file = request.FILES.get('image')
        if user_profile:
            user_profile.profil_img = file
            user_profile.save()
            

    if request.method == 'POST' and "profil" in request.POST:
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        
        following_list = Profil.objects.filter(followers__in=[request.user.id])
        print(following_list)
        context={
            "following_list":following_list
        }

        return redirect('/profil/',context=context)

    return render(request, 'profil.html', {"user_profile": user_profile})
