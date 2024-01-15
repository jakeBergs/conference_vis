from selenium import webdriver
from selenium.webdriver.common.by import By
import psycopg2

# Replace with your database connection details
conn = psycopg2.connect(
    dbname="cfb_conferences",
    port="5432"
)
cursor = conn.cursor()

for year in range(2002, 2019):
# year = 2020

# Replace 'path_to_chromedriver' with the actual path to your ChromeDriver executable
    driver = webdriver.Chrome()
    cursor = conn.cursor()

    # Navigate to a webpage
    driver.get('https://www.sports-reference.com/cfb/conferences/sec/' + str(year) +'.html')

    # Get and print the page title
    page_title = driver.title
    print("Page Title:", page_title)

    elements = driver.find_elements(by=By.XPATH, value='//*[contains(@id, "standings")]//*[contains(@data-stat, "school_name")]//a')

    print(len(elements))
    for element in elements:
        school = element.text
        school_id_query = "SELECT id FROM school WHERE '" + school + "' = ANY(aliases);"
        cursor.execute(school_id_query)
        school_id = cursor.fetchone()[0]
        print(element.text)
        print(school_id)
        aff_query = "INSERT INTO affiliation (school_id, conference_id, year) VALUES (" + str(school_id) + ", 1, " + str(year) + ");"
        print(aff_query)
        cursor.execute(aff_query)
        # print(parent)

    conn.commit()
    cursor.close()
    # Close the browser
    driver.quit()


conn.close()
