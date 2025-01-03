# Testing API Endpoints with Postman: A Comprehensive Guide

## Why Choose Postman Over Browsers?

### 1. Advanced Request Capabilities
- Support for all HTTP methods (GET, POST, PUT, DELETE, etc.)
- Easy handling of request headers and authentication tokens
- Better management of request bodies (JSON, form-data, raw text)
- Built-in support for file uploads

### 2. Request Organization
- Create collections to group related requests
- Save and reuse requests
- Share collections with team members
- Create environments for different setups (local, staging, production)

### 3. Testing Features
- Automated testing capabilities
- Environment variables for dynamic values
- Pre-request and post-request scripts
- Response validation

### 4. Better Debugging
- Detailed response information
- Status codes clearly displayed
- Response headers easily visible
- Response timing information
- Pretty-printing of JSON responses

### 5. Documentation
- Auto-generate API documentation
- Export collections for sharing
- Create example requests and responses

## Step-by-Step Guide to Testing Our API

### Step 1: Initial Setup
1. Download and install Postman from [https://www.postman.com/downloads/](https://www.postman.com/downloads/)
2. Create a new collection called "Social Media API"
3. Set up an environment:
   - Click "Environments" in the sidebar
   - Create a new environment called "Render"
   - Add variables:
     - `base_url`: `https://social-media-alx-project.onrender.com`
     - `token`: (Leave empty initially)

### Step 2: Authentication Endpoints

#### Register a New User - Detailed Steps

1. Open Postman and create a new request
2. Set the request method to `POST`
3. Enter the URL: `{{base_url}}/api/auth/register/`
4. Set up the request:
   - Click on the "Headers" tab
   - Add header: `Content-Type: application/json`
   - Click on the "Body" tab
   - Select "raw" and choose "JSON" from the dropdown
   - Enter this JSON in the body:
   ```json
   {
       "username": "testuser1",
       "email": "testuser1@example.com",
       "password": "testpass123",
       "first_name": "Test",
       "last_name": "User"
   }
   ```
5. Click "Send"
6. Expected Response (201 Created):
   ```json
   {
       "user": {
           "id": 1,
           "username": "testuser1",
           "email": "testuser1@example.com"
       },
       "refresh": "your_refresh_token",
       "access": "your_access_token"
   }
   ```
7. Save the `access` token for future requests

Common Registration Issues:
- Username already exists
- Invalid email format
- Password too short
- Missing required fields

Tips:
- Keep track of the credentials you use
- Save the request in your Postman collection
- Test with invalid data to see error responses

#### Login - Detailed Steps

1. Create a new request in Postman
2. Set the request method to `POST`
3. Enter the URL: `{{base_url}}/api/auth/login/`
4. Set up the request:
   - Click on the "Headers" tab
   - Add header: `Content-Type: application/json`
   - Click on the "Body" tab
   - Select "raw" and choose "JSON" from the dropdown
   - Enter this JSON in the body:
   ```json
   {
       "username": "testuser1",
       "password": "testpass123"
   }
   ```
5. Click "Send"
6. Expected Response (200 OK):
   ```json
   {
       "refresh": "your_refresh_token",
       "access": "your_access_token"
   }
   ```

7. Save the tokens:
   - Copy the `access` token
   - In Postman environments:
     - Click "Environments" in the sidebar
     - Select your environment
     - Find the variable `token`
     - Paste the access token in the "Current Value" field
     - Click "Save"

Now you can use this token for authenticated requests:
1. In any new request, go to the "Headers" tab
2. Add: `Authorization: Bearer {{token}}`

Common Login Issues:
- Incorrect username or password
- Token not properly saved in environment
- Token expired (use refresh token to get new access token)

Tips:
- Keep your tokens secure
- Don't share requests with active tokens
- If you get 401 Unauthorized, try refreshing your token

#### Login
```
POST {{base_url}}/api/auth/login/
Body (raw JSON):
{
    "username": "testuser1",
    "password": "testpass123"
}
```
- After successful login, copy the access token
- Set the environment variable `token` to this value

#### Creating a Post - Detailed Steps

1. Create a new request in Postman
2. Set the request method to `POST`
3. Enter the URL: `{{base_url}}/api/posts/`
4. Set up Authentication:
   - Click the "Authorization" tab
   - Type: "Bearer Token"
   - Token: Paste your access token or use `{{token}}`

5. Set up the request body:
   - Click on the "Body" tab
   - Select "raw" and choose "JSON" from the dropdown
   - Enter this JSON in the body:
   ```json
   {
       "content": "My first post using Postman!",
       "visibility": "public"
   }
   ```

6. Click "Send"
7. Expected Response (201 Created):
   ```json
   {
       "id": 1,
       "user": {
           "id": 1,
           "username": "testuser1"
       },
       "content": "My first post using Postman!",
       "visibility": "public",
       "created_at": "2024-12-30T15:55:24Z",
       "updated_at": "2024-12-30T15:55:24Z"
   }
   ```

Common Post Creation Issues:
- 401 Unauthorized: Token missing or expired
- 400 Bad Request: Missing required fields
- 413 Payload Too Large: Image file too big

Tips:
- Make sure your Authorization header is set correctly
- For image uploads, use form-data not raw JSON
- Keep image files under the size limit
- Test both with and without images

Next Steps After Creating a Post:
1. Try viewing all posts (GET /api/posts/)
2. View your specific post (GET /api/posts/1/)
3. Update your post (PUT /api/posts/1/)
4. Test the feed endpoint (GET /api/feed/)

Would you like to try any of these operations next?

### Step 3: Setting Up Authentication
1. Create a folder in your collection for authenticated requests
2. Add this to the folder's Authorization tab:
   - Type: Bearer Token
   - Token: {{token}}
3. All requests in this folder will inherit this authentication

### Step 4: Testing User Endpoints

#### Get All Users
```
GET {{base_url}}/api/users/
```

#### Get Single User
```
GET {{base_url}}/api/users/1/
```

#### Update User
```
PUT {{base_url}}/api/users/1/
Body (raw JSON):
{
    "bio": "Updated bio"
}
```

### Step 5: Testing Post Endpoints

#### Create Post
```
POST {{base_url}}/api/posts/
Body (raw JSON):
{
    "content": "This is my first test post",
    "visibility": "public"
}
```

#### Get All Posts
```
GET {{base_url}}/api/posts/
```

#### Get Single Post
```
GET {{base_url}}/api/posts/1/
```

### Step 6: Testing Follow System

#### Testing Follow Functionality - Detailed Steps

1. First, Create Another User to Follow
   ```
   POST {{base_url}}/api/auth/register/
   Body (raw JSON):
   {
       "username": "testuser2",
       "email": "testuser2@example.com",
       "password": "testpass123",
       "first_name": "Test",
       "last_name": "User"
   }
   ```
   - Save this user's ID from the response

2. Follow the User
   - Create a new request in Postman
   - Set the request method to `POST`
   - URL: `{{base_url}}/api/users/{user_id}/follow/`
     (Replace {user_id} with the ID of the user you want to follow)
   
   Headers:
   ```
   Authorization: Bearer {{token}}
   Content-Type: application/json
   ```

   - Click "Send"
   - Expected Response (200 OK):
   ```json
   {
       "detail": "You are now following testuser2"
   }
   ```

3. Test Unfollow
   - Send the same POST request again to the same endpoint
   - This will unfollow the user
   - Expected Response (200 OK):
   ```json
   {
       "detail": "You have unfollowed testuser2"
   }
   ```

Common Follow/Unfollow Issues:
- 401 Unauthorized: Token missing or expired
- 404 Not Found: User ID doesn't exist
- 400 Bad Request: Trying to follow yourself

Testing Tips:
1. Try following multiple users
2. Verify follow status by checking your feed
3. Test error cases:
   - Try following yourself
   - Try following non-existent users
   - Try following without authentication

Next Steps After Following:
1. View your feed to see posts from followed users (GET /api/feed/)
2. Create posts as different users to test the feed
3. Test unfollowing users

Would you like to try any of these operations next?

#### Follow User
```
POST {{base_url}}/api/users/2/follow/
```

### Step 7: Testing Feed

#### Get User Feed
```
GET {{base_url}}/api/feed/
```

## Best Practices

### 1. Environment Management
- Create separate environments for local and production
- Never hardcode sensitive data
- Use variables for base URLs and tokens

### 2. Request Organization
- Group related requests in folders
- Use descriptive names for requests
- Add descriptions to complex requests

### 3. Testing Workflow
1. Start with authentication
2. Test happy paths first
3. Then test error cases
4. Verify response status codes
5. Check response body structure

### 4. Security
- Never share collections with tokens
- Reset sensitive data before sharing
- Use environment variables for sensitive data

## Common Issues and Solutions

### 1. Authentication Issues
- Check if token is correctly set in environment
- Verify token hasn't expired
- Ensure Authorization header is correct

### 2. File Upload Issues
- Use form-data for file uploads
- Set correct Content-Type header
- Check file size limits

### 3. CORS Issues
- These won't appear in Postman (advantage over browsers)
- Useful for isolating CORS vs API issues

## Testing Checklist

- [ ] Authentication endpoints working
- [ ] Can create new users
- [ ] Can create posts with images
- [ ] Can follow/unfollow users
- [ ] Feed shows correct posts
- [ ] Profile updates working
- [ ] Error handling working correctly
- [ ] Response formats are consistent
- [ ] Status codes are appropriate

## Conclusion

Postman provides a robust environment for API testing that surpasses browser capabilities. By following this guide and utilizing Postman's features, you can effectively test and debug your API endpoints.

Remember to:
1. Keep your environment variables updated
2. Save your requests after testing
3. Document any special requirements
4. Test both success and failure cases

## Social Media API - Postman Testing Guide

## Base URL
```
https://social-media-alx-project.onrender.com
```

## Authentication
- Most GET endpoints are public
- POST, PUT, DELETE endpoints require authentication
- Use JWT tokens for authentication

## 1. User Management

### 1.1 Create User (Register)
- **Endpoint**: `POST /api/auth/register/`
- **Body** (raw JSON):
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "your_password",
    "first_name": "Test",
    "last_name": "User"
}
```
- **Note**: All fields are required
- **Response**: Returns user data and token

### 1.2 User Login
- **Endpoint**: `POST /api/auth/login/`
- **Body** (raw JSON):
```json
{
    "username": "testuser",
    "password": "your_password"
}
```
- **Response**: Returns access and refresh tokens

### 1.3 View User Profile
- **Endpoint**: `GET /api/users/{user_id}/`
- **Auth**: Not required
- **Response**: Returns user profile data

## 2. Posts

### 2.1 Create Post
- **Endpoint**: `POST /api/posts/`
- **Auth**: Required
- **Body** (raw JSON):
```json
{
    "content": "This is a test post",
    "visibility": "public"
}
```
- **Note**: visibility can be "public", "private", or "followers"

### 2.2 Get Posts
- **Endpoint**: `GET /api/posts/`
- **Auth**: Not required
- **Response**: Returns list of public posts

### 2.3 Get Single Post
- **Endpoint**: `GET /api/posts/{post_id}/`
- **Auth**: Not required
- **Response**: Returns post details

## 3. Feed

### 3.1 Get Feed
- **Endpoint**: `GET /api/feed/`
- **Auth**: Not required for public posts
- **Response**: 
  - Unauthenticated: Returns public posts
  - Authenticated: Returns personalized feed

## 4. Follow System

### 4.1 Follow User
- **Endpoint**: `POST /api/users/{user_id}/follow/`
- **Auth**: Required
- **Response**: Returns follow status

## Testing Steps

1. **Create Test Users**:
   - Create at least 2 test users using the register endpoint
   - Save their credentials
   - Verify you can log in with both users

2. **Test Post Creation**:
   - Login with first user
   - Create a post
   - Verify post appears in feed

3. **Test Follow System**:
   - Login with second user
   - Follow first user
   - Verify first user's posts appear in second user's feed

## Common Issues & Solutions

1. **Authentication Issues**:
   - Make sure to include token in Authorization header
   - Format: `Bearer <your_token>`

2. **Post Creation Issues**:
   - Ensure you're authenticated
   - Check content is not empty

3. **Profile Issues**:
   - Profile is automatically created on user registration
   - No need to create profile separately

## Environment Setup

1. Create environment variables in Postman:
   - `BASE_URL`: Your API base URL
   - `TOKEN`: Store your auth token here

2. Use these variables in your requests:
   - URL: `{{BASE_URL}}/api/endpoint`
   - Auth Header: `Bearer {{TOKEN}}`

## Testing Workflow

1. Register new user
2. Login to get token
3. Update environment with new token
4. Test protected endpoints
5. Verify data persistence
6. Test error cases

Remember to test both successful and error scenarios for each endpoint!
