import pytest
import requests
import random
import string
from datetime import datetime, timedelta
from time import sleep, time
from faker import Faker
from requests.exceptions import JSONDecodeError
from utils.settings import USER_ADMIN_API, PASS_ADMIN_API
from pages.API.api_helper import (
    get_admin_token, make_auth_headers, login, signup,
    delete_user_by_id, create_airport, delete_airport_by_code,
    create_aircraft, delete_aircraft_by_code,
    create_flight, delete_flight_by_code,
    create_booking, delete_booking_by_id
)

faker = Faker()

# --------------------- FIXTURES AUTH ---------------------

@pytest.fixture(scope="session")
def admin_token(api_request):
    return get_admin_token(username=USER_ADMIN_API, password=PASS_ADMIN_API, api_request=api_request)

@pytest.fixture
def auth_headers(admin_token):
    return make_auth_headers(admin_token)

# --------------------- FIXTURES LOGIN ---------------------

@pytest.fixture
def api_login(api_request):
    # Devuelve la función de login para usar en los tests
    return login

# --------------------- FIXTURES USERS ---------------------

@pytest.fixture
def temporary_user(auth_headers, api_request):
    email = f"{faker.user_name()}{str(int(time()*100))[-6:]}@example.org"
    password = "password"
    fullname = faker.name()
    # Crear usuario
    r = signup(email, password, fullname, api_request)
    assert r.status_code == 201, f"Signup falló: {r.status_code} - {r.text} - {email}"
    user_data = r.json()
    user_id = user_data.get("id")
    assert user_id, f"Signup no devolvió ID: {user_data}"
    yield {
        "id": user_id,
        "email": email,
        "password": password,
        "full_name": fullname,
    }
    resp = delete_user_by_id(user_id, auth_headers, api_request)
    if not resp:
        print(f"[WARN] No se pudo borrar el usuario {email} con id {user_id}")

@pytest.fixture
def delete_user(api_request, auth_headers):
    created_user_ids = []
    def register(user_id):
        if user_id:
            created_user_ids.append(user_id)
    yield register
    # Teardown: borrar todos los usuarios creados
    for uid in created_user_ids:
        ok = delete_user_by_id(uid, auth_headers, api_request)
        if not ok:
            print(f"[WARN] No se pudo borrar el usuario con id {uid}")

# --------------------- FIXTURES AIRPORTS ---------------------

@pytest.fixture
def temporary_airport(auth_headers, api_request):
    iata_code = faker.unique.bothify(text="???", letters=string.ascii_uppercase)
    city = faker.city()
    country = faker.country()
    # Crear aeropuerto
    r = create_airport(iata_code, city, country, api_request, auth_headers)
    assert r.status_code == 201, f"Signup falló: {r.status_code} - {r.text} - {iata_code}"
    yield {
        "iata_code": iata_code, "city": city, "country": country
    }
    resp = delete_airport_by_code(iata_code, api_request, auth_headers)
    if not resp:
        print(f"[WARN] No se pudo borrar el aeropuerto con iata_code {iata_code}")

@pytest.fixture
def delete_airport(api_request, auth_headers):
    created_iatas = []
    def register(iata_code):
        if iata_code:
            created_iatas.append(iata_code)
    yield register
    # Teardown: borrar todos los aeropuertos creados
    for iata in created_iatas:
        ok = delete_airport_by_code(iata, api_request, auth_headers)
        if not ok:
            print(f"[WARN] No se pudo borrar el aeropuerto IATA={iata}")

# --------------------- FIXTURES AIRCRAFT ---------------------

@pytest.fixture
def temporary_aircraft(auth_headers, api_request):
    tail_number = f"LV-{faker.unique.lexify('???').upper()}"
    model = faker.random_element([
        "Airbus A320", "Airbus A380", "Boeing 737", "Boeing 747",
        "Cessna 172", "Embraer E190", "Bombardier Q400", "Sukhoi Superjet 100",
        "Airbus A321", "Airbus A330", "Boeing 727", "Boeing 787"
    ])
    capacity = random.randint(4, 200)
    # Crear aeronave
    r = create_aircraft(tail_number, model, capacity, api_request, auth_headers)
    aircraft_data = r.json()
    aircraft_id = aircraft_data.get("id")
    assert aircraft_id, f"Create no devolvió ID: {aircraft_data}"
    yield {
        "id": aircraft_id,
        "tail_number": tail_number,
        "model": model,
        "capacity": capacity
    }
    resp = delete_aircraft_by_code(tail_number, api_request, auth_headers)
    if not resp:
        print(f"[WARN] No se pudo borrar la aeronave {tail_number} con aircraft_id {aircraft_id}")

@pytest.fixture
def delete_aircraft(api_request, auth_headers):
    created_tail = []
    def register(tail_number):
        if tail_number:
            created_tail.append(tail_number)
    yield register
    # Teardown: borrar todos las aeronaves creadas
    for tail in created_tail:
        ok = delete_aircraft_by_code(tail, api_request, auth_headers)
        if not ok:
            print(f"[WARN] No se pudo borrar la aeronave TAIL={tail}")

