from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os

os.environ["GRADIENT_ACCESS_TOKEN"] = "4qIVNL6ym9D4dBJotzfV1aIdIdhuWBeo"
os.environ["GRADIENT_WORKSPACE_ID"] = "55ae1e95-beff-4fd0-99b0-aa0d23c29729_workspace"

from llama_index.llms import GradientBaseModelLLM


def extract_text_from_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


# Function to check for privacy intrusion in terms and conditions using Laama
def check_privacy_intrusion_in_terms_and_conditions(terms_and_conditions):
    llm = GradientBaseModelLLM(
        base_model_slug="nous-hermes2",
        max_tokens=300,
    )
    result = llm.complete(
        f"Given the following terms and conditions:\n"
        + terms_and_conditions
        + "\n\nDo these terms and conditions include any privacy intrusion?"
    )
    result = str(result)
    return result

@csrf_exempt
def default(request):
    request_json = json.loads(request.body)
    link = request_json.get('link')

    website_link = (link)
    website_text = extract_text_from_website(website_link)
    if website_text:
        privacy_intrusion_result = check_privacy_intrusion_in_terms_and_conditions(
            website_text
        )
        return JsonResponse({'text': privacy_intrusion_result})
    else:
        return JsonResponse({'text': 'error'})



# Create your views here.
