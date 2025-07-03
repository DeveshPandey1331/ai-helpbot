
# AI Help Bot for Knowledge Retrieval

## Project Structure

- `backend/`
  - `app.py` — FastAPI backend serving the chatbot API, loads vector store.
  - `generate_vector_store.py` — Generates vector store from cleaned text.
- `scraper/`
  - `mosdac_scraper.py` — Scrapes MOSDAC website, saves raw text.
- `data/`
  - `raw_scraped.txt` — Raw scraped data from MOSDAC.
  - `cleaned_text.txt` — Cleaned text for vector store.
  - `clean_text.py` — Script to clean raw text.
- `frontend/`
  - `index.html`, `script.js`, `style.css` — Chat UI.
- `requirements.txt` — Python dependencies.

## Data Pipeline

1. **Scrape Data**
   - Run: `python scraper/mosdac_scraper.py`
   - Output: `data/raw_scraped.txt`
2. **Clean Data**
   - Run: `python data/clean_text.py`
   - Output: `data/cleaned_text.txt`
3. **Generate Vector Store**
   - Run: `python backend/generate_vector_store.py`
   - Output: `backend/vector_store.pkl`
4. **Start Backend**
   - Run: `uvicorn backend.app:app --reload`
5. **Open Frontend**
   - Open `frontend/index.html` in browser.

## Notes
- Ensure `.env` contains your OpenAI API key: `OPENAI_API_KEY=...`
- All file paths are now consistent and robust.
- For new data, repeat steps 1–3.

## Troubleshooting
- If you see file not found errors, check that all data steps are run in order.
- For API errors, check `.env` and OpenAI API key.
  
## TO RUN 
-python -m uvicorn backend.app:app --reload     in our terminal
-then open html code in browser by going live in bottom right corner

For further help, see comments in each script or ask for code samples for any step.

# ai-helpbot

