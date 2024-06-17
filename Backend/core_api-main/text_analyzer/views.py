import re
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.utils import timezone
from rndmfrst_model import Model_Prediction_On_Text
from django.views.decorators.csrf import csrf_exempt
from core.models import Website, validationWithTime, validationForLowStock, validationForActivityNotification
import json

@csrf_exempt
def default(request):
    received_json_data=json.loads(request.body)

    text = received_json_data.get('text')
    webName = received_json_data.get('webName')
    baseUrl = received_json_data.get('baseUrl')
    prodName = received_json_data.get('prodName')
    isProdPage = received_json_data.get('isProdPage')
    count = received_json_data.get('count')
    if(text==None):
        
        res = {'flag': 'error', "pattern": "No text param found in request"}
        return JsonResponse(res)
    if(webName==None):
        res = {'flag': 'error', "pattern": "No webName param found in request"}
        return JsonResponse(res)
    if(baseUrl==None):
        res = {'flag': 'error', "pattern": "No baseUrl param found in request"}
        return JsonResponse(res)
    if(prodName==None):
        res = {'flag': 'error', "pattern": "No prodName param found in request"}
        return JsonResponse(res)
    if(isProdPage==None):
        res = {'flag': 'error', "pattern": "No isProdPage param found in request"}
        return JsonResponse(res)
    pattern = Model_Prediction_On_Text.Predict_Dark_Pattern_Type(text)
    #pattern = LLM_MODEL_DETECTION.llm_model_output(text)
    severity = "high"
    if (isProdPage == 'true' and "$$$$" in text):
        if(text[-1]=='$'):
            ind = 0
            length = len(text)
            for i in range(length):
                if(text[i].isdigit()):
                    ind = i
                    break
            text = text[ind: length-4]
        else:
            text = text[text.find('$')+4:]
        curr_time = convert_to_seconds(text)
        severity = validatorWithTime(baseUrl= baseUrl, prod_name= prodName, curr_time=curr_time)
        pattern = "Countdown Timer"
    if(count<100):
        if(isProdPage == 'true' and pattern == "Low-stock Message" and "left" in text.lower() and "few" not in text.lower()):
            quantity = extractNumber(text)
            severity = stockValidator(baseUrl= baseUrl, prod_name= prodName, quantity = quantity)
        elif(isProdPage == 'true' and pattern == "Activity Notification"):
            if('hours' in text.lower()):
                severity = activityNotificationValidatorHour(baseUrl=baseUrl, prod_name=prodName, msg=text)
            elif('days' in text.lower()):
                severity = activityNotificationValidatorDays(baseUrl=baseUrl, prod_name=prodName, msg=text)
            elif('weeks' in text.lower()):
                severity = activityNotificationValidatorWeeks(baseUrl=baseUrl, prod_name=prodName, msg=text)
            elif('month' in text.lower()):
                severity = activityNotificationValidatorMonths(baseUrl=baseUrl, prod_name=prodName, msg=text)
            else:
                severity = activityNotificationValidatorGeneral(baseUrl=baseUrl, prod_name=prodName, msg=text)
    if('Clean' not in pattern):
        if(severity == 'high'):
            Website.create_or_update_website(baseURL=baseUrl, webName=webName, category_names=[pattern])
        res = {"flag": "true", "pattern": pattern, "level": severity}
    else:
        res = {"flag": "false", "pattern": "clean", "level": "low"}
    return JsonResponse(res, status=200)

@csrf_exempt
def updateStock(request):
    received_json_data = json.loads(request.body)
    baseUrl = received_json_data.get('baseUrl')
    prodName = received_json_data.get('prodName')
    if(baseUrl==None):
        res = {'flag': 'error', "pattern": "No baseUrl param found in request"}
        return JsonResponse(res)
    if(prodName==None):
        res = {'flag': 'error', "pattern": "No prodName param found in request"}
        return JsonResponse(res)
    try:
        row = validationForLowStock.objects.filter(baseUrl= baseUrl, prod_name= prodName).first()
        row.quantity -= 0.5
        row.save()
        return JsonResponse({'status' : 'success'})
    except:
        return JsonResponse({'status':'success'})
    


