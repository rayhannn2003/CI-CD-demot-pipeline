#!/usr/bin/env python3
"""
Automated Jenkins Screenshot Capture Script
============================================
This script captures screenshots of the successful Jenkins pipeline run.
It uses Selenium WebDriver to navigate Jenkins UI and Blue Ocean, then saves screenshots.

Requirements:
  pip install selenium webdriver-manager

Usage:
  python3 capture_jenkins_screenshots.py
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Configuration
JENKINS_URL = os.environ.get('JENKINS_URL', 'http://localhost:8080')
JENKINS_USER = os.environ.get('JENKINS_USER', 'rayhan')
JENKINS_PASS = os.environ.get('JENKINS_PASS', 'rayhan')
JOB_NAME = 'cicd-demo-pipeline'
BUILD_NUMBER = '5'  # The successful build

# Screenshot output directory
OUTPUT_DIR = 'jenkins-screenshots'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_driver():
    """Setup Chrome WebDriver with headless options"""
    chrome_options = Options()
    # Run in headless mode (no GUI)
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_to_jenkins(driver):
    """Login to Jenkins"""
    print(f"Logging in to Jenkins at {JENKINS_URL}...")
    driver.get(f'{JENKINS_URL}/login')
    time.sleep(2)
    
    try:
        # Find and fill login form
        username_field = driver.find_element(By.NAME, 'j_username')
        password_field = driver.find_element(By.NAME, 'j_password')
        
        username_field.send_keys(JENKINS_USER)
        password_field.send_keys(JENKINS_PASS)
        
        # Submit login
        submit_button = driver.find_element(By.NAME, 'Submit')
        submit_button.click()
        time.sleep(3)
        print("✅ Logged in successfully")
    except Exception as e:
        print(f"Login form not found or already logged in: {e}")

def capture_classic_pipeline_view(driver):
    """Capture the classic Jenkins pipeline view"""
    print(f"\n📸 Capturing classic pipeline view for build #{BUILD_NUMBER}...")
    url = f'{JENKINS_URL}/job/{JOB_NAME}/{BUILD_NUMBER}/'
    driver.get(url)
    time.sleep(3)
    
    screenshot_path = os.path.join(OUTPUT_DIR, f'1_classic_pipeline_build_{BUILD_NUMBER}.png')
    driver.save_screenshot(screenshot_path)
    print(f"✅ Saved: {screenshot_path}")

def capture_console_output(driver):
    """Capture the console output"""
    print(f"\n📸 Capturing console output for build #{BUILD_NUMBER}...")
    url = f'{JENKINS_URL}/job/{JOB_NAME}/{BUILD_NUMBER}/console'
    driver.get(url)
    time.sleep(2)
    
    screenshot_path = os.path.join(OUTPUT_DIR, f'2_console_output_build_{BUILD_NUMBER}.png')
    driver.save_screenshot(screenshot_path)
    print(f"✅ Saved: {screenshot_path}")

def capture_blue_ocean_pipeline(driver):
    """Capture Blue Ocean pipeline visualization"""
    print(f"\n📸 Capturing Blue Ocean pipeline view...")
    url = f'{JENKINS_URL}/blue/organizations/jenkins/{JOB_NAME}/detail/{JOB_NAME}/{BUILD_NUMBER}/pipeline'
    driver.get(url)
    time.sleep(5)  # Blue Ocean needs more time to load
    
    try:
        # Wait for pipeline graph to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'PipelineGraph'))
        )
    except Exception as e:
        print(f"Blue Ocean UI not fully loaded: {e}")
    
    screenshot_path = os.path.join(OUTPUT_DIR, f'3_blueocean_pipeline_build_{BUILD_NUMBER}.png')
    driver.save_screenshot(screenshot_path)
    print(f"✅ Saved: {screenshot_path}")

def capture_job_list(driver):
    """Capture the Jenkins job list showing our successful build"""
    print(f"\n📸 Capturing Jenkins dashboard/job list...")
    url = f'{JENKINS_URL}/'
    driver.get(url)
    time.sleep(2)
    
    screenshot_path = os.path.join(OUTPUT_DIR, f'4_jenkins_dashboard.png')
    driver.save_screenshot(screenshot_path)
    print(f"✅ Saved: {screenshot_path}")

def download_console_text(driver):
    """Download console output as text file"""
    print(f"\n📄 Downloading console text output...")
    url = f'{JENKINS_URL}/job/{JOB_NAME}/{BUILD_NUMBER}/consoleText'
    driver.get(url)
    time.sleep(1)
    
    console_text = driver.find_element(By.TAG_NAME, 'pre').text
    
    text_path = os.path.join(OUTPUT_DIR, f'console_output_build_{BUILD_NUMBER}.txt')
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(console_text)
    print(f"✅ Saved: {text_path}")

def main():
    """Main function to capture all screenshots"""
    print("=" * 60)
    print("Jenkins Pipeline Screenshot Capture Tool")
    print("=" * 60)
    
    driver = None
    try:
        driver = setup_driver()
        print(f"✅ Chrome WebDriver initialized")
        
        login_to_jenkins(driver)
        capture_classic_pipeline_view(driver)
        capture_console_output(driver)
        capture_blue_ocean_pipeline(driver)
        capture_job_list(driver)
        download_console_text(driver)
        
        print("\n" + "=" * 60)
        print("✅ All screenshots captured successfully!")
        print(f"📁 Screenshots saved to: {os.path.abspath(OUTPUT_DIR)}/")
        print("=" * 60)
        
        # List captured files
        print("\n📋 Captured files:")
        for filename in sorted(os.listdir(OUTPUT_DIR)):
            filepath = os.path.join(OUTPUT_DIR, filename)
            size_kb = os.path.getsize(filepath) / 1024
            print(f"  - {filename} ({size_kb:.1f} KB)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
            print("\n🔒 Browser closed")

if __name__ == '__main__':
    main()
