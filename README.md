# 🤑 Offer Scraper

![Poster](./.imgs/Poster.png)

---

*💸 Please consider [donating](https://www.paypal.com/donate/?hosted_button_id=4EWXTWQ9FUFLA) on Paypal to keep this project alive.*

A Python-based web scraper that extracts credit card offer information from bank websites, parses the data, and stores it in structured JSON format for analysis and retrieval.

## 🤑 Overview

This project scrapes card offers from multiple bank websites (currently supporting NDB and DFCC banks), extracting key information such as:
- Vendor/merchant names
- Discount/savings amounts
- Contact phone numbers
- Offer expiration dates
- Offer images and descriptions
- Card categories and types

The scraper is designed to handle different website structures through configurable parameters, allowing it to adapt to different bank offer page layouts.

## 🤑 Features

- **Multi-bank Support**: Extensible architecture supports scraping from different bank websites
- **Flexible Configuration**: Uses JSON configuration files to define CSS selectors for different banks
- **Data Validation**: Validates extracted data for consistency across multiple category pages
- **Organized Storage**: Stores offers organized by vendor name and saving type
- **Command-line Interface**: Multiple search and filtering options via command-line arguments
- **Date-based Output**: Automatically organizes output files by month and year

## 🤑 License
> Offer Scraper is licensed under the **MIT License**.

This program is licensed under the **MIT License** but the scraped websites will have their own licenses and conditions. **PLEASE BE AWARE OF THAT.** This program is only for educational purposes.

A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.

### Permissions
✔️ Commercial use | Modification | Distribution | Private use

### Limitations
❌ Liability | Warranty

### Conditions
ℹ️ License and copyright notice

Refer to the [License declaration](./LICENSE) for more details.

## 🤑 Project Structure

```
offer-scraper/
├── .gitignore                   # Gitignore file
├── LICENSE                      # License file
├── offer-scraper.py             # Main scraper script
├── parameters.json              # Default bank configuration (can be customized)
├── README.md                    # README file
├── requirements.txt             # PIP requirements file
├── parameters/
│   ├── parameters_dfcc.json     # DFCC Bank configuration
│   └── parameters_ndb.json      # NDB Bank configuration
│   └── ...                      # NDB Bank configuration
├── offers/
    └── ...                      # Scraped data (month_year.json format)
```

## 🤑 Installation

### Prerequisites
- Python 3.6+
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd offer-scraper
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies
- **requests**: HTTP library for web scraping
- **beautifulsoup4**: HTML parsing library for extracting data from pages

## 🤑 Usage

### Basic Scraping
Run the scraper with default parameters:
```bash
python offer-scraper.py
```

### Command-line Arguments

#### Fresh Scrape (`-f`)
Delete existing data file and perform a fresh scrape:
```bash
python offer-scraper.py -f
```

#### Search by Vendor (`-v`)
Search and display offers for a specific vendor:
```bash
# List all vendors
python offer-scraper.py -v

# Search for specific vendor (case-insensitive)
python offer-scraper.py -v "cinnamon"
```

#### Search by Category (`-c`)
Search and display all offers in a specific category:
```bash
# List all categories
python offer-scraper.py -c

# Search for specific category (case-insensitive)
python offer-scraper.py -c "dining"
```

#### Information (`-i`)
Information about the program:
```bash
python offer-scraper.py -i
```

## 🤑 Configuration

### Configuration File Format
Configuration files are JSON-based and define CSS selectors and extraction rules for each bank's website structure.

**Key Parameters:**
- `version`: Configuration version string
- `bank`: Bank identifier (e.g., "ndb", "dfcc")
- `url`: Base URL of the bank's card offers page
- `subcategories`: CSS selector for category links
- `items`: CSS selector for individual offer items
- `vendor`: CSS selector for vendor/merchant names
- `saving`: CSS selector for discount/savings amounts
- `phone`: CSS selector for contact phone numbers
- `until`: CSS selector for expiration dates
- `img_items`/`offer_img`: CSS selectors for offer images
- `root_is_content`: Whether the root URL contains offer details

Each selector is defined as an array: `[selector_value, selector_type, html_element, navigation_required]`

### Adding a New Bank

1. Create a new configuration file in the `parameters/` directory (e.g., `parameters_newbank.json`)
2. Define CSS selectors for your target bank's website structure
3. Update `parameters.json` to include the same configuration
4. Run the scraper

## 🤑 Output Format

Scraped data is stored in JSON files in the `offers/` directory with filenames following the pattern: `offers_M_YYYY.json` (month_year).

**Data Structure:**
```json
{
  "vendor_name": {
    "offer_type": {
      "category": "category_name",
      "savings": "discount_amount",
      "phone": "contact_number",
      "until": "expiration_date",
      "vendor": "vendor_name",
      ...
    }
  }
}
```

## 🤑 Requirements

- Python 3.6 or higher
- Internet connection for web scraping
- Compliant with website terms of service (web scraping should respect robots.txt and terms of use)

## 🤑 Notes

- The scraper requires an active internet connection to retrieve web pages
- Headers and user-agent information should be configured appropriately when making requests
- Some websites may require additional handling for dynamic content or anti-scraping measures
- Output files are automatically generated and organized by month/year
- It's recommended to review the target websites' robots.txt and terms of service before deploying this scraper in production

## 🤑 Troubleshooting

**ERROR: Failed to retrieve the page!**
- Check your internet connection
- Verify the bank URLs are correct and accessible
- Ensure you're not being blocked by the website

**ERROR: Could not find parameters in JSON**
- Verify the configuration file exists and contains all required fields
- Check that CSS selectors match the current website structure (websites may change over time)

**No offers found**
- The website structure may have changed; update CSS selectors in the configuration
- Check if the bank's website is accessible

## 🤑 Releases

#### Version 1.0 [19/02/2026]

[Bank Card Offers Web Scraper 1.0](https://github.com/asankaSovis/offer-scraper/releases/tag/offer-scraper_v1.0)

- Initial commit

#### Version 1.1 [19/02/2026]

[Offer Scraper 1.1](https://github.com/asankaSovis/offer-scraper/releases/tag/offer-scraper_v1.1)

- Added about commands
- License updated to MIT license
- Renamed to 'Offer Scraper'
- Updated README
- Project made public

`© 2026 Asanka Sovis`