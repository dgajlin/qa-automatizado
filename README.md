# 📘 Proyecto de Pruebas Automatizadas – QA

Este repositorio contiene un conjunto de **tests automatizados** desarrollados en **Pytest** para validar tanto la **interfaz de usuario (UI)** como los **endpoints de API** de aplicaciones demo:  

- 🛒 **E-commerce (UI)**: `https://shophub-commerce.vercel.app`  
- 🛫 **Aerolínea (API)**: `https://cf-automation-airline-api.onrender.com`  

El objetivo es contar con una **suite E2E (End-to-End)** que asegure la calidad de las aplicaciones a nivel frontend y backend.

---

## 🚀 Comenzando

### Clonar el repositorio
```bash
git clone https://github.com/<tu-usuario>/<tu-repo>.git
cd qa
```

### Crear y activar entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar pruebas
```bash
python -m pytest -v --tb=short
```

### Ejecutar pruebas de UI
```bash
python -m pytest -q tests/tests_UI
```

### Ejecutar pruebas de API
```bash
python -m pytest -q tests/tests_API
```

Con reporte HTML:
```bash
python -m pytest -v --tb=short --html=report.html --self-contained-html
```

---

## 🧪 Estructura de Tests

### 🔹 Tests de UI (Frontend ShopHub Commerce)

Estos tests usan **Selenium + Pytest** para validar la experiencia de usuario en el sitio de compras:

- test_login_ui.py: login en la aplicación web con Selenium (credenciales válidas/erróneas)
- test_purchase_e2e.py: flujo end-to-end de compra (login → carrito → checkout → confirmación -> pago)
- test_validation.py: validación de campos del formulario (placeholders, mensajes de error, restricciones)

---

### 🔹 Tests de API (Funcionales)

Estos tests validan los endpoints REST usando **requests + Pytest**.

**Aircraft**:
  - test_create_aircraft.py: crea un nuevo avión y valida status/response
  - test_delete_aircraft.py: elimina un avión existente
  - test_list_aircraft.py: lista todos los aviones disponibles
  - test_update_aircraft.py: actualiza datos de un avión

**Airports**:
  - test_create_airport.py: crea un nuevo aeropuerto
  - test_delete_airport.py: elimina un aeropuerto existente
  - test_list_airports.py: lista aeropuertos
  - test_update_airport.py: actualiza datos de un aeropuerto

**Flights**:
  - test_create_flight.py: crea un vuelo nuevo
  - test_delete_flight.py: elimina un vuelo
  - test_list_flight.py: lista vuelos existentes
  - test_update_flight.py: actualiza datos de un vuelo

**Users**:
  - test_login_api.py: login de usuario
  - test_signup.py: signup de usuario nuevo
  - test_list_users.py: obtener lista de usuarios
  - test_update_user.py: actualizar datos de usuario
  - test_delete_user.py: eliminar usuario

---

### 🔹 Tests de Schema (Validación de contratos)

Estos tests validan que las respuestas de la API cumplen con los **JSON Schema** definidos.

**Aircraft**:
  - test_create_schema_aircraft.py: validar esquema de creación de avión

**Airports**:
  - test_create_schema_airport.py: validar esquema de creación de aeropuerto

**Flights**:
  - test_create_schema_flight.py: validar esquema de creación de vuelo

**Users**:
  - test_login_schema.py: validar esquema de login
  - test_signup_schema.py: validar esquema de signup de usuario

---

## 📂 Estructura del Repositorio

```
qa/
│── pages/                     
│   ├── UI/                    # Page Objects / Modelos para pruebas de UI
│   ├── API/
│       ├── api_helper.py      # Definición del API Helper para pruebas de API
│── tests/
│   ├── tests_UI/              # Pruebas de UI con Selenium (ShopHub Commerce)
│   ├── tests_API/             # Pruebas de API (Aerolínea)
│       ├── api/               # Pruebas funcionales de API
│       ├── schema/            # Pruebas de schema de API
│       ├── conftest.py        # Fixtures compartidos para pruebas de API
│── utils/
│   ├── driver_factory.py      # Definición de drivers Selenium
│   ├── settings.py            # Seteos desde las variables de entorno
│── .env                       # Variables de entorno: credenciales y constantes
│── pytest.ini                 # Configuración de Pytest (rutas y marcadores)
│── requirements.txt           # Librerías y dependencias del proyecto
│── README.md                  # Documentación del proyecto
```

---

## 🔧 Tecnologías Utilizadas

- [Python 3.11](https://www.python.org/)  
- [Pytest](https://docs.pytest.org/)  
- [Selenium](https://www.selenium.dev/)  
- [Requests](https://docs.python-requests.org/)  
- [Allure / HTML Reports](https://docs.qameta.io/allure/)  

---

## 🤝 Contribuir

1. Haz un **Fork** del repositorio.  
2. Crea una rama para tu feature/fix:  
   ```bash
   git checkout -b mi-nueva-feature
   ```
3. Realiza tus cambios y haz commit:  
   ```bash
   git commit -m "Agrego test de login negativo"
   ```
4. Haz push a tu rama:  
   ```bash
   git push origin mi-nueva-feature
   ```
5. Abre un **Pull Request** en GitHub.

---

## 📸 Evidencias

En caso de fallo en los tests de UI, se genera automáticamente un **screenshot** que se guarda en la carpeta `screenshots/`.
Paralelamente, los reportes se guardan en la carpeta raíz con el nombre ingresado por parametro al ejecutar la prueba. 

---

## 👨‍💻 Autores

Proyecto desarrollado con fines de práctica académica para codigofacilito© por Dario Ajlin  
Puedes usarlo como referencia para tus propios proyectos de QA.

---

# ⚙️ CI/CD con GitHub Actions

Para ejecutar los tests automáticamente en cada push/pull request, se crea el archivo:  

**`.github/workflows/tests.yml`**

```yaml
name: CI QA Tests
run-name: CI ${{ github.ref_name }}

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
  
jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Instalar Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        
    - name: Cache pip
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: pip-${{ runner.os }}-${{ hashFiles('**/requirements*.txt') }}
        restore-keys: |
          pip-${{ runner.os }}-

    - name: Instalar dependencias
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then
          pip install -r requirements.txt
        else
          pip install pytest selenium webdriver-manager pytest-html pytest-cov behave pytest-bdd
        fi

    - name: Instalar Google Chrome
      uses: browser-actions/setup-chrome@v1
      with:
        chrome-version: stable

    - name: Ejecutar pruebas con Pytest
      run: |
        export PYTHONPATH=$PYTHONPATH:$(pwd)
        pytest -v --tb=short --maxfail=3 --disable-warnings

    - name: Carga de artefactos (reportes y screenshots)
      if: ${{ always() }}
      uses: actions/upload-artifact@v4
      with:
        name: test-artifacts
        path: |
          reports/**
          screenshots/**
        if-no-files-found: ignore
```
