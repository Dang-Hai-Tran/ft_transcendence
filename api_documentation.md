# API Documentation

## Authentication

### Token Obtain
**Endpoint:** `/api/token`
**Method:** POST
**Description:** Obtain a JWT access and refresh token.
**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```
**Response:**
```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```

### Token Refresh
**Endpoint:** `/api/token/refresh`
**Method:** POST
**Description:** Refresh the access token using the refresh token.
**Request Body:**
```json
{
  "refresh": "your_refresh_token"
}
```
**Response:**
```json
{
  "access": "new_access_token"
}
```

## Users

### List Users
**Endpoint:** `/api/users`
**Method:** GET
**Description:** Retrieve a list of all users.
**Response:**
```json
[
  {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com",
    "level": 1,
    "status": "online",
    "profilePicture": "",
    "created_at": "2023-04-01T12:00:00Z",
    "updated_at": "2023-04-01T12:00:00Z"
  },
  {
    "id": 2,
    "username": "user2",
    "email": "user2@example.com",
    "level": 2,
    "status": "offline",
    "profilePicture": "",
    "created_at": "2023-04-02T12:00:00Z",
    "updated_at": "2023-04-02T12:00:00Z"
  }
]
```

### Create User
**Endpoint:** `/api/users`
**Method:** POST
**Description:** Create a new user.
**Request Body:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "password123"
}
```
**Response:**
```json
{
  "id": 3,
  "username": "newuser",
  "email": "newuser@example.com",
  "level": 1,
  "status": "offline",
  "profilePicture": "",
  "created_at": "2023-04-03T12:00:00Z",
  "updated_at": "2023-04-03T12:00:00Z"
}
```

### Retrieve User
**Endpoint:** `/api/users/{id}`
**Method:** GET
**Description:** Retrieve a specific user.
**Response:**
```json
{
  "id": 1,
  "username": "user1",
  "email": "user1@example.com",
  "level": 1,
  "status": "online",
  "profilePicture": "",
  "created_at": "2023-04-01T12:00:00Z",
  "updated_at": "2023-04-01T12:00:00Z"
}
```

### Update User
**Endpoint:** `/api/users/{id}`
**Method:** PUT
**Description:** Update a specific user.
**Request Body:**
```json
{
  "username": "updateduser",
  "email": "updateduser@example.com",
  "level": 2,
  "status": "busy",
  "profilePicture": "https://example.com/profile.jpg"
}
```
**Response:**
```json
{
  "id": 1,
  "username": "updateduser",
  "email": "updateduser@example.com",
  "level": 2,
  "status": "busy",
  "profilePicture": "https://example.com/profile.jpg",
  "created_at": "2023-04-01T12:00:00Z",
  "updated_at": "2023-04-05T18:00:00Z"
}


