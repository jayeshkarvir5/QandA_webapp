from django.contrib.auth import get_user_model

User = get_user_model()

test = User.objects.last()

# my followers
test.profile.followers.all()

# who i follow
test.is_following.all()  # test.profile.following.all()
