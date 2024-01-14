import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import re
from encrypt import encrypt_data, gen_public_key

session = requests.session()

url = "https://online.mobitel.lk/onlinepay/payment"
headers = {
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "online.mobitel.lk",
    "Origin": "https://online.mobitel.lk",
    "Referer": "https://online.mobitel.lk/onlinepay/card",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "sec-ch-ua":
    "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
}

payload_data = {
    "serviceNumber": "0702400408",
    "reServiceNumber": "0702400408",
    "amount": "50",
    "email": "technexo@outlook.com",
    "amountAlert": "0",
}

response = session.post(url, headers=headers, data=payload_data)

soup = BeautifulSoup(response.text, 'html.parser')

# Find the value of the transactionId
transcation_id = soup.find('input', {'id': 'transcationId'}).get('value')
# Print response headers

initial_cookies_dict = {}

initial_cookies = response.cookies
for cookie in initial_cookies:
  initial_cookies_dict[cookie.name] = cookie.value
#bot.edit_message_text(chat_id=sent_message.chat.id,message_id=sent_message.message_id,text="Step 1 - 3")
# Convert the dictionary to JSON format
initial_cookies_json = json.dumps(initial_cookies_dict)

parsed_json = json.loads(initial_cookies_json)
print(parsed_json)

# Access specific values to create variables
JSESSIONID = parsed_json.get('JSESSIONID')
cookiesession1 = parsed_json.get('cookiesession1')
nsc = parsed_json.get('NSC_pomjofqbz-MC')

cookie = f"JSESSIONID={JSESSIONID}; NSC_pomjofqbz-MC={nsc}; cookiesession1={cookiesession1}"

print(f'Transaction ID: {transcation_id}')

header = {
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": cookie,
    "Host": "online.mobitel.lk",
    "Origin": "https://online.mobitel.lk",
    "Referer": "https://online.mobitel.lk/onlinepay/payment",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "sec-ch-ua":
    "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
}

payload = {
    "serviceNumber": "0702400408",
    "reServiceNumber": "0702400408",
    "amount": "50",
    "email": "technexo@outlook.com",
    "transcationId": transcation_id,
    "conType": "PRE",
    "pkgRefNo": "0",
}

# Make the POST request
response1 = session.post("https://online.mobitel.lk/onlinepay/payNow",
                         headers=header,
                         data=payload,
                         allow_redirects=True)
# Print response headers
print("Response Headers:")
for key, value in response1.headers.items():
  print(f"{key}: {value}")

if response1.history:
  final_url = response1.url
  print(f"Referer-url: {final_url}")
else:
  print("No redirection occurred.")

#print(response1.text)

soup1 = BeautifulSoup(response1.text, 'html.parser')

# Extract href attributes from the <a> tags
base_url = "https://selfcare.mobitel.lk/MCardPay"
first_a_tag = soup1.select_one('ul.method_ul li a')

if first_a_tag:
  href_url = first_a_tag.get('href')
  m_pay = f"{base_url}{href_url.replace('..', '')}"
  print(f"New URL: {m_pay}")
else:
  print("No <a> tag found.")

headers = {
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9",
    "Connection": "keep-alive",
    "Cookie": cookie,
    "Host": "selfcare.mobitel.lk",
    "Referer": final_url,
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "sec-ch-ua":
    "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
}

# Make the GET request
response2 = session.get(m_pay, headers=headers)

soup3 = BeautifulSoup(response2.text, 'html.parser')

# Extracting values using BeautifulSoup
access_key = soup3.find('input', {'id': 'access_key'}).get('value')
profile_id = soup3.find('input', {'id': 'profile_id'}).get('value')
transaction_uuid = soup3.find('input', {
    'name': 'transaction_uuid'
}).get('value')
signed_field_names = soup3.find('input', {
    'name': 'signed_field_names'
}).get('value')
unsigned_field_names = soup3.find('input', {
    'name': 'unsigned_field_names'
}).get('value', None)
signed_date_time = soup3.find('input', {
    'name': 'signed_date_time'
}).get('value')
locale = soup3.find('input', {'name': 'locale'}).get('value')
transaction_type = soup3.find('input', {
    'name': 'transaction_type'
}).get('value')
reference_number = soup3.find('input', {
    'name': 'reference_number'
}).get('value')
amount = soup3.find('input', {'name': 'amount'}).get('value')
currency = soup3.find('input', {'name': 'currency'}).get('value')
bill_to_forename = soup3.find('input', {
    'name': 'bill_to_forename'
}).get('value')
bill_to_surname = soup3.find('input', {'name': 'bill_to_surname'}).get('value')
bill_to_email = soup3.find('input', {'name': 'bill_to_email'}).get('value')
bill_to_address_city = soup3.find('input', {
    'name': 'bill_to_address_city'
}).get('value')
bill_to_address_line1 = soup3.find('input', {
    'name': 'bill_to_address_line1'
}).get('value')
bill_to_address_state = soup3.find('input', {
    'name': 'bill_to_address_state'
}).get('value')
bill_to_address_country = soup3.find('input', {
    'name': 'bill_to_address_country'
}).get('value')
signature = soup3.find('input', {'id': 'signature'}).get('value')

