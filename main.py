import telebot
from src.check import checking_function
import threading
import logging

bot = telebot.TeleBot('6799026148:AAEE3F5aTgVTV4U65ktGzFr8fqNIBIkDgcA')

your_channel_id = -1001838455066


def process_lines(lines_subset):
  for line in lines_subset:
    cc_number = line.strip()
    checking_function(cc_number, bot)


@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(
      message.chat.id,
      'Hello, I am cc checking bot! /cs 440393xxxxxxxxxx|xx|xx|xxx @xSukka')


@bot.message_handler(commands=['cs'])
def check_cc(message):
  try:

    cc_number = message.text.split(' ')[1]
    # Create a thread to execute the checking function
    msg = bot.reply_to(message, "Checking..!")
    check_thread = threading.Thread(target=checking_function,
                                    args=(cc_number, bot, msg))
    check_thread.start()

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
