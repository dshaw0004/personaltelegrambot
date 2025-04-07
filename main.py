import os, time, datetime
import telebot


from firebase.db import get_all_message, add_new_message



TOKEN = os.environ["TOKEN"]
MASTER = os.environ["MASTER"]

bot = telebot.TeleBot(TOKEN)

  
print('server is live at', time.localtime() )

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
  user_name = message.from_user.username if message.from_user.username != None else message.from_user.first_name
  bot.reply_to(message, f'hello {user_name}\nHow are you doing ?')  


###---###

@bot.message_handler(commands=['about'])
def send_about(message):
  ABOUT:str = '''
  *About me*
  
  I am a telegram bot made by *Dipankar Shaw* (a.k.a. - [dshaw0004](https://dshaw0004.netlify.app)) to make communication bridge between you (the user) and him 
 (the owner of this bot).
  
  I can pass your message to the owner. Also you can comment to his blogs from here(not available yet).
  
  Use */sendtomaster* to send a message to the owner.
  Use */help* for help.
  '''  
  bot.send_message(message.from_user.id, ABOUT, parse_mode='MARKDOWN')

###---###

@bot.message_handler(commands=['help'])
def help(message):
  ABOUT:str = '''
  *Help*
  
  Use */sendtomaster* to send a message to the owner.
  Use */help* for help.
  '''  
  bot.send_message(message.from_user.id, ABOUT, parse_mode='MARKDOWN')

###---###


@bot.message_handler(commands=['sendtomaster', 'send_to_master', 'deliver_to_dshaw'])
def get_message_for_master(message):
  reply = 'Write your message now.'
  sent_msg = bot.send_message(message.chat.id, reply, parse_mode="Markdown")
  bot.register_next_step_handler(sent_msg, deliver_to_master)
  

def deliver_to_master(message):
  sender_name = f'{message.from_user.first_name} {message.from_user.last_name}'
  sender_id = message.from_user.id
  msg_for_master = f'''
  Message from {sender_name}
  Sender id {sender_id}\n
  {message.text}
  '''
  add_new_message(message.text, sender_name, str(sender_id))
  bot.send_message(MASTER, msg_for_master, parse_mode="Markdown")
  bot.send_message(sender_id, 'your message is deliver')


###---###


@bot.message_handler(commands=['seeallmessage'])
def send_all_message1(message):
  reply = 'Please Enter the password'
  sent_msg = bot.send_message(message.chat.id, reply, parse_mode="Markdown")
  bot.register_next_step_handler(sent_msg, send_all_message2)
  

def send_all_message2(message):
  if message.text != 'jeskone':
    bot.send_message(message.from_user.id, "<b>I AM REPORTING ABOUT YOU TO MASTER</b>", parse_mode="HTML")
    sender_name = f'{message.from_user.first_name} {message.from_user.last_name}'
    sender_id = message.from_user.id
    msg_for_master = f'''
    some tries to access your messages
    Name: {sender_name}
    Id: {sender_id}
    '''
    bot.send_message(MASTER, msg_for_master, parse_mode="Markdown")
    return
  all_messages = get_all_message()

  for each_message in all_messages:
    # msg = each_message.to_dict()
    msg_for_master = f'<b><u>Message</u></b>\n{each_message["message"]}\n\n<b><u>Sender info</u></b>\nName : <b>{each_message["senderName"]}</b>\nContact: <b>{each_message["senderContact"]}</b>'
    # print(each_message["message"])
    bot.send_message(MASTER, msg_for_master, parse_mode="HTML")

####

@bot.message_handler(commands=['reply_to'])
def reply_to_1(message):
  reply = '''Enter your message and receivers id in this format \n<sender_id>\n===\n<your message>'''
  sent_msg = bot.send_message(message.chat.id, reply)
  bot.register_next_step_handler(sent_msg, reply_to_2)
  

def reply_to_2(message):
  msg = message.text
  msg_arr = msg.split("===")
  sent_message = f'''
  **dshaw0004** sent you this message
  ----
  {msg_arr[1]}
  '''
  bot.send_message(msg_arr[0], sent_message, parse_mode="Markdown")


@bot.message_handler(content_types=['location'])
def loc(message):
  user_name = message.from_user.username if message.from_user.username != None else message.from_user.first_name
  # df = pd.DataFrame(columns=['date', 'person_name', 'person_id', 'long', 'lat'])
  
  # if os.path.exists("location_history.csv"):
  #   df = pd.read_csv("location_history.csv")

  # row_in_df, _ = df.shape

  # df.loc[int(row_in_df)+1] = [
  #   datetime.datetime.now(),
  #   user_name,
  #   message.from_user.id, 
  #   message.location.longitude,
  #   message.location.latitude
  # ]
  # df.to_csv("location_history.csv")
  url = f'https://maps.google.com/?q={message.location.latitude},{message.location.longitude}'
  bot.reply_to(message, f"so {user_name}, you are currently at this location \n{url}")


@bot.message_handler(content_types=['venue'])
def venue(message):
  user_name = message.from_user.username if message.from_user.username != None else message.from_user.first_name
  # df = pd.DataFrame(columns=['date', 'person_name', 'person_id', 'long', 'lat'])
  
  # if os.path.exists("location_history.csv"):
  #   df = pd.read_csv("location_history.csv")

  # row_in_df, _ = df.shape

  # df.loc[int(row_in_df)+1] = [
  #   datetime.datetime.now(),
  #   user_name,
  #   message.from_user.id, 
  #   message.location.longitude,
  #   message.location.latitude
  # ]
  # df.to_csv("location_history.csv")
  url = f'https://maps.google.com/?q={message.location.latitude},{message.location.longitude}'
  bot.reply_to(message, f"so {user_name}, you are currently at this location \n{url}")

@bot.message_handler(commands=['paid'])
def paid(message):
  print('message.photo =', message.photo)
  fileID = message.photo[-1].file_id
  print('fileID =', fileID)
  file_info = bot.get_file(fileID)
  print('file.file_path =', file_info.file_path)
  downloaded_file = bot.download_file(file_info.file_path)

  with open("image.jpg", 'wb') as new_file:
      new_file.write(downloaded_file)
# start_api()
# Thread(target=start_api).start()

bot.infinity_polling()
