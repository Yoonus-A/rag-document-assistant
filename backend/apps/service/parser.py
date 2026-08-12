import pymupdf

file_path = "docs/Yoonus Ahmed CV.pdf"


def extract_text_from_pdf(file_path):
    doc = pymupdf.open(file_path)

    pages = []

    for page_number, page in enumerate(doc):
        text = page.get_text()

        pages.append({
            "page_number": page_number + 1,
            "text": text
        })

    doc.close()

    return pages


extracted_text = extract_text_from_pdf(file_path)
for page in extracted_text:
    print(f"--- Page {page['page_number']} ---")
    print(page["text"])