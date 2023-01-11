import re
from django.db import models
from django.conf import settings
from django.urls import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # 추상메소드 : abstract = True, class를 다른 곳에 상속시켜야 할 때 사용


class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_post_set")
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.CharField(max_length=500)  # 사진설명
    location = models.CharField(max_length=100)  # 위치
    tag_set = models.ManyToManyField('Tag', blank=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post_set')

    class Meta:
        # ordering : 정렬 / +은 직렬화 정렬(기본값) , -는 역순화 정렬
        ordering = ['-pk']

    def get_absolute_url(self):
        return reverse('instagram:post_detail', args=[self.pk])

    # caption에서 tag삭제하고 글씨만 남기는 함수
    def caption_replace(self):
        caption = re.sub(r"#([a-zA-z\dㄱ-힣]+)", "", self.caption).strip()
        self.caption = caption
        return self.caption

    # caption에서 tag를 쓸 수 있게 하는 함수
    def extract_tag_list(self):
        # re.findall() : 정규표현식에 해당하는 것들을 전부 찾아온다.
        tag_name_list = re.findall(r"#([a-zA-z\dㄱ-힣]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(
                name=tag_name)  # name에 tag_name_list에서 순차적으로 다시 담은 tag_name을 넣어준다.
            tag_list.append(tag)  # append : 리스트에 변수를 넣어주는 역할
        return tag_list

    def is_like_user(self, user):
        # 현재 로그인한 유저가 좋아요한 포스팅의 존재여부를 확인
        # exists() : 존재한다면 True 아니라면 False
        return self.like_user_set.filter(pk=user.pk).exists()

    def __str__(self):
        return self.caption
    #     def __str__(self):
    #         # caption : 웰시코기
    #         # Post objects (1) - admin 페이지
    #         # __str__ 의  self.caption 사용후 / Post objects (1) > 웰시코기
    #         return self.caption


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Comment(BaseModel): # BaseModel엔 comment_set 내장되어있나? 뭐지 pk도 그냥 넘겨주나
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    messages = models.TextField()  # 댓글메세지

    class Meta:
        ordering = ['-pk']
