import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_hotel_name(caption):
    try:
        return caption.find('span', class_='GallerySlideCaptionHedText-iqjOmM jwPuvZ').text
    except AttributeError:
        return None

def extract_primary_hotel_link(caption):
    try:
        link_element = caption.find('a', class_='external-link')
        if link_element:
            return link_element['href']
    except AttributeError:
        return None

def scrape_hotel_details(hotel_link):
    response = requests.get(hotel_link)
    external_link = None
    paragraphs = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract hotel website URL
        address_wrapper = soup.find('div', class_='VenuePageVenueAddressWrapper-ezUZcT jJGvfj')
        if address_wrapper:
            address_details = address_wrapper.find('div', class_='VenueAddressDetails')
            if address_details:
                # Extracting external link
                external_link_tag = address_details.find('a', class_='external-link')
                
                if external_link_tag and 'href' in external_link_tag.attrs:
                    external_link = external_link_tag['href']

                    # Now check for the existence of the specified div and class
                    inner_container = soup.find('div', class_='container--body-inner')
                    if inner_container:
                        # Extracting all paragraphs within the specified div
                        paragraphs = [paragraph.get_text(separator='\n').strip() for paragraph in inner_container.find_all('p')]
                    else:
                        print("Container for paragraphs not found.")
                else:
                    print("External link not found.")
            else:
                print("Venue address details not found.")
        else:
            print("Venue address wrapper not found.")
    else:
        print(f"Error: Unable to fetch the hotel page. Status code: {response.status_code}")

    return external_link, paragraphs

def extract_awards_list(detail_element):
    try:
        awards_text = detail_element.get_text(separator=' ').strip()
        awards_list_start = awards_text.find('$$$ | ') + len('$$$ | ')
        cleaned_awards_list = awards_text[awards_list_start:].strip()

        # Counting the number of dollar signs
        dollar_sign_count = awards_text.count('$')

        return cleaned_awards_list, dollar_sign_count
    except (AttributeError, IndexError):
        return None, 0

def extract_description(caption):
    try:
        return caption.find('div', class_='GallerySlideCaptionDekContainer-hLUdt gSWuis').find('p').text
    except AttributeError:
        return None

def scrape_conde():
    base_url = 'https://www.cntraveler.com'

    # replace link here to scrape conde list
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