def validatorWithTime(baseUrl, prod_name, curr_time):
    try:
        if(curr_time == 0):
            return "high"
        record = validationWithTime.objects.get(baseUrl=baseUrl, prod_name=prod_name)
        time_difference = timezone.now() - record.init_time

        if(time_difference.total_seconds() >= 604800):
            validationWithTime.objects.aupdate(shown_time=curr_time)
            return "low"

        shown_time = record.shown_time
        recorded_time_diff = abs(shown_time - curr_time)
        time_difference_seconds = time_difference.total_seconds()
        if(abs(recorded_time_diff-time_difference_seconds) <= 10):
            return "low"
        else:
            return "high"
    except validationWithTime.DoesNotExist:
        validationWithTime.objects.create(baseUrl=baseUrl, prod_name=prod_name, shown_time = curr_time)
        return "low"

def stockValidator(baseUrl, prod_name, quantity):
    try:
        record = validationForLowStock.objects.get(baseUrl=baseUrl, prod_name=prod_name)
        if(int(record.quantity)!=quantity):
            return "high"
        else:
            return "low"
    except validationForLowStock.DoesNotExist:
        validationForLowStock.objects.create(baseUrl=baseUrl, prod_name=prod_name, quantity=quantity)
        return "low"
    
def activityNotificationValidatorGeneral(baseUrl, msg, prod_name):
    try:
        record = validationForActivityNotification.objects.get(baseUrl= baseUrl, prod_name = prod_name, msg = msg)
        time_diff = timezone.now() - record.timestamp
        if(time_diff > timedelta(days=1)):
            if(record.msg == msg):
                return "high"
            else:
                return "low"
        return "low"
    except validationForActivityNotification.DoesNotExist:
        validationForActivityNotification.objects.create(baseUrl=baseUrl, msg=msg, prod_name=prod_name)
        return "low"

def activityNotificationValidatorHour(baseUrl, msg, prod_name):
    try:
        record = validationForActivityNotification.objects.get(baseUrl= baseUrl, prod_name = prod_name, msg = msg)
        time_diff = timezone.now() - record.timestamp
        if(time_diff > timedelta(hours=1)):
            if(record.msg == msg):
                return "high"
            else:
                return "low"
        return "low"
    except validationForActivityNotification.DoesNotExist:
        validationForActivityNotification.objects.create(baseUrl=baseUrl, msg=msg, prod_name=prod_name)
        return "low"

def activityNotificationValidatorDays(baseUrl, msg, prod_name):
    try:
        record = validationForActivityNotification.objects.get(baseUrl=baseUrl, prod_name=prod_name, msg=msg)
        time_diff = timezone.now() - record.timestamp
        if(time_diff > timedelta(days=1)):
            if(record.msg == msg):
                return "high"
            else:
                return "low"
        return "low"
    except validationForActivityNotification.DoesNotExist:
        validationForActivityNotification.objects.create(baseUrl=baseUrl, msg=msg, prod_name=prod_name)
        return "low"

def activityNotificationValidatorWeeks(baseUrl, msg, prod_name):
    try:
        record = validationForActivityNotification.objects.get(baseUrl=baseUrl, prod_name=prod_name, msg=msg)
        time_diff = timezone.now() - record.timestamp
        if(time_diff > timedelta(weeks=1)):
            if(record.msg == msg):
                return "high"
            else:
                return "low"
        return "low"
    except validationForActivityNotification.DoesNotExist:
        validationForActivityNotification.objects.create(baseUrl=baseUrl, msg=msg, prod_name=prod_name)
        return "low"

def activityNotificationValidatorMonths(baseUrl, msg, prod_name):
    try:
        record = validationForActivityNotification.objects.get(baseUrl=baseUrl, prod_name=prod_name, msg=msg)
        difference_in_months = relativedelta(timezone.now(), record.timestamp).months
        if(difference_in_months>1):
            if(record.msg == msg):
                return "high"
            else:
                return "low"
        return "low"
    except validationForActivityNotification.DoesNotExist:
        validationForActivityNotification.objects.create(baseUrl=baseUrl, msg=msg, prod_name=prod_name)
        return "low"

    
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

def extractNumber(input_string):
    numbers = []

    for char in input_string:
        if char.isdigit():
            numbers.append(int(char))

    result = int(''.join(map(str, numbers)))

    return result
