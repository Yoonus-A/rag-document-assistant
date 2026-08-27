import chromadb


class vectorStore:
    def __init__(self, persistent_dir = "chroma_db",collection_name = "my_collection"):
        self.client = chromadb.PersistentClient(path=persistent_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, chunks):
        self.collection.add(
            ids=[str(chunk["chunk_id"]) for chunk in chunks],
            documents=[chunk["text"] for chunk in chunks],
            metadatas=[{"page_number": chunk["page_number"]} for chunk in chunks],
            embeddings=[chunk["embedding"] for chunk in chunks]
        )

    def query(self, query_embedding, top_k=2):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return [
            {
                "chunk_id" : results["ids"][0][i],
                "text" : results["documents"][0][i],
                "page_number" : results["metadatas"][0][i]["page_number"],
                "distance" : results["distances"][0][i]
            }
            for i in range(len(results.id[0]))
        ]

