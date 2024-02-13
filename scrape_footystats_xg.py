from selenium import webdriver
from selenium.webdriver.common.by import By
import time

###
import undetected_chromedriver as uc


driver = uc.Chrome()
driver.get('https://nowsecure.nl')  # my own test test site with max anti-bot protection
# ###
url = 'https://footystats.org/ecuador/cd-cuenca-vs-cs-emelec-h2h-stats#5231377'

options = webdriver.ChromeOptions()
# options = webdriver.FirefoxOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--disable-extensions')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

driver.execute_script(f"window.open('{url}', '_blank')")
time.sleep(15)
driver.switch_to.window(driver.window_handles[1])

driver.switch_to.frame(0)

# row = driver.find_element(
#     By.XPATH,
#     '//*[@id="h2h_content2"]/section[1]/div[2]/div[2]/table/tbody/tr[7]'
# )

row = driver.find_element(By.XPATH, '//*[@id="h2h_content2"]')


