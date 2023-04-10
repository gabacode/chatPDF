import os
import sys
from pathlib import Path

import openai
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from llama_index import GPTSimpleVectorIndex, LLMPredictor, ServiceContext, download_loader

from utils import CACHE, initialize, select_file

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def handle_exit():
    print("\nGoodbye!\n")
    sys.exit(1)


def ask(file):
    print("👀 Loading...")

    llm_predictor = LLMPredictor(
        llm=ChatOpenAI(temperature=0.618, model_name="gpt-3.5-turbo", max_tokens=256, streaming=True)
    )
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size_limit=1024)
    # Check if file is in cache
    cache_file = os.path.join(CACHE, f"{Path(file).stem}.json")
    if os.path.exists(cache_file):
        index = GPTSimpleVectorIndex.load_from_disk(cache_file)
    else:
        PDFReader = download_loader("PDFReader")
        loader = PDFReader()
        documents = loader.load_data(file=Path(file))

        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        index.save_to_disk(cache_file)

    # clear the screen
    os.system("clear")

    print("✅ Ready! Let's start the conversation")
    print("ℹ️ Press Ctrl+C to exit")

    try:
        while True:
            prompt = input("\n😎 Prompt: ")
            if prompt == "exit":
                handle_exit()
            response = index.query(prompt)
            print("\n👻 Response: " + str(response))
    except KeyboardInterrupt:
        handle_exit()


if __name__ == "__main__":
    initialize()
    file = select_file()
    if file:
        ask(file)
    else:
        print("No files found")
        handle_exit()
