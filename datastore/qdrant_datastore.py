from qdrant_client import QdrantClient

from qdrant_client.models import VectorParams, Distance

import numpy as np
from qdrant_client.models import PointStruct



import uuid



class QdrantDatastore():

    def __init__(self, embedder, collection_name = 'documents'):

        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = collection_name
        self.embedder = embedder


        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

    def insert(self, text):
        vector = self.embedder(text)
        self.client.upsert(
        collection_name=self.collection_name,
        points=[
            PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={"text": text}
            )
        ]
        )

    def insert_multiple_chunks(self, chunks):
        for idx, chunk in enumerate(chunks):
            vector = self.embedder(chunk)
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={"text": chunk}
                    )       
                ]
            )
    def search(self, text):
        query_vector = self.embedder(text)
        hits = self.client.search(
        collection_name=self.collection_name,
        query_vector=query_vector,
        limit=5  # Return 5 closest points
        )
        return hits

    def delete_collection(self):
        self.client.delete_collection(collection_name=self.collection_name)



