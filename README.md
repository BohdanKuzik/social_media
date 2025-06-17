# Social Media API

A robust RESTful API for a social media platform built with Django and Django REST Framework. This API provides features for user management, posts, comments, likes, follows, and hashtags.

## Features

- **User Management**
  - User registration and authentication
  - Token-based authentication
  - User profiles with bio and profile pictures

- **Posts**
  - Create, read, update, and delete posts
  - Support for text and image content
  - Post scheduling functionality
  - Hashtag support

- **Social Interactions**
  - Like/unlike posts
  - Comment on posts
  - Follow/unfollow users
  - View user profiles

- **API Documentation**
  - Interactive API documentation with Swagger UI
  - ReDoc alternative documentation
  - OpenAPI schema

## Tech Stack

- Python 3.12+
- Django 5.2
- Django REST Framework
- Celery for task scheduling
- Redis for message broker
- PostgreSQL (production) / SQLite (development)
- DRF Spectacular for API documentation

## Prerequisites

- Python 3.12 or higher
- Redis server
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd social_media
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start Redis server:
```bash
redis-server
```

7. Start Celery worker:
```bash
celery -A social_media worker --loglevel=info -P eventlet
```

8. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/

## API Endpoints

### Authentication
- `POST /api/register/` - Register a new user
- `POST /api/login/` - Obtain authentication token
- `GET /api/me/` - Get current user profile

### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create a new post
- `GET /api/posts/{id}/` - Retrieve a specific post
- `PUT /api/posts/{id}/` - Update a post
- `DELETE /api/posts/{id}/` - Delete a post

### Comments
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create a new comment
- `GET /api/comments/{id}/` - Retrieve a specific comment
- `PUT /api/comments/{id}/` - Update a comment
- `DELETE /api/comments/{id}/` - Delete a comment

### Likes
- `POST /api/likes/` - Like/unlike a post
- `GET /api/likes/` - List all likes

### Follows
- `POST /api/follows/` - Follow/unfollow a user
- `GET /api/follows/` - List all follows

### Hashtags
- `GET /api/hashtags/` - List all hashtags
- `POST /api/hashtags/` - Create a new hashtag

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
The project follows PEP 8 style guide. To check your code:
```bash
flake8
```

### Task Scheduling
The project uses Celery for task scheduling, particularly for scheduled posts. Make sure Redis is running and the Celery worker is started.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
