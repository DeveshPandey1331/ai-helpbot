# data/clean_text.py
"""
Script to clean raw scraped text for vector store ingestion.
Usage: Run after scraping to produce cleaned_text.txt
"""
import re
import sys

RAW_PATH = "data/raw_scraped.txt"
CLEANED_PATH = "data/cleaned_text.txt"

def clean_text(text):
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Remove HTML tags if any
    text = re.sub(r'<.*?>', '', text)
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    # Remove special characters except basic punctuation
    text = re.sub(r'[^\w\s.,;:!?\-]', '', text)
    text = text.strip()
    return text

if __name__ == "__main__":
    try:
        with open(RAW_PATH, "r", encoding="utf-8") as f:
            raw = f.read()
        cleaned = clean_text(raw)
        with open(CLEANED_PATH, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"✅ Cleaned text saved to {CLEANED_PATH}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
