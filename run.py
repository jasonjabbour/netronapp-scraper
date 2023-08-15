from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time 


# Function to get value for a given attribute
def get_value(soup, attribute_name):
    item_name = soup.find('input', {'title': attribute_name})
    if item_name:
        value_div = item_name.find_next('div', class_='sidebar-item-value-line')
        if value_div:
            return value_div.get_text(strip=True)
    return None


def main():

    # Set up the driver
    dir_path = os.path.dirname(os.path.realpath(__file__))  
    chrome_driver_path = os.path.join(dir_path, 'chromedriver')
    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    # Open the website
    driver.get('https://netron.app/')

    # Pause the script and wait for the user to open the file and then hit Enter
    input("Please open the file on the website and then press Enter...")
    print("-" * 30) 

    # Using Selenium to find nodes that start with 'node-name'
    nodes = driver.find_elements("css selector", "[id^='node-name-']")

    for node in nodes:
        node.click()  # Simulate click
        time.sleep(.1)
        
        # Get updated page source after clicking
        html_content = driver.page_source  
        soup = BeautifulSoup(html_content, 'html.parser')

        # Convert the Selenium node to BeautifulSoup object
        node_html = node.get_attribute('outerHTML')
        node_soup = BeautifulSoup(node_html, 'html.parser')

        # Extract the content of the <text> tag within the node (e.g., '_convolution')
        layer_type = node_soup.find("g", class_="node-item-type-layer").find("text").text.strip()
        node_name = node_soup.find("g", class_="node-item-type-layer").find("title").text.strip()
        print(f"Layer Type: {layer_type}")
        print(f"Node Name: {node_name}")

        # Find all <tspan> elements within the node
        tspans = node_soup.find_all("tspan")

        for tspan in tspans:
            # If the tspan contains vector details like 〈10×4×3〉 or 〈10〉, print them out
            if "〈" in tspan.text and "〉" in tspan.text:
                descriptor = tspan.previous_sibling.string if tspan.previous_sibling else None
                print(f"{descriptor}: {tspan.text.strip()}")

        # Get sidebar element for this node
        sidebar_element = driver.find_element(By.ID, 'sidebar-content')
        sidebar_html = sidebar_element.get_attribute('outerHTML')
        sidebar_soup = BeautifulSoup(sidebar_html, 'html.parser')

        # Extract and print stride and padding values
        stride_value = get_value(sidebar_soup, 'stride')
        padding_value = get_value(sidebar_soup, 'padding')

        if stride_value:
            print(f"Stride: {stride_value}")

        if padding_value:
            print(f"Padding: {padding_value}")

        print("-" * 30)  # just to separate multiple nodes, if any

    
    driver.quit()


if __name__ == "__main__":
    main()


