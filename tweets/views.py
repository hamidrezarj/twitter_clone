from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, HttpResponse, get_object_or_404
from django.utils import timezone
from .models import Post, Comment, Likes, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    user_profile = get_object_or_404(Profile, user=request.user)

    btn_text = request.GET.get('btn_text', None)
    print('button text: ', btn_text)
    # handle like or dislike by AJAX
    if btn_text:
        btn_value = request.GET.get('btn_value', None)
        liked_tweet = get_object_or_404(Post, id=int(btn_value))

        if btn_text == 'Dislike':
            # then add to number of likes
            if not liked_tweet.likes_set.filter(profile=user_profile).exists():
                liked_tweet.likes_set.create(profile=user_profile)
                liked_tweet.save()

        else:
            Likes.objects.get(profile=user_profile, post=liked_tweet).delete()

        # context = dict()
        # context['is_liked'] = Tracklike.objects.filter(post=liked_tweet, user=request.user).exists()

        data = {
            'has_changed': True,
            'likes_count': liked_tweet.likes_set.count(),
        }
        return JsonResponse(data)

    else:
        recent_tweets = Post.objects.all().order_by('-pub_date')[:6]
        is_liked = []
        for i, tweet in enumerate(recent_tweets):
            if tweet.likes_set.filter(profile=user_profile):
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
                Profile.objects.create(user=new_user)
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
    if request.method == 'POST':
        content = request.POST.get('content')
        p = get_object_or_404(Post, id=post_id)
        user_profile = get_object_or_404(Profile, user=request.user)
        Comment.objects.create(post=p, content=content, profile=user_profile)
        return redirect('/')
    return render(request, 'tweets/comment.html', {'post_id': post_id})


def profile_view(request, username):
    personal_tweets = Post.objects.filter(profile__user__username=username)
    user = User.objects.get(username=username)
    profile = get_object_or_404(Profile, user=user)

    return render(request, 'tweets/profile.html', {
        'tweets': personal_tweets,
        'user_profile': profile,
        'show_like': False
    })
