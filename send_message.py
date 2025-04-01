from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Instagram login credentials for two accounts
accounts = [
    {"username": "python1test", "password": "python12@"},
    {"username": "python2test", "password": "python@12"}
]

# Load profile URLs from file
with open("instagram_profiles.txt", "r") as file:
    profiles_list = [line.strip() for line in file.readlines()]

def login(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    
    user_input = driver.find_element(By.NAME, "username")
    pass_input = driver.find_element(By.NAME, "password")

    user_input.send_keys(username)
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Wait for login process

    # Handle "Save Login Info" popup
    try:
        not_now_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
        )
        not_now_btn.click()
        time.sleep(2)
    except:
        pass  # If the popup doesn't appear, continue

    # Handle "Turn on Notifications" popup
    try:
        not_now_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
        )
        not_now_btn.click()
        time.sleep(2)
    except:
        pass  # If the popup doesn't appear, continue

def send_message(driver, profile_url, message="Hi"):
    driver.get(profile_url)
    time.sleep(5)
    
    try:
        wait = WebDriverWait(driver, 10)

        # Click "Message" button
        message_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Message')]")))
        message_button.click()
        time.sleep(5)  # Allow message window to fully load

        # Locate message input box (contenteditable div)
        text_area_xpath = "//div[@contenteditable='true' and @role='textbox']"
        text_area = wait.until(EC.presence_of_element_located((By.XPATH, text_area_xpath)))

        # Ensure text area is active
        text_area.click()
        time.sleep(2)

        # Send the message
        text_area.send_keys(message)
        time.sleep(2)

        # Locate and click the Send button
        send_button_xpath = "//div[@role='button' and contains(text(), 'Send')]"
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
        send_button.click()
        time.sleep(3)

        print(f"✅ Message sent to {profile_url}")

    except Exception as e:
        print(f"❌ Failed to send message to {profile_url}: {e}")
def logout(driver):
    driver.get("https://www.instagram.com/")
    time.sleep(3)
    
    try:
        profile_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Profile']"))
        )
        profile_icon.click()
        time.sleep(3)
        
        logout_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Log out']"))
        )
        logout_menu.click()
        time.sleep(5)
    except Exception as e:
        print(f"Logout failed: {e}")

def main():
    driver = webdriver.Chrome()

    for i in range(0, len(profiles_list), 10):
        account = accounts[(i // 10) % 2]  # Switch accounts every 10 messages
        login(driver, account["username"], account["password"])

        for profile in profiles_list[i:i+10]:
            send_message(driver, profile)

        logout(driver)

    driver.quit()

if __name__ == "__main__":
    main()
