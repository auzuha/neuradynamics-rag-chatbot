import pdfplumber
from io import BytesIO

from services.services import qd

CHUNK_SIZE = 1000



def read_pdf_with_pdfplumber(file_bytes: bytes) -> str:
    text = ""
    file_bytes = BytesIO(file_bytes)

    with pdfplumber.open(file_bytes) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def upload_to_qdrant(file):
    try:
        text = read_pdf_with_pdfplumber(file)
        chunks = get_chunks_for_text(text)
        qd.insert_multiple_chunks(chunks)
        return True, 'Successfully uploaded file to Qdrant.'
    except Exception as e: 
        print(e)
        return False, 'Could not upload file to Qdrant'
def get_chunks_for_text(text):
    chunks = []
    for i in range(0,len(text),CHUNK_SIZE):
        chunks.append(text[i:i+CHUNK_SIZE])
    
    return chunks