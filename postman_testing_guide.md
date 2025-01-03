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
     - `base_url`: `https://social-media-alx-project.onrender.com/api`
     - `token`: (Leave empty initially)

### Step 2: Authentication Endpoints

#### Register a New User - Detailed Steps

1. Open Postman and create a new request
2. Set the request method to `POST`
3. Enter the URL: `{{base_url}}/auth/register/`
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
       "password2": "testpass123"
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
3. Enter the URL: `{{base_url}}/auth/login/`
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
POST {{base_url}}/auth/login/
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
3. Enter the URL: `{{base_url}}/posts/`
4. Set up Authentication:
   - Click the "Authorization" tab
   - Type: "Bearer Token"
   - Token: Paste your access token or use `{{token}}`

5. Set up the request body:
   - Click on the "Body" tab
   - Select "form-data"
   - Add the following fields:
     ```
     content: "My first post using Postman!"
     image: [Select File] (optional - click "Select Files" to upload an image)
     visibility: "public"
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
       "image": "url_to_image_if_uploaded",
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
1. Try viewing all posts (GET /posts/)
2. View your specific post (GET /posts/1/)
3. Update your post (PUT /posts/1/)
4. Test the feed endpoint (GET /feed/)

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
GET {{base_url}}/users/
```

#### Get Single User
```
GET {{base_url}}/users/1/
```

#### Update User
```
PUT {{base_url}}/users/1/
Body (raw JSON):
{
    "bio": "Updated bio"
}
```

### Step 5: Testing Post Endpoints

#### Create Post
```
POST {{base_url}}/posts/
Body (form-data):
- content: "This is my first test post"
- image: [Select File] (optional)
- visibility: "public"
```

#### Get All Posts
```
GET {{base_url}}/posts/
```

#### Get Single Post
```
GET {{base_url}}/posts/1/
```

### Step 6: Testing Follow System

#### Testing Follow Functionality - Detailed Steps

1. First, Create Another User to Follow
   ```
   POST {{base_url}}/auth/register/
   Body (raw JSON):
   {
       "username": "testuser2",
       "email": "testuser2@example.com",
       "password": "testpass123",
       "password2": "testpass123"
   }
   ```
   - Save this user's ID from the response

2. Follow the User
   - Create a new request in Postman
   - Set the request method to `POST`
   - URL: `{{base_url}}/users/{user_id}/follow/`
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
1. View your feed to see posts from followed users (GET /feed/)
2. Create posts as different users to test the feed
3. Test unfollowing users

Would you like to try any of these operations next?

#### Follow User
```
POST {{base_url}}/users/2/follow/
```

### Step 7: Testing Feed

#### Get User Feed
```
GET {{base_url}}/feed/
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

# Social Media API Testing Guide

## Base URL
```
https://social-media-alx-project.onrender.com
```

## Authentication

### 1. Get CSRF Token
```
GET /csrf/
```
- Save the csrftoken from cookies for subsequent requests

### 2. User Registration
```
POST /api/auth/register/
Headers:
- X-CSRFToken: <csrf_token>
- Content-Type: application/json

Body:
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "password2": "securepassword123"
}
```

### 3. User Login
```
POST /api/auth/login/
Headers:
- X-CSRFToken: <csrf_token>
- Content-Type: application/json

Body:
{
    "username": "testuser",
    "password": "securepassword123"
}
```
- Save the access token for subsequent authenticated requests

## User Management

### 1. List Users
```
GET /api/users/
Headers:
- Authorization: Bearer <access_token>
```

### 2. Get User Details
```
GET /api/users/{user_id}/
Headers:
- Authorization: Bearer <access_token>
```

### 3. Update User
```
PUT /api/users/{user_id}/
Headers:
- Authorization: Bearer <access_token>
- Content-Type: application/json

Body:
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
}
```

### 4. Delete User
```
DELETE /api/users/{user_id}/
Headers:
- Authorization: Bearer <access_token>
```

## Profile Management

### 1. Get User Profile
```
GET /api/profiles/{user_id}/
Headers:
- Authorization: Bearer <access_token>
```

### 2. Update Profile
```
PUT /api/profiles/{user_id}/
Headers:
- Authorization: Bearer <access_token>
- Content-Type: multipart/form-data

Body:
- bio: "My bio text"
- profile_picture: [file upload]
- cover_photo: [file upload]
- website: "https://example.com"
- location: "New York"
```

## Post Management

### 1. Create Post
```
POST /api/posts/
Headers:
- Authorization: Bearer <access_token>
- Content-Type: multipart/form-data

Body:
- content: "This is my post #test @mention"
- image: [file upload]
- visibility: "public" | "followers" | "private"
```

### 2. List Posts
```
GET /api/posts/
Headers:
- Authorization: Bearer <access_token>
```

### 3. Get Post Details
```
GET /api/posts/{post_id}/
Headers:
- Authorization: Bearer <access_token>
```

### 4. Update Post
```
PUT /api/posts/{post_id}/
Headers:
- Authorization: Bearer <access_token>
- Content-Type: multipart/form-data

Body:
- content: "Updated post content"
- image: [file upload]
- visibility: "public"
```

### 5. Delete Post
```
DELETE /api/posts/{post_id}/
Headers:
- Authorization: Bearer <access_token>
```

### 6. Like/Unlike Post
```
POST /api/posts/{post_id}/like/
Headers:
- Authorization: Bearer <access_token>
```

### 7. Comment on Post
```
POST /api/posts/{post_id}/comment/
Headers:
- Authorization: Bearer <access_token>
- Content-Type: application/json

Body:
{
    "content": "Great post!"
}
```

### 8. Share Post
```
POST /api/posts/{post_id}/share/
Headers:
- Authorization: Bearer <access_token>
```

## Follow System

### 1. Follow User
```
POST /api/users/{user_id}/follow/
Headers:
- Authorization: Bearer <access_token>
```

### 2. Get User Feed
```
GET /api/feed/
Headers:
- Authorization: Bearer <access_token>
```

## Direct Messaging

### 1. Send Message
```
POST /api/messages/
Headers:
- Authorization: Bearer <access_token>
- Content-Type: application/json

Body:
{
    "recipient": user_id,
    "content": "Hello!"
}
```

### 2. List Messages
```
GET /api/messages/
Headers:
- Authorization: Bearer <access_token>
```

## Notifications

### 1. List Notifications
```
GET /api/notifications/
Headers:
- Authorization: Bearer <access_token>
```

### 2. Mark Notification as Read
```
POST /api/notifications/{notification_id}/mark_read/
Headers:
- Authorization: Bearer <access_token>
```

## Testing Flow

1. Get CSRF token
2. Register a new user
3. Login and get access token
4. Update user profile
5. Create a post
6. Like and comment on the post
7. Follow another user
8. Check feed for posts
9. Send a direct message
10. Check notifications

## Error Handling
All endpoints return appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

## Pagination
List endpoints support pagination with query parameters:
```
?page=1&page_size=10
```

## Search and Filtering
Some endpoints support search and filtering:
```
/api/posts/?search=keyword
/api/users/?search=username
```

## Environment Variables
Create these environment variables in Postman:
- `BASE_URL`: https://social-media-alx-project.onrender.com
- `ACCESS_TOKEN`: Your JWT access token after login
- `CSRF_TOKEN`: Your CSRF token
