from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Customer
def sign_out(request):
    logout(request)
    return redirect('home')
# Create your views here.
def show_account(request):
    context={}
    if request.POST and 'register' in request.POST:
        context['register']=True
        try:  
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            address=request.POST.get('address')
            phone=request.POST.get('phone')
            # creates user accounts
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            # creates customer account
            customer=Customer.objects.create(
                name=username,
                user=user,
                phone=phone,
                address=address
            )
            print("Customer",customer)
            success_message="User registered successfully"
            messages.success(request,success_message)
            
        except Exception as e:
            print("error",e)
            error_message="Duplicate username or invalid inputs"
            messages.error(request,error_message)
    if request.POST and 'login' in request.POST:
        context['register']=False
        print(request.POST)
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'invalid user credentials')
    return render(request,'account.html',context)

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        user = request.user
        user.username = username
        user.email = email
        #user.customer_profile.phone = phone
        #user.customer_profile.address = address
        user.save()
        customer=Customer.objects.get(
            user=user
        )
        customer.phone=phone
        customer.address=address
        customer.save()
        print(user)
        print(user.customer_profile.phone)
        messages.success(request, "Profile updated successfully!")
        return redirect('edit_profile')  # or wherever you want to redirect
    
    elif request.method == 'GET':
        return render(request, 'edit_profile.html', {'user': user})
        
