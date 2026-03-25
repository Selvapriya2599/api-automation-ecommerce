import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL","https://reqres.in")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
MANAGE_KEY= os.getenv("MANAGE_KEY")