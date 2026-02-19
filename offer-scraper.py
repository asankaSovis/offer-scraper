"""
Offer Scraper
This module scrapes card offers from the Bank website, extracts offer details,
validates the data, and stores it in JSON format for later retrieval and analysis.
The scraper navigates through different card offer categories, extracts information
such as vendor names, savings amounts, phone numbers, expiration dates, and images,
then validates the extracted data for consistency across multiple category pages.
Args:
    -f : Delete existing JSON backup file and perform a fresh scrape
    -v [vendor_name] : Search and display offers for a specific vendor (case-insensitive)
    -c [category_name] : Search and display all offers in a specific category (case-insensitive)
    {For -v and -c, [vendor_name] and [category_name] can be left blank to list all}
    -i : Prints about and license information
Example:
    offer-scraper.py -v
    offer-scraper.py -v "cinnamon"
    offer-scraper.py -c "dining"
    offer-scraper.py -f
    offer-scraper.py -i
Attributes:
    url (str): The main URL of Bank card offers page
    offers (dict): Nested dictionary storing all vendor offers organized by vendor and saving type
    subcategories (dict): Dictionary mapping category names to their respective URLs
    found_vendors (list): List of all unique vendors found during scraping
    root (str): Root URL of the Bank website used for constructing relative links
Functions:
    extract_items: Extracts items from parameters
    extract_content: Parses HTML and extracts offer details from card offer elements
    extract_url: Extracts category URLs from the main offers page
    scrape: Performs HTTP GET request and returns HTML content
    print_vendor: Displays all offers for a specific vendor
    print_category: Displays all offers in a specific category
    load_params: Load parameters
    information: Prints information and about
@author © Asanka Sovis
@date 2026/02/19
@version 1.1
@note Requires internet connection for web scraping. Uses BeautifulSoup for HTML parsing. For educational purposes only.
"""

import os
import requests
import json
import datetime
from bs4 import BeautifulSoup
import sys

VERSION = "1.1"
COPYRIGHT = "2026"
AUTHOR = "Asanka Sovis (asankasovis.com)"
DATE = "19-02-2026"
LICENSE = "MIT"
PROJ = "github.com/asankaSovis/offer-scraper"
SUPPORTED_VERSIONS = ["1.0", "1.1"]

#The URL to be scraped
url = ""

root = ""
offers = {}
subcategories = {}
found_vendors = []
parameters = {}
param_list = ['subcategories', 'view_offer_details', 'img_items', 'offer_img', 'card', 'until', 'phone', 'saving', 'vendor', 'items', 'root_is_content', 'subitems_text', 'subitems_link']

def extract_items(item, cls, type="class", root="div", navi_str="false", no=3):
    if (type == "class"):
        if navi_str == "true":
            return [list(item.find(root, class_=cls).stripped_strings)[no]]
        else:
            return item.find_all(root, class_=cls)
    elif(type == "title"):
        if navi_str == "true":
            
            return [list(item.find(root, title=cls).stripped_strings)[no]]
        else:
            return item.find_all(root, title=cls)
    else:
        return []

