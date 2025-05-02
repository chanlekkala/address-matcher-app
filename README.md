
# 🏠 AccuAddress — Smart US Address Deduplication & Validation

This project is a Streamlit web app that:
✅ Normalizes and parses U.S. addresses (including street addresses and PO Boxes)  
✅ Detects similar/duplicate addresses using fuzzy matching  
✅ Flags invalid or incomplete addresses  
✅ Handles unit/apartment/suite numbers intelligently  
✅ Provides downloadable CSV reports for all cleaned datasets

---

### 🌐 Live Demo

✅ Check out the hosted live app here:  
[https://accuaddress.streamlit.app/](https://accuaddress.streamlit.app/)

You can upload your own test files or use the provided sample data to explore its features.

---

### 🚀 Features

- Upload CSV or JSON files
- Select which column contains the address data
- Structured parsing using [`usaddress`](https://github.com/datamade/usaddress) to break addresses into components (house number, street, city, state, zip, unit)
- Intelligent fuzzy matching using [`RapidFuzz`](https://maxbachmann.github.io/RapidFuzz/) to detect near-duplicates (ignoring house numbers and units when needed)
- PO Box support using specific USPS components (`USPSBoxType`, `USPSBoxID`)
- Downloadable reports:
  - All valid addresses
  - Deduplicated addresses
  - Invalid/unparseable addresses
  - Similar address pairs

---

### 🛠 Technologies and Packages Used

- **Python** → core language
- **[Streamlit](https://streamlit.io/)** → builds the interactive web app and handles file uploads and displays
- **[pandas](https://pandas.pydata.org/)** → manages uploaded data as DataFrames for easy processing
- **[usaddress](https://github.com/datamade/usaddress)** → parses U.S. addresses into structured fields (like `AddressNumber`, `StreetName`, `PlaceName`, `USPSBoxType`), improving accuracy over raw string matching
- **[RapidFuzz](https://maxbachmann.github.io/RapidFuzz/)** → performs fast and memory-efficient fuzzy matching between address components (using token sort ratio) to detect near-duplicate addresses, even with small variations

Docker is also provided for easy containerized deployment, allowing you to run the app anywhere with a single command.

---

### 💻 How to Run

#### Option 1: Local Python

1️⃣ Clone the repo:
```bash
git clone https://github.com/yourusername/accuaddress.git
cd accuaddress
```

2️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

3️⃣ Run the app:
```bash
streamlit run app.py
```

4️⃣ Visit:
```
http://localhost:8501
```

---

#### Option 2: Streamlit Cloud

✅ Push the repo to GitHub  
✅ Go to [streamlit.io/cloud](https://streamlit.io/cloud)  
✅ Connect the repo and deploy  
✅ Share the public app link

---

#### Option 3: Docker

1️⃣ Build the image:
```bash
docker build -t accuaddress .
```

2️⃣ Run the container:
```bash
docker run -p 8501:8501 accuaddress
```

3️⃣ Access the app:
```
http://localhost:8501
```

---

### 📦 Example Test Data

We provide:
- `sample_addresses.json` → basic test cases
- `expanded_sample_addresses.json` → advanced tricky cases (e.g., PO Boxes, unit numbers, typos, formatting differences)

Upload these into the app to explore and test.

---

### ✨ Demo Features

✅ Displays only 5 rows by default (adjustable by user)  
✅ Exports CSVs for all processed datasets  
✅ Skips false duplicates across unit numbers  
✅ Now correctly validates PO Box addresses (recent fix!)  
✅ Uses structured address parsing instead of raw string comparisons

---

### 🙌 Credits

Built by [Your Name] as a proof of concept for address normalization, deduplication, and matching in data engineering and data quality workflows.
