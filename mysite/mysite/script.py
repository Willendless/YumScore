import os
os.environ['DJANGO_SETTINGS_MODULE']='mysite.settings'
import django
django.setup()
import json
from scoringsystem.models import Business, Tip, Review, Photo
from login.models import UserProfile, User
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.files import File


def f_business():
    f = open(r'D:\linux\business.json', "r", encoding='utf-8')
    line = f.readline()
    i = 0
    while line:
        print(i)
        obj = json.loads(line, encoding='utf-8')
        business_id = obj['business_id']
        business_name = obj['name']
        business_address = obj['address']
        business_city = obj['city']
        business_state = obj['state']
        business_postal_code = obj['postal_code']
        business_lat = obj['latitude']
        business_long = obj['longitude']
        business_stars = obj['stars']
        business_review_count = obj['review_count']
        tmp = obj['hours']
        if tmp is None:
            business_mon = ""
            business_tue = ""
            business_wed = ""
            business_thu = ""
            business_fri = ""
            business_sat = ""
            business_sun = ""
        else:
            business_mon = obj['hours'].get('Monday', "Closed")
            business_tue = obj['hours'].get('Tuesday', "Closed")
            business_wed = obj['hours'].get('Wednesday', "Closed")
            business_thu = obj['hours'].get('Thursday', "Closed")
            business_fri = obj['hours'].get('Friday', "Closed")
            business_sat = obj['hours'].get('Saturday', "Closed")
            business_sun = obj['hours'].get('Sunday', "Closed")
        Business(business_id=business_id, business_name=business_name, business_address=business_address, business_city=business_city,
                 business_lat=business_lat, business_long=business_long, business_postal_code=business_postal_code,
                 business_state=business_state, business_stars=business_stars, business_review_count=business_review_count,
                 business_mon=business_mon, business_tue=business_tue, business_wed=business_wed, business_thu=business_thu,
                 business_fri=business_fri, business_sat=business_sat, business_sun=business_sun).save()
        line = f.readline()
        i += 1


def f_user():
    f = open(r'D:\linux\user.json', "r", encoding='utf-8')
    line = f.readline()
    i = 0
    while line:
        obj = json.loads(line, encoding='utf-8')
        print(i)
        try:
            if User.objects.get(username=i):
                i += 1
                continue
        except ObjectDoesNotExist:
            pass
        user = User(username=i, password=i)
        user_name = obj['name']
        user_identifier = obj['user_id']
        try:
            if UserProfile.objects.get(user_identifier=user_identifier):
                i += 1
                continue
        except ObjectDoesNotExist:
            pass
        user_review_count = obj['review_count']
        user_date = obj['yelping_since']
        user_average_stars = obj['average_stars']
        user_fans = obj['fans']
        user_useful_votes = obj['useful']
        user_funny_votes = obj['funny']
        user_cool_votes = obj['cool']
        user.save()
        UserProfile(user=user, user_name=user_name, user_identifier=user_identifier, user_review_count=user_review_count,
                    user_date=user_date, user_average_stars=user_average_stars, user_fans=user_fans, user_useful_votes=user_useful_votes,
                    user_funny_votes=user_funny_votes, user_cool_votes=user_cool_votes).save()
        line = f.readline()
        i += 1
    f.close()


def f_review():
    f = open(r'D:\linux\review.json', "r", encoding='utf-8')
    line = f.readline()
    i = 0
    while line:
        print(i)
        obj = json.loads(line, encoding='utf-8')
        try:
            review_user_id = UserProfile.objects.get(user_identifier=obj['user_id'])
            review_business_id = Business.objects.get(business_id=obj['business_id'])
            review_stars = obj['stars']
            review_text = obj['text']
            review_date = obj['date']
            review_useful_vote = obj['useful']
            review_funny_vote = obj['funny']
            review_cool_vote = obj['cool']
            Review(review_user_id=review_user_id, review_business_id=review_business_id,
                   review_stars=review_stars, review_text=review_text, review_date=review_date,
                   review_useful_vote=review_useful_vote, review_funny_vote=review_funny_vote,
                   review_cool_vote=review_cool_vote).save()
            i += 1
        except ObjectDoesNotExist:
            pass
        line = f.readline()
    f.close()


def f_tip():
    f = open(r'D:\linux\tip.json', 'r', encoding='utf-8')
    line = f.readline()
    i = 0
    while line:
        print(i)
        obj = json.loads(line, encoding='utf-8')
        try:
            tip_text = obj['text']
            tip_date = obj['date']
            tip_business_id = Business.objects.get(business_id=obj['business_id'])
            tip_user_id = UserProfile.objects.get(user_identifier=obj['user_id'])
            Tip(tip_text=tip_text, tip_date=tip_date, tip_business_id=tip_business_id,
                tip_user_id=tip_user_id).save()
            i += 1
        except ObjectDoesNotExist:
            pass
        line = f.readline()
    f.close()


def f_photo():
    f = open(r'D:\linux\photo.json', 'r', encoding='utf-8')
    line = f.readline()
    i = 0
    while line:
        print(i)
        obj = json.loads(line, encoding='utf-8')
        try:
            photo_business_id = Business.objects.get(business_id=obj['business_id'])
            photo_caption = obj['caption']
            photo_label = obj['label']
            image_path = os.path.join('D:\\linux\\yelp_photos\\photos\\', obj['photo_id'] + '.jpg')
            content = ContentFile(File(open(image_path, 'rb')).read())
            instance = Photo(photo_business_id=photo_business_id, photo_caption=photo_caption,
                             photo_label=photo_label)
            instance.photo_image.save(obj['photo_id'] + '.jpg', content)
            instance.save()
            obj = Photo.objects.get(id=instance.id)
            i += 1
            print(instance.id)

        except ObjectDoesNotExist:
            pass
        line = f.readline()


#f_business()
#f_user()
#f_review()
#f_tip()
#f_photo()

