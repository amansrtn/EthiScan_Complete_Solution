import base64
import json
import os
import re
import easyocr
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import Website, validationForActivityNotification, validationWithTime
from rndmfrst_model.Disguised_UI import find_Disguised_UI
from rndmfrst_model.Hidden_Cost import flag_hidden_cost
from rndmfrst_model.Model_Prediction_On_Text import Predict_Dark_Pattern_Type
from rndmfrst_model.Review_Checker import review_checker
from rndmfrst_model.App_Name_LLM import AppNameFinder
from datetime import timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta



temp_dir = "temp_images"
os.makedirs(temp_dir, exist_ok=True)

def image_to_text(image_path, language="en"):
    reader = easyocr.Reader([language])
    result = reader.readtext(image_path)
    text = "\n".join([item[1] for item in result])
    return text

def website_exists_and_does_not_contain_any_category(base_url, category_names):
    try:
        website = Website.objects.get(baseURL=base_url)
        for category_name in category_names:
            if not website.category.filter(patternName=category_name).exists():
                return {
                    'website_exists': True,
                    'does_not_contain_any_category': True
                }
        return {
            'website_exists': True,
            'does_not_contain_any_category': False
        }

    except Website.DoesNotExist:
        return {
            'website_exists': False,
            'does_not_contain_any_category': True
        }

@csrf_exempt
def default(request):
    received_json_data=json.loads(request.body)
    base64_image = received_json_data.get('base64_image')
    if(base64_image==None):
        res = {'result_dark_pattern_type': 'error, no base64_img param found in request'}
        return JsonResponse(res)
    image_data = base64.b64decode(base64_image)
    image_filename = "uploaded_image.jpg"
    image_path = os.path.join(temp_dir, image_filename)
    with open(image_path, "wb") as image_file:
            image_file.write(image_data)
            image_file.close
            image_file.flush
    image_path = "temp_images\\uploaded_image.jpg"
    result_text = image_to_text(image_path)
    print(result_text)
    app_details = AppNameFinder(result_text)
    result_text_lst=result_text.split('\n')
    app_name = app_details[0]
    prod_name = app_details[1]
    res=[]
    mp={}
    for result_text in result_text_lst:
        output_dark_pattern_type = Predict_Dark_Pattern_Type(result_text)
        if output_dark_pattern_type!="Clean":
            status = "confirmed"
            visiblity = "Today"
            if output_dark_pattern_type == 'Activity Notification':
                if('hours' in result_text.lower()):
                    status = activityNotificationValidatorHour(baseUrl=app_name+".mobile", prod_name=prod_name, msg=result_text)
                elif('days' in result_text.lower()):
                    status = activityNotificationValidatorDays(baseUrl=app_name+".mobile", prod_name=prod_name, msg=result_text)
                elif('weeks' in result_text.lower()):
                    status = activityNotificationValidatorWeeks(baseUrl=app_name+".mobile", prod_name=prod_name, msg=result_text)
                elif('month' in result_text.lower()):
                    status = activityNotificationValidatorMonths(baseUrl=app_name+".mobile", prod_name=prod_name, msg=result_text)
                else:
                    status = activityNotificationValidatorGeneral(baseUrl=app_name+".mobile", prod_name=prod_name, msg=result_text)
                record = validationForActivityNotification.objects.get(baseUrl=app_name+".mobile", prod_name=prod_name, msg = result_text)
                visiblity = relativedelta(timezone.now(), record.timestamp).days
                if(visiblity == 0):
                    visiblity = "Today"
                elif(visiblity!="Today"):
                    visiblity = str(visiblity)+" Days"
            elif output_dark_pattern_type == "Countdown Timer":
                ind = 0
                for i in range(len(result_text)):
                    if(result_text[i].isdigit()):
                        ind = i
                        break
                result_text = result_text[ind:]
                curr_time = convert_to_seconds(result_text)
                status = validatorWithTime(baseUrl= app_name+".mobile", prod_name= prod_name, curr_time=curr_time)
                record = validationWithTime.objects.get(baseUrl=app_name+".mobile", prod_name=prod_name)
                visiblity = relativedelta(timezone.now(), record.init_time).days
                if(visiblity == 0):
                    visiblity = "Today"
                elif(visiblity!="Today"):
                    visiblity = str(visiblity)+" Days"
            mp[result_text]=[output_dark_pattern_type,status, visiblity]
            res.append(output_dark_pattern_type)
    output_hidden_cost = flag_hidden_cost(result_text_lst)
    disguised_ui = find_Disguised_UI(result_text)
    review_check = review_checker([result_text])
    # patterns = []
    # patterns.append(output_dark_pattern_type)
    if(output_hidden_cost["flag"]=="Found"):
         res.append("Hidden Costs")
         
        
    checkForUnique = website_exists_and_does_not_contain_any_category(base_url=app_name+".mobile", category_names=res)
    if len(res)==0:
         checkForUnique["does_not_contain_any_category"]=False
         mp=""
    Website.create_or_update_website(baseURL=app_name+".mobile", webName=app_name, category_names=res)
    return JsonResponse({
            
            "result_dark_pattern_type": mp,
            "result_hidden_cost_flag": output_hidden_cost["flag"],
            "result_hidden_cost_type": output_hidden_cost["keyword"],
            "Disguised_flag": disguised_ui["Disguised_flag"],
            "Disguised_max_word": disguised_ui["max_word"],
            "Disguised_max_count": disguised_ui["max_count"],
            "Fake_Review": review_check,
            "App_Name": app_name,
            "Unique": checkForUnique['does_not_contain_any_category']
        }, status = 200)

