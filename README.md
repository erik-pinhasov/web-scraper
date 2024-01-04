# 📱 Smartphone Price Scraper

Compare real-time smartphone prices from leading Israelis retailers: KSP, Ivory, and BUG.

## 🚀 Features

- **Real-time Price Comparison:** Prices shown for compares are real-time data.
- **Weekly Auto-Update:** Weekly auto-update mechanism for brands and models menu.
- **Efficient Web Scraping:** Max of two HTTP requests per comparison (for each website).
- **Fast Results:** Few second for each comparison. No API and DB used.

## 🔧 **Tech Stack:**
- **Server:** Built with Flask 🌐
- **Frontend:** Enhanced with JavaScript 🚀, HTML with Jinja 🧑‍🎨, and CSS for a polished UI 🎨
- **Multiple Scraping Techniques:** Utilize various scraping techniques, including XML paths, CSS elements, and API discovery (JSON), to expedite the data retrieval process.
- **Concurrency:** Utilizes threading for improved performance and responsiveness ⚡


## 🛠️ How to Run
`Note: Running the server may take 2-3 minutes. This process involves scraping the latest models and loading the browser on start for faster results. Please be patient.`
### 🌐 Docker Hub
Fast and simple: you can pull the pre-built Docker image from Docker Hub:

```bash
docker pull erikpi/web-scraper:local
docker run -p 5000:5000 erikpi/web-scraper:local
```

### 🌐 Git & Docker
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
### In case that image build failed try to restart Docker Engine
#### Windows: (as administrator)
```bash
net stop com.docker.service
net start com.docker.service
```
#### Linux:
```bash
sudo systemctl restart docker
```
Access the application at http://localhost:5000 in your web browser.

