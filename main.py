from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from credentials import username, password

db_string = "postgresql://" + username + ":" + password + "@reddwarf.cs.rit.edu:5432/p320_03d"
db = create_engine(db_string)

