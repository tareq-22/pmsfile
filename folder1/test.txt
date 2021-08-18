# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, Permission
from .models import User
from django.forms.utils import ErrorList
from django.template import loader
from django.http import HttpResponse
from django import template
from .forms import LoginForm, SignUpForm, GropuCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
"""
Method to handle user login
"""
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            # django default method to authenticate user
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    


    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            is_manager = form.cleaned_data.get("is_manager")
            if is_manager == True:
                group = Group.objects.get(name='Project Manager')
                user.groups.add(group)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })

@login_required
@permission_required('auth.view_user',raise_exception=True)
def show_users(request):
    users = User.objects.all()
    context = {
            'users': users,
            'segment' : 'auth',
            'subsegment' : 'user'
        }
    html_template = loader.get_template( 'users/allUsers.html' )
    return HttpResponse(html_template.render(context, request))  

@permission_required('auth.delete_user',raise_exception=True)
def del_user(request, id):    
    try:
        u = User.objects.get(id = id)
        u.delete()
        messages.success(request, "The user is deleted")            

    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")    
        return redirect('all_users')

    except Exception as e: 
        return redirect('all_users')

    return redirect('all_users')

@permission_required('auth.view_group',raise_exception=True)
def all_groups(request):
    groups = Group.objects.all()
    context = {
            'groups': groups,
            'segment' : 'auth',
            'subsegment' : 'groups'
        }
    return render(request,'users/all_groups.html',context)

@permission_required('auth.delete_group',raise_exception=True)
def del_group(request,id):
    group = Group.objects.get(id=id)
    group.delete()
    messages.success(request,"Successfully Deleted")

    return redirect('all_groups')

@permission_required('auth.edit_group',raise_exception=True)
def edit_group(request,id):
    group = Group.objects.get(id=id)
    if request.method == "POST":
        form = GropuCreationForm(request.POST,instance=group)
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully Updated")
            return redirect('all_groups')
        else:
            messages.error(request,form.errors)
            return redirect('edit_group',id)
    else:
        form = GropuCreationForm(instance=group)
        return render(request,'users/edit_group.html',{
            'form':form,
            'segment' : 'auth',
            'subsegment' : 'groups'
        })

@permission_required('auth.add_group',raise_exception=True)
def add_group(request):
    if request.method == "POST":
        form = GropuCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "successfully Created")
            return redirect('all_groups')
        else:
            messages.error(request,form.errors)
            return redirect('add_group')

    else:
        form = GropuCreationForm
        return render(request,'users/add_group.html',{
            'form':form,
            'segment' : 'auth',
            'subsegment' : 'groups'
        })

def no_access(request):
    return render(request, 'accounts/no_access.html')