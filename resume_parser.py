import spacy
import PyPDF2
import os

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Extract raw text from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_entities(text):
    """Extract named entities using spaCy (for future use)."""
    doc = nlp(text)
    entities = {
        "PERSON": [],
        "ORG": [],
        "GPE": [],
        "SKILLS": []  # We'll fill this manually or with keyword matching
    }
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities

def parse_resume(pdf_path):
    """Parse resume and return raw text."""
    text = extract_text_from_pdf(pdf_path)
    return text
