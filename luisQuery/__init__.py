import logging
import azure.functions as func
import pandas as pd
import numpy as np
import requests
from io import BytesIO
import json 
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

try:
    with open('./luisQuery/auth.json') as authFile:
        secrets = json.load(authFile)

    luisEndpoint = secrets['luisEndpoint']
    luisKey = secrets['luisKey']

    logging.info('Secrets loaded.')
except: 
    logging.info('Failed to load secrets.')

# Function to call LUIS model 
def callLuis(txt):
    try: 
        resp = requests.get(luisEndpoint + txt.replace(' ', '+'))
        data = json.loads(resp.content.decode("UTF-8"))
    except:
        data = "{'exception':'JSON Decoding Error'}"
    return data

# Function to tokenize messages and call LUIS once for each sentence
def parseMsg(msg):
    # Tokenize the message into an array of sentences
    msgSentences = nltk.sent_tokenize(msg)

    # Call LUIS for each element in the sentence array
    vectorFunc = np.vectorize(callLuis)
    luisResult = vectorFunc(msgSentences)

    # Find the top scoring intents and entities from the luisResult
    intents = '"intents":[ '
    entities = '"entities":[ '
    score = 0

    for i in luisResult:
        try:
            score = json.dumps(i['topScoringIntent']['score'])
            intent = json.dumps(i['topScoringIntent'])
            
            if (float(score) > .60):
                intents += intent + ','
            
            ents = i['entities']
            for e in ents:
                del e['startIndex']
                del e['endIndex']

            if (len(ents) > 0):
                entities += json.dumps(ents)[1:-1] + ','
                
        except:
            score = 0
            
    intents = intents[0:-1] + ']'
    entities = entities[0:-1] + ']'

    result = '{' + intents + ', ' + entities + '}'

    return result

# Look for a message on the query string or in the request body. 
# Run messages against LUIS model and return the top scoring intents. 
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing LUIS request.')

    # Get LUIS Secrets
    msg = req.params.get('msg')
    if not msg:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            msg = req_body.get('msg')

    if msg:
        func.HttpResponse.mimetype = "application/json"
        resp = parseMsg(msg)
        return func.HttpResponse(resp)
    else:
        return func.HttpResponse(
             "Pass text to be analyzed on the query string or in the request body.",
             status_code=400
        )
