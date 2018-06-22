from . import models as m

def setup_web_session(request, user):
	request.session['user_id'] = user.id
	request.session['email'] = user.email
	request.session['full_name'] = user.full_name

def user_followings(user_id):
	followings_ids = []
	followings = m.Follow.objects.filter(follower_id=user_id)
	
	for user_following in followings:
		followings_ids.append(user_following.following_id)
	return followings_ids


def user_followers(user_id):
	followers_ids = []
	followers = m.Follow.objects.filter(following_id=user_id)

	for user_following in followers:
		followers_ids.append(user_following.following_id)
	return followers_ids

# def related_user(user_id):
# 	followers_ids = []
# 	related_users = m.Follow.objects.filter(Q(following_id=user_id) | Q(follower_id=user_id))

# 	for u_id in related_users:
# 		followers_ids.append(u_id.)

# def combine(list1, list2, index, newlist):
# 	# first list must be biger than second one
# 	if len(list2) > len(list1):
# 		return combine(list2, list1, index, newlist)
# 	# termination condition
# 	if len(list1) == index:
# 		return newlist
# 	# update statement
	