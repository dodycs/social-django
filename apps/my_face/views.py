import os, re, bcrypt, time
from django.shortcuts import render, redirect
from . import models as m
from django.contrib import messages
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from . import models as m
from . import utilities as utils

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

# GENERAL
def index(request):
	# login area
	if 'user_id' in request.session:
		posts = m.Post.objects.filter(from_user_id=request.session['user_id'])
		followings = utils.user_followings(request.session['user_id'])
		context = {
			'followings': followings,
			'posts': posts,
		}
		return render(request, 'my_face/index.html', context)
	else:
		return redirect('my_face:login')

# POST
def create_post(request):
	if 'user_id' in request.session:
		if request.method == 'POST':
			content = request.POST['content']
			post_to_user_id = request.POST['post_to_user_id']
			# validate post
			# ...
			post = m.Post()
			post.content = content
			post.from_user_id = request.session['user_id']
			post.to_user_id = post_to_user_id
			post.save()
	return redirect(request.META['HTTP_REFERER'])

def posts(request):
	return render(request, 'my_face/post/posts.html')

def delete_post(request, post_id):
	# check if current user create the post
	# ...
	post = m.Post.objects.get(id=post_id)
	post.delete()
	return redirect('my_face:index')

# COMMENT
def create_comment(request):
	if 'user_id' in request.session:
		if request.method == 'POST':
			content = request.POST['comment']
			post_id = request.POST['post_id']
			# validate post
			# ...
			comment = m.Comment()
			comment.content = content
			comment.post_id = post_id
			comment.user_id = request.session['user_id']
			comment.save()
	return redirect('my_face:index')

def delete_comment(request, comment_id):
	# check if current user create the comment
	# ...
	comment = m.Comment.objects.get(id=comment_id)
	comment.delete()
	return redirect('my_face:index')

# USER
def register(request):
	# if user logedin, rediret to index
	if 'user_id' in request.session:
		return redirect('my_face:index')

	if request.method == 'POST':
		error_messages = []
		full_name = request.POST['full_name']
		email = request.POST['email']
		password = request.POST['password']
		confirm = request.POST['confirm']
		# validation
		# cannot blank
		if len(full_name) < 1:
				error_messages.append('Full name cannot be blank')
		if len(email) < 1:
				error_messages.append('Email cannot be blank')
		if len(password) < 1:
				error_messages.append('Password cannot be blank')
		if len(confirm) < 1:
				error_messages.append('Confirm password cannot be blank')
		# password more than 6 character
		if len(password) < 6:
				error_messages.append('Password must at least 6 character')
		# password missmatch
		if password != confirm:
				error_messages.append('Password not match')
		# email format
		if not EMAIL_REGEX.match(email):
				error_messages.append('Wrong email format')

		# if no error message:
		if len(error_messages) == 0:
			user = m.User()
			user.full_name = full_name
			user.email = email
			hash_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('utf-8')
			user.password = hash_password
			user.save()
			messages.success(request, 'Success to register')
			utils.setup_web_session(request, user)
		else:
			for msg in error_messages:
				messages.error(request, msg)
		return redirect('my_face:register')

	return render(request, 'my_face/user/register.html')

def login(request):
	# check if user login
	if 'user_id' in request.session:
		return redirect('my_face:index')

	# check if method is post
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		# check input is valid
		# check if blank
		error_messages = []
		if len(email)==0:
			error_messages.append('Email cannot be blank')
		if len(password)<6:
			error_messages.append('Password must at least 6 character')
		# email format
		if not EMAIL_REGEX.match(email):
			error_messages.append('Wrong email format')
		
		# if thre is error message
		if len(error_messages) > 0:
			for msg in error_messages:
				messages.error(request, msg)
		else:
			# user exist
			try:
				user = m.User.objects.get(email=email)
				# if the password match
				if bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
					utils.setup_web_session(request, user)
					messages.success(request, 'Login Successfully')
					return redirect('my_face:index')
			except:
				messages.error(request, 'Wrong email or password')
		return redirect('my_face:login')
	return render(request, 'my_face/user/login.html')

