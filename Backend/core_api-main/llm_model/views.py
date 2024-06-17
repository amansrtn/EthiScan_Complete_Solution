from django.shortcuts import render
from rndmfrst_model.LLM_MODEL import LLM_MODEL_PREDICTION
import json

global mymodel
# Create your views here.
def default(request):
    mymodel = LLM_MODEL_PREDICTION()

def analyze(request):
    json_data=json.loads(request.body)
    text=json_data.get()
