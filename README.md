# 📱 Smartphone Price Scraper
Compare real-time smartphone prices from Israelis retailers: KSP, Ivory, and BUG.

## 🚀 Features

- **Real-time Price Comparison:** Prices shown for compares are real-time data.
- **Weekly Auto-Update:** Weekly auto-update mechanism for brands and models menu.
- **Efficient Web Scraping:** Max of two HTTP requests per comparison (for each website).
- **Fast Results:** Few second for each comparison. No API and DB used.

## 🔧 **Tech Stack:**
- **Server:** Built with Flask 🌐
- **Frontend:** Enhanced with JavaScript 🚀, HTML with Jinja 🧑‍🎨, and CSS for a polished UI 🎨
- **Multiple Scraping Techniques:** Utilize various scraping techniques, including Xpaths, CSS elements, and API discovery (JSON), to expedite the data retrieval process.
- **Multithreading:** Utilizes threading for improved performance and responsiveness ⚡


## 🛠️ How to Run
`Note: Running the server may take 2-3 minutes. This process involves scraping the latest models and loading the browser on start for faster results. Please be patient.`
### 🌐 Docker 
Fast and simple: you can pull the pre-built Docker image from Docker Hub and run it on port 5000:

```bash
docker pull erikpi/web-scraper:local
docker run -p 5000:5000 erikpi/web-scraper:local
```

### 🌐 Git
### 1. Clone the Repository

```bash
git clone https://github.com/erik-pinhasov/web-scraper.git
```

### 2. Install requirements
```bash
python -m pip install --upgrade pip
cd web-scraper
pip install -r requirements.txt
```

### 3. Run the app
```bash
cd src
python -m web_app.app
```
Access the application at http://localhost:5000 in your web browser.

https://github.com/erik-pinhasov/web-scraper/assets/96497924/33527807-225a-427f-bc2d-31f753863fc1

