import os
import nltk
import nltk.downloader
from pyresparser import ResumeParser
nltk.download('stopwords')
nltk.download('words')


def parse_resume(resume_path):
    return ResumeParser(resume_path)


def parse_resume_file(file_path: str):
    """
    Parse a resume given a file path.
    """
    return ResumeParser(file_path).get_extracted_data()


def parse_resume_file_upload(file_bytes: bytes, filename: str = "uploaded_resume.pdf"):
    """
    Save uploaded file bytes temporarily, parse it, then delete the file.
    """
    temp_path = f"temp_{filename}"
    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    try:
        parsed_data = ResumeParser(temp_path).get_extracted_data()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return parsed_data


def parse_resume_text(text: str):
    """
    Parse resume plain text (fallback if no file).
    Very basic - can improve later.
    """
    return {
        "skills": [],
        "experience": [],
        "raw_text": text
    }
