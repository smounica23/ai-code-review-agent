import chromadb
from config import settings

client = chromadb.PersistentClient(path=settings.chroma_persist_dir)

def chunk_markdown(text:str)-> list[str] :
    chunks = text.split("##")
    cleaned_chunks  = [chunk.strip() for chunk in chunks if chunk.strip()]
    return cleaned_chunks 

def ingest_file(filepath, collection_name) :
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_markdown(text)
    collection = client.get_or_create_collection(name=collection_name)
    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    print(f"Ingested {len(chunks)} chunks into {collection_name}")
    return


def ingest_all():

    ingest_file("rag/knowledge_base/owasp_top10.md", "security_guidelines")
    ingest_file("rag/knowledge_base/python_best_practices.md", "python_guidelines")
    ingest_file("rag/knowledge_base/java_best_practices.md", "java_guidelines")
    ingest_file("rag/knowledge_base/secure_coding_guidelines.md", "secure_coding")


if __name__ == "__main__":
    ingest_all()
