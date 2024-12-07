# Library Management System

## Project Overview
A Flask-based API for managing a library's books and members with CRUD operations, search functionality, and token-based authentication.

## Features
- Create, Read, Update, Delete (CRUD) operations for books
- Create, Read, Update, Delete (CRUD) operations for members
- Book search by title or author
- Pagination for book listings
- Token-based authentication for protected routes

## Requirements
- Python 3.8+
- Flask (included in the standard library)

## Setup and Installation
1. Clone the repository:  
   `git clone https://github.com/Garvit-Nag/Library-Management-System/tree/main`  
   `cd library-management-system`  

2. Create and activate a virtual environment:  
   `python -m venv venv`  
   `source venv/bin/activate  # On Windows, use venv\Scripts\activate`   

3. Run the application:  
   `python run.py`  
 

## API Endpoints
### Books
- `POST /books`: Create a new book  
- `GET /books`: List books with pagination  
- `GET /books/search`: Search books by title or author  
- `GET /books/<id>`: Get book details  
- `PUT /books/<id>`: Update book  
- `DELETE /books/<id>`: Delete book  

### Members
- `POST /members`: Create a new member  
- `GET /members`: List members  
- `GET /members/<id>`: Get member details  
- `PUT /members/<id>`: Update member  
- `DELETE /members/<id>`: Delete member  

### Authentication
- `POST /auth/token`: Generate a token using valid credentials.  

### Token-Based Authentication
Protected endpoints require an authentication token passed in the request headers.  

Example:  
`curl -X GET http://localhost:5000/books -H "Authorization: Bearer <your_token>"`  

To generate a token:  
1. Use the `/auth/token` endpoint with valid credentials (e.g., username and password).  
2. Include the token in the `Authorization` header for all subsequent requests to protected routes.  

## Design Choices
- **In-Memory Database**: Data is stored in memory for simplicity. All data is lost when the application restarts.  
- **Dataclasses**: Used for defining data models, ensuring type safety and simplicity.  
- **Token Authentication**: Basic token generation and validation implemented for securing protected endpoints.  

## Future Scope
- **Authentication Enhancements**: Upgrade to JWT (JSON Web Tokens) for more secure and scalable authentication. Implement token expiration and refresh mechanisms.  
- **Database Integration**: Replace the in-memory database with a persistent solution such as PostgreSQL or MongoDB. Implement migrations and scalable data models.  
- **Enhanced Search**: Add advanced filtering and sorting capabilities for book searches.  
- **Improved Error Handling**: Standardize error messages and HTTP status codes across the API.  

## Limitations
- Data is not persistent and will be lost on application restart.  
- Basic authentication without token expiration or refresh mechanisms.  
- No user roles or access levels implemented.  


