from django import template

register = template.Library()


# _post_card.html에 넣을 내용
@register.filter
def is_like_user(post, user):
    return post.is_like_user(user)