def extract_content(response, category, found_items, ret=False):
    content = {}
    local_found_items = []
    # 4. Parse the HTML content
    soup = BeautifulSoup(response, 'html.parser')
    
    #items = soup.find_all("div", class_="cardOfferItem swiper-slide cardofferslide")
    items = extract_items(soup, parameters[param_list[9]][0], parameters[param_list[9]][1], parameters[param_list[9]][2], parameters[param_list[9]][3])
    
    for item in items:
        #vendor = item.find_all("p", class_=parameters[param_list[8]][0])
        vendor = extract_items(item, parameters[param_list[8]][0], parameters[param_list[8]][1], parameters[param_list[8]][2], parameters[param_list[8]][3])
        if len(vendor) > 0:
            if isinstance(vendor[0], str):
                vendor = vendor[0]
            else:
                vendor = vendor[0].text.strip()
        else:
            vendor = "None"

        #saving = item.find_all("h5", class_=parameters[param_list[7]][0])
        saving = extract_items(item, parameters[param_list[7]][0], parameters[param_list[7]][1], parameters[param_list[7]][2], parameters[param_list[7]][3])
        if len(saving) > 0:
            if isinstance(saving[0], str):
                saving = saving[0]
            else:
                saving = saving[0].text.strip()
        else:
            saving = "None"

        #phone_number = list(item.find("div", class_=parameters[param_list[6]][0]).stripped_strings)[3]
        phone_number = extract_items(item, parameters[param_list[6]][0], parameters[param_list[6]][1], parameters[param_list[6]][2], parameters[param_list[6]][3])
        if len(phone_number) > 0:
            if isinstance(phone_number[0], str):
                phone_number = phone_number[0]
            else:
                phone_number = phone_number[0].text.strip()
        else:
            phone_number = ""

        #until = item.find_all("p", class_=parameters[param_list[5]][0])
        until = extract_items(item, parameters[param_list[5]][0], parameters[param_list[5]][1], parameters[param_list[5]][2], parameters[param_list[5]][3])
        if len(until) > 0:
            if isinstance(until[0], str):
                until = until[0]
            else:
                until = until[0].text.strip()
        else:
            until = ""

        #card = item.find_all("p", class_=parameters[param_list[4]][0])
        card = extract_items(item, parameters[param_list[4]][0], parameters[param_list[4]][1], parameters[param_list[4]][2], parameters[param_list[4]][3])
        if len(card) > 0:
            if isinstance(card[0], str):
                card = card[0]
            else:
                card = card[0].text.strip()
        else:
            card = "None"

        offer_img = ""
        vendor_img = ""

        #img_items = item.find_all("img", class_=parameters[param_list[3]][0])
        img_items = extract_items(item, parameters[param_list[3]][0], parameters[param_list[3]][1], parameters[param_list[3]][2], parameters[param_list[3]][3])
        if len(img_items) > 0:
            if img_items[0].has_attr('src'):
                offer_img = img_items[0]['src']

        #img_items = item.find_all("img", class_=parameters[param_list[2]][0])
        img_items = extract_items(item, parameters[param_list[2]][0], parameters[param_list[2]][1], parameters[param_list[2]][2], parameters[param_list[2]][3])
        if len(img_items) > 0:
            if img_items[0].has_attr('src'):
                vendor_img = img_items[0]['src']
            
        #link = item.find_all("a", title=parameters[param_list[1]][0])
        link = extract_items(item, parameters[param_list[1]][0], parameters[param_list[1]][1], parameters[param_list[1]][2], parameters[param_list[1]][3])
        if len(link) > 0:
            if link[0].has_attr('href'):
                link = root + link[0]['href']
            else:
                link = link[0].find("a")
                if link.has_attr('href'):
                    a = link['href'].split("/")
                    link = root + a[len(a) - 2] + "/" + a[len(a) - 1]

        if ret:
            try:
                if not(vendor in content):
                    content[vendor] = {}

                content[vendor][saving] = {
                    'name': vendor,
                    'saving': saving,
                    'phone': phone_number,
                    'until': until,
                    'card': card,
                    'offer_img': offer_img,
                    'vendor_img': vendor_img,
                    'link':link,
                    'category': [category]
                }
            except:
                print("Error: " + vendor)

            if local_found_items.count(vendor) == 0:
                local_found_items.append(vendor)
        else:
            try:
                if not(vendor in offers):
                    offers[vendor] = {}

                if saving in offers[vendor]:
                    if (offers[vendor][saving]['name'] != vendor):
                        print(f"Vendor '{vendor}', offer '{saving}' found multiple times. Vendor names don't match. Original: '{offers[vendor][saving]['name']}' | New: '{vendor}'")
                    if (offers[vendor][saving]['saving'] != saving):
                        print(f"Vendor '{vendor}', offer '{saving}' found multiple times. Offers don't match. Original: '{offers[vendor][saving]['saving']}' | New: '{saving}'")
                    if (offers[vendor][saving]['phone'] != phone_number):
                        print(f"Vendor '{vendor}', offer '{saving}' found multiple times. Phone numbers don't match. Original: '{offers[vendor][saving]['phone']}' | New: '{phone_number}'")
                    if (offers[vendor][saving]['until'] != until):
                        print(f"Vendor '{vendor}', offer '{saving}' found multiple times. Expire dates don't match. Original: '{offers[vendor][saving]['until']}' | New: '{until}'")

                    if category != "None":
                        offers[vendor][saving]['category'].append(category)

                else:
                    offers[vendor][saving] = {
                        'name': vendor,
                        'saving': saving,
                        'phone': phone_number,
                        'until': until,
                        'card': card,
                        'offer_img': offer_img,
                        'vendor_img': vendor_img,
                        'link': link,
                        'category': [category]
                    }

            except:
                print("Error: " + vendor)

            if found_items.count(vendor) == 0:
                found_items.append(vendor)

    return content

