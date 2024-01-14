import telebot
import os
from telebot import types
import time
import telebot
import logging
import threading
from telebot import types

from config import config
from src.check import checking_function
from bin_look import bin_lokup
from database.blacklist import add_blacklist, get_blacklisted, remove_blacklist, check_blacklist
from database.sudousers import add_sudolist, check_sudolist, remove_sudolist, get_sudolisted
from database.userchats import add_chat, get_phone_number_by_id, add_phone, get_all_chats, get_all_phones, remove_phone, remove_chat
from src.reload import reaload_function
from src.mobitel import mobitel_gateway

cooldowns = {}
bot = telebot.TeleBot(config.MAIN_TOKEN)

CHANNEL_ID = config.CHANNEL_ID
POST_CHANNEL = config.POST_CHANNEL
OWNER_ID = config.OWNER_ID


@bot.message_handler(commands=['reload'])
def reload_handler(message):
  al = get_sudolisted()
  if (message.from_user.id == OWNER_ID) or (message.from_user.id in al):
    try:
      number = message.text.split(' ')[1]
    except IndexError:
      return bot.reply_to(
          message,
          "<b>Send This command in the below format👇</b>\n\n<code>/reload cc_number</code> (Replace 'cc_number', before using this command you have to add the phone number to the bot, for more info send /add_phone command!)",
          parse_mode='HTML')

    user_id = message.from_user.id

    msg = bot.reply_to(message, "<b>Reloading ◈◇◇◇</b>", parse_mode='HTML')
    check_thread = threading.Thread(target=reaload_function,
                                    args=(number, bot, msg, user_id))
    check_thread.start()
  else:
    bot.reply_to(message,
                 f'<b>You are not authorized to use this command.</b>',
                 parse_mode='HTML')


@bot.message_handler(commands=['cmds'])
def commandHandler(message):
  user_id = message.from_user.id
  fuser = message.from_user.id
  if check_blacklist(fuser):
    message.reply_to(message, "Sorry! You are Banned!")
    return
  add_chat(fuser)
  try:
    bot.forward_message(user_id, from_chat_id=POST_CHANNEL, message_id=5)
  except Exception as e:
    print(f"Error forwarding message: {e}")


@bot.message_handler(commands=['start'])
def start_message(message):
  user_id = message.from_user.id
  fuser = message.from_user.id
  if check_blacklist(fuser):
    message.reply_to(message, "Sorry! You are Banned!")
    return
  add_chat(fuser)
  is_member = bot.get_chat_member(CHANNEL_ID, user_id).status != 'left'
  if is_member:
    user_id = message.from_user.id
    try:
      bot.forward_message(user_id, from_chat_id=POST_CHANNEL, message_id=4)
    except Exception as e:
      print(f"Error forwarding message: {e}")
  else:
    # User is not a member of the channel, send an inline button with the invite link
    try:
      bot.forward_message(user_id, from_chat_id=POST_CHANNEL, message_id=4)
    except Exception as e:
      print(f"Error forwarding message: {e}")


# bin lookup
@bot.message_handler(commands=['bin'])
def bin_message(message):
  try:
    bin = message.text.split(' ')[1][:6]
    response_data = bin_lokup(bin)

    bin_number = response_data['bin']
    country = response_data['country']
    card_type = response_data['card_type']
    bank = response_data['bank']
    bot.reply_to(
        message,
        f"Bin: {bin_number}\nBank: {bank}\nCountry: {country}\nCard Type: {card_type}"
    )

  except Exception as e:
    bot.send_message(message.chat.id, f"Error: {e}")





