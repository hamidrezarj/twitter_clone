#twitter clone

### Some features are:
* users can Post their tweets.
* users can Comment on tweets.
* users can Like each other's tweets.
* users can Retweet each other's tweets.

YOU NEED Postgresql and have to change the password of it on setting.py yourself!
CREATE A VIRTUAL ENVIRONMENT THEN CLONE THIS INTO FOLDER OF env!
Commands to  inside 'blog-post' folder:
```
python manage.py makemigrations
python manage.py makemigrations tweets
python manage.py migrate
python manage.py migrate tweets
python manage.py runserver
```

## Open Endpoints

Open endpoints require no Authentication.

* [Login](login.md) : `POST /api/login/`
* [Register](Register.md) : `POST /api/register/`

## Endpoints that require Authentication

Closed endpoints require a valid Token to be included in the header of the
request.

### Navigating and Activities of User

* [Home](Home.md) : `GET /api/`
* [Post](Post.md) : `POST /api/post/`
* [Like](Like.md) : `POST /api/ajax/like/`
* [Retweet](Retweet.md) : `POST /api/ajax/retweet/`
* [Delete](Delete.md) : `POST /api/delete_tweet/<int:post_id>/`
* [Reply](Reply.md) : `POST /api/comment/<int:post_id>/`
* [Tweet + Comments](Comment.md) : `GET /api/comment/<int:post_id>/`
* [Likes User List](Show_likes.md) : `GET /api/show_likes/<int:post_id>/`
* [Profile](Profile.md) : `GET /api/user/<username>/`

### Current User related

Each endpoint manipulates or displays information related to the User whose
Token is provided with the request:

* [Logout](Logout.md) : `POST /api/logout/`
* [Edit Profile](Edit.md) : `POST /api/user/<username>/edit_profile/`
* [Notification](Notification.md) : `GET /api/user/notification/`

### Account related

Endpoints for viewing and manipulating other Users Relation with the User
Token is provided with request:

* [Follow/Unfollow](Follow.md) : `POST /api/user/<username>/follow/`
