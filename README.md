# Integration-backend

- Clone the repo using `git clone https://github.com/nayan2608/Integration-backend.git`

- Create Virtual Environment

- Install Dependencies using `pip install -r requirements.txt`

- Create .env file

- Replace .env file contents with the following:

```.env
FLAVOUR=dev

NOTION_CLIENT_ID = 
NOTION_CLIENT_SECRET = 

AIRTABLE_CLIENT_ID = 
AIRTABLE_CLIENT_SECRET = 

HUBSPOT_CLIENT_ID = 
HUBSPOT_CLIENT_SECRET = 

```
Replace your credentials 

- Run the Application `uvicorn app.main:app --reload`
  
- Access the API Docs 
  Swagger UI: http://localhost:8000/docs



