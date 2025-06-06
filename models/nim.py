from openai import OpenAI
from models import Model
from utils.secrets import read_secret

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings


class Nim(Model):

    def __init__(self) -> None:
        super().__init__()
        self.__embedding_model = "text-embedding-ada-002"
        self.__model = "meta/llama-3.1-8b-instruct"
        self.__client = OpenAI(
            base_url="http://104.199.9.79:8000/v1/",
            api_key='not-used',
        )
        self.__langchain_embedding = OpenAIEmbeddings(
            base_url="http://104.199.9.79:8000/v1/",
            openai_api_key='not-used',
            model=self.__embedding_model,
        )
        self.__langchain_llm = ChatOpenAI(
            base_url="http://104.199.9.79:8000/v1/",
            openai_api_key='not-used',
            model=self.__model,
        )

    def embedding(self, prompt):
        return self.__client.embeddings.create(
            input=prompt,
            model=self.__embedding_model,
            encoding_format="float",
        )

    def chat(self, prompt) -> str:
        chat_completion = self.__client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.__model,
            temperature=0.8,
            max_tokens=300,
        )
        message = ""
        if chat_completion and hasattr(chat_completion, "choices"):
            for m in chat_completion.choices:
                message += f" {m.message.content}"
        return message

    def langchain_embedding(self):
        return self.__langchain_embedding

    def langchain_llm(self):
        return self.__langchain_llm
