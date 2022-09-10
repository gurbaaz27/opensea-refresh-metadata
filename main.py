import sys
import logging
import logging.config
from time import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

NFT_COLLECTION_URL = "https://opensea.io/collection/donutshop"
BASE_URL = "https://opensea.io/assets/ethereum/0xca20f7279f7defd14e7524e609704ea2f436a539/"
BUTTON_XPATH = '//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[2]/section[1]/div[1]/div[2]/div/button[1]'
# BUTTON_XPATH = (
#     '//*[@id="main"]/div/div/div/div[2]/div/section[1]/div[1]/div[2]/div/button[1]'
# )

logging.config.fileConfig("./logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def main():
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(
            options=options,
            service=Service(ChromeDriverManager().install()),
        )
        driver.maximize_window()

        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        driver.get(NFT_COLLECTION_URL)
        driver.save_screenshot("images/main.png")

        # collection = driver.find_elements(By.CLASS_NAME, "Asset--anchor")
        # urls = []
        # for entry in collection:
        #     urls.append(entry.get_attribute("href"))
        # print(len(urls))

        tic = time()

        for i in range(5432):
            try:
                driver.get(BASE_URL + str(i))

                button = driver.find_element(By.XPATH, BUTTON_XPATH)
                button.click()

                driver.save_screenshot(f"images/{i}.png")

                logger.info(f"Donut {i} refreshed")

            except:
                logger.error("uncaught exception: %s", traceback.format_exc())

        driver.quit()

        toc = time()

        logger.info(f"Refreshing completes in {(toc - tic) / 60} minutes")

        return 0

    except Exception:
        traceback.print_exc()

        return -1


if __name__ == "__main__":
    sys.exit(main())
