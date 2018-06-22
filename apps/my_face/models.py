from django.db import models

class User(models.Model):
	full_name = models.CharField(max_length=64)
	email = models.CharField(max_length=64, unique=True)
	password = models.CharField(max_length=64)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Follow(models.Model):
	following = models.ForeignKey(User, related_name='follow_by', on_delete=models.CASCADE)
	follower = models.ForeignKey(User, related_name='follower_of', on_delete=models.CASCADE)
	# follower
	# USER ------------------------ FOLLOW ------------------------ USER
	# dody1                        following                        dody2 >>MEAN>> dody1 following dody2
	# dody2                        follow_by                        dody1 >>MEAN>> dody2 follows_by dody1
	
	# USER ------------------------ FOLLOW ------------------------ USER
	# dody1                        follower       :                 dody2 >>MEAN>> dody1    follower     dody2
	# dody2                       follower_of                       dody1 >>MEAN>> dody2   follower_of   dody1

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Photo(models.Model):
	title = models.CharField(max_length=64)
	path = models.CharField(max_length=254, unique=True)

	user = models.ForeignKey(User, related_name='photos', on_delete=models.CASCADE)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Post(models.Model):
	content = models.TextField()

	to_user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE) # to who post is posted
	from_user = models.ForeignKey(User, related_name='has_posts', on_delete=models.CASCADE) # who post it

	# to_user
	# USER <=========== POST ==============> USER
	#        posts              to_user

	# from_user
	# USER <=========== POST ==============> USER
	#        has_posts         from_user

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
	content = models.TextField()

	user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
