from django.shortcuts import render, redirect

from models import User, Item
import bcrypt
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.

def index(request):

	return render(request,"belt/index.html")

def logval(request):
	
	errors = User.objects.login_validator(request.POST)
	print "inside logval"
	if len(errors):
		for key,value in errors.iteritems():
			messages.error(request,value,extra_tags=key)
		return redirect('/')
	else:
		email = request.POST['email']
		if "email" not in request.session:
			request.session['email'] = email
	return redirect("/items")

def regval(request):
	
	errors = User.objects.register_validator(request.POST)

	if len(errors):
		for key,value in errors.iteritems():
			messages.error(request,value,extra_tags=key)
		return redirect('/')
	else:
		hash_pwd = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
		User.objects.create(
							name=request.POST['name'],
							alias=request.POST['alias'],
							email=request.POST['email'],
							password=hash_pwd)

		if "email" not in request.session:
			request.session['email'] = request.POST['email']

		User.objects.get(email=request.POST['email'])

		if "login_user_id" not in request.session:
			request.session['login_user_id'] = User.objects.get(email=request.POST['email']).id
		

		return redirect("/items")

def show_items(request):

	# other_users = Users.objects.all().exclude(email=request.session["email"])
	user = User.objects.get(email=request.session['email'])


	context = {
				"welcome_user" : User.objects.get(email=request.session['email']),
				"liked_items" : User.objects.get(email=request.session['email']).liked_items.all(),
				"other_items" : Item.objects.all().exclude(uploader=user),
			}
	return render(request,"belt/items.html", context)

def show(request, id):

	context	= {
				"single_item" : Item.objects.get(id=id),
				"liked_users" : Item.objects.get(id=id).liked_users.all()

	}

	return render(request,"belt/show_item.html", context)

def create(request):


	return render(request,"belt/create.html")

def add_item(request):
	
	errors = Item.objects.item_validator(request.POST)

	if errors:
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/items')
	else:
		if request.method == "POST":

			user = User.objects.get(email=request.session['email'])

			wish_add = Item.objects.create(item_name=request.POST['product'],\
				uploader=user)

			user.liked_items.add(wish_add)

			return redirect('/items')

def add(request,id):

	user = User.objects.get(email=request.session['email'])
	item = Item.objects.get(id=id)
	
	item.liked_users.add(user)

	return redirect('/items')

def remove(request,id):
	
	user = User.objects.get(email=request.session['email'])
	item = Item.objects.get(id=id)

	item.liked_users.remove(user)

	return redirect('/items')

def delete(request,id):

	user = User.objects.get(email=request.session['email'])
	item = Item.objects.get(id=id)

	item.liked_users.delete(user)

	return redirect('/items')

def logoutpage(request):
	
	logout(request)
	return redirect('/')









