from django.db import models
from django.utils import timezone
from login.models import UserProfile


class Business(models.Model):
    business_id = models.CharField(max_length=22, unique=True)
    business_name = models.CharField('企业名', max_length=100, db_index=True)
    business_address = models.CharField('企业地址', max_length=100)
    business_city = models.CharField('企业城市', max_length=100)
    business_state = models.CharField('企业所在州', max_length=100)
    business_postal_code = models.CharField('邮编', max_length=20)
    business_lat = models.FloatField('纬度')
    business_long = models.FloatField('经度')
    business_stars = models.FloatField('得分', default=0.0, db_index=True)
    business_review_count = models.IntegerField('评论计数', default=0)
    business_mon = models.CharField('周一', max_length=20, blank=True)
    business_tue = models.CharField('周二', max_length=20, blank=True)
    business_wed = models.CharField('周三', max_length=20, blank=True)
    business_thu = models.CharField('周四', max_length=20, blank=True)
    business_fri = models.CharField('周五', max_length=20, blank=True)
    business_sat = models.CharField('周六', max_length=20, blank=True)
    business_sun = models.CharField('周日', max_length=20, blank=True)

    def __str__(self):
        return self.business_name

    class Meta:
        ordering = ['-business_review_count']


class Review(models.Model):
    review_user_id = models.ForeignKey(
        UserProfile,
        on_delete=models.SET('用户已注销'),
        db_index=True
    )
    review_business_id = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        db_index=True
    )
    review_stars = models.FloatField('评分', default=0)
    review_text = models.TextField('评论')
    review_date = models.DateTimeField('日期', default=timezone.now)
    review_useful_vote = models.IntegerField(default=0)
    review_funny_vote = models.IntegerField(default=0)
    review_cool_vote = models.IntegerField(default=0)

    class Meta:
        ordering = ['-review_date']


class Tip(models.Model):
    tip_text = models.CharField('便签', max_length=500)
    tip_date = models.DateTimeField('日期', default=timezone.now)
    tip_business_id = models.ForeignKey(Business, on_delete=models.CASCADE)
    tip_user_id = models.ForeignKey(UserProfile, on_delete=models.SET('用户已注销'))

    class Meta:
        ordering = ['-tip_date']


class Photo(models.Model):
    photo_business_id = models.ForeignKey(Business, on_delete=models.CASCADE)
    photo_caption = models.CharField('类别', max_length=200)
    photo_label = models.CharField('标题', max_length=200)
    photo_image = models.ImageField('图片', upload_to='business_img', max_length=250)


class Vote(models.Model):
    option = [
        (1, 'Useful'),
        (2, 'Funny'),
        (3, 'Cool'),
    ]
    vote_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vote_review = models.ForeignKey(Review, on_delete=models.CASCADE)
    vote_option = models.IntegerField('投票选择', default=0, choices=option)