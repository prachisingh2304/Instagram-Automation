from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Instagram Credentials
USERNAME = "username"
PASSWORD = "pass"
HASHTAG = "gilbil"  # Change to any hashtag

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Step 1: Open Instagram and Login
    driver.get("https://www.instagram.com/")
    time.sleep(5)

    # Find and fill login fields
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(10)  # Wait for login

    # Step 2: Navigate to Hashtag Page
    driver.get(f"https://www.instagram.com/explore/tags/{HASHTAG}/")
    time.sleep(5)

    # Step 3: Extract Post Links
    post_links = set()

    for _ in range(5):  # Scroll and get posts
        posts = driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')
        for post in posts:
            post_links.add(post.get_attribute("href"))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    print(f"Found {len(post_links)} posts!")

    # Step 4: Open Each Post and Get Profile Link
    profile_urls = set()

    for post_link in list(post_links)[:50]:  # Limit to first 40
        driver.get(post_link)
        time.sleep(5)

        try:
            profile_element = driver.find_element(By.XPATH, '//a[contains(@href, "/")]')
            profile_url = profile_element.get_attribute("href")
            profile_urls.add(profile_url)
            print(f"Extracted: {profile_url}")
        except:
            print("⚠️ Could not extract profile")

    # Step 5: Save Profile URLs to File
    with open("instagram_profiles.txt", "w") as file:
        for url in profile_urls:
            file.write(url + "\n")

    print(f"✅ Successfully saved {len(profile_urls)} profile URLs!")

finally:
    driver.quit()  # Close the browser
