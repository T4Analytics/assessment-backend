import sys
import os
from fastapi import FastAPI

from modules.helpers import Helpers
from modules.constants import Constants

from routes import auth
from routes import attendees
from routes import choices
from routes import customers
from routes import customer_tests
from routes import optiongroups
from routes import papers
from routes import partner_tests
from routes import partners
from routes import questions
from routes import sessions
from routes import tests
from routes import users

# this is important, you can't import from an external folder without this
# sys.path.append(os.path.realpath(".."))
sys.path.append(os.path.realpath("."))

h = Helpers()
c = Constants()


app = FastAPI(
	title="T4Analytics Assessment API",
	description="t4analytics.com",
	version="1.0.0",
	contact={
		"name": "Necmettin Begiter",
		"email": "necmettin@t4analytics.com",
		"url": "https://t4analytics.com"
	},
	openapi_tags=[
		{"name": "auth", "description": "Auth"},
		{"name": "partners", "description": "Partners"},
		{"name": "users", "description": "Users"},
		{"name": "customers", "description": "Customers"},
		{"name": "attendees", "description": "Attendees"},
		{"name": "tests", "description": "Tests"},
		{"name": "partner_tests", "description": "Tests Available to Partners"},
		{"name": "customer_tests", "description": "Tests Assigned to Customers"},
		{"name": "questions", "description": "Questions in Tests"},
		{"name": "perms", "description": "Permissions"},
		{"name": "papers", "description": "Papers"},
		{"name": "optiongroups", "description": "Option Groups (for each question)"},
		{"name": "sessions", "description": "Sessions (Open or Finished)"},
		{"name": "choices", "description": "Users' Choices in Tests"},
	],
	docs_url="/api/v1/docs",
	redoc_url="/api/v1/redoc",
	openapi_url="/api/v1/openapi.json"
)


@app.get("/", tags=["root"], include_in_schema=False)
@app.get("/api/", tags=["root"], include_in_schema=False)
@app.get("/api/v1/", tags=["root"], include_in_schema=False)
def root():
	return h.err(303, {"url": c.docsurl})


app.include_router(auth.router)
app.include_router(attendees.router)
app.include_router(choices.router)
app.include_router(customers.router)
app.include_router(customer_tests.router)
app.include_router(optiongroups.router)
app.include_router(papers.router)
app.include_router(partner_tests.router)
app.include_router(partners.router)
app.include_router(questions.router)
app.include_router(sessions.router)
app.include_router(tests.router)
app.include_router(users.router)
