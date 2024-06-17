from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rndmfrst_model.Subscription_Tricky_LLM import SubscriptionTricky
import json

@csrf_exempt
def default(request):
    recieved_json = json.loads(request.body)
    buttons = recieved_json.get('buttons')


    buttons_str = "["

    for button in buttons:
        buttons_str += (button+", ")
    
    buttons_str = buttons_str.replace("\n", " ")
    buttons_str = buttons_str.replace("\t", " ")
    buttons_str = buttons_str[:len(buttons_str)-2]
    buttons_str = buttons_str[:1000]
    buttons_str+="]"
    key = SubscriptionTricky(buttons_str)
    print("$$$$", key)
    key = str(key)
    res = ""
    for c in key:
        if c.lower() in "abcdefghijklmnopqrstuvwxyz&_-,; ":
            res+=c
    
    found = "false"
    if("cancel" in key):
        found = "true"
    
    return JsonResponse({"found": found, "step": res})

