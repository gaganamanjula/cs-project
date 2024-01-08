import telebot
from src.check import checking_function
import threading
import logging
from telebot import types
import time
cooldowns = {}

bot = telebot.TeleBot('1970098920:AAHNU5dYWWATCtojpfKgHuwfYXHgp5dyOKs')

CHANNEL_ID = -1001838455066
POST_CHANNEL = -1002078366567

@bot.message_handler(commands=['cmds'])
def commandHandler(message):
  user_id = message.from_user.id
  try:
    bot.forward_message(user_id, from_chat_id=POST_CHANNEL, message_id=5)
  except Exception as e:
    print(f"Error forwarding message: {e}")

def process_lines(lines_subset):
  for line in lines_subset:
    cc_number = line.strip()
    checking_function(cc_number, bot)


@bot.message_handler(commands=['start'])
def start_message(message):
  user_id = message.from_user.id
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
  
@bot.message_handler(commands=['cs'])
def check_cc(message):
  try:
    user_id = message.from_user.id
    is_member = bot.get_chat_member(CHANNEL_ID, user_id).status != 'left'
    
    def update_cooldown(user_id, time):
      cooldowns[user_id] = time
      
    if is_member:
      current_time = time.time()

      # Check if the user has a cooldown time recorded
      if user_id in cooldowns:
          # Check if the cooldown period (25 seconds) has passed
          if current_time - cooldowns[user_id] < 40:
              remaining_time = int(40 - (current_time - cooldowns[user_id]))
              bot.reply_to(message, f"Please wait {remaining_time} seconds ")
              return

      # Update or set the cooldown time for the user
      cooldowns[user_id] = current_time

      # Rest of your /cs command logic here
      cc_number = message.text.split(' ')[1]
      msg = bot.reply_to(message, "**Checking..!**", parse_mode='Markdown')
      check_thread = threading.Thread(target=checking_function, args=(cc_number, bot, msg, update_cooldown, user_id))
      check_thread.start()
    else:
      # User is not a member of the channel, send an inline button with the invite link
      user_id = message.from_user.id
      try:
        bot.forward_message(user_id, from_chat_id=POST_CHANNEL, message_id=4)
      except Exception as e:
        print(f"Error forwarding message: {e}")

  except Exception as e:
    bot.send_message(message.chat.id,
                     'Error processing the credit card: {}'.format(e))


"""@bot.message_handler(content_types=['document'])
def handle_document(message):
  try:
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    bot.reply_to(message, 'Checking!')

    # Save the downloaded file to the bot's directory
    file_name = f"downloaded_{message.document.file_name}"
    with open(file_name, 'wb') as new_file:
      new_file.write(downloaded_file)

    with open(file_name, 'r') as txt_file:
      content = txt_file.read()
      lines = content.split("\n")

    # Split lines into 2 or 3 subsets for threading
    num_threads = min(len(lines), 3)  # Set the maximum number of threads to 3
    line_chunks = [lines[i::num_threads] for i in range(num_threads)]

    # Create and start a thread for each subset of lines
    threads = []
    for chunk in line_chunks:
      thread = threading.Thread(target=process_lines, args=(chunk, ))
      threads.append(thread)
      thread.start()

    # Wait for all threads to complete
    for thread in threads:
      thread.join()

  except Exception as e:
    bot.reply_to(message, f"Error processing file: {str(e)}")"""

# Start the bot
bot.polling()
