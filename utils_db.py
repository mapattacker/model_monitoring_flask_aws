import boto3
from time import time


dynamodb = boto3.resource('dynamodb')

def db_putitem(item, type, partner_name, project_code, company="xxx", department="yyy"):
    """upload requests & responses to dynamodb
    takes >0.15s to upload, use a separate thread when using this function
    note, DB table must have a timestamp as partition key, with type as number
    Only give item put access for permissions
    
    Args:
        item (json): request or reponse from API
        type (str): 'request' or 'response'
        partner_name (str): denotated by TP's synonym, e.g. TP1 or TP2
        project_code (str): as described"""

    timestamp = int(str(time()).replace(".",""))
    item["timestamp"] = timestamp

    table_name = f"dynamodb-{company}-{department}-{project_code}-{partner_name}-{type}"

    table = dynamodb.Table(table_name)
    table.put_item(Item= item)



if __name__ == "__main__":
    partner_name = "tp1"
    project_code = "rre"
    type = "request"
    item = {"prediction": "yes"}
    

    start = time()
    import threading
    threading.Thread(target=db_putitem(item, type, partner_name, project_code)).start()

    db_putitem(item, type, partner_name, project_code)
    print(time()- start)
