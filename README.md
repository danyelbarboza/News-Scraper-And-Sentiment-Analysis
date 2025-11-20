# News Scraper, Sentiment Analysis & Topic Classification

## Description

A robust web scraping tool developed in Python designed to monitor, collect, and analyze news from major Brazilian portals. Beyond simple extraction, this system leverages AI models to perform Sentiment Analysis and Zero-Shot Topic Classification (Main Labels and Sublabels). It features a memory-efficient data pipeline that saves records in batches to a MySQL database.

## Supported Portals

1. **G1** - General News
2. **Exame** - Economics and Business
3. **CartaCapital** - Politics and Analysis
4. **MoneyTimes** - Financial Markets and Investments
5. **Suno** - Personal Finance and Investing

## Key Features

### Automated Extraction
- Extracts titles, links, publication dates, and full article content.
- Supports pagination and time-based filtering (e.g., Last hour, Today, Last 7 days, Last 30 days).
- **Duplicate Check:** Verifies existing URLs/Titles in the database before processing to avoid redundancy.

### AI-Powered Topic Classification (New!)
- **Zero-Shot Classification:** Uses the `facebook/bart-large-mnli` model to categorize news without specific training data.
- **Hierarchical Labeling:**
    - **Main Labels:** Classifies news into 13 major categories (e.g., *Politics, Economy, Technology, Health, Crime, Sports*).
    - **Second Labels:** Identifies the second most probable category to provide broader context (e.g., a news item about tax reform might be classified primarily as *Politics* but secondarily as *Economy*).
    - **Sublabels:** Automatically assigns a specific sub-context based on the main label (e.g., *Politics* -> *Elections, Legislation, Diplomacy*; *Economy* -> *Inflation, Markets, Jobs*).
  
### Sentiment Analysis
- Analyzes the sentiment of the article body (Positive, Neutral, Negative).
- Uses the `cardiffnlp/twitter-xlm-roberta-base-sentiment` model for high accuracy on multilingual text.
- Returns both the sentiment label and a confidence score.

### Robust Data Pipeline (Batch Saving)
- **Batch Processing:** Instead of saving all data at the end (risk of data loss) or one by one (slow), the system processes and saves news in **batches of 10**.
- **Memory Efficiency:** Clears processed data from memory after every successful database commit.
- **Error Handling:** If a specific news item fails, the pipeline logs the error and continues to the next item without crashing the entire scraping session.

## Technical Requirements

### Main Dependencies
- **Python 3.8+**
- **Web Scraping:** `requests`, `beautifulsoup4`, `cloudscraper` (for anti-bot protection), `fake-useragent`.
- **Database:** `pymysql`.
- **AI & ML:** `transformers`, `torch` (PyTorch).
- **Utils:** `python-dotenv` (environment variables).

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/news-scraper-classifier.git](https://github.com/your-username/news-scraper-classifier.git)
   ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: This will install PyTorch and Transformers, which may require significant disk space).*

## Configuration

Create a `.env` file in the root directory to configure your MySQL database connection:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=news_database
```

## Usage

1. **Run the Main Script**:

    ```bash
    python src/main.py
    ```

2.  **Interactive Menu**: Follow the terminal prompts to select the portal and the time period.

    ```plaintext
    Bem-vindo ao Keyword Monitor!

    Você deseja analisar qual desses portais?
    1 - G1
    2 - Exame
    3 - Carta Capital
    4 - Money Times
    5 - Suno
    ...
    ```

3.  **Process**: The system will scrape, classify, analyze, and save data in real-time batches.

## Database Structure

The data is stored with the following schema, including the new classification fields:

| Column | Type | Description |
| :--- | :--- | :--- |
| `title` | VARCHAR | Article title |
| `link` | VARCHAR | URL to the full article |
| `scraping_date` | DATETIME | When the script ran |
| `news_date` | DATETIME | When the article was published |
| `article` | TEXT | Full content of the news |
| `sentiment_analysis` | VARCHAR | *Positive, Negative, Neutral* |
| `score_sentiment` | FLOAT | Confidence score (0.0 - 1.0) |
| `main_label` | VARCHAR | e.g., *Politics, Economy* |
| `score_main_label` | FLOAT | Confidence score for main label |
| `second_label` | VARCHAR | The second most likely category |
| `second_score` | FLOAT | Confidence score for second label |
| `sublabel` | VARCHAR | e.g., *Inflation, Elections* |
| `score_sublabel` | FLOAT | Confidence score for sublabel |


## Project Structure

```
news-scraper-classifier/
├── .gitignore
├── README.md
├── requirements.txt
└── src/
    ├── main.py                 # Entry point
    ├── dto/                    # Data Transfer Objects (Scrapers)
    │   ├── g1_scraper.py
    │   ├── exame_scraper.py
    │   ├── carta_scraper.py
    │   ├── moneytimes_scraper.py
    │   └── suno_scraper.py
    └── service/                # Business Logic
        ├── run_scrapers.py     # Orchestrator (Batch logic here)
        ├── save_database.py    # Database connection & operations
        ├── sentiment_analysis.py # Sentiment AI Wrapper
        ├── classifier_model.py   # Categorization AI Wrapper (BART)
        └── user_input.py       # CLI Menu
```