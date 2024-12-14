# My Social Media API

I've built a robust Django REST Framework-based social media API that provides a comprehensive set of features for building a social media platform.

## Features

- User Authentication (JWT-based)
- User Profile Management
- Post Creation and Management
- Media Upload Support
- Friend/Follow System
- API Documentation

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Setup Instructions

1. Clone the repository:
   ```cmd
   git clone <repository-url>
   cd My_capstone
   ```

2. Create and activate a virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=your_database_url (optional)
   ```

5. Apply database migrations:
   ```cmd
   python manage.py migrate
   ```

6. Create a superuser (admin):
   ```cmd
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```cmd
   python manage.py runserver
   ```

You can access the API at `http://localhost:8000/`

## API Documentation

I've provided detailed documentation in these files:
- `API_DOCUMENTATION.md`: Complete API endpoints documentation
- `authentication.md`: Authentication system documentation
- `ERD_Documentation.md`: Database schema documentation

## Dependencies

I'm using these packages:
- Django 5.0
- Django REST Framework 3.14.0
- djangorestframework-simplejwt 5.3.1
- python-dotenv 1.0.0
- Pillow 10.1.0
- django-cors-headers 4.3.1
- psycopg2-binary 2.9.9
- gunicorn 21.2.0
- whitenoise 6.6.0

## Project Structure

```
My_capstone/
├── api/                    # Main API application
├── social_media_api/       # Project settings
├── media/                  # Media files storage
├── requirements.txt        # Project dependencies
└── manage.py              # Django management script
```

## Contributing

If you'd like to contribute:
1. Fork my repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

I've licensed this project under the MIT License - see the LICENSE file for details.
