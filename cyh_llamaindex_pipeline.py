"""
title: Llama Index Ollama Pipeline
author: open-webui
date: 2024-09-09
version: 1.0
license: MIT
description: A pipeline for retrieving relevant information from a knowledge base using the Llama Index library with Ollama embeddings.

"""

from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
import os

from pydantic import BaseModel


class Pipeline:

    class Valves(BaseModel):
        LLAMAINDEX_OLLAMA_BASE_URL: str
        LLAMAINDEX_MODEL_NAME: str
        LLAMAINDEX_EMBEDDING_MODEL_NAME: str

    def __init__(self):
        self.documents = None
        self.index = None
        
        self.id = "cyh_lamaindex_pipe"
        self.name = "cyh_lamaindex_pipe"
        
        self.valves = self.Valves(
            **{
                "LLAMAINDEX_OLLAMA_BASE_URL": os.getenv("LLAMAINDEX_OLLAMA_BASE_URL", "http://172.17.0.1:11434"),
                "LLAMAINDEX_MODEL_NAME": os.getenv("LLAMAINDEX_MODEL_NAME", "llama3"),
                "LLAMAINDEX_EMBEDDING_MODEL_NAME": os.getenv("LLAMAINDEX_EMBEDDING_MODEL_NAME", "chatfire/bge-m3:q8_0"),
            }
        )

    async def on_startup(self):
        from llama_index.embeddings.ollama import OllamaEmbedding
        from llama_index.llms.ollama import Ollama
        from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader

        Settings.embed_model = OllamaEmbedding(
            model_name=self.valves.LLAMAINDEX_EMBEDDING_MODEL_NAME,
            base_url=self.valves.LLAMAINDEX_OLLAMA_BASE_URL,
        )
        Settings.llm = Ollama(
            model=self.valves.LLAMAINDEX_MODEL_NAME,
            base_url=self.valves.LLAMAINDEX_OLLAMA_BASE_URL,
        )
        print('=============  ollama setting finished =============')
        # This function is called when the server is started.
        global documents, index

        print('=============  SimpleDirectoryReader =============')
        # self.documents = SimpleDirectoryReader("/app/data", required_exts=[".pdf", ".docx"]).load_data()
        try:
            self.documents = SimpleDirectoryReader("/app/data", required_exts=[".pdf", ".docx"]).load_data()
        except Exception as e:
            print(f"Failed to load data: {e}")

        
        print('=============  VectorStoreIndex =============')
        self.index = VectorStoreIndex.from_documents(self.documents)
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom RAG pipeline.
        # Typically, you would retrieve relevant information from your knowledge base and synthesize it to generate a response.
        print('=============  index.as_query_engine =============')
        print(messages)
        print(user_message)
        
        query_engine = self.index.as_query_engine(streaming=True)
        response = query_engine.query(user_message)

        return response.response_gen
