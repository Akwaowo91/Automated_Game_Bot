from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# THIS IS TO KEEP CHROME OPEN AFTER PROGRAM FINISHES
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://orteil.dashnet.org/experiments/cookie/")

# cookie_documentation_link = driver.find_element(By.CSS_SELECTOR, value=".middle cookie")
# print(cookie_documentation_link.text)
# cookie_documentation_link.click()

# cookie = driver.find_element(By.XPATH, value='//*[@id="cookie"]')
cookie = driver.find_element(By.ID, value="cookie")

# store_container = driver.find_element(By.ID, value="store")
# store_items = store_container.find_elements(By.XPATH, ".//*")

# for item in store_items:
#     print(item.text)

money_element = driver.find_element(By.ID, value="money")

# Dictionary to track the number of clicks for each upgrade
upgrade_clicks = {}


# cursor_element = driver.find_element(By.ID, value="buyCursor")
# grandma_element = driver.find_element(By.ID, value="buyGrandma")

# Helper function to parse the money value
def get_money():
    money_text = money_element.text.replace(",", "")
    return int(money_text) if money_text else 0


# Helper function to find and click the most expensive affordable upgrade
def buy_most_expensive_upgrade():
    store_items = driver.find_elements(By.CSS_SELECTOR, "#store b")
    affordable_items = []

    for item in store_items:
        item_text = item.text
        if "-" in item_text:
            # Extract the cost from the item text
            cost = int(item_text.split("-")[1].strip().replace(",", ""))
            affordable_items.append((cost, item))

    # Sort items by cost in descending order
    affordable_items.sort(reverse=True, key=lambda x: x[0])

    # Get the current amount of money
    current_money = get_money()

    # Find the most expensive item that we can afford
    for cost, item in affordable_items:
        if current_money >= cost:
            item_id = item.find_element(By.XPATH, "..").get_attribute("id")
            if item_id not in upgrade_clicks:
                upgrade_clicks[item_id] = 0

            if upgrade_clicks[item_id] < 5:  # Made ever upgrade have a max click of 5
                item.click()
                upgrade_clicks[item_id] += 1
            break


# Start the timer
start_time = time.time()

while True:
    cookie.click()
    # num_cookies = int(money_element.text.replace(",", ""))  # Remove commas if present and convert to int
    # if num_cookies > 15:

    time.sleep(0.1)  # Adding a short delay to prevent overwhelming the browser with clicks

    if time.time() % 5 < 0.1:  # Check every 5 seconds
        buy_most_expensive_upgrade()

    # Check if five minute has passed
    elapsed_time = time.time() - start_time
    if elapsed_time > 900:  # Game stop after 15 minutes and outputs the cookies per-second generated during the runtime
        cookie_per_sec = driver.find_element(By.ID, value="cps")
        print(cookie_per_sec.text)
        break

driver.quit()

# print(cookie.size)

# Get upgrade item ids.
# items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
# item_ids = [item.get_attribute("id") for item in items]

# driver.quit()
