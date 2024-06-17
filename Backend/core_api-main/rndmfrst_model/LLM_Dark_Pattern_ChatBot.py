import os
from pathlib import Path
import asyncio

os.environ["GRADIENT_ACCESS_TOKEN"] = "QfvDxrjOtixFcZU7ODqg91XzmEOAhOT6"
os.environ["GRADIENT_WORKSPACE_ID"] = "d5619d70-239b-4353-b0f9-99ce6f87b3df_workspace"

from llama_index.llms import GradientBaseModelLLM
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.embeddings import GradientEmbedding


async def ChatBotCalling(message):
    llm = GradientBaseModelLLM(
        base_model_slug="llama2-7b-chat",
        max_tokens=150,
    )
    paths= Path(__file__).parent.joinpath("data\\")
    documents = SimpleDirectoryReader(paths).load_data()
    embed_model = GradientEmbedding(
        gradient_access_token=os.environ["GRADIENT_ACCESS_TOKEN"],
        gradient_workspace_id=os.environ["GRADIENT_WORKSPACE_ID"],
        # gradient_access_token= "QfvDxrjOtixFcZU7ODqg91XzmEOAhOT6",
        # gradient_workspace_id="d5619d70-239b-4353-b0f9-99ce6f87b3df_workspace",
        gradient_model_slug="bge-large",
    )
    service_context = ServiceContext.from_defaults(
        chunk_size=1024, llm=llm, embed_model=embed_model
    )
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(message)
    print(response)
    return response
