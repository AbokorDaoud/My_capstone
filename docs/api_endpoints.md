# API Endpoints Documentation

## Authentication Endpoints

### User Registration and Authentication
- `POST /api/auth/register/`
  - Register a new user
  - Request body: `username`, `email`, `password`
  - Returns: User details and authentication token

- `POST /api/auth/login/`
  - Login existing user
  - Request body: `username`, `password`
  - Returns: Authentication token

- `POST /api/auth/logout/`
  - Logout user
  - Requires: Authentication token
  - Returns: Success message

## User Endpoints

- `GET /api/users/`
  - List all users
  - Requires: Authentication token
  - Optional query params: `page`, `limit`

- `GET /api/users/{user_id}/`
  - Get specific user details
  - Requires: Authentication token

- `PUT /api/users/{user_id}/`
  - Update user profile
  - Requires: Authentication token
  - Request body: `profile_picture`, `bio`

## Post Endpoints

- `GET /api/posts/`
  - List all posts
  - Requires: Authentication token
  - Optional query params: `page`, `limit`

- `POST /api/posts/`
  - Create new post
  - Requires: Authentication token
  - Request body: `content`, `media_url` (optional)

- `GET /api/posts/{post_id}/`
  - Get specific post details
  - Requires: Authentication token

- `PUT /api/posts/{post_id}/`
  - Update post
  - Requires: Authentication token
  - Request body: `content`, `media_url`

- `DELETE /api/posts/{post_id}/`
  - Delete post
  - Requires: Authentication token

## Comment Endpoints

- `GET /api/posts/{post_id}/comments/`
  - List all comments on a post
  - Requires: Authentication token
  - Optional query params: `page`, `limit`

- `POST /api/posts/{post_id}/comments/`
  - Add comment to post
  - Requires: Authentication token
  - Request body: `content`

- `PUT /api/comments/{comment_id}/`
  - Update comment
  - Requires: Authentication token
  - Request body: `content`

- `DELETE /api/comments/{comment_id}/`
  - Delete comment
  - Requires: Authentication token

## Like Endpoints

- `POST /api/posts/{post_id}/like/`
  - Like a post
  - Requires: Authentication token

- `DELETE /api/posts/{post_id}/like/`
  - Unlike a post
  - Requires: Authentication token

## Follow Endpoints

- `POST /api/users/{user_id}/follow/`
  - Follow a user
  - Requires: Authentication token

- `DELETE /api/users/{user_id}/follow/`
  - Unfollow a user
  - Requires: Authentication token

- `GET /api/users/{user_id}/followers/`
  - Get user's followers
  - Requires: Authentication token
  - Optional query params: `page`, `limit`

- `GET /api/users/{user_id}/following/`
  - Get users being followed
  - Requires: Authentication token
  - Optional query params: `page`, `limit`

## Feed Endpoint

- `GET /api/feed/`
  - Get personalized feed of posts from followed users
  - Requires: Authentication token
  - Optional query params: `page`, `limit`

## Response Formats

All endpoints return responses in the following format:

```json
{
    "status": "success|error",
    "data": {
        // Response data here
    },
    "message": "Success or error message"
}
```

## Error Handling

Common HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

- API requests are limited to 100 requests per minute per user
- Rate limit information is included in response headers
