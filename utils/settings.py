import os
from dotenv import load_dotenv

load_dotenv()

# Constantes para pruebas de UI
WEB_BASE_URL_UI = os.getenv("WEB_BASE_URL_UI", "").strip()
USER_LOGIN_UI = os.getenv("USER_LOGIN_UI", "").strip()
USER_PASSWORD_UI = os.getenv("USER_PASSWORD_UI", "").strip()

# Constantes para pruebas de API
WEB_BASE_URL_API = os.getenv("WEB_BASE_URL_API", "").strip()
USER_ADMIN_API = os.getenv("USER_ADMIN_API", "").strip()
PASS_ADMIN_API = os.getenv("PASS_ADMIN_API", "").strip()
AUTH_SIGNUP = "/auth/signup"
AUTH_LOGIN = "/auth/login/"
USERS = "/users"
AIRPORTS = "/airports"
AIRCRAFT = "/aircrafts"
FLIGHTS = "/flights"