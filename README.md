# SkyLine API

SkyLine is an API for booking flights. This project is built using Django REST Framework.

## Features

- User authentication and authorization using Djoser and JWT.
- API documentation using Swagger and ReDoc.
- Flight booking functionalities.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/SkyLine.git
    cd SkyLine
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

- Admin: `/admin/`
- API: `/api/`
- Authentication: `/auth/`
- Swagger UI: `/`
- ReDoc: `/redoc/`

## License

This project is licensed under the Test License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact suskidee@gmail.com.
