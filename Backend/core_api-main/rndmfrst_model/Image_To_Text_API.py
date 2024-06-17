
import base64
import os
from PIL import Image
import easyocr
from . import Hidden_Cost
from . import Model_Prediction_On_Text

temp_dir = "temp_images"
os.makedirs(temp_dir, exist_ok=True)


def image_to_text(image_path, language="en"):
    reader = easyocr.Reader([language])

    result = reader.readtext(image_path)

    text = " ".join([item[1] for item in result])
    return text

def save_and_extract_text(base64_image):
    try:
        image_data = base64.b64decode(base64_image)
        image_filename = "uploaded_image.jpg"
        image_path = os.path.join(temp_dir, image_filename)
        with open(image_path, "wb") as image_file:
            image_file.write(image_data)
            image_file.flush
        # trail my aman
        image_path = "temp_images\\uploaded_image.jpg"
        result_text = image_to_text(image_path)
        output_dark_pattern_type = Model_Prediction_On_Text.Predict_Dark_Pattern_Type(result_text)
        output_hidden_cost = Hidden_Cost.flag_hidden_cost(result_text)
        return {
            "result_dark_pattern_type": output_dark_pattern_type,
            "result_hidden_cost_flag": output_hidden_cost["flag"],
            "result_hidden_cost_type": output_hidden_cost["keyword"],
        }
    except Exception as e:
        return str(e)

