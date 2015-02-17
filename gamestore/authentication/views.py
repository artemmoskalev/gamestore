from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.contrib import auth
from django.http import Http404
from django.template import RequestContext
from django.core.mail import EmailMessage
from authentication.models import RegistrationKey
from django.core.exceptions import PermissionDenied

""" method which registers a new user """
def request_register_page(request):	
	if request.user.is_authenticated():
		raise PermissionDenied
	
	errors = []
	
	if request.method == "POST" :
		login = request.POST["login"]
		password = request.POST["password"]
		password_re = request.POST["password_re"]
		email = request.POST["email"]		
		user_group = request.POST["user_group"]
		
		if login == "":
			errors.append("Login cannot be empty")
		elif User.objects.filter(username=login).count() > 0:
			errors.append("Your login is already taken") 	
		if password == "" or password_re == "":
			errors.append("Passwords cannot be empty")
		elif password != password_re:
			errors.append("Passwords do not match")
		if email == "":
			errors.append("Email cannot be empty") 			
			
		if len(errors) == 0:
			user = User.objects.create_user(login, email, password)
			if user_group == "player":
				playersGroup, isCreated = Group.objects.get_or_create(name="players")
				if isCreated:
					content_type = ContentType.objects.get(app_label='gamedata', model='game')
					playPermission = Permission.objects.get_or_create(name="Can Play", codename="can_play", content_type=content_type)
					playersGroup.permissions.add(playPermission[0])
															
				playersGroup.user_set.add(user)	
				user.is_active = False
				user.save()
			else:
				developersGroup, isCreated = Group.objects.get_or_create(name="developers")
				if isCreated:
					content_type = ContentType.objects.get(app_label='gamedata', model='game')
					playPermission = Permission.objects.get_or_create(name="Can Play", codename="can_play", content_type=content_type)
					publishPermission = Permission.objects.get_or_create(name="Can Publish", codename="can_publish", content_type=content_type)
					developersGroup.permissions.add(playPermission[0])
					developersGroup.permissions.add(publishPermission[0])
					
				developersGroup.user_set.add(user)
				user.is_active = False
				user.save()			
			
			registration_key = RegistrationKey(registered_user=user)
			registration_key.createUniqueKey()
			registration_key.save()
			auth_address = request.build_absolute_uri() + "validate/?auth_key=" + registration_key.auth_key
			
			html_text = ("<p>Use the following link to validate your new account: </p><p><a href='" + auth_address + "'>Click Here</a></p>")
			email = EmailMessage('Email Validation from WSD Gaming',  html_text, to=[user.email])
			email.content_subtype = "html"
			email.send(fail_silently=False)
			return HttpResponseRedirect("/login")	
	
	context = {}
	context.update(csrf(request))	
	context["errors"] = errors
	return render_to_response( 'register.html' , context_instance=RequestContext(request, context) )


""" method which logs in the user """
def request_login_page(request):
	if request.user.is_authenticated():
		raise PermissionDenied
	
	errors = []
	
	if request.method == "POST" :
		login = request.POST["login"]
		password = request.POST["password"]
		
		if login == "":
			errors.append("Provide your login")		
		elif password == "":
			errors.append("Provide your password") 
		else:
			user = auth.authenticate(username=login, password=password)
			if user is not None:
				if user.is_active:
					auth.login(request, user)
					return HttpResponseRedirect("/games")
				else:
					errors.append("Validate your account!")
			else:
				errors.append("Wrong credentials")
		
	context = {}
	context.update(csrf(request))	
	context["errors"] = errors
	return render_to_response("login.html", context_instance=RequestContext(request, context))
	
	
""" method which logs out the user """
def request_logout(request):
	auth.logout(request)	
	return HttpResponseRedirect("/login")

""" method for email account validation """
def request_register_validate(request):
	if request.user.is_authenticated():
		raise PermissionDenied
	
	auth_key = request.GET['auth_key']
	keys = RegistrationKey.objects.filter(auth_key=auth_key)
	if keys.count() > 0:	
		user = keys[0].registered_user
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		auth.login(request, user)
		user.is_active = True
		user.save()
		keys.delete()
		return HttpResponseRedirect("/games")	
	else:
		raise Http404
		

