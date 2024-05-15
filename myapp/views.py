from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from myapp.models import Room, Message
from django.http import HttpResponse, JsonResponse

#from .models import Feature
# Create your views here.

def index(request):
	
	return render(request,'index.html')

def register(request):
	if request.method == 'POST':
		#fetch details from regster.html
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']

		if password == password2:
			if User.objects.filter(email=email).exists():
				messages.info(request,'Email Already Exist')
				return redirect('register')
			elif User.objects.filter(username=username).exists():
				messages.info(request,'Username Already Exist')
				return redirect('register')
			else:
				user = User.objects.create_user(username=username,email=email,password=password)
				user.save();
				return redirect('/')
		else:
			messages.info(request,'Password does not match')
			return redirect('register')
	else:
		return render(request,'register.html')

def room(request):
	return render(request,'room.html')

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username, password=password)
		
		if user is not None:
			auth.login(request, user)
			return redirect('home') 
		else:
			messages.info(request,'Credentials Invalid')
			return redirect('/')

	else:
		return render(request,'login.html')

def logout(request):
	auth.logout(request)
	return redirect('/')

def post(request,pk):
	return render(request,'post.html',{'pk':pk})

def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})