@bot.message_handler(commands=['cs'])
def check_cc(message):
  fuser = message.from_user.id
  if check_blacklist(fuser):
    message.reply_to(message, "Sorry! You are Banned!")
    return
  add_chat(fuser)
  try:
    user_id = message.from_user.id
    is_member = bot.get_chat_member(CHANNEL_ID, user_id).status != 'left'

    def update_cooldown(user_id, time):
      cooldowns[user_id] = time

    if is_member:
      current_time = time.time()
      if user_id in cooldowns:
        if current_time - cooldowns[user_id] < 50:
          remaining_time = int(50 - (current_time - cooldowns[user_id]))
          bot.reply_to(message, f"Please wait {remaining_time} seconds ")
          return

      al = get_sudolisted()
      if message.from_user.id not in al:
        cooldowns[user_id] = current_time
      try:
        cc_number = message.text.split(' ')[1]
        msg = bot.reply_to(message, "<b>CHECKING ◈◇◇◇</b>", parse_mode='HTML')
        check_thread = threading.Thread(target=checking_function,
                                        args=(cc_number, bot, msg,
                                              update_cooldown, user_id))
        check_thread.start()
      except:
        return 'ERROR'
    else:
      user_id = message.from_user.id
      try:
        bot.forward_message(user_id, from_chat_id=POST_CHANNEL, message_id=4)
      except Exception as e:
        print(f"Error forwarding message: {e}")

  except IndexError:
      return bot.reply_to(
          message,
          "<b>Send This command in the below format👇</b>\n\n<code>/cs cc_number</code> Replace 'cc_number' with ur credit card number!",
          parse_mode='HTML')


# Broadcast commands
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
  if message.from_user.id == OWNER_ID:
    if message.reply_to_message:
      msg = message.reply_to_message
    else:
      return bot.reply_to(
          message,
          "First send me the message that you want to send to the other users of this bot! Then as a reply to it send /broadcast"
      )

    m = bot.reply_to(message, "`Broadcasting..`")
    all_chats = get_all_chats()
    success_count = 0
    fail_count = 0
    error_report = "ERROR Report !\n\n"

    for chat in all_chats:
      try:
        bot.send_message(chat, msg.text)
        success_count += 1
      except Exception as e:
        fail_count += 1
        error_report += f"{chat} - {str(e)}\n"

    bot.reply_to(
        message,
        f"Successfully Broadcasted to {success_count} Chats\nFailed - {fail_count} Chats !"
    )

    if fail_count > 0:
      bot.edit_message_text("Generating Error Report !",
                            chat_id=message.chat.id,
                            message_id=m.message_id)
      with open("ErrorReport.txt", "w") as error_file:
        error_file.write(error_report)
      bot.send_document(message.chat.id,
                        open("ErrorReport.txt", "rb"),
                        caption="Errors on Broadcast")
      os.remove("ErrorReport.txt")
    bot.delete_message(chat_id=message.chat.id, message_id=m.message_id)


@bot.message_handler(commands=['stats'])
def get_stats(message):
  if message.from_user.id == OWNER_ID:
    all_chats = get_all_chats()
    all_phones = get_all_phones()
    all_sudos = get_sudolisted()
    bot.reply_to(
        message,
        f"Total Chats in Database - {len(all_chats)}\nPremium Users - {len(all_sudos)}\nTotal Phone NUmbers - {len(all_phones)}"
    )


# add phone number adding function
@bot.message_handler(commands=['add_phone'])
def add_phone_number(message):
  al = get_sudolisted()
  if message.from_user.id in al:
    try:
      user = message.from_user.id
      phone = message.text.split()[1]
    except IndexError:
      return bot.reply_to(
          message,
          "<b>Send This command in the below format👇</b>\n\n<code>/add_phone 75xxxxxxx</code> (Replace '75xxxxxxx' with your Airtel Phone Number without 0 to the front..!)",
          parse_mode='HTML')

    add_phone(user, phone)
    bot.reply_to(message,
                 "<b>Phone number added successfully.</b>",
                 parse_mode="HTML")


@bot.message_handler(commands=['remove_phone'])
def remove_phone_number(message):
  al = get_sudolisted()
  if message.from_user.id in al:
    try:
      user_id = message.from_user.id
      rm = remove_phone(user_id)
      if rm:
        bot.reply_to(message,
                     "<b>Phone number removed successfully.</b>",
                     parse_mode="HTML")
      else:
        bot.reply_to(message,
                     "<b>Phone number not found.</b>",
                     parse_mode="HTML")

    except IndexError:
      return bot.reply_to(message, "Remove Faild!", parse_mode='HTML')