# --------------------- FIXTURES FLIGHTS ---------------------

@pytest.fixture
def temporary_flight(auth_headers, api_request, temporary_aircraft, temporary_airport):
    origin = temporary_airport["iata_code"]
    destination = faker.unique.bothify(text="???").upper()
    departure_time = (datetime.now() + timedelta(hours=1)).isoformat() + "Z"
    arrival_time = (datetime.now() + timedelta(hours=3)).isoformat() + "Z"
    base_price = random.randint(100, 500)
    aircraft_id = temporary_aircraft["id"]
    # Crear vuelo
    r = create_flight(origin, destination, departure_time, arrival_time, base_price, aircraft_id, api_request, auth_headers)
    flight_data = r.json()
    flight_id = flight_data.get("id")
    assert flight_id, f"Create no devolvió ID: {flight_data}"
    yield {
        "id": flight_id,
        "origin": origin,
        "destination": destination,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "base_price": base_price,
        "aircraft_id": aircraft_id
    }
    # Teardown
    resp = delete_flight_by_code(flight_id, api_request, auth_headers)
    if not resp:
        print(f"[WARN] No se pudo borrar el vuelo {flight_id}")

@pytest.fixture
def delete_flight(api_request, auth_headers):
    created_flight = []
    def register(flight_id):
        if flight_id:
            created_flight.append(flight_id)
    yield register
    # Teardown: borrar todos los vuelos creados
    for flight in created_flight:
        ok = delete_flight_by_code(flight, api_request, auth_headers)
        if not ok:
            print(f"[WARN] No se pudo borrar el vuelo FLIGHT_ID={flight}")

# --------------------- FIXTURES BOOKINGS ---------------------

@pytest.fixture
def temporary_booking(auth_headers, api_request, temporary_flight):
    flight_id = temporary_flight["id"]
    passenger = {
        "full_name": faker.name(),
        "passport": faker.bothify(text="??######", letters=string.ascii_uppercase),
        "seat": faker.bothify(text="##?", letters="ABCDEF"),
    }
    # Crear reserva
    r = create_booking(
        passenger["full_name"],
        passenger["passport"],
        passenger["seat"],
        flight_id,
        api_request,
        auth_headers
    )
    booking_data = r.json()
    booking_id = booking_data.get("id")
    assert booking_id, f"Create booking no devolvió ID: {booking_data}"
    yield {
        "id": booking_id,
        "flight_id": flight_id,
        "passenger": passenger
    }
    # Teardown
    ok = delete_booking_by_id(booking_id, api_request, auth_headers)
    if not ok:
        print(f"[WARN] No se pudo borrar la reserva {booking_id}")

@pytest.fixture
def delete_booking(api_request, auth_headers):
    created_bookings = []
    def register(booking_id):
        if booking_id:
            created_bookings.append(booking_id)
    yield register
    # Teardown: borrar todos las reservas creadas
    for booking in created_bookings:
        ok = delete_booking_by_id(booking, api_request, auth_headers)
        if not ok:
            print(f"[WARN] No se pudo borrar la reserva BOOKING_ID={booking}")

# --------------------- REQUEST CON REINTENTOS ---------------------

RETRIES = 10
TIMEOUT = 5
BACKOFF = 0.1
def call_with_retries(method, url, **kw):
    timeout = kw.pop("timeout", TIMEOUT)
    r = None
    for i in range(RETRIES + 1):
        try:
            r = requests.request(method, url, timeout=timeout, **kw)
            try:
                detail = r.json().get("detail")
            except (ValueError, JSONDecodeError, AttributeError):
                detail = None
            # Reintentar para codigos de error 5xx y "Simulated 4xx bug" (hasta "RETRIES" veces)
            if ((500 <= r.status_code < 600) or (detail == "Simulated 4xx bug")) and i < RETRIES:
                sleep(BACKOFF * (2 ** i))
                continue
            return r
        except requests.RequestException:
            if i == RETRIES:
                raise
            sleep(BACKOFF * (2 ** i))
    return r

@pytest.fixture(scope="session")
def api_request():
    # Fixture para enviar requests con reintentos y timeout
    return call_with_retries

# --------------------- LISTAR TODOS LOS ELEMENTOS ---------------------

@pytest.fixture
def fetch_all_elements(api_request):
    def fetch(endpoint, headers=None, limit=100, max_pages=10_000):
        skip = 0
        results = []
        pages = 0
        status_codes = []
        while True:
            pages += 1
            if pages > max_pages:
                break
            r = api_request(
                "GET",
                endpoint,
                headers=headers,
                params={"skip": skip, "limit": limit}
            )
            status_codes.append(r.status_code)
            try:
                elements = r.json()
            except (ValueError, JSONDecodeError):
                elements = []
                break
            if not elements:
                break
            results.extend(elements)
            skip += limit
        return results, {"pages": pages, "status_codes": status_codes,"intentos": len(status_codes)}
    return fetch
