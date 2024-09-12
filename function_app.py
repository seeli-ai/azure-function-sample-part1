import azure.functions as func
import logging
import json
import uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ask_for_translation")
@app.queue_output(arg_name="msg", queue_name="translation-requests", connection="AzureWebJobsStorage")
def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        
        # Add a unique identifier to the message
        req_body['id'] = str(uuid.uuid4())
        
        # Convert the request body to a string
        message = json.dumps(req_body)
        
        # Send the message to the queue
        msg.set(message)
        
        return func.HttpResponse(
            f"Message added to the queue successfully. Message ID: {req_body['id']}",
            status_code=200
        )
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON in the request body",
            status_code=400
        )
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )