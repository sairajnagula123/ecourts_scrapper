# 🏛️ eCourts Scraper Internship Task

This project automates the process of fetching court listings and cause lists from the official [eCourts Portal](https://services.ecourts.gov.in/ecourtindia_v6/).

The main goal is to demonstrate **web automation and data extraction** using Python and Selenium by:
- Searching court cases by **CNR number**
- Downloading the **daily cause list** for any district court as a PDF file

---

## 🚀 Features

✅ **Search Case by CNR**  
- Opens the eCourts portal  
- Inputs the given CNR number  
- Detects if the page requires CAPTCHA (for manual entry)

✅ **Download District Cause List (Main Task)**  
- Opens the District Courts section  
- Captures and saves the entire page as a PDF file  
- Stores the output inside the `outputs/` folder  

✅ **Automatic File Saving**  
- Saves results to:
  - `outputs/results.json` (CNR case search results)
  - `outputs/<district>_cause_list.pdf` (Cause list PDF)

---

## 🧱 Project Structure
ecourts_scraper/
├─ main.py # Entry point - handles CLI input
├─ scraper.py # Core Selenium automation logic
├─ requirements.txt # Required Python packages
├─ README.md # Project documentation
└─ outputs/ # Saved results (JSON / PDF)
