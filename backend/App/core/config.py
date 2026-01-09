from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    def __init__(self) -> None:
        self.__PROJECT_NAME = "MeetUp - AI Powered Meeting Platform"
        self.__PROJECT_VERSION = "0.1.0"
        self.__PROJECT_DESCRIPTION = "This project serves as tool to ease out project meeting tasks."
        self.__GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.__SQL_DATABASE_URL = "sqlite:///./MeetUp.db"
        self.__SECRET_KEY = "16bbc3d6873f2db90079fd8043b6c751"
        self.__ALGORITHM = "HS256"

    def get_project_name(self):
        return self.__PROJECT_NAME
    
    def get_project_description(self):
        return self.__PROJECT_DESCRIPTION
    
    def get_project_version(self):
        return self.__PROJECT_VERSION
    
    def get_gemini_api_key(self):
        return self.__GEMINI_API_KEY
    
    def get_sql_database_url(self):
        return self.__SQL_DATABASE_URL
    
    def get_secret_key(self):
        return self.__SECRET_KEY
    
    def get_algorithm(self):
        return self.__ALGORITHM

setting = Settings()