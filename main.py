print("👀 Loading...")

# suppress imports output
import logging
logging.basicConfig(level=logging.CRITICAL)

# loading libraries
import os
from pathlib import Path
from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, download_loader
import openai

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

def ask(file):
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    documents = loader.load_data(file=Path(file))

    index = GPTSimpleVectorIndex.from_documents(documents)

    # clear the screen
    os.system("clear")

    print("✅ Ready! Let's start the conversation")
    print("ℹ️ Press Ctrl+C to exit")

    while True:
        prompt = input("\n😎 Prompt: ")
        response = index.query(prompt)
        print()

        # transform response to string
        response = str(response)

        # if response starts with "\n", remove it
        if response.startswith("\n"):
            response = response[1:]

        print("👻 Response: " + str(response))


if __name__ == "__main__":
    ask("file.pdf")