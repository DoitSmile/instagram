from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, logout_then_login, PasswordChangeView as AuthPasswordChangeView)
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login, get_user_model

from accounts.forms import SignupForm, ProfileForm, PasswordChangeForm


class Login(LoginView):
    template_name = 'accounts/login_form.html'

    def get_success_url(self):
        messages.success(self.request, '로그인 성공')
        return reverse_lazy('root')


login = Login.as_view()


@login_required
def logout(request):
    messages.success(request, '로그아웃 완료')
    return logout_then_login(request)  # 로그아웃 하자마자 login 페이지로


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)  # 회원가입하자마자 로그인
            messages.success(request, '회원가입 축하합니다.')
            next_url = request.GET.get('next', '/')  # next가 있다면 next_url추가 (마지막 render에서 바로 원하는 페이지로 보낼 수 있게 도와주는 역할
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form
    })

@login_required()
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '수정이 완료되었습니다.')
            redirect('accounts:profile_edit')  # 자동새로고침하고 profile_edit으로 이동

    else:
        form = ProfileForm(instance=request.user)  # 빈폼을 보여주면 안된다 수정 전 유저의 프로필을 보여줄 것 !
    return render(request, 'accounts/profile_edit.html', {
        'form': form
    })


#  LoginRequiredMixin:  @login_required와 똑같은 기능 class 기반 view에서는 이렇게 사용
class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url = reverse_lazy('accounts:password_change')
    template_name = 'accounts/password_change.html'
    # 커스텀한 form을가져올땐 from accounts.forms를 import해야한다.
    form_class = PasswordChangeForm

    # 유효성 검사하는 함수, class에서 messages.success를 쓰기 위해선 함수를 재정의 해서 써야한다
    def form_valid(self, form):
        messages.success(self.request, '암호가 성공적으로 변경되었습니다.')
        return super().form_valid(form)  # form_valid(): form.save()같은것들 내장되어있는 것


password_change = PasswordChangeView.as_view()



# @login_required
def user_follow(request, username):
    following_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    request.user.following_set.add(following_user) # following_set , follower_set model필드명임
    following_user.follower_set.add(request.user)
    messages.success(request, f'{following_user} 님을 팔로우하였습니다.')
    redirect_url = request.META.get('HTTP_REFERER', 'root')
    # HTTP_REFERER : url 값 root: url patternname이지만 redirect가 유연하게 둘다 검색해보기때문에 가능한 것 (patternname먼저 검색해범)
    return redirect(redirect_url)


def user_unfollow(request, username):
    unfollowing_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    request.user.following_set.remove(unfollowing_user)
    unfollowing_user.follower_set.remove(request.user)
    messages.success(request, f'{unfollowing_user} 님을 언팔로우하였습니다.')
    redirect_url = request.META.get('HTTP_REFERER', 'root')
    return redirect(redirect_url)


