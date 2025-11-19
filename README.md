#  Real-Time News Sentiment Analysis Dashboard  
### Dockerized Streamlit App using Google RSS + VADER

This project provides a real-time dashboard that analyzes global news sentiment using **Google News RSS feeds** and **VADER Sentiment Analyzer**.  
The entire application is containerized using **Docker**, making it easy to run on any system with zero setup.

---

##  Features

### 🔹 Real-Time News Fetching  
- Pulls live headlines using **Google News RSS** (no API key required)

### 🔹 Sentiment Analysis  
- Uses **VADER Sentiment Analyzer**  
- Classifies sentiment into:
  - Positive  
  - Negative  
  - Neutral  
- Extracts sentiment score (`prob_pos`)

### 🔹 Interactive Streamlit Dashboard  
- Latest headlines table  
- Sentiment distribution bar chart  
- Positive sentiment trend line  
- Auto updates and saves results as Parquet files

### 🔹 100% Containerized with Docker  
- No local setup needed  
- Packaged with all dependencies  
- Runs identically on any machine

---

##  Run With Docker (Recommended)

 
1️⃣ Pull the Docker image
bash
docker pull sreyak07/news-sentiment-app:latest
2️⃣ Run the container
bash
Copy code
docker run -p 8501:8501 sreyak07/news-sentiment-app:latest
3️⃣ Open the app in your browser
arduino
Copy code
http://localhost:8501
📁 Project Structure
bash
Copy code
news-app/
│── real_time_news_sentiment.py   # Main Streamlit app
│── requirements.txt              # Python dependencies
│── Dockerfile                    # Docker build file
│── predictions_parquet/          # Auto-saved sentiment results
└── README.md                     # Project documentation
 Technologies Used
Python 3.10

Streamlit

VADER Sentiment Analysis

Feedparser (RSS)

Pandas

Plotly

Docker

 How It Works
Fetches news from Google News RSS

Parses titles + publish dates

Runs VADER sentiment analysis

Saves results as Parquet

Visualizes sentiment trends + counts

Streams everything via Streamlit UI

 Build Docker Image (Optional)
If you want to build the image yourself:

bash
Copy code
docker build -t news-sentiment-app .
docker run -p 8501:8501 news-sentiment-app
 Author
Sreya K
Real-Time Sentiment Analysis Project
Fully Dockerized Streamlit App

