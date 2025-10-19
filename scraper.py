# scraper.py
import time
import json
import base64
from datetime import date, timedelta
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(headless=False):
    """Create Selenium Chrome driver."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def search_case_by_cnr(cnr: str):
    """Try to search by CNR (note: blocked by captcha)."""
    print(f"🔍 Starting search for CNR: {cnr}")
    driver = create_driver(headless=False)
    result = {}

    try:
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")
        wait = WebDriverWait(driver, 20)

        cnr_input = wait.until(EC.presence_of_element_located((By.ID, "cino")))
        cnr_input.clear()
        cnr_input.send_keys(cnr)
        print("✅ CNR entered successfully.")

        driver.find_element(By.ID, "searchbtn").click()
        print("🔎 Search button clicked.")

        # Wait and read the whole body (likely shows captcha)
        time.sleep(3)
        page_text = driver.find_element(By.TAG_NAME, "body").text

        if "Captcha" in page_text or "captcha" in page_text:
            print("⚠️ eCourts site requires CAPTCHA — cannot auto-scrape case data.")
            result["note"] = "Manual captcha entry required"
        else:
            result["raw_text"] = page_text

        result["cnr"] = cnr
        result["status"] = "Not listed (Captcha page reached)"

        Path("outputs").mkdir(exist_ok=True)
        with open("outputs/results.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print("💾 Results saved: outputs/results.json")

    except Exception as e:
        print(f"❌ Error while searching CNR: {e}")
    finally:
        driver.quit()

    return result


def download_cause_list(district_name: str):
    """Download today's cause list for any district."""
    print(f"📥 Downloading cause list for: {district_name}")
    driver = create_driver(headless=False)
    Path("outputs").mkdir(exist_ok=True)
    pdf_path = Path(f"outputs/{district_name}_cause_list.pdf")

    try:
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")
        wait = WebDriverWait(driver, 20)

        print("🌐 Opening 'District Courts' section...")
        dc_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "District Courts")))
        dc_link.click()
        time.sleep(4)

        print("✅ Page opened. You can now manually choose the state/district if needed...")

        time.sleep(3)
        print("📄 Saving this page as PDF...")
        pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
        pdf_bytes = base64.b64decode(pdf_data["data"])

        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        print(f"✅ Cause list page saved: {pdf_path}")

    except Exception as e:
        print(f"❌ Error while downloading cause list: {e}")

    finally:
        driver.quit()
