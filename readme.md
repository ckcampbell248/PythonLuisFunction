# Python Azure Function to call LUIS Service for text analysis
This project contains code to deploy a Python Azure Function. It parses a message text sent in the request body (msg) into sentences and then calls a LUIS model for each sentence to determine intents. Only intents with a score > .60 are returned. 
## LUIS Secrets
Secrets are stored in the file auth.json. A template version of this file is included in the project (auth_template.json). Rename this file and include your LUIS endpoint and key in the file. 
## Deploying to Azure Functions
To set up a VS Code development environment for Azure functions, start with [https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python)
