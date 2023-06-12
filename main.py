import logging

logging.basicConfig(level=logging.CRITICAL)

import os
from pathlib import Path

import openai
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from llama_index import (
    GPTVectorStoreIndex,
    LLMPredictor,
    ServiceContext,
    StorageContext,
    download_loader,
    load_index_from_storage,
)
from utils import CACHE, FILES, models, cls, handle_save, handle_exit, initialize, select_file

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
history = []

llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.618, model_name=models["gpt-3"], max_tokens=256))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size_limit=1024)


def make_index(file):
    cls()
    print("👀 Loading...")

    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    documents = loader.load_data(file=Path(FILES) / file)

    if os.path.exists(Path(CACHE) / file):
        print("📚 Index found in cache")
        return
    else:
        print("📚 Index not found in cache, creating it...")
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        index.storage_context.persist(persist_dir=Path(CACHE) / file)


def chat(file_name, index):
    while True:
        prompt = input("\n😎 Prompt: ")
        if prompt == "exit":
            handle_exit()
        elif prompt == "save":
            handle_save(str(file_name), history)

        query_engine = index.as_query_engine(response_mode="compact")

        response = query_engine.query(prompt)
        print("\n👻 Response: " + str(response))
        history.append({"user": prompt, "response": str(response)})


def ask(file_name):
    try:
        print("👀 Loading...")
        storage_context = StorageContext.from_defaults(persist_dir=Path(CACHE) / file_name)
        index = load_index_from_storage(storage_context, service_context=service_context)
        cls()
        print("✅ Ready! Let's start the conversation")
        print("ℹ️ Press Ctrl+C to exit")
        chat(file_name, index)
    except KeyboardInterrupt:
        handle_exit()


if __name__ == "__main__":
    initialize()
    file = select_file()
    if file:
        file_name = Path(file).name
        make_index(file_name)
        ask(file_name)
    else:
        print("No files found")
        handle_exit()
