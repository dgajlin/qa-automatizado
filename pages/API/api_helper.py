from utils.settings import WEB_BASE_URL_API, AUTH_LOGIN, AUTH_SIGNUP, USERS, AIRPORTS, AIRCRAFT, FLIGHTS, BOOKINGS

# --------------------- AUTH ---------------------

def login(username, password, api_request):
    # Login
    payload = {"username": username, "password": password}
    return api_request(
        "POST",
        f"{WEB_BASE_URL_API}{AUTH_LOGIN}/",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

def get_admin_token(username, password, api_request):
    # Obtener el token del admin y validar respuesta
    r = login(username, password, api_request)
    assert r.status_code in (200, 201), f"Login admin falló: {r.status_code} - {r.text}"
    token = r.json().get("access_token")
    assert token, f"Respuesta de login sin access_token: {r.text}"
    return token

def make_auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

# --------------------- USERS ---------------------

def create_admin(email, password, full_name, api_request, auth_headers):
    payload = {"email": email, "password": password, "full_name": full_name, "role": "admin"}
    return api_request(
        "POST",
        f"{WEB_BASE_URL_API}{USERS}",
        json=payload,
        headers=auth_headers
    )

def signup(email, password, full_name, api_request):
    # Crear usuario
    payload = {"email": email, "password": password, "full_name": full_name}
    return api_request(
        "POST",
        f"{WEB_BASE_URL_API}{AUTH_SIGNUP}",
        json=payload
    )

def delete_user_by_id(user_id, auth_headers, api_request):
    # Eliminar usuario por ID
    if not user_id:
        return False
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{USERS}/{user_id}",
        headers=auth_headers
    )
    return r.status_code == 204

# --------------------- AIRPORTS ---------------------

def create_airport(iata_code, city, country, api_request, auth_headers):
    # Crear aeropuerto
    payload = {"iata_code": iata_code, "city": city, "country": country}
    return api_request(
        "POST",
        f"{WEB_BASE_URL_API}{AIRPORTS}",
        headers=auth_headers,
        json=payload
    )

def delete_airport_by_code(iata_code, api_request, auth_headers):
    # Eliminar aeropuerto por IATA_CODE
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRPORTS}/{iata_code}",
        headers=auth_headers
    )
    return r.status_code == 204

# --------------------- AIRCRAFT ---------------------

def create_aircraft(tail_number, model, capacity, api_request, auth_headers):
    # Crear aeronave
    payload = {"tail_number": tail_number, "model": model, "capacity": capacity}
    return api_request(
        "POST",
        f"{WEB_BASE_URL_API}{AIRCRAFT}",
        headers=auth_headers,
        json=payload
    )

def delete_aircraft_by_code(aircraft_id, api_request, auth_headers):
    # Eliminar aeronave por AIRCRAFT_ID
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRCRAFT}/{aircraft_id}",
        headers=auth_headers
    )
    return r.status_code == 204

# --------------------- FLIGHT ---------------------

def create_flight(origin, destination, departure_time, arrival_time, base_price, aircraft_id, api_request, auth_headers):
    # Crear vuelo
    payload = {
        "origin": origin,
        "destination": destination,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "base_price": base_price,
        "aircraft_id": aircraft_id
    }
    return api_request(
        "POST",
        f"{WEB_BASE_URL_API}{FLIGHTS}",
        headers=auth_headers,
        json=payload
    )

def delete_flight_by_code(flight_id, api_request, auth_headers):
    # Eliminar vuelo por FLIGHT_ID
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{FLIGHTS}/{flight_id}",
        headers=auth_headers
    )
    return r.status_code == 204

# --------------------- BOOKING ---------------------

def create_booking(full_name, passport, seat, flight_id, api_request, auth_headers):
    # Crear Reserva
    passenger = {
        "full_name": full_name,
        "passport": passport,
        "seat": seat,
    }
    payload = {
        "flight_id": flight_id,
        "passengers": [passenger]
    }
    return api_request(
        "POST",
        f"{WEB_BASE_URL_API}{BOOKINGS}",
        headers=auth_headers,
        json=payload
    )

def delete_booking_by_id(booking_id, api_request, auth_headers):
    # Eliminar reserva por BOOKING_ID
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{BOOKINGS}/{booking_id}",
        headers=auth_headers
    )
    return r.status_code == 204