def logout(request):
	request.session.clear()
	messages.success(request, 'You are loged out')
	return redirect('my_face:index')

def post_search_user(request):
	# validate post
	keyword = request.POST['keyword']
	# ...
	return redirect('my_face:search_user', keyword=keyword)

def search_user(request, keyword):
	users = m.User.objects.filter(Q(full_name__contains=keyword) | Q(email__contains=keyword)).exclude(id=request.session['user_id'])
	followings = utils.user_followings(request.session['user_id'])
	context = {
		'users': users,
		'followings': followings
	}
	return render(request, 'my_face/user/users.html', context)

def following(request, user_id):
	users = m.User.objects.filter(follow_by__follower_id=user_id)
	followings = utils.user_followings(request.session['user_id'])
	context = {
		'users': users,
		'followings': followings
	}
	return render(request, 'my_face/user/users.html', context)

def follower(request, user_id):
	users = m.User.objects.filter(follower_of__following_id=user_id)
	followings = utils.user_followings(request.session['user_id'])
	context = {
		'users': users,
		'followings': followings
	}
	return render(request, 'my_face/user/users.html', context)

def follow(request, follower_id, following_id):
	try:
		follow = m.Follow.objects.get(follower_id=follower_id, following_id=following_id)
		messages.error(request, 'You already follow {}'.format(follow.following.full_name))
	except:
		follow = m.Follow()
		follow.follower_id = follower_id
		follow.following_id = following_id
		follow.save()
		messages.success(request, 'Now you Follow {}'.format(follow.following.full_name))
	return redirect(request.META['HTTP_REFERER'])

def unfollow(request, follower_id, following_id):
	try:
		follow = m.Follow.objects.get(follower_id=follower_id, following_id=following_id)
		messages.success(request, 'Now you Unfollow {}'.format(follow.following.full_name))
		follow.delete()
	except:
		messages.error(request, 'You are not following {}'.format(follow.following.full_name))
	
	# validate if user manualy go to this url manualy
	# ...
	return redirect(request.META['HTTP_REFERER'])


def wall(request, user_id):
	posts = m.Post.objects.filter(to_user_id=user_id)
	followings = utils.user_followings(request.session['user_id'])
	followers = utils.user_followers(request.session['user_id'])
	related_user = followings+followers
	user = m.User.objects.get(id=user_id)
	context = {
		'user': user,
		'related_user': related_user,
		'followings': followings,
		'followers': followers,
		'post_to_user_id': user_id,
		'posts': posts,
	}
	return render(request, 'my_face/user/wall.html', context)

def generate_user(request):
	for i in range(5, 20):
		user = m.User()
		user.full_name = 'Dody {}'.format(i)
		user.email = 'dody{}@dody.dody'.format(i)
		password_string = '12341234'
		user.password = bcrypt.hashpw(password_string.encode('UTF-8'), bcrypt.gensalt()).decode('utf-8')
		messages.success(request, '{} with email {} Created'.format(user.full_name, user.email))
		user.save()
	return redirect('my_face:index')


# PHOTO
def photo(request):
	photos = m.Photo.objects.all()
	context = {
		'photos': photos
	}
	if request.method == 'POST' and request.FILES['photo']:
		title = request.POST['title']
		photo_file = request.FILES['photo']
		# validate input
		# ...
		photo = m.Photo()
		photo.title = title
		# ts = time.time()
		# filename = title.replace(' ', '_')+ts

		# upload file
		fs = FileSystemStorage()
		photo_name = fs.save(photo_file.name, photo_file)
		photo.path = fs.url(photo_name)
		photo.user_id = request.session['user_id']
		photo.save()
		return redirect('my_face:photo')
	return render(request, 'my_face/photo/photo.html', context)

def delete_photo(request, photo_id):
	try:
		photo = m.Photo.objects.get(id=photo_id)
		os.remove(settings.MEDIA_ROOT+photo.path)
		# messages.error(request, 'Photo deleted')
		photo.delete()
	except:
		raise
		messages.success(request, 'Failed delete the photo')

	return redirect(request.META['HTTP_REFERER'])
