import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from typing import Optional


def checker(email: str, proxy: str) -> Optional[bool]:
    seleniumwire_options = {
        'proxy': {
            'https': proxy,
        }
    }

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36")
    chrome_options.add_argument('--ignore-certificate-errors')

    driver = None
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options, seleniumwire_options=seleniumwire_options)
        driver.get("https://ru.lovense.com/signin")
        WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        driver.find_element(By.XPATH, "//span[@data-name='signup']").click()
        driver.find_element(By.XPATH, "//input[@name='email']").send_keys(email)
        driver.find_element(By.XPATH, "//span[@data-name='login']").click()
        time.sleep(1) #Для активации проверки email нужно кликнуть в другое поле
        driver.find_element(By.XPATH, "//span[@data-name='signup']").click()
        time.sleep(1)
        try:
            element = driver.find_element(By.XPATH, "//*[text()='Email уже существует']")
            if element:
                return True
            else:
                return False
        except Exception:
            return False

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if driver:
            driver.quit()


email_to_check = input('email:')
proxy_to_use = input('proxy:')
print(checker(email_to_check, proxy_to_use))