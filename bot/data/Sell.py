import selenium
from selenium import webdriver

driver = webdriver.Chrome()  # or webdriver.Firefox(), etc., depending on your browser and driver
driver.get("http://www.python.org")
assert "Python" in driver.title
driver.quit()