# Print or use the extracted values as needed
"""print("Access Key:", access_key)
print("Profile ID:", profile_id)
print("Transaction UUID:", transaction_uuid)
print("Signed Field Names:", signed_field_names)
print("Unsigned Field Names:", unsigned_field_names)
print("Signed Date Time:", signed_date_time)
print("Locale:", locale)
print("Transaction Type:", transaction_type)
print("Reference Number:", reference_number)
print("Amount:", amount)
print("Currency:", currency)
print("Bill to Forename:", bill_to_forename)
print("Bill to Surname:", bill_to_surname)
print("Bill to Email:", bill_to_email)
print("Bill to Address City:", bill_to_address_city)
print("Bill to Address Line1:", bill_to_address_line1)
print("Bill to Address State:", bill_to_address_state)
print("Bill to Address Country:", bill_to_address_country)
print("Signature:", signature)"""

headers3 = {
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language":
    "en-GB,en;q=0.9",
    "Cache-Control":
    "max-age=0",
    "Content-Length":
    "878",  # Adjust this if the actual content length is different
    "Content-Type":
    "application/x-www-form-urlencoded",
    "Origin":
    "https://selfcare.mobitel.lk",
    "Referer":
    "https://selfcare.mobitel.lk/",
    "Sec-Ch-Ua":
    "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "Sec-Ch-Ua-Mobile":
    "?0",
    "Sec-Ch-Ua-Platform":
    "\"Windows\"",
    "Sec-Fetch-Dest":
    "document",
    "Sec-Fetch-Mode":
    "navigate",
    "Sec-Fetch-Site":
    "cross-site",
    "Sec-Fetch-User":
    "?1",
    "Upgrade-Insecure-Requests":
    "1",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}

payload3 = {
    "access_key": access_key,
    "profile_id": profile_id,
    "transaction_uuid": transaction_uuid,
    "signed_field_names":
    "access_key,profile_id,transaction_uuid,signed_field_names,unsigned_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency,bill_to_forename,bill_to_surname,bill_to_email,bill_to_address_line1,bill_to_address_state,bill_to_address_country,bill_to_address_city",
    "unsigned_field_names": "",
    "signed_date_time": signed_date_time,
    "locale": "en",
    "transaction_type": "sale",
    "reference_number": reference_number,
    "amount": "50.00",
    "currency": "LKR",
    "bill_to_forename": "Mobitel",
    "bill_to_surname": "Mobitel",
    "bill_to_email": "test_it@mobitel.com",
    "bill_to_address_city": "Colombo",
    "bill_to_address_line1": "Mobitel",
    "bill_to_address_state": "",
    "bill_to_address_country": "LK",
    "signature": signature,
}

response4 = session.post("https://secureacceptance.cybersource.com/pay",
                         headers=headers3,
                         data=payload3)

#print(response4.text)

pattern = r'<input type="hidden" id="jwk" value=\'(.*?)\''
matches = re.search(pattern, response4.text)
if matches:
  jwk_value = matches.group(1)
json_response = json.loads(jwk_value)
print('Encrpting Data : ', json_response)
cc = "4610460304113822"
cvv = "421"
public_key = gen_public_key(json_response)
card_number = encrypt_data(public_key, cc)
cvv_number = encrypt_data(public_key, cvv)

print('encrypted cc num :', card_number)
print('encrypted cvv :', cvv_number)

session_uuid = re.search(
    r'<input type="hidden" name="session_uuid" id="session_uuid" value="(\w+)" autocomplete="off" />',
    response4.text).group(1)

print('Session UUID : ', session_uuid)

authenticity_token = re.search(
    r'<input type="hidden" name="authenticity_token" value="(.*?)"',
    response4.text).group(1)
print('authenticity_token : ', authenticity_token)

initial_cookies_dict2 = {}
initial_cookies2 = response4.history[0].cookies
for cookie in initial_cookies2:
  initial_cookies_dict2[cookie.name] = cookie.value
#bot.edit_message_text(chat_id=sent_message.chat.id,message_id=sent_message.message_id,text="Step 1 - 3")
# Convert the dictionary to JSON format
initial_cookies_json2 = json.dumps(initial_cookies_dict2)

parsed_json2 = json.loads(initial_cookies_json2)

# Access specific values to create variables
JSESSIONID2 = parsed_json2.get('JSESSIONID')
cfruid2 = parsed_json2.get('__cfruid')

cookie2 = f"JSESSIONID={JSESSIONID2}; __cfruid={cfruid2}"

print(cookie2)

