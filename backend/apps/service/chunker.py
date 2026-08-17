from parser import extract_text_from_pdf

def recursive_chunk_text(text, chunk_size=1000, overlap=200):
    if len(text) <= chunk_size:
        return [text.strip()]

    separators = ["\n\n", "\n", ". ", " "]

    for sep in separators:
        parts = text.split(sep)

        if len(parts) == 1:
            continue

        chunks = []
        current_chunk = ""

        for part in parts:
            part = part.strip()

            if not part:
                continue

            candidate = (
                current_chunk + sep + part
                if current_chunk else part
            )

            if len(candidate) <= chunk_size:

                current_chunk = candidate

            else:
                # Save the current chunk
                if current_chunk:
                    chunks.append(current_chunk.strip())
                # Start the next chunk with overlap
                if overlap > 0 and current_chunk:
                    overlap_text = current_chunk[-overlap:]
                    current_chunk = overlap_text + sep + part
                else:
                    current_chunk = part

        if current_chunk:
            chunks.append(current_chunk.strip())

        if chunks:
            return chunks

    # if none of the separators worked, split by character count
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(
            text[start:end].strip()
        )
        start += chunk_size - overlap

    return chunks


def chunk_pages(pages, chunk_size, overlap):
    chunks = []
    for page in pages:
        page_chunks = recursive_chunk_text(
            page["text"],
            chunk_size,
            overlap
        )

        for chunk in page_chunks:
            chunks.append({
                "text": chunk,
                "page_number": page["page_number"]
            })

    return chunks





pages = extract_text_from_pdf("docs/football_rules.docx")

chunks = chunk_pages(
    pages,
    chunk_size=600,
    overlap=100
)

for i, chunk in enumerate(chunks[:5]):
    print(f"\nChunk {i + 1}")
    print(f"Page: {chunk['page_number']}")
    print("-" * 50)
    print(chunk["text"])