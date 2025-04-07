import os


def set_no_of_message():
  if os.path.exists('no_of_message.txt'):
    with open('no_of_message.txt', 'r') as f:
      no = int(f.read())
    with open('no_of_message.txt', 'w') as f:
      f.write(str(no + 1))
  else:
    with open('no_of_message.txt', 'w') as f:
      f.write('1')

def get_no_of_message(): 
  if os.path.exists('no_of_message.txt'):
    with open('no_of_message.txt', 'r') as f:
      no = int(f.read())
    return no
  else:
    return 0