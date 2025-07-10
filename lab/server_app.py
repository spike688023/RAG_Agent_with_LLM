# https://python.langchain.com/docs/langserve#server
from fastapi import FastAPI
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from langserve import add_routes

## May be useful later
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.runnables import RunnableLambda, RunnableBranch, RunnablePassthrough
from langchain_core.runnables.passthrough import RunnableAssign
from langchain_community.document_transformers import LongContextReorder
from functools import partial
from operator import itemgetter

from langchain_community.vectorstores import FAISS
import os

# 初始化向量資料庫 (假設已 embedding 過，否則需先 embedding)
## For demonstration, build simple vectorstore here

os.environ["NVIDIA_API_KEY"] = "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"

## TODO: Make sure to pick your LLM and do your prompt engineering as necessary for the final assessment
embedder = NVIDIAEmbeddings(model="nvidia/nv-embed-v1", truncate="END")
instruct_llm = ChatNVIDIA(model="meta/llama3-8b-instruct", api_key=os.environ["NVIDIA_API_KEY"])

#!tar xzvf docstore_index.tgz
docstore = FAISS.load_local("docstore_index", embedder, allow_dangerous_deserialization=True)
retriever = docstore.as_retriever()


## 定義 prompt
generator_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert AI assistant. Answer the question using only the provided context."),
    ("user", "CONTEXT:\n{context}\n\nQUESTION:\n{input}\n\nAnswer concisely and accurately.")
])

## 定義 generator chain
generator_chain = (
    generator_prompt
    | instruct_llm  # 你已在 server_app.py 定義 ChatNVIDIA
    | StrOutputParser()
)

app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple api server using Langchain's Runnable interfaces",
)

## PRE-ASSESSMENT: Run as-is and see the basic chain in action

add_routes(
    app,
    instruct_llm,
    path="/basic_chat",
)

## ASSESSMENT TODO: Implement these components as appropriate

add_routes(
    app,
    generator_chain,
    path="/generator",
)

add_routes(
    app,
    retriever,
    path="/retriever",
)

## Might be encountered if this were for a standalone python file...
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9012)
