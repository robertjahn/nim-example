import os

import logging
logger = logging.getLogger(__name__)

from openai import OpenAI
from models import Model
from utils.secrets import read_secret

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

class Nim(Model):

    def __init__(self) -> None:
        super().__init__()

        nim_model = os.environ['NIM_MODEL']
        nim_embedding_model = os.environ['NIM_EMBEDDING_MODEL']
        client_base_url = os.environ['CLIENT_BASE_URL']
        langchain_embedding_base_url = os.environ['LANGCHAIN_EMBEDDING_BASE_URL']
        langchain_llm_base_url = os.environ['LANGCHAIN_LLM_BASE_URL']

        logger.info("Init Nim Model")
        logger.info("nim_model = " + nim_model)
        logger.info("nim_embedding_model = " + nim_embedding_model)
        logger.info("client_base_url = " + client_base_url)
        logger.info("langchain_embedding_base_url = " + langchain_embedding_base_url)
        logger.info("langchain_llm_base_url = " + langchain_llm_base_url)

        self.__embedding_model = nim_embedding_model
        self.__model = nim_model

        self.__client = OpenAI(
            base_url=client_base_url,
            api_key='not-used',
        )
        self.__langchain_embedding = OpenAIEmbeddings(
            base_url=langchain_embedding_base_url,
            openai_api_key='not-used',
            model=self.__embedding_model,
        )
        self.__langchain_llm = ChatOpenAI(
            base_url=langchain_llm_base_url,
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