def extract_url(response):
    soup = BeautifulSoup(response, 'html.parser')

    #items = soup.find_all("a", class_=parameters[param_list[0]][0])
    items = extract_items(soup, parameters[param_list[0]][0], parameters[param_list[0]][1], parameters[param_list[0]][2], parameters[param_list[0]][3])

    for item in items:
        if item.has_attr('href'):
            if 'www' in item['href']:
                link_url = item['href']
                subcategories[item.text.strip()] = link_url
            else:
                link_url = root + item['href']
                subcategories[item.text.strip()] = link_url
        else:
            subitems_text = extract_items(item, parameters[param_list[11]][0], parameters[param_list[11]][1], parameters[param_list[11]][2], parameters[param_list[11]][3])
            #print(subitems_text[0].text.strip())
            subitems_url = extract_items(item, parameters[param_list[12]][0], parameters[param_list[12]][1], parameters[param_list[12]][2], parameters[param_list[12]][3])
            #print(subitems_url[0].text.strip())
            #exit()
            if subitems_url[0].has_attr('href'):
                if 'www' in subitems_url[0]['href']:
                    link_url = subitems_url[0]['href']
                    subcategories[subitems_text[0].text.strip()] = link_url
                else:
                    link_url = root + subitems_url[0]['href']
                    subcategories[subitems_text[0].text.strip()] = link_url
    
    return subcategories