headers5 = {
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language":
    "en-GB,en;q=0.9",
    "Cache-Control":
    "max-age=0",
    "Content-Length":
    "878",  # Adjust this if the actual content length is different
    "Content-Type":
    "application/x-www-form-urlencoded",
    "Cookie":
    cookie2,
    "Origin":
    "https://selfcare.mobitel.lk",
    "Referer":
    "https://selfcare.mobitel.lk/",
    "Sec-Ch-Ua":
    "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "Sec-Ch-Ua-Mobile":
    "?0",
    "Sec-Ch-Ua-Platform":
    "\"Windows\"",
    "Sec-Fetch-Dest":
    "document",
    "Sec-Fetch-Mode":
    "navigate",
    "Sec-Fetch-Site":
    "cross-site",
    "Sec-Fetch-User":
    "?1",
    "Upgrade-Insecure-Requests":
    "1",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}

payload5 = {
    "utf8": "✓",
    "authenticity_token": authenticity_token,
    "session_uuid": session_uuid,
    "payment_method": "card",
    "card_type": "001",
    "card_number": cc,
    "__e.card_number": card_number,
    "card_expiry_month": "01",
    "card_expiry_year": "2025",
    "card_cvn": cvv,
    "__e.card_cvn": cvv_number,
    "ccaRetryAction": "/checkout",
    "customer_utc_offset": "330",
}

response5 = session.post(
    "https://secureacceptance.cybersource.com/checkout_update",
    headers=headers5,
    data=payload5)

match6 = re.search(r"window.ccaOptions = ({.*});", response5.text)
if match6:
  options_json = match6.group(1)
  options = json.loads(options_json)

  # Access the desired values
  referenceId = options.get("referenceId")
  authenticityToken = options.get("authenticityToken")

  print("referenceId:", referenceId)
  print("authenticityToken:", authenticityToken)
else:
  print("ccaOptions not found in the HTML code.")

#print(response5.text)

headers6 = {
    "Accept":
    "*/*",
    "Accept-Language":
    "en-GB,en;q=0.9",
    "Content-Length":
    "492",  # Adjust this if the actual content length is different
    "Content-Type":
    "application/x-www-form-urlencoded",
    "Cookie":
    cookie2,
    "Origin":
    "https://secureacceptance.cybersource.com",
    "Referer":
    "https://secureacceptance.cybersource.com/payer_authentication/hybrid?ccaAction=load",
    "Sec-Ch-Ua":
    "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "Sec-Ch-Ua-Mobile":
    "?0",
    "Sec-Ch-Ua-Platform":
    "\"Windows\"",
    "Sec-Fetch-Dest":
    "empty",
    "Sec-Fetch-Mode":
    "cors",
    "Sec-Fetch-Site":
    "same-origin",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}

payload6 = {
    "ccaAction": "check",
    "ccaSessionId": referenceId,
    "ccaClientSessionId": "0_3094f50a-deeb-40ed-bbdb-ce6ba679c7ba",
    "ccaTiming": "6481",
    "authenticity_token": authenticityToken,
    "customer_browser_color_depth": "24",
    "customer_browser_language": "en-GB",
    "customer_browser_java_enabled": "false",
    "customer_browser_screen_height": "1200",
    "customer_browser_screen_width": "1920",
    "customer_browser_time_difference": "-330",
    "__inner_width": "1912",
    "__inner_height": "1078",
}

response6 = session.post(
    "https://secureacceptance.cybersource.com/payer_authentication/hybrid",
    headers=headers6,
    data=payload6)

print(response6.text)

headers7 = {
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language":
    "en-GB,en;q=0.9",
    "Cache-Control":
    "max-age=0",
    "Content-Length":
    "153",
    "Content-Type":
    "application/x-www-form-urlencoded",
    "Cookie":
    cookie2,
    "Origin":
    "https://secureacceptance.cybersource.com",
    "Referer":
    "https://secureacceptance.cybersource.com/payer_authentication/hybrid?ccaAction=load",
    "Sec-Ch-Ua":
    "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "Sec-Ch-Ua-Mobile":
    "?0",
    "Sec-Ch-Ua-Platform":
    "\"Windows\"",
    "Sec-Fetch-Dest":
    "document",
    "Sec-Fetch-Mode":
    "navigate",
    "Sec-Fetch-Site":
    "same-origin",
    "Upgrade-Insecure-Requests":
    "1",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}

payload7 = {
    "authenticity_token": authenticityToken,
    "ccaAction": "completeEarly",
    "ccaErrorsHandled": "[]",
    # Add more parameters if needed
}

response7 = session.post(
    "https://secureacceptance.cybersource.com/payer_authentication/hybrid",
    headers=headers7,
    data=payload7)

#print(response7.text)

soup5 = BeautifulSoup(response7.text, 'html.parser')

# Find the input element with name="message"
message_input = soup5.find('input', {'name': 'message'})
message_decision = soup5.find('input', {'name': 'decision'})
if message_input and message_decision:
  message_value = message_input.get('value')
  message_decision_value = message_decision.get('value')
print(message_value, message_decision_value)
