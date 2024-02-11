import requests
from bs4 import BeautifulSoup
import pandas as pd
from helpers import extract_hotel_name, extract_primary_hotel_link, scrape_hotel_details, extract_awards_list, extract_description

def scrape_conde():
    base_url = 'https://www.cntraveler.com'

    # Conde link to scrape
    url = 'https://www.cntraveler.com/gallery/best-hotels-in-los-angeles'

    response = requests.get(url)

    data = {'Hotel Name': [], 'Awards': [], 'Price Point': [], 'Description (List)': [], 'Description (Hotel)': [], 'Hotel Website URL': []}

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')    

        hotel_captions = soup.find_all('div', class_='GallerySlideFigCaption-dOeyTg jgkmHh')

        for caption in hotel_captions:
            # Extract the hotel name
            hotel_name = extract_hotel_name(caption)
            print(hotel_name)
            data['Hotel Name'].append(hotel_name)

            # Extract the primary hotel link
            primary_hotel_link = base_url + extract_primary_hotel_link(caption)

            # Extract the detail element
            detail_element = caption.find('div', class_='GallerySlideCaptionDetail-hSFZKt bPsOid')

            # Check if detail_element is not None before proceeding
            if detail_element:
                # Extract the awards list and count of dollar signs
                awards_list, dollar_sign_count = extract_awards_list(detail_element)
                data['Awards'].append(awards_list)
                data['Price Point'].append(dollar_sign_count)
                external_link, paragraphs = scrape_hotel_details(primary_hotel_link)
                data['Hotel Website URL'].append(external_link)
                data['Description (Hotel)'].append('\n'.join(paragraphs))

            else:
                print("Incomplete information: No detail element found.")
                data['Awards'].append(None)
                data['Price Point'].append(None)
                data['Hotel Website URL'].append(None)
                data['Description (Hotel)'].append(None)

            # Extract other relevant information as needed
            description = extract_description(caption)
            data['Description (List)'].append(description)        
            
    else:
        print(f"Error: Unable to fetch the page. Status code: {response.status_code}")

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Save DataFrame to an Excel file
    df.to_excel('hotel_data.xlsx', index=False)

if __name__ == "__main__":
    scrape_conde()