from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.controllers.ApplicationController import mainApplicationFlow
from src.credentials import username as user, password as passwrd
from src.models import *

# Configure Database:

db_string = "postgresql://" + user + ":" + passwrd + "@reddwarf.cs.rit.edu:5432/p320_03d"
db = create_engine(db_string)
Session = sessionmaker()
Session.configure(bind=db)

# Create the Models in the Database
Base.metadata.create_all(db)



# Application
mainApplicationFlow(Session())
