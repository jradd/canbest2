# Django-Blog-with-REST-Api

Blog web application with Django Rest Framework API

## Testing

Run migrations : 
- `$ python manage.py makemigrations`
- `$ python manage.py migrate`

Collect static files:
- `$ python manage.py collectstatic`

Runserver
- `$ python manage.py runserver`


### Available Endpoints

| Endpoint | Description |
| --- | --------------- |
| API | --------------- |
| [POST /api/accounts/register](#) |  Register user.|
| [POST /api/accounts/login](#) | Login user. |
| [GET /api/posts/](#) | List all posts. |
| [POST /api/posts/create/](#) | Create a new post. |
| [GET /api/post/{id}/delete/](#) | Delete a post. |
| [POST /api/comments/create](#) | Create a comment|
| [GET /api/comments/](#) | List all comments |
| [GET /api/comments/{id}/delete](#) | Delete a comment |
| Blog | --------------- |
| [/accounts/register](#) |  Register user.|
| [/accounts/login](#) | Login user. |
| [/posts/](#) | List all posts. |
| [/posts/create/](#) | Create a new post. |
| [/post/{id}/delete/](#) | Delete a post. |
| [/comments/create](#) | Create a comment|
| [/comments/](#) | List all comments |
| [/comments/{id}/delete](#) | Delete a comment |
