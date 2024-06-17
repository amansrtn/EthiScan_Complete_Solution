def llm_model_prediction(text, mymodel):
    completion_after = mymodel.complete(
        query=text + "\n\n### assistant:", max_generated_token_count=100
    ).generated_output

    print(f"Generated (after fine-tune): {completion_after}")
    return completion_after
