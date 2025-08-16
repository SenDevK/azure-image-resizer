This project demonstrates a modern, event-driven, and serverless architecture built on Microsoft Azure. It consists of a Python Azure Function that is automatically triggered whenever a new image is uploaded to an Azure Blob Storage container.

The function uses the Pillow library to resize the uploaded image into a 128x128 thumbnail and saves the result to a separate output container. All necessary cloud resources (Resource Group, Storage Account, and Function App) were provisioned using the Azure CLI.

Technologies Used: Azure Functions, Azure Blob Storage, Serverless Architecture, Python, Azure CLI.
