import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

#SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['DATABASE_USER']}:@{os.environ['DATABASE_HOST']}/{os.environ['DATABASE_NAME']}"

###user = os.environ['DATABASE_USER']
###password = os.environ['DATABASE_PASSWORD']
###host = os.environ['DATABASE_HOST']
###port = os.environ['DATABASE_PORT']
###db_name = os.environ['DATABASE_NAME']

###SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
SQLALCHEMY_DATABASE_URL = f"postgresql://basepdfs_4srh_user:FTabMoWIG6cSiSf99m1jt30jp3pZLcYL@dpg-cvcnv0l2ng1s7390lpc0-a/basepdfs_4srh"

                                         
print("%%%%%%%% SQLALCHEMY_DATABASE_URL NO DATABASE.PY %%%%%%%%% ==========> ", SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()