# chatPDF

Load a PDF file and ask questions via llama_index and GPT

## Instructions

- Install the requirements

```bash
pip install -r requirements.txt
```

- Get a GPT API key from [OpenAI](https://platform.openai.com/account/api-keys) if you don't have one already.

- Paste your API key in a file called `.env` in the root directory of the project.

```bash
OPENAI_API_KEY=<your key here>
```

- Select a file from the menu or replace the default file `file.pdf` with the PDF you want to use.

- Run the script.

```bash
python3 main.py
```

- Ask any questions about the content of the PDF.

- You can find other loaders at [Llama Hub](https://llamahub.ai/).

- Enjoy!

