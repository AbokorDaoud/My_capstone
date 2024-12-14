# Authentication Setup and Testing Guide

## Authentication System

This API uses JSON Web Tokens (JWT) for authentication. When users login successfully, they receive a token that must be included in subsequent requests to authenticate them.

## Token Format

The authentication token should be included in the HTTP header of each request:
```
Authorization: Bearer <your_token_here>
```

## Setting Up Authentication

1. Install required packages:
```bash
pip install djangorestframework-simplejwt
```

2. Add to your Django settings:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': YOUR_SECRET_KEY,
}
```

## Testing Authentication

### Using cURL

1. Register a new user:
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123","email":"test@example.com"}'
```

2. Login to get token:
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

3. Use the token in subsequent requests:
```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer <your_token_here>"
```

### Using Postman

1. Create a new request
2. Set the request method (GET, POST, etc.)
3. Add the Authorization header:
   - Click on the "Headers" tab
   - Add a new header with key "Authorization" and value "Bearer <your_token_here>"

### Common Authentication Issues

1. Token expired
   - Error: "Token has expired"
   - Solution: Get a new token by logging in again

2. Invalid token format
   - Error: "Invalid token header. No credentials provided"
   - Solution: Ensure the token is prefixed with "Bearer "

3. Missing token
   - Error: "Authentication credentials were not provided"
   - Solution: Add the Authorization header with the token

## Security Best Practices

1. Always use HTTPS in production
2. Store tokens securely (e.g., in HttpOnly cookies)
3. Implement token refresh mechanism
4. Set appropriate token expiration times
5. Implement rate limiting
6. Use strong passwords
7. Implement password reset functionality
