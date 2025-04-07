from firebase_admin import firestore

''' my modules '''
from .main import app
from .repldb import get_no_of_message, set_no_of_message



db = firestore.client(app)



def get_all_message():
  ref = db.collection("messages")
  docs = ref.stream()
  all_messages = []
  for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
    all_messages.append(doc.to_dict())
  print(all_messages)
  return all_messages
  

def add_new_message(message:str, senderName:str, senderContact:str):
  
  no_of_message = get_no_of_message()
  doc_ref = db.collection("messages").document(f"demo{no_of_message}")
  doc_ref.set({"message":message, "senderName":senderName, "senderContact": senderContact})
  # set_no_of_message()
  # except:
  #   print("error")
  