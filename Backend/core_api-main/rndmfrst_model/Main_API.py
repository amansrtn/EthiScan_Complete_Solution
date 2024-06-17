import asyncio
from flask import Flask, request, jsonify
import base64
import os
from PIL import Image
from flask_cors import CORS
import easyocr
from APP_NAME_FINDER import appdetector
from Disguised_UI import find_Disguised_UI
from Hidden_Cost import flag_hidden_cost
from LLM_Dark_Pattern_ChatBot import ChatBotCalling
from LLM_MODEL import LLM_MODEL_PREDICTION
from LLM_Prediction import llm_model_prediction
from Model_Prediction_On_Text import Predict_Dark_Pattern_Type
from Review_Checker import review_checker

app = Flask(__name__)
CORS(app)
temp_dir = "temp_images"
os.makedirs(temp_dir, exist_ok=True)
global mymodel


def image_to_text(image_path, language="en"):
    reader = easyocr.Reader([language])
    result = reader.readtext(image_path)
    text = " ".join([item[1] for item in result])
    return text


@app.route("/", methods=["POST"])
def save_and_extract_text():
    try:
        base64_image = request.json.get("base64_image")
        image_data = base64.b64decode(base64_image)
        image_filename = "uploaded_image.jpg"
        image_path = os.path.join(temp_dir, image_filename)
        with open(image_path, "wb") as image_file:
            image_file.write(image_data)
            image_file.close
            image_file.flush
        # trail my aman
        image_path = "temp_images\\uploaded_image.jpg"
        app_name = appdetector("temp_images\\uploaded_image.jpg")
        result_text = image_to_text(image_path)
        output_dark_pattern_type = Predict_Dark_Pattern_Type(result_text)

        llm_model_data = llm_model_prediction("get 20% off", mymodel)

        output_hidden_cost = flag_hidden_cost(result_text)
        disguised_ui = find_Disguised_UI(result_text)
        review_check = review_checker([result_text])
        return {
            "result_dark_pattern_type": output_dark_pattern_type,
            "result_hidden_cost_flag": output_hidden_cost["flag"],
            "result_hidden_cost_type": output_hidden_cost["keyword"],
            "Disguised_flag": disguised_ui["Disguised_flag"],
            "Disguised_max_word": disguised_ui["max_word"],
            "Disguised_max_count": disguised_ui["max_count"],
            "Fake_Review": review_check,
            "App_Name": app_name,
            "Unique": True,
        }
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/EthiBot", methods=["POST"])
def Bot_Communication():
    try:
        message = str(request.json.get("user_message"))
        response = asyncio.run(ChatBotCalling(message))
        response = response.replace("\n", " ")
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def get_data():
    return jsonify({"result": "Welcome to The World Of EthiScan."})


if __name__ == "__main__":
    mymodel = LLM_MODEL_PREDICTION()
    app.run(debug=False, port=80)
