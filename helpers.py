import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import process
import re

# Get hotel name
def extract_hotel_name(caption):
    try:
        return caption.find('span', class_='GallerySlideCaptionHedText-iqjOmM jwPuvZ').text
    except AttributeError:
        return None

# Get hotel link
def extract_primary_hotel_link(caption):
    try:
        link_element = caption.find('a', class_='external-link')
        if link_element:
            return link_element['href']
    except AttributeError:
        return None

# Abstract parts of Beautiful Soup
def extract_soup_from_response(response):
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(
            f"Error: Unable to fetch the hotel page. Status code: {response.status_code}")
        return None

# Get hotel details
def scrape_hotel_details(hotel_link):
    response = requests.get(hotel_link)
    external_link = ''
    paragraphs = []
    address = ''
    soup = extract_soup_from_response(response)

    if soup:
        address_wrapper = soup.find(
            'div', class_='VenuePageVenueAddressWrapper-ezUZcT jJGvfj')
        if address_wrapper:
            # Get address data from Conde
            address_details = address_wrapper.find(
                'div', class_='VenueAddressDetails')
            if address_details:
                address_element = address_details.find(
                    'div', class_='VenueAddress')
                country_details = address_wrapper.find(
                    'div', {'data-testid': 'VenueAddressCountry'})
                if address_element:
                    address = address_element.text.strip()
                    if country_details:
                        country = country_details.text.strip()
                        address = f"{address}, {country}"

                external_link_tag = address_details.find(
                    'a', class_='external-link')

                if external_link_tag and 'href' in external_link_tag.attrs:
                    external_link = external_link_tag['href']
                    inner_container = soup.find(
                        'div', class_='container--body-inner')
                    if inner_container:
                        paragraphs = [paragraph.get_text(separator='\n').strip(
                        ) for paragraph in inner_container.find_all('p')]

    return external_link, paragraphs, address

# Fuzzy match award name to known award categories
def categorize_awards(award_name):
    categories = ["Readers' Choice Awards", "Gold List", "Hot List"]
    match, score = process.extractOne(award_name, categories)

    if score >= 80:
        return match
    else:
        return 'Other'

# Clean data for easier parsing
def format_awards_list(awards_list):
    formatted_awards_list = []

    for award in awards_list:
        matches = re.findall(r'(\D+)(\d+)', award)
        if matches:
            award_name = matches[0][0].strip()

            # Fuzzy match award name for consistent style
            award_name = categorize_awards(award_name)

            years = [match[1] for match in matches]
            for year in years:
                formatted_awards_list.append(f"{award_name}, {year}.")

    formatted_awards_string = ' '.join(formatted_awards_list)
    return formatted_awards_string

# Get awards list
def extract_awards_list(detail_element):
    try:
        awards_text = detail_element.get_text(separator=' ').strip()
        awards_list = awards_text.strip().split('   ')
        cleaned_awards_list = [
            award for award in awards_list if '$' not in award]

        # Process data
        formatted_awards_list = format_awards_list(cleaned_awards_list)

        # Counting the number of dollar signs
        dollar_sign_count = awards_text.count('$')

        return formatted_awards_list, dollar_sign_count
    except (AttributeError, IndexError):
        return None, 0

# Get hotel description from Conde list
def extract_description(caption):
    try:
        return caption.find('div', class_='GallerySlideCaptionDekContainer-hLUdt gSWuis').find('p').text
    except AttributeError:
        return None

# Get all hotel info needed
def get_all_info(link):
    base_link = 'https://www.cntraveler.com'

    response = requests.get(link)
    soup = extract_soup_from_response(response)

    hotel_captions = soup.find_all(
        'div', class_='GallerySlideFigCaption-dOeyTg jgkmHh')

    results = []

    name = ''
    hotel_link = ''
    awards_list = ''
    dollar_sign_count = 0
    external_link = ''
    description_hotel = ''
    address = ''
    description_list = ''

    for caption in hotel_captions:
        # Extract the hotel name
        name = extract_hotel_name(caption)

        # Extract the primary hotel link
        hotel_link = extract_primary_hotel_link(caption)
        if (hotel_link):
            primary_hotel_link = base_link + extract_primary_hotel_link(caption)
        else:
            primary_hotel_link = base_link
        hotel_link = primary_hotel_link

        # Extract the detail element
        detail_element = caption.find(
            'div', class_='GallerySlideCaptionDetail-hSFZKt bPsOid')

        # Check if detail_element is not None before proceeding
        if detail_element:
            # Extract the awards list and count of dollar signs
            awards_list, dollar_sign_count = extract_awards_list(
                detail_element)
            external_link, description_hotel, address = scrape_hotel_details(
                primary_hotel_link)

        # Extract other relevant information as needed
        description_list = extract_description(caption)

        results.append([name, awards_list, dollar_sign_count, description_list, description_hotel, address, hotel_link, external_link])

    return results