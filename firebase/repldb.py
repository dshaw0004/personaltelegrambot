def set_no_of_message():
  with open('no_of_message.txt', 'r') as f:
    no = int(f.read())
  with open('no_of_message.txt', 'w') as f:
    f.write(str(no + 1))

def get_no_of_message(): 
  with open('no_of_message.txt', 'r') as f:
    no = int(f.read())