def scrape(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        print(f"ERROR: Failed to retrieve the page! Status code: {response.status_code}")
        return ""

def print_vendor(vendor):
    print(vendor + " :")

    for item in offers[vendor].keys():
        print("     " + item + " :")
        for category in offers[vendor][item].keys():
            if isinstance(offers[vendor][item][category], str):
                print("         " + category + " : " + offers[vendor][item][category])

        print()

def print_category(str):
    print(str + " :")
    for vendor in offers.keys():
        for item in offers[vendor].keys():
            if 'category' in offers[vendor][item]:
                if (offers[vendor][item]['category'].count(str) > 0):
                    print("     " + vendor + " : " + item)

def load_params():
    global parameters
    global url

    if os.path.exists("parameters.json"):
        try:
            # Load the JSON file from backup
            with open("parameters.json", "r") as file:
                parameters = json.load(file)

                if ('version' in parameters.keys()):
                    if not (parameters['version'] in SUPPORTED_VERSIONS):
                        print("ERROR: Incorrect version of JSON!")
                        exit(1)
                else:
                    print("ERROR: Could not validate the version string for JSON!")
                    exit(1)

                if ('url' in parameters.keys()):
                    url = parameters['url']
                else:
                    print("ERROR: Could not find URL in JSON!")
                    exit(1)

                for param in param_list:
                    if param not in parameters.keys():
                        print(f"ERROR: Could not find '{param}' in JSON!")
                        exit(1)

            #print("JSON file loaded successfully.")
        except:
            print("ERROR: Failed to read JSON file!")
            exit(1)
    else:
        print("ERROR: 'parameters.json' file does not exist!")
        exit(1)

def information():
    print("A Python-based web scraper that extracts credit card offer information from bank websites, parses the data, and stores it in structured JSON format for analysis and retrieval.")
    print("")
    print("     -f : Delete existing JSON backup file and perform a fresh scrape")
    print("     -v [vendor_name] : Search and display offers for a specific vendor (case-insensitive)")
    print("     -c [category_name] : Search and display all offers in a specific category (case-insensitive)")
    print("         {For -v and -c, [vendor_name] and [category_name] can be left blank to list all}")
    print("     -i : Prints about and license information")
    print("")
    print(f"This program is licensed unde the {LICENSE} license:")
    print("")
    try:
        with open("LICENSE", "r") as file:
            print(file.read())
    except:
        print("???")
    print("")
    print(f"Find more info and support, visit: {PROJ}")
    print("")

if (__name__ == "__main__"):
    load_params()

    print(f"-- OFFER SCRAPER v{VERSION} ----------------------------------------------")
    print("")
    print(f"    - Copyright {COPYRIGHT}, {AUTHOR}")
    print(f"    - Release: {DATE}")
    print("    - Today: " + datetime.datetime.now().isoformat(sep=' ', timespec='seconds'))
    print("    - URL: " + url)
    print()

    #exit(0)

    find_str = ""
    find_type = 0
    if ('root' in parameters):
        root = parameters['root']
    else:
        root = url.split('/')[0] + "//" + url.split('/')[2]
    
    filename = "./offers/offers_" + str(datetime.datetime.now().month) + "_" + str(datetime.datetime.now().year) + ".json"

    if len(sys.argv) > 1:
        if sys.argv[1] == '-f':
            # Delete the JSON file if it exists
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    print(f"Deleted '{filename}'...")
                except:
                    print(f"ERROR: Failed to detete '{filename}'!")

                    exit(0)
        elif sys.argv[1] == '-v':
            if len(sys.argv) > 2:
                find_str = sys.argv[2]
            find_type = 0
        elif sys.argv[1] == '-c':
            if len(sys.argv) > 2:
                find_str = sys.argv[2]
            find_type = 1
        elif sys.argv[1] == '-i':
            information()
            exit(0)

    if not os.path.exists("./offers"):
        try:
            os.makedirs("./offers")
        except:
            print("ERROR: Could not create 'offers' directory!")
            exit(1)

    if not(os.path.exists(filename)):
        print(f"Scraping '{root}' for categories...")
        response = scrape(url)

        if (response != ""):
            subcategories = {}

            subcategories.update(extract_url(response))
            if (parameters[param_list[10]] == "true"):
                subcategories["None"] = url

            print(f"Categories: {str(len(subcategories))}")

            print("Extracting offers...")

            for item in subcategories.keys():
                response = scrape(subcategories[item])
                if (response != ""):
                    extract_content(response, item, found_vendors)
                else:
                    print("ERROR: Failed to extract offers! Network error.")
                    exit(1)

            print(f"Offers: {str(len(offers))}")

            print("Re-validating...")

            issues = 0

            for category in subcategories.keys():
                response = scrape(subcategories[category])
                if (response != ""):
                    subcontent = extract_content(response, category, found_vendors, True)
                    for vendor in subcontent.keys():
                        if not(vendor in offers.keys()):
                            print(f"ERROR: Vendor {vendor} is not in offers!")
                            issues += 1
                        else:
                            for subitem in subcontent[vendor].keys():
                                if not(subitem in offers[vendor].keys()):
                                    print(f"Offer {subitem} of vendor {vendor} not in offers!")
                                    issues += 1
                else:
                    print("ERROR: Failed to validate offers! Network error.")
                    issues = -1

            if (issues == 0):
                print("Validation complete. No issues found.")
            elif (issues == -1):
                print("ERROR: Problem in validation!")
            else:
                print(f"Validation complete. Issues found: {str(issues)}!")

            print("Dumping to JSON...")

            json_dump = {
                'title': 'Bank Card Offers',
                'version': VERSION,
                'month': datetime.datetime.now().month,
                'year': datetime.datetime.now().year,
                'date': datetime.datetime.now().isoformat(sep=' ', timespec='seconds'),
                'vendors': found_vendors,
                'categories': subcategories
            }

            json_dump['offers'] = offers

            try:
                with open(filename, "w") as file:
                    json.dump(json_dump, file, indent=4)

                print("Dumping complete.")

            except:
                print("ERROR: Failed to write to JSON!")
                exit(1)
    else:
        print("JSON backup exist. Reading...")

        try:
            # Load the JSON file from backup
            with open(filename, "r") as file:
                json_dump = json.load(file)

                if ('version' in json_dump.keys()):
                    if (json_dump['version'] != VERSION):
                        print("ERROR: Unsupported JSON!")
                        exit(1)
                else:
                    print("ERROR: Could not validate the version of the JSON!")
                    exit(1)

                if ('offers' in json_dump.keys()):
                    offers = json_dump['offers']
                else:
                    print("ERROR: Could not find offers in JSON!")

                    exit(1)

                if ('vendors' in json_dump.keys()):
                    found_vendors = json_dump['vendors']
                else:
                    print("ERROR: Could not find vendors in JSON!")

                    exit(1)

                if ('categories' in json_dump.keys()):
                    subcategories = json_dump['categories']
                else:
                    print("ERROR: Could not find categories in JSON!")

                    exit(1)

            print("JSON file loaded successfully.")
        except:
            print("ERROR: Failed to read JSON file!")

            exit(1)

    while(True):
        print()

        search = []

        if (find_type == 0):
            for item in found_vendors:
                # Check if the substring is in the target string (case-insensitive)
                if find_str.lower() in item.lower():
                    search.append(item)

        elif (find_type == 1):
            for item in subcategories.keys():
                # Check if the substring is in the target string (case-insensitive)
                if find_str.lower() in item.lower():
                    search.append(item)

        if len(search) > 0:
            if len(search) > 1:
                count = 0

                for item in search:
                    print(str(count) + ": " + item)
                    count += 1

                print("\nEnter number to see contents: ")
                user_input = input()

                if user_input.isdigit():
                    find_str = search[int(user_input)]
                    continue
            else:
                if find_type == 0:
                    print_vendor(search[0])
                elif find_type == 1:
                    print_category(search[0])
        else:
            print(f"ERROR: No items found for search term '{find_str}'!")

        break

    exit(0)