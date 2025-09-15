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

### 🔹 Tests de UI (ShopHub Commerce)

Estos tests usan **Selenium + Pytest** para validar la experiencia de usuario en el sitio de compras:

- **`test_homepage.py`**  
  Verifica que la página principal cargue correctamente y que los elementos clave estén presentes (títulos, botones, productos).

- **`test_checkout.py`**  
  - Valida los **placeholders** de los inputbox en el proceso de checkout.  
  - Captura un **screenshot en caso de fallo** para facilitar el debugging.

- **`test_login_ui.py`**  
  - Casos positivos: login exitoso con credenciales válidas.  
  - Casos negativos: manejo de errores con credenciales inválidas o campos vacíos.

- **`test_navigation.py`**  
  Confirma la correcta navegación entre secciones (inicio → productos → carrito → checkout → confirmación).

---

### 🔹 Tests de API (Backends Aerolínea)

Estos tests validan los endpoints REST usando **requests + Pytest**.

- **`test_auth_api.py`**  
  - **Login** con credenciales correctas retorna `200 OK` y token válido.  
  - **Login fallido** retorna errores esperados (`401`, `422`).

- **`test_users_api.py`**  
  - Obtener lista de usuarios.  
  - Crear usuario nuevo (positivo y negativo: email duplicado).  
  - Eliminar usuario temporal de pruebas.

- **`test_airports_api.py`**  
  - Validación de endpoints `/airports` de la aerolínea.  
  - Respuesta en formato JSON y estructura de datos esperada.

- **`test_movies_api.py`**  
  - Validación de cartelera y detalles de películas en la API de cine.  
  - Comprobación de que los campos requeridos existan.

---

## 📂 Estructura del Repositorio

```
qa/
│── pages/                     
│   ├── UI/                    # Page Objects / Modelos para pruebas de UI
│   ├── API/
│       ├── api_helper.py      # Definicion del API Helper para pruebas de API
│── tests/
│   ├── tests_UI/              # Pruebas de UI con Selenium (ShopHub Commerce)
│   ├── tests_API/             # Pruebas de API (Aerolínea)
│       ├── conftest.py        # Fixtures compartidos para pruebas de API
│── utils/
│   ├── driver_factory.py      # Definicion de drivers Selenium
│   ├── settings.py            # Configuración a partir de variables de entorno
│── .env                       # Variables de entorno: credenciales y constantes
│── pytest.ini                 # Configuración de Pytest (rutas y marcadores)
│── requirements.txt           # Librerías y dependencias del proyecto
│── README.md                  # Documentación del proyecto
```

---

## 🔧 Tecnologías Utilizadas

- [Python 3.x](https://www.python.org/)  
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

En caso de fallo en los tests de UI, se genera automáticamente un **screenshot** que se guarda en la carpeta `./screenshots/`.

---

## 👨‍💻 Autores

Proyecto desarrollado con fines de práctica académica para CodigoFacilito (C) por Dario Ajlin  
Puedes usarlo como referencia para tus propios proyectos de QA.

---

# ⚙️ CI/CD con GitHub Actions

Para ejecutar los tests automáticamente en cada push/pull request, crea el archivo:  

**`.github/workflows/tests.yml`**

```yaml
name: Run QA Tests

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run pytest
      run: |
        pytest -v --tb=short --maxfail=3 --disable-warnings
```
