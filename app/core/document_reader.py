import pypdf
import docx
import io

def extract_text(filename, content):
    if filename.endswith(".pdf"):
        reader = pypdf.PdfReader(io.BytesIO(content))
        text = "git reset"
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return "Unsupported file format"