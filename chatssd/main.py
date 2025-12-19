from flask import Flask, request
# from src.utils import getCountry
from ai_agent.agent import create_session, run_root_agent


app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():
  return {"message": "Welcome to Chatssd", "status": "up"}

@app.route("/ussd", methods = ['POST'])
def ussd():
    # phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    
    # country = getCountry(phoneNumber=phone_number)
    if text == '':
        # This is the first request. Note how we start the response with CON
        response  = "CON Welcome to ChatSSD\n"
        response += "Ask question any question \n"
        response += "Type 0 to Exit!"
    elif text == '0':
        response = "END Finished Chatting!"     
    else:
        session = create_session()
        response = run_root_agent(session.id, text)
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
