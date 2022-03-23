import threading
import os

from flask import Flask, request


app = Flask(__name__)


# init logger of request & response
try: 
    partner_name = os.environ["partner_name"]
    from utils_db import db_putitem
    log_req_resp = True
    print("""[WARNING] your requests & responses will be logged to IMDA's server. To disable this Feature, comment out 'partner_name' in your docker-compose.yml file""")
except:
    log_req_resp = False



@app.route("/predict", methods=["POST"])
def prediction():
    req = request.json

    # log request
    if log_req_resp:
        threading.Thread(target=db_putitem(req, "request", partner_name, "rre")).start()

    # dummy response
    response = req

    # log response
    if log_req_resp:
        threading.Thread(target=db_putitem(response, "response", partner_name, "rre")).start()

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
