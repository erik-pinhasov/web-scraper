# 📱 Smartphone Price Scraper

Compare real-time smartphone prices from leading Israelis retailers: KSP, Ivory, and BUG. By seamlessly integrating Playwright and Requests, this tool provides an efficient solution for price monitoring.

## 🚀 Features

- **Real-time Price Comparison:** Instantly compare smartphone prices from KSP, Bug, and Ivory.
- **Playwright and Requests:** Utilize Playwright for interactive scraping and Requests for efficient API-based data retrieval.
- **Weekly Auto-Update:** Keep your smartphone models up-to-date with a weekly auto-update mechanism.
- **Efficient Web Scraping:** Optimize efficiency with a maximum of two HTTP requests per comparison (for each website).
- **Fast Results:** Few second for each comparison. No API and DB used.
- **Multiple Scraping Techniques:** Utilize various scraping techniques, including XML paths, CSS elements, and API discovery (JSON), to expedite the data retrieval process.

## 🔧 **Tech Stack:**
- **Server:** Built with Flask 🌐
- **Frontend:** Enhanced with JavaScript 🚀, HTML with Jinja 🧑‍🎨, and CSS for a polished UI 🎨
- **Scraping with Python:** Leveraging Python libraries and tools such as Playwright, Requests, XML paths, and CSS selectors for efficient and comprehensive web scraping 🐍

## ⚙️ Prerequisites

- [Docker](https://www.docker.com/) installed on your machine.

## 🛠️ How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/erik-pinhasov/web-scraper.git
cd web-scraper
```

### 2. Build the Docker Image
```bash
docker build -t web-scraper .
```

### 3. Run the Docker Container
```bash
docker run -p 5000:5000 web-scraper
```

Access the application at http://localhost:5000 in your web browser.

### 🌐 Docker Hub
Alternatively, you can pull the pre-built Docker image from Docker Hub:

```bash
docker pull erikpi/web-scraper:latest
docker run -p 5000:5000 erikpi/web-scraper:latest
```

Access the application at http://localhost:5000 after pulling the image.