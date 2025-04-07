from datastore.qdrant_datastore import QdrantDatastore
from services.openai_utils import OpenAI
from services.graph import Agent

oai = OpenAI()
qd = QdrantDatastore(embedder=oai.get_embedding)
agent = Agent()



