from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, HttpResponse, get_object_or_404
from django.utils import timezone
from .models import Post, Comment, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from operator import attrgetter
from .forms import EditForm


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    current_user = get_object_or_404(Profile, user=request.user)
    # print('current user: ', current_user)

    # btn_text = request.GET.get('btn_text', None)
    # print('button text: ', btn_text)
    # # handle like or dislike by AJAX
    # if btn_text:
    #     btn_value = request.GET.get('btn_value', None)
    #     liked_tweet = get_object_or_404(Post, id=int(btn_value))
    #
    #     if btn_text == 'Dislike':
    #         # then add to number of likes
    #         if not liked_tweet.likes_set.filter(profile=current_user).exists():
    #             liked_tweet.likes_set.create(profile=current_user)
    #             liked_tweet.save()
    #
    #     else:
    #         Likes.objects.get(profile=current_user, post=liked_tweet).delete()
    #
    #     # context = dict()
    #     # context['is_liked'] = Tracklike.objects.filter(post=liked_tweet, user=request.user).exists()
    #
    #     data = {
    #         'has_changed': True,
    #         'likes_count': liked_tweet.likes_set.count(),
    #     }
    #     return JsonResponse(data)

    # else:
    recent_tweets = []
    following_list = current_user.following.all()
    for f in following_list:
        temp = get_object_or_404(Profile, user=f)
        recent_tweets.extend(temp.post_set.all())

    recent_tweets.sort(key=attrgetter('pub_date'), reverse=True)

    # recent_tweets = Post.objects.all().order_by('-pub_date')[:6]
    is_liked = []
    for i, tweet in enumerate(recent_tweets):
        # if tweet.likes_set.filter(profile=current_user):
        if current_user in tweet.likes.all():
            is_liked.append(True)
        else:
            is_liked.append(False)

    return render(request, 'tweets/index.html', {
        'recent_tweets': recent_tweets,
        'is_liked': is_liked,
        'zipped': zip(is_liked, recent_tweets),
        'show_like': True
    })


def post(request):
    if request.method == 'POST':
        user_profile = get_object_or_404(Profile, user=request.user)
        Post.objects.create(profile=user_profile, content=request.POST['content'], pub_date=timezone.now())
        return HttpResponseRedirect(reverse('tweets:index'))

    elif request.method == 'GET':
        return render(request, 'tweets/post.html', {})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            print(request.user.is_authenticated)
            # context['form'] = LoginForm()
            login(request, user)
            # LoginForm()
            return HttpResponseRedirect(reverse('tweets:index'))
        else:
            if User.objects.filter(username=username).count() > 0:
                return render(request, 'tweets/login.html', {'wrong_pass': 'Wrong password for this username!'})
            else:
                return render(request, 'tweets/login.html', {'error_message': 'This user has not registered yet!'})
    elif request.method == 'GET':
        return render(request, 'tweets/login.html', {})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        users = User.objects.filter(username=username)
        if users.count() > 0:
            error_message = True
            return render(request, 'tweets/register.html', {'error_message': error_message, 'username': username})
        else:
            password2 = request.POST.get('password2')
            if password == password2:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                profile = Profile.objects.create(user=new_user)
                profile.following.add(new_user)
                print(new_user)
                return redirect('/login')
            else:
                pass_error = True
                return render(request, 'tweets/register.html', {'pass_error': pass_error})

    else:
        return render(request, 'tweets/register.html', {})


def logout_view(request):
    username = request.user.username
    logout(request)
    return render(request, 'tweets/logout.html', {'username': username})


def personal_page(request, username):
    posts = Post.objects.filter(profile__user__username=username)
    print(posts)
    return render(request, 'tweets/user.html', {'posts': posts, 'username': username})


def hashtag_view(request):
    pass


def comment_view(request, post_id):
    tweet = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        user_profile = get_object_or_404(Profile, user=request.user)
        Comment.objects.create(post=tweet, content=content, profile=user_profile)
        return redirect('/')

    comments = tweet.comment_set.all()
    return render(request, 'tweets/tweet_with_replies.html', {
        'post_id': post_id,
        'tweet': tweet
    })


def get_user_followers(current_user):
    followers = []
    for profile in Profile.objects.all():
        print('user {} has followings: {}'.format(profile, profile.following.all()))
        if profile.user != current_user and current_user in profile.following.all():
            followers.append(profile)

    return followers


def profile_view(request, username):
    personal_tweets = Post.objects.filter(profile__user__username=username)
    user_profile = User.objects.get(username=username)
    profile = get_object_or_404(Profile, user=user_profile)
    logged_in_user = get_object_or_404(Profile, user=request.user)
    is_followed = logged_in_user.following.filter(username=username).exists()

    followings = profile.following.all().exclude(username=username)
    followers = get_user_followers(user_profile)
    print('followers: ', followers)

    return render(request, 'tweets/profile.html', {
        'tweets': personal_tweets,
        'user_profile': profile,
        'show_like': False,
        'is_followed': is_followed,
        'followings': followings,
        'followers': followers,
        'form': EditForm()
    })


def toggle_follow_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    current_user = get_object_or_404(Profile, user=request.user)
    followed = False
    updated = False
    if request.user.is_authenticated:
        if user_to_follow in current_user.following.all():
            followed = False
            current_user.following.remove(user_to_follow)
        else:
            followed = True
            current_user.following.add(user_to_follow)
        updated = True

    data = {
        'followed': followed,
        'updated': updated
    }
    return JsonResponse(data)


def edit_profile_view(request, username):
    print(request.POST, request.FILES)
    # chosen_image = request.POST.get('image_url', None)
    # print('image: ', chosen_image)

    # update_profile = get_object_or_404(Profile, user__username=username)
    # update_profile.profile_img = chosen_image
    # update_profile.save()

    if request.method == "POST":
        form = EditForm(request.POST, request.FILES)
        updated = False
        if form.is_valid():
            print(form.cleaned_data)
            user = get_object_or_404(User, username=username)
            update_profile = get_object_or_404(Profile, user__username=username)
            if form.cleaned_data['username']:
                user.username = form.cleaned_data['username']
                user.save()

            if form.cleaned_data['profile_img']:
                update_profile.profile_img = form.cleaned_data['profile_img']
                update_profile.save()

            updated = True

        # if image_saved:
        #     return HttpResponseRedirect(reverse('tweets:profile', args=(request.user.username,)))

        # print(request.POST)
        return JsonResponse({
            'updated': updated,
            'form_error': form.errors
        })


def like_unlike_view(request):
    btn_value = request.GET.get('btn_value', None)
    to_be_liked_tweet = get_object_or_404(Post, id=int(btn_value))

    if request.user.is_authenticated and btn_value:
        current_user_profile = get_object_or_404(Profile, user=request.user)
        is_liked = False
        updated = False

        if current_user_profile in to_be_liked_tweet.likes.all():
            is_liked = False
            to_be_liked_tweet.likes.remove(current_user_profile)
        else:
            is_liked = True
            to_be_liked_tweet.likes.add(current_user_profile)

        updated = True
        # liked_user = to_be_liked_tweet.likes_set.filter(profile=current_user_profile)
        # print('liked user: ', liked_user)
        # if liked_user.exists():
        #     is_liked = False
        #     to_be_liked_tweet.likes_set.remove(liked_user[0])
        #
        # else:
        #     is_liked = True
        # l = Likes.objects.create(profile=current_user_profile)
        # to_be_liked_tweet.likes_set.add(l)
        # to_be_liked_tweet.likes_set.add(liked_user[0])

    data = {

        'is_liked': is_liked,
        'updated': updated,
    }
    return JsonResponse(data)