def list_all_phones():
  all_phones = get_all_phones()

  if not all_phones:
    return "No phone numbers found."

  message_text = "List of Users and Phone Numbers:\n"

  for user_info in all_phones:
    user_id = list(user_info.keys())[
        0]  # Assuming each dictionary has only one key (user ID)
    phone_number = user_info[user_id]
    message_text += f"{user_id} - {phone_number}\n"

  return message_text


@bot.message_handler(commands=['listphones'])
def list_phones(message):
  if message.from_user.id == OWNER_ID:
    m = bot.reply_to(message, "`...`")
    message_text = list_all_phones()
    bot.edit_message_text(message_text, message.chat.id, m.message_id)


# add sudo list commands
@bot.message_handler(commands=['sudo'])
def add_sudo(message):
  if message.from_user.id == OWNER_ID:
    try:
      user_id = int(message.text.split()[1])
    except IndexError:
      return bot.reply_to(
          message,
          "<b>Send This command in the below format👇</b>\n\n<code>/black userid</code> (Replace 'userid' with the user's Telegram ID of who you want to add the sudo to the bot!)",
          parse_mode='HTML')
    add_sudolist(user_id)
    bot.reply_to(message,
                 f"<b>User {user_id} has been added to the sudo list!</b>",
                 parse_mode='HTML')


@bot.message_handler(commands=['unsudo'])
def unblack_user(message):
  if message.from_user.id == OWNER_ID:
    try:
      user_id = int(message.text.split(" ", maxsplit=1)[1])
    except IndexError:
      return bot.reply_to(
          message,
          "<b>Send This command in the below format👇</b>\n\n<code>/unblack userid</code> (Replace 'userid' with the user's Telegram ID of who you want to unsudo to the bot!)",
          parse_mode='HTML')

    result = remove_sudolist(user_id)
    bot.reply_to(message, result)


@bot.message_handler(commands=['listsudo'])
def list_black(message):
  if message.from_user.id == OWNER_ID:
    m = bot.reply_to(message, "`...`")
    al = get_sudolisted()
    TE = "List of Sudo Users !"
    for user_id in al:
      TE += "\n" + str(user_id)
    bot.edit_message_text(TE, message.chat.id, m.message_id)


# blacklist commands
@bot.message_handler(commands=['black'])
def black_user(message):
  if message.from_user.id == OWNER_ID:
    try:
      user_id = int(message.text.split(" ", maxsplit=1)[1])
    except IndexError:
      return bot.reply_to(
          message,
          "<b>Send This command in the below format👇</b>\n\n<code>/black userid</code> (Replace 'userid' with the user's Telegram ID of who you want to ban from the bot!)",
          parse_mode='HTML')

    add_blacklist(user_id)
    print(get_blacklisted())
    bot.reply_to(message, f"Blacklisted {user_id} !")


@bot.message_handler(commands=['unblack'])
def unblack_user(message):
  if message.from_user.id == OWNER_ID:
    try:
      user_id = int(message.text.split(" ", maxsplit=1)[1])
    except IndexError:
      return bot.reply_to(
          message,
          "<b>Send This command in the below format👇</b>\n\n<code>/unblack userid</code> (Replace 'userid' with the user's Telegram ID of who you want to unban from the bot!)",
          parse_mode='HTML')

    result = remove_blacklist(user_id)
    bot.reply_to(message, result)


@bot.message_handler(commands=['listblack'])
def list_black(message):
  if message.from_user.id == OWNER_ID:
    m = bot.reply_to(message, "`...`")
    al = get_blacklisted()
    TE = "List of Blacklisted User !"
    for user_id in al:
      TE += "\n" + str(user_id)
    bot.edit_message_text(TE, message.chat.id, m.message_id)


bot.polling()
