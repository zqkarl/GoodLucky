#coding:utf-8
import random
import uuid
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from lunch.models import RollRecord
from lunch.models import Activity
# Create your views here.


def create_index(request):
    return render(request, "create.html")


def create(request):
    """新建选项"""
    name = request.POST.get("activity_name")
    activity_name = ""
    if name == '1':
        activity_name = "午饭"
    if name == '2':
        activity_name = "下午茶"
    if name == '3':
        activity_name = "晚饭"
    foods = request.POST.get("foods")
    foods_zu = foods.split(" ")
    print type(foods_zu)
    activity = Activity(activity_name=activity_name, food_selects=str(foods_zu))
    activity.save()
    return HttpResponse("http://172.28.125.52/eatwhat?id="+str(activity.id))


def index(request):
    """投票界面"""
    id = request.GET.get("id")
    print str(id)
    activity = Activity.objects.get(id=id)
    ip = '0.0.0.0'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    try:
        record = RollRecord.objects.get(user_ip=ip, uuid_id=uuid.UUID(id))
        return HttpResponseRedirect(reverse("result") + "?id_=" + id)
    except RollRecord.DoesNotExist:
        return render(request, 'home.html', {'id_': id, 'selects': eval(activity.food_selects),
                                             'activity': activity})
    except:
        raise


def roll(request):
    """抽奖入口"""
    id = request.GET.get("id_")
    name = request.POST.get("nickname", "null")
    food = request.POST.get("foodname", "null")
    ip = '0.0.0.0'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    try:
        result = RollRecord.objects.get(user_ip=ip, uuid_id=uuid.UUID(id))
    except RollRecord.DoesNotExist:
        if name == "null" or food == "null":
            activity = Activity.objects.get(id=id)
            return render(request, 'home.html', {'id_': id, 'selects': eval(activity.food_selects), 'activity': activity})
        else:
            record = RollRecord(name=name, food=food)
            record.num = random.randint(0, 100)
            record.user_ip = ip
            record.uuid = Activity.objects.get(id=id)
            record.save()

    return HttpResponseRedirect(reverse("result")+"?id_="+id)


def result_view(request):
    id = request.GET.get("id_")
    ip = '0.0.0.0'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    try:
        result = RollRecord.objects.get(user_ip=ip, uuid_id=uuid.UUID(id))
    #    result = RollRecord.objects.get(user_ip=ip)
    except RollRecord.DoesNotExist:
        return HttpResponseRedirect(reverse("add") + "?id_=" + id)
    activity = Activity.objects.get(id=id)
    results = RollRecord.objects.filter(uuid_id=uuid.UUID(id)).order_by("-num")
    unpay_record = RollRecord.objects.filter(is_payed=False).filter(user_ip=ip).filter(uuid__biller_name__isnull=False)
    if len(unpay_record) is 0:
        unpay_record = None
    else:
        unpay_record = unpay_record[0]
    record = RollRecord.objects.get(user_ip=ip, uuid_id=uuid.UUID(id))  # 本次投票本人记录
    return render(request, 'result.html', {'resultList': results, 'activity': activity, 'ip': ip,
                                           'unpay_record': unpay_record, 'record': record})


def unpayed(request):
    id = request.GET.get("id_")
    ip = '0.0.0.0'
    results = RollRecord.objects.filter(is_payed=False).filter(uuid__biller_name__isnull=False)
    # for r in results:
    #     dict = {}
    #     dict["who"] = 1
    #     dict["biller"] = ""
    #     dict["which"] = ""
    if len(results) is not 0:
        return render(request, 'unpayed.html', {"result": results, "id_": id})
    else:
        return HttpResponseRedirect(reverse("eatwhat") + "?id_" + id)


def bill(request):
    """记账页面"""
    id = request.GET.get("id_")
    ip = '0.0.0.0'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    activity = Activity.objects.get(id=id)
    results = RollRecord.objects.filter(uuid_id=uuid.UUID(id))
    return render(request, 'bill.html', {'resultList': results, 'activity': activity, 'id': id, 'ip': ip})


def settle(request):
    id = request.GET.get("id_")
    user_id = request.GET.get("user_id")
    ip = '0.0.0.0'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    activity = Activity.objects.get(id=id)
    #TODO: 加入安全环境判断
    if activity.biller_ip == ip:
        record = RollRecord.objects.get(id=user_id)
        record.is_payed = True
        record.save()
        return HttpResponseRedirect(reverse("bill") + "?id_=" + id)
    else:
        return HttpResponse("请在"+str(activity.biller_ip)+"环境下操作")


def bill_claim_confirm(request):
    id = request.GET.get("id_")
    activity = Activity.objects.get(id=id)
    ip = '0.0.0.0'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    try:
        record = RollRecord.objects.get(user_ip=ip, uuid_id=uuid.UUID(id))
        return render(request, 'bill_confirm.html', {'record': record, 'id': id, 'activity': activity})
    except RollRecord.DoesNotExist:
        return render(request, 'newbiller.html')


def bill_claim_submit(request):
    id = request.GET.get("id_")
    nickname = request.GET.get("nickname")
    ip = '0.0.0.0'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    activity = Activity.objects.get(id=id)
    activity.biller_name = nickname
    activity.biller_ip = ip
    activity.save()
    record = RollRecord.objects.get(user_ip=ip, uuid_id=uuid.UUID(id))
    record.is_payed = True
    record.save()
    return HttpResponseRedirect(reverse("bill")+"?id_="+id)


def lists(request):
    """历史记账记录"""
    all = request.GET.get("all")
    if all == "1":
        activities = Activity.objects.filter(biller_ip__isnull=False).order_by("-create_date")
    else:
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        activities = Activity.objects.filter(biller_ip=ip).order_by("-create_date")
    for activity in activities:
        record = RollRecord.objects.filter(uuid=activity).filter(is_payed=False)
        if len(record) is not 0:
            activity.clear = False
        else:
            activity.clear = True
    return render(request, "historylist.html", {"activities": activities})