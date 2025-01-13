import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Optional


def checker(email: str, proxy: str) -> Optional[bool]:
    proxy_parts = proxy.split('@')
    credentials = proxy_parts[0].split(':')
    proxy_ip_port = proxy_parts[1].split(':')

    proxy_user = credentials[0]
    proxy_password = credentials[1] if len(credentials) > 1 else None
    proxy_ip = proxy_ip_port[0]
    proxy_port = proxy_ip_port[1] if len(proxy_ip_port) > 1 else None

    seleniumwire_options = {
        'proxy': {
            'http': f'http://{proxy_user}:{proxy_password}@{proxy_ip}:{proxy_port}',
        }
    }

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36")
    chrome_options.add_argument('--ignore-certificate-errors')

    driver = None
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options, seleniumwire_options=seleniumwire_options)
        driver.get("https://app.any.do")
        WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(2)

        driver.find_element(By.XPATH, "//input[@type='email']").send_keys(email)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='AppLoginTabHeader__title' and text()='Welcome Back!']"))
            )
            return True
        except TimeoutException:
            return False

    except Exception:
        return None
    finally:
        if driver:
            driver.quit()


email_to_check = input('email:')
proxy_to_use = input('proxy:')
result = checker(email_to_check, proxy_to_use)
print(result)
