import os
import spacy
import PyPDF2
import importlib.util

# ✅ Check if spaCy model is installed; if not, download it (Streamlit compatible)
model_name = "en_core_web_sm"
if importlib.util.find_spec(model_name) is None:
    from spacy.cli import download
    download(model_name)

nlp = spacy.load(model_name)

def extract_text_from_pdf(pdf_path):
    """Extract raw text from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text

def parse_resume(pdf_path):
    """Parse resume and return raw text."""
    return extract_text_from_pdf(pdf_path)

def extract_entities(text):
    """Extract basic named entities using spaCy (optional feature)."""
    doc = nlp(text)
    entities = {
        "PERSON": [],
        "ORG": [],
        "GPE": [],
    }
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities
