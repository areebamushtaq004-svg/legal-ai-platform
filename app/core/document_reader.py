import pypdf
import docx
import io

def extract_text(filename, content):
    if filename.endswith(".pdf"):
        reader = pypdf.PdfReader(io.BytesIO(content))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        return "\n".join([para.text for para in doc.paragraphs])
    elif filename.endswith(".txt"):
        return content.decode("utf-8")
    else:
        return "Unsupported file format"