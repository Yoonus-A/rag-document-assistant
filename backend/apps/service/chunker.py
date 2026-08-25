from parser import extract_text_from_pdf

def recursive_chunk_text(text, chunk_size=1000, overlap=200, separators=None):
    if separators is None:
        separators = ["\n\n", "\n", ". ", " "]

    text = text.strip()
    if len(text) <= chunk_size:
        return [text] if text else []

    if not separators:
        # base case: character-level fallback
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += chunk_size - overlap
        return chunks

    sep, *rest_separators = separators
    parts = text.split(sep)

    if len(parts) == 1:
        # separator not present, try the next one
        return recursive_chunk_text(text, chunk_size, overlap, rest_separators)

    chunks = []
    current_chunk = ""

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # if a single part is itself too big, recurse into it directly
        if len(part) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            chunks.extend(
                recursive_chunk_text(part, chunk_size, overlap, rest_separators)
            )
            continue

        candidate = current_chunk + sep + part if current_chunk else part

        if len(candidate) <= chunk_size:
            current_chunk = candidate
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            if overlap > 0 and current_chunk:
                overlap_text = current_chunk[-overlap:]
                current_chunk = overlap_text + sep + part
            else:
                current_chunk = part

    if current_chunk:
        chunks.append(current_chunk.strip())

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
    chunk_size=1000,
    overlap=200
)

print("Number of pages:", len(pages))
print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}")
    print(f"Page: {chunk['page_number']}")
    print("-" * 50)
    print(chunk["text"])