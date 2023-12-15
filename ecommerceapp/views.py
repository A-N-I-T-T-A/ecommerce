from django.shortcuts import render,redirect
from ecommerceapp.models import product,category,cart1,userdetails
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
import os

# Create your views here.
def index(request):
    cata=category.objects.all()
    return render(request,"index.html",{'category':cata})
def loginpage(request):
    return render(request,"login.html")
def loginuser(request):
    if request.method == 'POST':
        user=request.POST['username']
        pwd=request.POST['password']
        usr1=auth.authenticate(username=user, password=pwd)
        if usr1 is not None:
            if usr1.is_staff:
                login(request,usr1)
                return redirect('adminhome')
            else:
                login(request,usr1)
                auth.login(request,usr1)
                # messages.info(request,f'{usr1}')
                return redirect('userindex')
            # request.session['uid']= usr.id
            
        else:
            messages.info(request,'Invalid Username or Password!. Try again')
            return redirect('loginpage')
    else:
        messages.info(request,'Invalid Username or Password!. Try again')
        return redirect('loginpage')
@login_required(login_url='loginpage') 
def adminhome(request):
    current=request.user.id 
    user=User.objects.get(id=current)
    return render(request,"adminhome.html",{'user':user})
@login_required(login_url='loginpage') 
def categorypage(request):
    return render(request,"category.html")
@login_required(login_url='loginpage') 
def addcata(request):
    if request.method == 'POST':
        cata=request.POST['cname']
        c=category(category_name=cata)
        c.save()
        messages.info(request,'Catagory Added')
        return redirect('categorypage')
@login_required(login_url='loginpage') 
def productpage(request):
    cata=category.objects.all()
    return render(request,"product.html",{'category':cata})
@login_required(login_url='loginpage') 
def addproduct(request):
    if request.method == 'POST':
        pname=request.POST['pname']
        des=request.POST['pdesc']
        sel=request.POST['sel']
        c1=category.objects.get(id=sel)
        price=request.POST['price']
        image=request.FILES.get('prdimage')
        p=product(pdname=pname,pdprice=price,pd_desc=des,pdimage=image,category=c1)
        p.save()
        messages.info(request,'Product Added')
        return redirect('productpage')
@login_required(login_url='loginpage') 
def productshow(request):
    p=product.objects.all()
    return render(request,"showproduct.html",{'product':p})
@login_required(login_url='loginpage') 
def delete_prod(request,a):
    p=product.objects.get(id=a)
    if len(p.pdimage)>0:
        os.remove(p.pdimage.path)
    up=cart1.objects.filter(product_id=a)
    up.delete()
    p.delete()
    return redirect('productshow')
@login_required(login_url='loginpage') 
def usershow(request):
    userd=userdetails.objects.all()
    return render(request,"showuser.html",{'users':userd})
@login_required(login_url='loginpage') 
def delete_user(request,a):
    us=userdetails.objects.get(id=a)
    up=cart1.objects.filter(user_id=a)
    if len(us.prf_image)>0:
        os.remove(us.prf_image.path)
    us.delete()
    up.delete()
    us.user.delete()
    return redirect('usershow')
@login_required(login_url='loginpage') 
def logout_admin(request):
    auth.logout(request)
    return redirect('index')
def allcategory(request):
    if request.user.is_authenticated:
        current=request.user.id 
        user=userdetails.objects.get(user_id=current)
        pd=product.objects.all()
        c=category.objects.all()
        return render(request,"userallcate.html",{'products':pd,'user':user,'nav':c})
    else:
        c=category.objects.all()
        pd=product.objects.all()
        return render(request,"allcate.html",{'products':pd,'nav':c})
def showcategory(request,a):
    if request.user.is_authenticated:
        current=request.user.id 
        user=userdetails.objects.get(user_id=current)
        pd=product.objects.filter(category_id=a)
        c=category.objects.all()
        cata=category.objects.get(id=a)
        return render(request,"usershowcate.html",{'products':pd,'category':cata,'user':user,'nav':c})
    else:
        pd=product.objects.filter(category_id=a)
        c=category.objects.all()
        cata=category.objects.get(id=a)
        return render(request,"showcate.html",{'products':pd,'category':cata,'nav':c})

def regpage(request):
    return render(request,"signup.html")
def reguser(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        user=request.POST['username']
        email=request.POST['email']
        pwd=request.POST['password']
        cpwd=request.POST['cpassword']
        address=request.POST['address']
        phone=request.POST['contact']
        image=request.FILES.get('profile')
        if pwd==cpwd:
            if User.objects.filter(username=user).exists():
                messages.info(request,'This username already exists!!')
                return redirect('regpage')
            else:
                usr=User.objects.create_user(first_name=fname,last_name=lname,username=user,email=email,password=pwd)
                usr.save()

                det=userdetails(address=address,phone=phone,prf_image=image,user=usr)
                det.save()
                subject='Your ecommerce username and password'
                message2= 'Username:'+user+'\n'+'Password:'+pwd
                send_mail(subject,message2,settings.EMAIL_HOST_USER,[email])
                return redirect('userindex')
        else:
            messages.info(request,'Password doesn"t match!!')
            return redirect('regpage')
    return render(request,'signup.html')

@login_required(login_url='loginpage')
def userindex(request):
    current=request.user.id 
    user=userdetails.objects.get(user_id=current) 
    cata=category.objects.all()
    return render(request,"userindex.html",{'category':cata,'user':user})

@login_required(login_url='loginpage')
def cart(request):
    current=request.user.id 
    pd=cart1.objects.filter(user_id=current)
    each_price=sum(p.product.pdprice for p in pd)
    num=cart1.objects.filter(user_id=current).count()
    user=userdetails.objects.get(user_id=current)
    cata=category.objects.all()
    return render(request,"cart.html",{'products':pd,'user':user,'category':cata,'number':num,'total':each_price})
@login_required(login_url='loginpage')
def addcart(request,a):
    current=request.user.id 
    user1=User.objects.get(id=current)
    prod=product.objects.get(id=a)
    cr=cart1(user=user1,product=prod)
    cr.save()
    return redirect('cart')
@login_required(login_url='loginpage') 
def delete_cart(request,a):
    c=cart1.objects.get(id=a)
    c.delete()
    return redirect('cart')
@login_required(login_url='loginpage')
def userprofile(request):  
    current=request.user.id  
    c=category.objects.all()
    user=userdetails.objects.get(user_id=current)
    return render(request,'userprofile.html',{'user':user,'nav':c})
@login_required(login_url='loginpage')
def logout_user(request):
    auth.logout(request)
    return redirect('index')