def validatorWithTime(baseUrl, prod_name, curr_time):
    try:
        if(curr_time == 0):
            return "confirmed"
        record = validationWithTime.objects.get(baseUrl=baseUrl, prod_name=prod_name)
        time_difference = timezone.now() - record.init_time

        if(time_difference.total_seconds() >= 604800):
            validationWithTime.objects.aupdate(shown_time=curr_time)
            return "warning"

        shown_time = record.shown_time
        recorded_time_diff = abs(shown_time - curr_time)
        time_difference_seconds = time_difference.total_seconds()
        if(abs(recorded_time_diff-time_difference_seconds) <= 10):
            return "warning"
        else:
            return "confirmed"
    except validationWithTime.DoesNotExist:
        validationWithTime.objects.create(baseUrl=baseUrl, prod_name=prod_name, shown_time = curr_time)
        return "warning"

def convert_to_seconds(time_str):
    if('s' not in time_str):
        lis = time_str.split(":")
        if(len(lis) == 3):
            lis[0] = lis[0] + 'h'
            lis[1] = lis[1] + 'm'
            lis[2] = lis[2] + 's'
        elif(len(lis) == 2):
            lis[0] = lis[0] + 'm'
            lis[1] = lis[1] + 's'
        else:
            lis[0] = lis[0] + 'd'
            lis[1] = lis[1] + 'h'
            lis[2] = lis[2] + 'm'
            lis[3] = lis[3] + 's'
        time_str = ''.join(lis)
    patterns = {
        'days': r'(\d+)\s*(d|days?)',
        'hours': r'(\d+)\s*(h|hours?)',
        'minutes': r'(\d+|0+)\s*(m|mins?|minutes?)',
        'seconds': r'(\d+|0+)\s*(s|secs?|seconds?)'
    }
    total_seconds = 0
    for unit, pattern in patterns.items():
        match = re.search(pattern, time_str, re.IGNORECASE)
        if match:
            value = int(match.group(1))
            if unit == 'days':
                total_seconds += value * 24 * 60 * 60
            elif unit == 'hours':
                total_seconds += value * 60 * 60
            elif unit == 'minutes':
                total_seconds += value * 60
            elif unit == 'seconds':
                total_seconds += value

    return total_seconds

def activityNotificationValidatorGeneral(baseUrl, msg, prod_name):
    try:
        record = validationForActivityNotification.objects.get(baseUrl= baseUrl, prod_name = prod_name, msg = msg)
        time_diff = timezone.now() - record.timestamp
        if(time_diff > timedelta(days=1)):
            if(record.msg == msg):
                return "confirmed"
            else:
                return "warning"
        return "warning"
    except validationForActivityNotification.DoesNotExist:
        validationForActivityNotification.objects.create(baseUrl=baseUrl, msg=msg, prod_name=prod_name)
        return "warning"

def activityNotificationValidatorHour(baseUrl, msg, prod_name):
    try:
        record = validationForActivityNotification.objects.get(baseUrl= baseUrl, prod_name = prod_name, msg = msg)
        time_diff = timezone.now() - record.timestamp
        if(time_diff > timedelta(hours=1)):
            if(record.msg == msg):
                return "confirmed"
            else:
                return "warning"
        return "warning"
    except validationForActivityNotification.DoesNotExist:
        validationForActivityNotification.objects.create(baseUrl=baseUrl, msg=msg, prod_name=prod_name)
        return "warning"

def activityNotificationValidatorDays(baseUrl, msg, prod_name):
    try:
        record = validationForActivityNotification.objects.get(baseUrl=baseUrl, prod_name=prod_name, msg=msg)
        time_diff = timezone.now() - record.timestamp
        if(time_diff > timedelta(days=1)):
            if(record.msg == msg):
                return "confirmed"
            else:
                return "warning"
        return "warning"
    except validationForActivityNotification.DoesNotExist:
        validationForActivityNotification.objects.create(baseUrl=baseUrl, msg=msg, prod_name=prod_name)
        return "warning"

def activityNotificationValidatorWeeks(baseUrl, msg, prod_name):
    try:
        record = validationForActivityNotification.objects.get(baseUrl=baseUrl, prod_name=prod_name, msg=msg)
        time_diff = timezone.now() - record.timestamp
        if(time_diff > timedelta(weeks=1)):
            if(record.msg == msg):
                return "confirmed"
            else:
                return "warning"
        return "warning"
    except validationForActivityNotification.DoesNotExist:
        validationForActivityNotification.objects.create(baseUrl=baseUrl, msg=msg, prod_name=prod_name)
        return "warning"

def activityNotificationValidatorMonths(baseUrl, msg, prod_name):
    try:
        record = validationForActivityNotification.objects.get(baseUrl=baseUrl, prod_name=prod_name, msg=msg)
        difference_in_months = relativedelta(timezone.now(), record.timestamp).months
        if(difference_in_months>1):
            if(record.msg == msg):
                return "confirmed"
            else:
                return "warning"
        return "warning"
    except validationForActivityNotification.DoesNotExist:
        validationForActivityNotification.objects.create(baseUrl=baseUrl, msg=msg, prod_name=prod_name)
        return "warning"