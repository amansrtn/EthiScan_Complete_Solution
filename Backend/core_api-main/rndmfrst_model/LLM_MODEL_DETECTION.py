from transformers import (
    AutoTokenizer,
    pipeline,
    XLNetForSequenceClassification,
)
from pathlib import Path

def llm_model_output(text):
    model_path = Path(__file__).parent.joinpath("XLNet_Fine_Tuned_Model")
    model = XLNetForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return nlp(text)[0]["label"]


print(llm_model_output("hello my name is aman"))
