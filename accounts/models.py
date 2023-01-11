from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import resolve_url
from django.conf import settings


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = 'M', '남성'
        FEMALE = 'W', '여성'
    follower_set = models.ManyToManyField('self', symmetrical=False, related_name='account_follower_set')
    following_set = models.ManyToManyField('self', symmetrical=False, related_name='account_following_set')
    bio = models.TextField()
    phone_number = models.CharField(blank=True, max_length=11, validators=[RegexValidator(r"^010[1-9]\d{3}\d{4}$")],
                                    help_text='하이폰(-)을빼고 입력해주세요')
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, blank=True)
    avatar = models.ImageField(blank=True, upload_to='accounts/avatar/%Y/%m/%d', help_text='help_text: 힌트입력하는곳의미')
    website_url = models.URLField(blank=True)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url('pydenticon_image', self.username)

    # templates user_page에서 사용 , 기본프로젝트에서 url로 만들 pattern name pydenticon_image 사용

    @property
    def name(self):
        return f'{self.first_name}{self.last_name}'
