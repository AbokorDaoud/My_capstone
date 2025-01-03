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

## Social Media API - Comprehensive Testing Guide

## Base URL
```
https://social-media-alx-project.onrender.com
```

## Setup in Postman

1. Create a new collection named "Social Media API"
2. Set up environment variables:
   - `base_url`: Your API base URL
   - `token`: For storing authentication token

## 1. User Management

### 1.1 User Registration
- **Endpoint**: `POST {{base_url}}/api/auth/register/`
- **Body** (raw JSON):
```json
{
    "username": "testuser1",
    "email": "test1@example.com",
    "password": "securepass123",
    "first_name": "Test",
    "last_name": "User"
}
```
- **Expected Response**: 201 Created
- **Test Cases**:
  - Valid registration
  - Duplicate username
  - Invalid email format
  - Password too short

### 1.2 User Login
- **Endpoint**: `POST {{base_url}}/api/auth/login/`
- **Body** (raw JSON):
```json
{
    "username": "testuser1",
    "password": "securepass123"
}
```
- **Expected Response**: 200 OK with tokens
- **Test Cases**:
  - Valid credentials
  - Invalid password
  - Non-existent user

### 1.3 View Profile
- **Endpoint**: `GET {{base_url}}/api/users/me/`
- **Auth**: Bearer Token
- **Test Cases**:
  - View own profile
  - View other user's profile
  - Invalid token

## 2. Post Management

### 2.1 Create Post
- **Endpoint**: `POST {{base_url}}/api/posts/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "content": "This is my first test post!",
    "visibility": "public"
}
```
- **Test Cases**:
  - Create public post
  - Create private post
  - Empty content
  - No authentication

### 2.2 Get Posts
- **Endpoint**: `GET {{base_url}}/api/posts/`
- **Query Parameters**:
  - `page`: Page number
  - `ordering`: `-created_at` (newest first)
- **Test Cases**:
  - Get all public posts
  - Test pagination
  - Test ordering

### 2.3 Update Post
- **Endpoint**: `PUT {{base_url}}/api/posts/{post_id}/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "content": "Updated post content",
    "visibility": "private"
}
```
- **Test Cases**:
  - Update own post
  - Update other's post
  - Invalid post ID

### 2.4 Delete Post
- **Endpoint**: `DELETE {{base_url}}/api/posts/{post_id}/`
- **Auth**: Bearer Token
- **Test Cases**:
  - Delete own post
  - Delete other's post
  - Delete non-existent post

## 3. Follow System

### 3.1 Follow User
- **Endpoint**: `POST {{base_url}}/api/users/{user_id}/follow/`
- **Auth**: Bearer Token
- **Test Cases**:
  - Follow user
  - Unfollow user
  - Follow self
  - Follow non-existent user

### 3.2 Get Followers/Following
- **Endpoint**: `GET {{base_url}}/api/users/{user_id}/followers/`
- **Endpoint**: `GET {{base_url}}/api/users/{user_id}/following/`
- **Test Cases**:
  - Get followers list
  - Get following list
  - Pagination test

## 4. Feed

### 4.1 Get Feed
- **Endpoint**: `GET {{base_url}}/api/feed/`
- **Auth**: Bearer Token
- **Query Parameters**:
  - `page`: Page number
  - `ordering`: `-created_at`
- **Test Cases**:
  - Get personalized feed
  - Test pagination
  - Test with no follows

## 5. Likes and Comments

### 5.1 Like Post
- **Endpoint**: `POST {{base_url}}/api/posts/{post_id}/like/`
- **Auth**: Bearer Token
- **Test Cases**:
  - Like post
  - Unlike post
  - Like non-existent post

### 5.2 Add Comment
- **Endpoint**: `POST {{base_url}}/api/posts/{post_id}/comments/`
- **Auth**: Bearer Token
- **Body** (raw JSON):
```json
{
    "content": "Great post!"
}
```
- **Test Cases**:
  - Add comment
  - Reply to comment
  - Empty comment

## Testing Workflow

1. **Initial Setup**:
   ```
   1. Register User 1
   2. Register User 2
   3. Login User 1 (save token)
   ```

2. **Post Testing**:
   ```
   1. Create post as User 1
   2. View posts
   3. Update post
   4. Try to delete other's post (should fail)
   ```

3. **Follow Testing**:
   ```
   1. User 2 follows User 1
   2. Verify follower count
   3. Check User 2's feed for User 1's posts
   ```

4. **Interaction Testing**:
   ```
   1. Like posts
   2. Comment on posts
   3. Reply to comments
   ```

## Common Issues & Solutions

1. **Authentication Issues**:
   - Check token format: `Bearer <token>`
   - Ensure token is not expired
   - Try re-login if unauthorized

2. **Post Creation Issues**:
   - Verify content is not empty
   - Check visibility setting
   - Ensure proper authentication

3. **Follow System Issues**:
   - Cannot follow self
   - Cannot follow same user twice
   - Must be authenticated

## Environment Variables

Create these variables in your Postman environment:
```
base_url: https://social-media-alx-project.onrender.com
token: <your_jwt_token>
user1_id: <after_registration>
user2_id: <after_registration>
post1_id: <after_creation>
```

## Testing Sequence

1. Run authentication tests first
2. Test CRUD operations on posts
3. Test follow system
4. Test feed generation
5. Test interactions (likes, comments)

Remember to:
- Save responses for later use
- Test both success and error cases
- Verify response status codes
- Check response data structure
