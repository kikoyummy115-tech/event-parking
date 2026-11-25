import sys
import hashlib

from dotenv import load_dotenv

load_dotenv()

from app import create_app

from extension import db
from app.models.rag_model import Document, DocumentChunk
from app.services.rag_service import generate_embedding


def split_text(text, chunk_size=180, overlap=30):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def ingest_document(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        content = file.read()

    content_hash = hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

    existing = Document.query.filter_by(
        content_hash=content_hash
    ).first()

    if existing:
        print("Document already exists.")
        return

    title = file_path.split("/")[-1]

    document = Document(
        title=title,
        source=file_path,
        content_hash=content_hash
    )

    db.session.add(document)

    db.session.flush()

    chunks = split_text(content)

    for index, chunk in enumerate(chunks):

        embedding = generate_embedding(chunk)

        document_chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            content=chunk,
            embedding=embedding
        )

        db.session.add(document_chunk)

    db.session.commit()

    print(f"Document: {title}")
    print(f"Chunks created: {len(chunks)}")
    print("Ingestion completed successfully.")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python ingest.py knowledge/cambodia.txt")
        sys.exit(1)

    app = create_app()

    with app.app_context():
        try:
            ingest_document(sys.argv[1])
        except Exception:
            db.session.rollback()
            raise