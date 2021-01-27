from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, HttpResponse, get_object_or_404
from django.utils import timezone
from .models import Post, Comment, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from operator import attrgetter
from .forms import EditForm
from django.contrib.postgres.search import SearchVector


def suggest_users_to_follow(current_user):
    pass


def tweets_are_liked_by_user(recent_tweets, current_user):
    is_liked = []
    for i, tweet in enumerate(recent_tweets):
        # if tweet.likes_set.filter(profile=current_user):
        if current_user in tweet.likes.all():
            is_liked.append(True)
        else:
            is_liked.append(False)

    return is_liked


def tweets_are_retweeted_by_user(recent_tweets, current_user):
    is_retweeted = []
    for i, tweet in enumerate(recent_tweets):
        # if tweet.likes_set.filter(profile=current_user):
        if current_user in tweet.retweets.all():
            is_retweeted.append(True)
        else:
            is_retweeted.append(False)

    return is_retweeted


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    current_user = get_object_or_404(Profile, user=request.user)
    following_list = current_user.following.all()

    if request.method == "POST":
        # print(request.POST)
        # print(request.POST['search_field'])

        search_text = request.POST['search_field']
        searched_queryset = []
        if search_text[0] == '@':
            # search among users
            searched_queryset = Post.objects.annotate(search=SearchVector('profile__user__username')).filter(
                search=search_text)
        else:
            # search among content
            searched_queryset = Post.objects.annotate(search=SearchVector('content')).filter(
                search=search_text)

        result_tweets = []
        for p in searched_queryset:
            for f in following_list:
                temp = get_object_or_404(Profile, user=f)

                if p in temp.post_set.all() or p in temp.retweets.all():
                    result_tweets.append(p)

        result_tweets = list(set(result_tweets))
        result_tweets.sort(key=attrgetter('pub_date'), reverse=True)

        is_liked = tweets_are_liked_by_user(result_tweets, current_user)
        is_retweeted = tweets_are_retweeted_by_user(result_tweets, current_user)

        return render(request, 'tweets/index.html', {
            'recent_tweets': result_tweets,
            'is_liked': is_liked,
            'zipped': zip(is_retweeted, is_liked, result_tweets),
            'show_like': True,
            'show_comment': True
        })

        # exclude unrelated tweets

    recent_tweets = []
    for f in following_list:
        temp = get_object_or_404(Profile, user=f)
        recent_tweets.extend(temp.post_set.all())
        recent_tweets.extend(temp.retweets.all().exclude(profile=current_user))

    recent_tweets = list(set(recent_tweets))
    recent_tweets.sort(key=attrgetter('pub_date'), reverse=True)

    is_liked = tweets_are_liked_by_user(recent_tweets, current_user)
    is_retweeted = tweets_are_retweeted_by_user(recent_tweets, current_user)

    return render(request, 'tweets/index.html', {
        'recent_tweets': recent_tweets,
        'is_liked': is_liked,
        'zipped': zip(is_retweeted, is_liked, recent_tweets),
        'show_like': True,
        'show_comment': True
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
        return HttpResponseRedirect(reverse('tweets:comment', args=(post_id,)))

    comments = tweet.comment_set.all()
    return render(request, 'tweets/tweet_with_replies.html', {
        'post_id': post_id,
        'tweet': tweet,
        'show_like': False,
        'show_comment': False
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

    all_tweets = []
    all_tweets.extend(personal_tweets)
    all_tweets.extend(profile.retweets.all())
    all_tweets = list(set(all_tweets))
    all_tweets.sort(key=attrgetter('pub_date'), reverse=True)

    logged_in_user = get_object_or_404(Profile, user=request.user)
    is_followed = logged_in_user.following.filter(username=username).exists()

    followings = profile.following.all().exclude(username=username)
    followers = get_user_followers(user_profile)
    print('followers: ', followers)
    is_liked = tweets_are_liked_by_user(all_tweets, logged_in_user)
    is_retweeted = tweets_are_retweeted_by_user(all_tweets, logged_in_user)

    return render(request, 'tweets/profile.html', {
        'tweets': all_tweets,
        'user_profile': profile,
        'show_like': True,
        'show_comment': True,
        'is_liked': is_liked,
        'is_followed': is_followed,
        'followings': followings,
        'followers': followers,
        'form': EditForm(),
        'zipped': zip(is_retweeted, is_liked, all_tweets)
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

    data = {

        'is_liked': is_liked,
        'updated': updated,
    }
    return JsonResponse(data)


def notification_view(request):
    return render(request, 'tweets/notification.html', {})


def followers_view(request):
    return render(request, 'tweets/followers.html', {})


def following_view(request):
    return render(request, 'tweets/following.html', {})


def retweet_view(request):
    btn_value = request.GET.get('btn_value', None)
    to_be_retweeted_tweet = get_object_or_404(Post, id=int(btn_value))

    if request.user.is_authenticated and btn_value:
        current_user_profile = get_object_or_404(Profile, user=request.user)
        is_retweeted = False
        updated = False

        if current_user_profile in to_be_retweeted_tweet.retweets.all():
            is_retweeted = False
            to_be_retweeted_tweet.retweets.remove(current_user_profile)
        else:
            is_retweeted = True
            to_be_retweeted_tweet.retweets.add(current_user_profile)

        updated = True

    data = {
        'is_retweeted': is_retweeted,
        # 'retweeter_user': request.user,
        'updated': updated,
    }

    return JsonResponse(data)
