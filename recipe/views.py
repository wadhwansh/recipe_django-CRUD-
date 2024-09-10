from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="/login/")
def recipes(request):
    if request.method == "POST":
        data=request.POST
        Recipe_image=request.FILES.get('Recipe_image')
        Recipe_name=data.get('Recipe_name')
        Recipe_description=data.get('Recipe_description')
        recipe.objects.create(
            Recipe_image=Recipe_image,
            Recipe_description=Recipe_description,
            Recipe_name=Recipe_name,
        )
        return redirect('/recipe')
    queryset = recipe.objects.all()
    if request.GET.get('Search'):#name which you declare in html page
        queryset=queryset.filter(Recipe_name__icontains = request.GET.get('Search')) 
    
   
    context = {'recipes':queryset}
    return render(request,"recipe.html",context)

@login_required(login_url="/login/")
def delete_recipe(request,id):
    queryset=recipe.objects.get(id = id)
    queryset.delete()
    return redirect('/recipe/')

@login_required(login_url="/login/")
def update_recipe(request,id):
    queryset=recipe.objects.get(id = id)
    if request.method == "POST":
        data=request.POST
        Recipe_image=request.FILES.get('Recipe_image')
        Recipe_name=data.get('Recipe_name')
        Recipe_description=data.get('Recipe_description')
        queryset.Recipe_name=Recipe_name
        queryset.Recipe_description=Recipe_description
        if Recipe_image:
            queryset.Recipe_image=Recipe_image
        queryset.save()
        return redirect('/recipe/')
        
    context = {'recipe':queryset}
    return render(request,"update_recipe.html",context)
    
def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username'),
        password=request.POST.get('password')
        if not User.objects.filter(username = username).exists():
            messages.error(request,"Username not found")
            return redirect('/login/')
        
        user=authenticate(username=username,password=password)
        
        if user is None:
            messages.error(request,"Invalid password")
            return redirect("/login/")
        
        else:
            login(request,user)
            return redirect("/recipe/")
    return render(request,'login.html')

def Register_page(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name'),
        last_name=request.POST.get('last_name'),
        username=request.POST.get('username'),
        password=request.POST.get('password')
        
        user=User.objects.filter(username = username)
        if user.exists():
            messages.error(request, "Username already exists")
            return redirect('/register/')
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
         )
        user.set_password(password)
        user.save()
        
        messages.info(request,"Registered successfully ")
        return redirect('/register/')
    return render(request,'register.html')

def log_out(request):
    logout(request)
    return redirect("/login/")
    