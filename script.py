import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
driver.get("https://edurank.org/geo/ph/")

# Prepare the CSV file
csv_file = open('/Users/gabrielramos/Desktop/cs132_data_repository/universities_data.csv', mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['rank', 'university', 'city', 'field', 'branch', 'acceptance_rate', 'funding'])

# Wait for the element to be visible and click it
try:
    field_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control.input-select.input-group__field--left"))
    )
    field_input.click()
    
    # Wait for the dropdown menu to be visible
    dropdown = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dropdown-menu.select-dropdown.d-block"))
    )
    
    # Get all list items in the dropdown
    field_items = dropdown.find_elements(By.CSS_SELECTOR, "li.dropdown-item")
    
    # Extract the text from each list item and store it in the 'fields' list
    fields = [item.text for item in field_items]
    print(fields)
    
    # Click each field in the dropdown and then click the "Go" button
    for i in range(len(field_items)):
        item = field_items[i]
        field_text = item.text
        if field_text == "Overall":
            item.click()
            print(f"Selected field: {field_text}")
            
            # Click on each university link and print the rank, name, city, field, and branch
            university_links = driver.find_elements(By.CSS_SELECTOR, "div.block-cont.pt-4.mb-4 h2 a")
            for university in university_links:
                university_full_name = university.text
                rank, university_name = university_full_name.split('. ', 1)
                city_element = university.find_element(By.XPATH, "../../div[@class='uni-card__geo text-center']/a/span")
                city_name = city_element.text
                university.click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                
                # Get the acceptance rate and funding from the second section
                sections = driver.find_elements(By.XPATH, "//section[@class='block-cont mb-4']")
                if len(sections) > 1:
                    section = sections[1]
                    try:
                        acceptance_rate = section.find_element(By.XPATH, ".//dt[contains(text(), 'Acceptance rate')]/following-sibling::dd").text.replace('%', '').replace('*', '').strip()
                    except NoSuchElementException:
                        acceptance_rate = "N/A"
                    try:
                        funding = section.find_element(By.XPATH, ".//dt[contains(text(), 'Funding')]/following-sibling::dd").text
                    except NoSuchElementException:
                        funding = "N/A"

                    row = [rank, university_name, city_name, field_text, "Overall", acceptance_rate, funding]
                    csv_writer.writerow(row)
                    print(row)
                else:
                    row = [rank, university_name, city_name, field_text, "Overall", "N/A", "N/A"]
                    csv_writer.writerow(row)
                    print(row)
                driver.back()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Navigate back to the field dropdown
            field_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control.input-select.input-group__field--left"))
            )
            field_input.click()
            dropdown = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dropdown-menu.select-dropdown.d-block"))
            )
            field_items = dropdown.find_elements(By.CSS_SELECTOR, "li.dropdown-item")
            continue
        
        try:
            item.click()
            go_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Go']"))
            )
            go_button.click()
            print(f"Selected field: {field_text}")
            
            # Wait for the new page to load and then print the current URL
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print(f"Current URL: {driver.current_url}")
            
            # Skip the page if the URL does not end with 'ph/'
            if not driver.current_url.endswith('ph/'):
                driver.back()
                branch_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control.input-select.input-group__field--center"))
                )
                branch_input.click()
                branch_dropdown = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dropdown-menu.dropdown-menu-right.select-dropdown.d-block"))
                )
                branch_items = branch_dropdown.find_elements(By.CSS_SELECTOR, "li.dropdown-item")
            
                continue
            
            # Handle the branch dropdown
            branch_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control.input-select.input-group__field--center"))
            )
            branch_input.click()
            branch_dropdown = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dropdown-menu.dropdown-menu-right.select-dropdown.d-block"))
            )
            branch_items = branch_dropdown.find_elements(By.CSS_SELECTOR, "li.dropdown-item")
            for j in range(len(branch_items)):
                branch_item = branch_items[j]
                branch_text = branch_item.text
                branch_item.click()
                if branch_text != "Overall":
                    go_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[text()='Go']"))
                    )
                    go_button.click()
                print(f"Selected branch: {branch_text}")
                
                # Wait for the new page to load and then print the current URL
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                print(f"Current URL: {driver.current_url}")
                
                # Skip the page if the URL does not end with 'ph/'
                if not driver.current_url.endswith('ph/'):
                    driver.back()
                    branch_input = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control.input-select.input-group__field--center"))
                    )
                    branch_input.click()
                    branch_dropdown = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dropdown-menu.dropdown-menu-right.select-dropdown.d-block"))
                    )
                    branch_items = branch_dropdown.find_elements(By.CSS_SELECTOR, "li.dropdown-item")
                    continue
                
                # Click on each university link and print the rank, name, city, field, and branch
                university_links = driver.find_elements(By.CSS_SELECTOR, "div.block-cont.pt-4.mb-4 h2 a")
                for university in university_links:
                    university_full_name = university.text
                    rank, university_name = university_full_name.split('. ', 1)
                    city_elements = university.find_elements(By.XPATH, "../../div[@class='uni-card__geo text-center']/a/span")
                    city_name = city_elements[1].text if len(city_elements) > 1 and city_elements[1].text != "Philippines" else "N/A"
                    university.click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    
                    # Get the acceptance rate and funding from the second section
                    sections = driver.find_elements(By.XPATH, "//section[@class='block-cont mb-4']")
                    if len(sections) > 1:
                        section = sections[1]
                        try:
                            acceptance_rate = section.find_element(By.XPATH, ".//dt[contains(text(), 'Acceptance rate')]/following-sibling::dd").text.replace('%', '').replace('*', '').strip()
                        except NoSuchElementException:
                            acceptance_rate = "N/A"
                        try:
                            funding = section.find_element(By.XPATH, ".//dt[contains(text(), 'Funding')]/following-sibling::dd").text
                        except NoSuchElementException:
                            funding = "N/A"
                        row = [rank, university_name, city_name, field_text, branch_text, acceptance_rate, funding]
                        csv_writer.writerow(row)
                        print(row)
                    else:
                        row = [rank, university_name, city_name, field_text, branch_text, "N/A", "N/A"]
                        csv_writer.writerow(row)
                        print(row)
                    driver.back()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                
                # Navigate back to the field dropdown
                field_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control.input-select.input-group__field--left"))
                )
                field_input.click()
                dropdown = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dropdown-menu.select-dropdown.d-block"))
                )
                field_items = dropdown.find_elements(By.CSS_SELECTOR, "li.dropdown-item")
                for k in range(len(field_items)):
                    if field_items[k].text == field_text:
                        field_items[k].click()
                        break
                
                # Navigate back to the branch dropdown
                branch_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control.input-select.input-group__field--center"))
                )
                branch_input.click()
                branch_dropdown = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dropdown-menu.dropdown-menu-right.select-dropdown.d-block"))
                )
                branch_items = branch_dropdown.find_elements(By.CSS_SELECTOR, "li.dropdown-item")
            
            # Navigate back to the field dropdown
            driver.back()
            field_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control.input-select.input-group__field--left"))
            )
            field_input.click()
            dropdown = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.dropdown-menu.select-dropdown.d-block"))
            )
            field_items = dropdown.find_elements(By.CSS_SELECTOR, "li.dropdown-item")
        except StaleElementReferenceException:
            continue
        
except Exception as e:
    print(f"An error occurred: {e}")

# Close the driver and CSV file
driver.quit()
csv_file.close()