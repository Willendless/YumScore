from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from login.models import UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

from django.db import connection


def index(request):
    business_list_1 = Business.objects.all()[:3]
    for i in business_list_1:
        if i.photo_set.count() == 0:
            i.image = Photo.objects.all()[0]
        else:
            i.image = i.photo_set.all()[0]

    business_list_2 = Business.objects.all()[3:6]
    for i in business_list_2:
        if i.photo_set.count() == 0:
            i.image = Photo.objects.all()[0]
        else:
            i.image = i.photo_set.all()[0]
    return render(request, "scoringsystem/index.html", {'business_list_1': business_list_1, 'business_list_2': business_list_2})


def homepage(request, user_id):
    meta = User.objects.get(id=user_id)
    user_obj = UserProfile.objects.get(user=meta)
    review_list = user_obj.review_set.all()
    paginator = Paginator(review_list, 8)
    num = request.GET.get('page')
    try:
        review_list = paginator.page(num)
    except PageNotAnInteger:
        review_list = paginator.page(1)
    except EmptyPage:
        review_list = paginator.page(paginator.num_pages)
    for i in review_list:
        if i.review_business_id.photo_set.count() == 0:
            i.image = Photo.objects.all()[0]
        else:
            i.image = i.review_business_id.photo_set.all()[0]
    return render(request, 'scoringsystem/homepage.html', {'user': user_obj, 'reviews': review_list})


def business(request, business_id):
    obj = get_object_or_404(Business, id=business_id)
    img_list = obj.photo_set.all()[:3]
    rev_list = obj.review_set.all()
    tip_list = obj.tip_set.all()[:3]
    paginator = Paginator(rev_list, 8)
    num = request.GET.get('page')
    try:
        rev_list = paginator.page(num)
    except PageNotAnInteger:
        rev_list = paginator.page(1)
    except EmptyPage:
        rev_list = paginator.page(paginator.num_pages)
    return render(request, 'scoringsystem/business.html', {'img_list': img_list, 'business': obj,
                                                           'reviews': rev_list, 'business_id': business_id,
                                                           'tip_list': tip_list})


def review(request, business_id):
    obj = get_object_or_404(Business, id=business_id)
    return render(request, 'scoringsystem/review.html', {'business': obj})


def review_post(request, business_id):
    review_text = request.POST.get('review_text')
    review_stars = request.POST.get('review_stars')
    if review_stars is None:
        review_stars = 1
    review_date = timezone.now()
    if request.session.get('id', None) is None:
        return redirect("/accounts/login")
    else:
        user = get_object_or_404(User, id=request.session.get('id'))
        user = get_object_or_404(UserProfile, user=user)
        business_obj = get_object_or_404(Business, id=business_id)
        user.user_review_count += 1
        business_obj.business_stars = (business_obj.business_stars * business_obj.business_review_count + int(review_stars)) / (business_obj.business_review_count + 1)
        business_obj.business_review_count += 1
        Review(review_user_id=user, review_business_id=business_obj, review_text=review_text,
               review_stars=review_stars, review_date=review_date).save()
        business_obj.save()
        url = "/scoringsystem/" + str(business_id) + '/business'
        return redirect(url)


def vote(request, review_id, vote_op):
    is_login = request.session.get('is_login', None)
    if is_login is None or is_login is False:
        return redirect("/accounts/login")
    else:
        user = get_object_or_404(User, id=request.session.get('id'))
        user = get_object_or_404(UserProfile, user=user)
        review_obj = get_object_or_404(Review, id=review_id)
        if review_obj.review_user_id.id == user.id:
            return redirect('/scoringsystem/'+str(review_obj.review_business_id.id)+'/business')
        user_dst = review_obj.review_user_id
        vote_obj = Vote.objects.get_or_create(vote_user=user, vote_review=review_obj)
        vote_obj = vote_obj[0]
        if vote_obj.vote_option is 0:
            vote_obj.vote_option = vote_op
            if vote_op == 1:
                review_obj.review_useful_vote += 1
                user_dst.user_useful_votes += 1
            elif vote_op == 2:
                review_obj.review_funny_vote += 1
                user_dst.user_funny_votes += 1
            else:
                review_obj.review_cool_vote += 1
                user_dst.user_cool_votes += 1
            review_obj.save()
            user_dst.save()
            vote_obj.save()
        else:
            if vote_obj.vote_option != vote_op:
                pass
            else:
                if vote_op == 1:
                    review_obj.review_useful_vote -= 1
                    user_dst.user_useful_votes -= 1
                elif vote_op == 2:
                    review_obj.review_funny_vote -= 1
                    user_dst.user_funny_votes -= 1
                else:
                    review_obj.review_cool_vote -= 1
                    user_dst.user_cool_votes -= 1
                vote_obj.delete()
                review_obj.save()
                user_dst.save()
        if request.GET.get('business', None) is '1':
            return redirect('/scoringsystem/'+str(review_obj.review_business_id.id)+'/business')
        else:
            return redirect('/scoringsystem/'+str(review_obj.review_user_id.id)+'/user')


def photos(request, business_id):
    photos_list = Business.objects.get(id=business_id).photo_set.all()
    paginator = Paginator(photos_list, 30)
    num = request.GET.get('page')
    try:
        photos_list = paginator.page(num)
    except PageNotAnInteger:
        photos_list = paginator.page(1)
    except EmptyPage:
        photos_list = paginator.page(paginator.num_pages)
    except InvalidPage:
        photos_list = paginator.page(1)
    return render(request, 'scoringsystem/photos.html', {'photos': photos_list, 'rows': 5, 'cols': 6})


def search(request, is_search_all=0):
    keyword = request.GET.get('search', None)
    if is_search_all:
        business_list = Business.objects.all()
    else:
        business_list = Business.objects.filter(business_name__icontains=keyword)
    paginator = Paginator(business_list, 10)
    num = request.GET.get('page')
    try:
        business_list = paginator.page(num)
    except PageNotAnInteger:
        business_list = paginator.page(1)
    except EmptyPage:
        business_list = paginator.page(paginator.num_pages)
    for i in business_list:
        if i.photo_set.count() == 0:
            i.image = Photo.objects.all()[0]
        else:
            i.image = i.photo_set.all()[0]
    return render(request, 'scoringsystem/search.html', {'search': keyword,'businesses': business_list})


def search_all(request):
    return search(request, 1)
