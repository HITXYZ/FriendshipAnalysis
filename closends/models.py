import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

marks = {'weibo': '微博', 'zhihu': '知乎', 'tieba': '贴吧'}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class UserInfo(models.Model):
    def __str__(self):
        return self.user.username

    def image_name(self):
        if not self.head_img.name:
            return 'default_head.svg'
        return self.head_img.name.split('/')[-1]

    user = models.OneToOneField(User)
    head_img = models.ImageField(blank=True, upload_to=BASE_DIR + '/media/head')
    group_list = models.CharField(default='未分组', max_length=1024)


class Website(models.Model):
    """用户各网站账号"""

    def __str__(self):
        return marks[self.site]

    def username(self):
        return self.user.user.username

    site_choices = (('weibo', '微博'), ('zhihu', '知乎'), ('tieba', '贴吧'))
    site = models.CharField(max_length=5, default='weibo', choices=site_choices)
    site_account = models.CharField(max_length=20)
    site_link = models.URLField(max_length=500)
    site_ID = models.CharField(max_length=20)
    site_head = models.URLField(max_length=500)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


class Friend(models.Model):
    """用户好友"""

    def __str__(self):
        return self.nickname

    def username(self):
        return self.user.user.username

    def image_name(self):
        if not self.head_img.name:
            return 'default_head.svg'
        return self.head_img.name.split('/')[-1]

    def weibo_is_blank(self):
        return not self.weibo_account

    def zhihu_is_blank(self):
        return not self.zhihu_account

    def tieba_is_blank(self):
        return not self.tieba_account

    group_choices = (('未分组', '未分组'), ('同学', '同学'), ('好友', '好友'), ('家人', '家人'))
    nickname = models.CharField(max_length=30)
    head_img = models.ImageField(blank=True, upload_to=BASE_DIR + '/media/head')
    group = models.CharField(max_length=10, default='未分组', choices=group_choices)

    weibo_account = models.CharField(max_length=20, blank=True)
    weibo_ID = models.CharField(max_length=100, blank=True)
    weibo_link = models.URLField(max_length=500, blank=True)
    weibo_head = models.URLField(max_length=500, blank=True)

    zhihu_account = models.CharField(max_length=20, blank=True)
    zhihu_ID = models.CharField(max_length=100, blank=True)
    zhihu_link = models.URLField(max_length=500, blank=True)
    zhihu_head = models.URLField(max_length=500, blank=True)
    zhihu_detail = models.CharField(max_length=200, blank=True)

    tieba_account = models.CharField(max_length=20, blank=True)
    tieba_ID = models.CharField(max_length=100, blank=True)
    tieba_link = models.URLField(max_length=500, blank=True)
    tieba_head = models.URLField(max_length=500, blank=True)

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


class WeiboContent(models.Model):
    """微博动态"""

    def __str__(self):
        return self.content[:20]

    def content_section(self):
        return self.content[:20]

    def friend_nickname(self):
        return self.friend.nickname

    def friend_head(self):
        return self.friend.image_name()

    def friend_weibo_account(self):
        return self.friend.weibo_account

    def friend_weibo_link(self):
        return self.friend.weibo_link

    def platform(self):
        return 'weibo'

    def str_time(self):
        return str(self.pub_date)[5:-3]

    pub_date = models.DateTimeField(default=timezone.now)
    src_url = models.URLField(max_length=500)
    content = models.TextField()

    is_repost = models.BooleanField()
    has_image = models.BooleanField()
    video_image = models.URLField(max_length=500, blank=True)

    origin_account = models.CharField(max_length=20, blank=True)
    origin_link = models.URLField(max_length=500, blank=True)

    origin_pub_date = models.CharField(max_length=20, blank=True)
    origin_src_url = models.URLField(max_length=500, blank=True)
    origin_content = models.TextField(blank=True)
    origin_has_image = models.BooleanField(default=False)
    origin_video_image = models.URLField(max_length=500, blank=True)

    topic = models.CharField(max_length=10, blank=True)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)


class ZhihuContent(models.Model):
    """知乎动态"""

    def __str__(self):
        return self.action_type

    def friend_nickname(self):
        return self.friend.nickname

    def friend_head(self):
        return self.friend.image_name()

    def friend_zhihu_account(self):
        return self.friend.zhihu_account

    def friend_zhihu_link(self):
        return self.friend.zhihu_link

    def has_cover_image(self):
        return not (not self.cover_image)

    def author_operation(self):
        return self.action_type == '回答了问题' or self.action_type == '发表了文章'

    def has_headline(self):
        return not self.target_user_headline

    def platform(self):
        return 'zhihu'

    def str_time(self):
        return str(self.pub_date)[5:-3]

    pub_date = models.DateTimeField(default=timezone.now)
    action_type = models.CharField(max_length=10)

    target_user_name = models.CharField(max_length=50)
    target_user_head = models.URLField(max_length=500)
    target_user_url = models.URLField(max_length=500)
    target_user_headline = models.CharField(max_length=100, blank=True)

    target_title = models.CharField(max_length=50)
    target_title_url = models.CharField(max_length=500)
    target_content = models.TextField()
    target_content_url = models.URLField(max_length=500)
    cover_image = models.URLField(max_length=500, blank=True)

    topic = models.CharField(max_length=10, blank=True)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)


class TiebaContent(models.Model):
    """贴吧动态"""

    def __str__(self):
        return self.title

    def friend_nickname(self):
        return self.friend.nickname

    def friend_head(self):
        return self.friend.image_name()

    def friend_tieba_account(self):
        return self.friend.tieba_account

    def friend_tieba_head(self):
        return self.friend.tieba_head

    def friend_tieba_link(self):
        return self.friend.tieba_link

    def platform(self):
        return 'tieba'

    def str_time(self):
        return str(self.pub_date)[5:-3]

    pub_date = models.DateTimeField(default=timezone.now)

    forum = models.CharField(max_length=20)
    forum_url = models.URLField(max_length=500)
    title = models.CharField(max_length=100)
    title_url = models.URLField(max_length=500)
    content = models.TextField()
    content_url = models.URLField(max_length=500)

    topic = models.CharField(max_length=10, blank=True)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)


class Image(models.Model):
    """所有动态的图片及链接"""

    def __str__(self):
        return self.image_url

    image_url = models.URLField(max_length=100, blank=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")
