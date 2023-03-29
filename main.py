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

    while True:
        prompt = input("[Prompt]: ")
        response = index.query(prompt)
        print("[Response]: " + response)


if __name__ == "__main__":
    ask("file.pdf")
