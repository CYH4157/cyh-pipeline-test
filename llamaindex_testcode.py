from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
documents = SimpleDirectoryReader("data").load_data()
print(f'documents:{documents}')
# bge-base embedding model
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text", base_url="http://172.17.0.1:11434")

# ollama
Settings.llm = Ollama(model="llama3", base_url="http://172.17.0.1:11434", request_timeout=360.0)

print(f'======== VectorStoreIndex ==========')
index = VectorStoreIndex.from_documents(
    documents,
    show_progress=True
)


query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)
