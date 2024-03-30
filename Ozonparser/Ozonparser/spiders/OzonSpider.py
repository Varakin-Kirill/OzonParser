import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions
import scrapy
class OzonSpider(scrapy.Spider):
    name = "Ozon"
    def start_requests(self):
        s=Service(executable_path="C:\\Users\\kiril\\.vscode\\ProjectTemplates\\Real_Example\\chromedriver.exe")
        options = ChromeOptions()
        driver = uc.Chrome(services=s, options=options)
        wait=WebDriverWait(driver, 20)
        driver.implicitly_wait(5)
        driver.get("https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?sorting=rating")
        count=0
        counter_page=0
        try:
            while count <100:
                counter_page+=1
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layoutPage"]//a[text()='+str(counter_page)+']')))
                next_page=driver.find_element(By.XPATH,'//*[@id="layoutPage"]//a[text()='+str(counter_page)+']').get_attribute("href")
                driver.get(next_page)
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)  
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break  
                    last_height = new_height
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#paginatorContent')))
                phones=driver.find_element(By.CSS_SELECTOR,'div#paginatorContent').find_elements(By.CSS_SELECTOR,'span.tsBody400Small')
                i=0
                for phone in phones:
                    i=i+1
                    text=phone.text
                    if "Смартфон" in text:
                        if count<100:
                            href=phone.find_element(By.XPATH,'//*[@id="paginatorContent"]/div/div/div['+str(i)+']/div[2]/div/a').get_attribute("href")
                            count=count + 1
                            yield  scrapy.Request(href,  callback=self.parse)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
    def parse(self, response):
        result = response.xpath('//div[matches(text(), "^IOS.*") or matches(text(), "^Android.*")]').get()
        yield {
            'version' : result
        }


