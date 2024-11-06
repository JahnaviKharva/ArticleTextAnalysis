import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from lxml import html

# Read 'input.xlsx' to get the URLs
input_file = r"C:\Blackoffer\Input.xlsx"  # Replace with your file path if needed
df = pd.read_excel(input_file)

# Directory to save extracted text files
output_dir = 'extracted_articles'
os.makedirs(output_dir, exist_ok=True)

# Function to extract article content with generalized XPath
def extract_article_text_with_general_xpath(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        tree = html.fromstring(response.content)

        # Generalized XPath for the title
        title_candidates = tree.xpath('//h1//text()')
        title = title_candidates[0].strip() if title_candidates else 'No Title Found'

        # Generalized XPath for main content area
        main_content_div = tree.xpath('//div[contains(@class, "td-post-content")]')
        if not main_content_div:
            return None, None

        main_content = main_content_div[0]
        content_list = []

        for element in main_content.iter():
            # Extract headings
            if element.tag in ['h1', 'h2', 'h3']:
                content_list.append(f"\n{element.text_content().strip()}\n")
            
            # Extract paragraphs
            elif element.tag == 'p':
                content_list.append(element.text_content().strip())
            
            # Extract links inside <div>, <a>, etc.
            elif element.tag in ['a', 'div']:
                link = element.get('href') or element.text_content().strip()
                if link.startswith('http'):
                    content_list.append(f"Link: {link}")
            
            # Extract list items
            elif element.tag == 'li':
                content_list.append(f"- {element.text_content().strip()}")

        # Join the extracted content into a single string
        article_text = '\n'.join(content_list)

        return title, article_text

    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None, None

# Loop through each URL and extract the article text
for _, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    # Extract the article title and body
    title, article_text = extract_article_text_with_general_xpath(url)
    
    if title and article_text:
        # Save the article text to a file named after URL_ID
        file_path = os.path.join(output_dir, f"{url_id}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n")
            file.write(article_text)
        print(f"Article saved to {file_path}")
    else:
        print(f"Failed to extract article from {url}")
