from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

browser = webdriver.Chrome()

urls = ["http://trialserver.rf.gd/trial6/www.classcentral.com/index.html","https://class-central.vercel.app/www.classcentral.com/index.html","https://classcentral-scrape-hindi.vercel.app/","https://graceful-sunburst-78f35d.netlify.app/www.classcentral.com/index.html"]


def language_percente(url):
    
    try:
        request = requests.get(url)

        
        if(request.status_code == 200):

            soup = BeautifulSoup(request.content, "html.parser")

            text = soup.get_text()

            count = 0

            for char in text:
                if ord(char) >= 0x0900 and ord(char) <= 0x097F:
                    count += 1
                    
            percentage = count / len(text) * 100
            
            print(f"{url} Hindi language percentage of the web page: {percentage:.2f}")
             
        else:
            print("Could not connect to website...")
    except:
        print("Something went wrong...")

def image_test(url):
        
    browser.get(url)
    
    images = browser.find_elements(By.TAG_NAME, 'img')
    image_urls = [image.get_attribute("src") for image in images]

    # Her resmin çözünürlüğünü kontrol et
    for url in image_urls:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            high_image = 0
            low_image = 0
            try:
                img = Image.open(BytesIO(response.content))
                width, height = img.size
                if width >= 1920 and height >= 1080:
                    high_image += 1
                else:
                    low_image += 1
                img.close()

            except:
                print(f"{url} is not a valid image file.")
        else:
            print(f"{url} could not be downloaded.")
    
    if(high_image > low_image):
        print("Image High Resoulation")
    else:
        print("Image Not High Resoulation")

def guidance_test(url):
    
    browser.get(url)
    
    excepted_url = url
    
    if(browser.current_url == excepted_url):
        print("You are on the right web page")
    else:
        print("You are not on the right web page")

def dropdown_test(url):
    browser.get(url)
    dropdown = WebDriverWait(browser, 2).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-name="LARGE_UP_MAIN_NAV_TRIGGER"]')))
    
    actions = ActionChains(browser)
    actions.move_to_element(browser).click().perform()

    if dropdown.is_displayed():
        print("Dropdown opened.")
    else:
        print("Dropdown didn't open.")
    
    

# Test 
test_count = 1
for i in urls:
    print(f"Test Count {test_count}")
    language_percente(i)
    image_test(i)
    guidance_test(i)
    
    #dropdown_test(i) I tried it for the first link and it worked, but I didn't choose to make it a comment line because I couldn't test for other links.
    
    test_count += 1
    
image_test(urls[0])

guidance_test(urls[0])
