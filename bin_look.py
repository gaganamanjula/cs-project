import requests
from bs4 import BeautifulSoup


def bin_lokup(bin):
  try:
    url = 'https://bins.su'

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '44',
        'Origin': 'https://bins.su',
        'Connection': 'keep-alive',
        'Referer': 'https://bins.su/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
    }

    params = {'action': 'searchbins', 'bins': bin, 'bank': '', 'country': ''}

    response = requests.post(url, headers=headers, data=params)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables in the HTML content
    tables = soup.find_all('table')

    # Extract details from the last table
    last_table = tables[-1]  # Get the last table

    # Extract the first record from the table
    rows = last_table.find_all('tr')
    if len(rows) > 1:
      first_row = rows[1]
      td_elements = first_row.find_all('td')
      if len(td_elements) >= 6:
        bin_number = td_elements[0].text.strip()
        country = td_elements[1].text.strip()
        vendor = td_elements[2].text.strip()
        card_type = td_elements[3].text.strip()
        level = td_elements[4].text.strip()
        bank_name = td_elements[5].text.strip()

        cardType = f"{vendor} {card_type} {level}"
        result_json = {
            "bin": bin_number,
            "country": country,
            "card_type": cardType,
            "bank": bank_name
        }
        return result_json
      else:
        print("Insufficient data in the row")
    else:
      print("No records found in the table")
  except Exception as e:
    print(f'{e}')


