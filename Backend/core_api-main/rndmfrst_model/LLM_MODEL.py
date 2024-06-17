import os
from pathlib import Path

os.environ["GRADIENT_ACCESS_TOKEN"] = "QfvDxrjOtixFcZU7ODqg91XzmEOAhOT6"
os.environ["GRADIENT_WORKSPACE_ID"] = "d5619d70-239b-4353-b0f9-99ce6f87b3df_workspace"

from gradientai import Gradient
from typing import List
import json


def load_samples_from_json(file_path: str) -> List[dict]:
    with open(file_path, "r") as file:
        data = json.load(file)
        for item in data:
            item["inputs"] = "<s>### " + item["inputs"]
        for item in data:
            item["instruction"] = "This is the instruction."
        return data  # Returning the modified data as samples


def LLM_MODEL_PREDICTION():
    with Gradient() as gradient:
        base_model = gradient.get_base_model(base_model_slug="nous-hermes2")
        new_model_adapter = base_model.create_model_adapter(name="test model 3")
        json_file_path = Path(__file__).parent.joinpath("LLM_MODEL_Dataset.json")
        samples_from_json = load_samples_from_json(json_file_path)
        if samples_from_json:
            batch_size = 100
            num_samples = int(len(samples_from_json)/10)
            for start_idx in range(0, num_samples, batch_size):
                end_idx = min(start_idx + batch_size, num_samples)
                batch_samples = [
                    {"inputs": sample["inputs"]}
                    for sample in samples_from_json[start_idx:end_idx]
                ]
                print(f"Fine-tuning batch from index {start_idx} to {end_idx}...")
                new_model_adapter.fine_tune(samples=batch_samples)
                print(
                    f"Fine-tuning batch from index {start_idx} to {end_idx} complete."
                )
            return new_model_adapter

        else:
            print("No samples loaded from the JSON file.")
