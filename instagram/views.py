from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from instagram.models import Post
from accounts.models import User
from instagram.forms import CommentForm, PostForm


@login_required
def index(request):
    post_list = Post.objects.filter(author=request.user)

    suggested_user_list = get_user_model().objects.all() \
        .exclude(pk=request.user.pk) \
        .exclude(pk__in=request.user.following_set.all())

    form = CommentForm()
    # 작성해주지 않으면 유효한 폼이 필요하다고 에러남
    # index html에서 comment관련 card를 include 해주므로 여기서도 CommentForm()이 필요하다.
    return render(request, 'instagram/index.html', {
        'post_list': post_list,
        'suggested_user_list': suggested_user_list,
        'form': form,

    })


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # commit?
            post.author = request.user
            post.save()
            post.tag_set.add(
                *post.extract_tag_list())
            # post.caption_replace() # 글씨 삭제하고 tag만 남기는 함수
            post.caption_replace()
            post.save()
            return redirect('/')
    else:
        form = PostForm()

    return render(request, 'instagram/post_form.html', {
        'form': form
        # 컨텍스트는 설정된 것이 아니라 딕트(사전형식)여야 합니다.
    })


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    return render(request, 'instagram/post_detail.html', {
        'post': post,
        'form': form,
    })


@login_required
def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count()  # 게시글 개수 반환
    follower_count = page_user.follower_set.count()
    following_count = page_user.following_set.count()
    if request.user.is_authenticated:
        is_follow = page_user.follower_set.filter(pk=request.user.pk).exists()
        # 유저 페이지에 들어갔을 때 요청 유저의 following_set에 접근 유저의 pk기 있다면 팔로우 상태임을 알 수 있다.
        # 한마디로 로그인, 인증 상태가 아니라면 겸상조차 불가능함. 이걸로 어떻게 써먹는지 다시 생각해보기
    else:
        is_follow = False

    return render(request, 'instagram/user_page.html', {
        'page_user': page_user,
        'post_list': post_list,
        'post_list_count': post_list_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_follow': is_follow,

    })


@login_required()
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f'{post.pk}번 게시물에 좋아요 완료되었습니다.')
    redirect_url = request.META.get('HTTP_REFERER', 'root')
    return redirect(redirect_url)


@login_required()
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f'{post.pk}번 게시물 좋아요 취소되었습니다.')
    redirect_url = request.META.get('HTTP_REFERER', 'root')
    return redirect(redirect_url)


@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # commit?
            comment.author = request.user
            comment.post = post  # comment의 post위치 정해주기, post는 위에서 정의한 post임
            comment.save()
            # 아래 부분은 ajax를 이용할 때 써야됨. ajax 요청을 받으면 실행됨
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return render(request, 'instagram/_comment.html', {
                    'comment': comment,
                })
            return redirect(comment.post)

    else:
        form = CommentForm()
    return render(request, 'instagram/_comment.html', {
        'form': form,
    })
