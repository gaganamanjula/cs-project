from . import DB, get_stuff

AL = DB.get("ALLCHATS")
if not AL:
  DB.set("ALLCHATS", "{'USERS':[], 'PHONE_NUMBERS':[]}")


def add_chat(id: str):
  CCH = get_stuff("ALLCHATS")
  if not CCH:
    CCH.update({"USERS": [id]})
    DB.set("ALLCHATS", str(CCH))
    return
  if CCH["USERS"] and id in CCH["USERS"]:
    return
  Ul = CCH["USERS"]
  if not Ul:
    Ul = []
  Ul.append(id)
  CCH.update({"USERS": Ul})
  DB.set("ALLCHATS", str(CCH))


def get_phone_number_by_id(user_id: str):
  CCH = get_stuff("ALLCHATS")

  if CCH and 'PHONE_NUMBERS' in CCH:
    phone_numbers_list = CCH['PHONE_NUMBERS']
    for user_dict in phone_numbers_list:
      if user_id in user_dict:
        return user_dict[user_id]

  return 'NO PHONE ASSOCIATED WITH THIS USER-ID'


def add_phone(id: str, phone_number: str):
  CCH = get_stuff("ALLCHATS")
  if 'PHONE_NUMBERS' not in CCH:
    CCH['PHONE_NUMBERS'] = []
  if not CCH:
    CCH.update({"PHONE_NUMBERS": [{id: phone_number}]})
    DB.set("ALLCHATS", str(CCH))
    return
  if CCH["PHONE_NUMBERS"]:
    for user_info in CCH["PHONE_NUMBERS"]:
      if id in user_info:
        return  # User already exists, do nothing
    CCH["PHONE_NUMBERS"].append({id: phone_number})
    DB.set("ALLCHATS", str(CCH))
  else:
    CCH["PHONE_NUMBERS"] = [{id: phone_number}]
    DB.set("ALLCHATS", str(CCH))


def get_all_chats():
  CCH = get_stuff("ALLCHATS")
  if not (CCH and CCH["USERS"]):
    return []
  return CCH["USERS"]


def get_all_phones():
  CCH = get_stuff("ALLCHATS")
  if not (CCH and CCH["PHONE_NUMBERS"]):
    return []
  return CCH["PHONE_NUMBERS"]


def remove_chat(id):
  CCH = get_stuff("ALLCHATS")
  if not CCH:
    return
  if CCH["USERS"] and id not in CCH["USERS"]:
    return
  li = CCH["USERS"]
  if id in li:
    li.remove(id)
  CCH.update({"USERS": li})
  DB.set("ALLCHATS", str(CCH))
  return True


def remove_phone(id: str):
  CCH = get_stuff("ALLCHATS")

  # Check if CCH is empty or 'PHONE_NUMBERS' key is not present
  if not CCH or 'PHONE_NUMBERS' not in CCH:
      return False

  phone_numbers = CCH['PHONE_NUMBERS']

  # Check if the user ID exists in the phone number list
  for user_info in phone_numbers:
      if id in user_info:
          phone_numbers.remove(user_info)
          DB.set("ALLCHATS", str(CCH))
          return True  # Phone number removed successfully

  # If the user ID is not found, return False
  return False

