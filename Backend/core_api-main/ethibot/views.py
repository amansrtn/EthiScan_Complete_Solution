from django.shortcuts import render
from django.http import JsonResponse
import asyncio
import json
from rndmfrst_model.LLM_Dark_Pattern_ChatBot import ChatBotCalling

from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def Bot_Communication(request):
    try:
        received_json_data=json.loads(request.body)

        message = received_json_data.get('user_message')
        response = asyncio.run(ChatBotCalling(message))
        response = str(response).replace("\n", " ")
        response=response.replace("Based on the additional context provided, here's a refined answer to the query:","")
        
        return JsonResponse({"result":response},safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)