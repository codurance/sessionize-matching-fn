import logging

from SessionizeMatching.function import matching

import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    matchRequest = req.params.get('matchRequest')
    pastPairing = req.params.get('previousPairing')
    if not matchRequest:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            matchRequest = req_body.get('matchRequest')

    if matchRequest:
        if not pastPairing:
            result =  matching.match({}, matchRequest)
        result =  matching.match(pastPairing, matchRequest)
        return func.HttpResponse(body = json.dumps(result), mimetype = "application/json")
        # return func.HttpResponse(f"Hello, {matchRequest}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a matchRequest in the query string or in the request body for a personalized response.",
            status_code=200
        )