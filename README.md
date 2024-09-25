
## **API Rate Limiter - README**

### **Overview**
This is a FastAPI-based application that provides rate-limiting features for different customers. You can register, login, and interact with protected routes, with rate limits enforced for each type of customer.

Deployment URL : http://api-rate-limiter-env.eba-7et5iisk.us-east-1.elasticbeanstalk.com/docs

### **Prerequisites**
- Docker
- Docker Compose (Optional, for local testing)

### **Running the Application with Docker**

1. **Build the Docker Image:**
   ```bash
   docker build -t api-rate-limiter .
   ```

2. **Run the Docker Container:**
   ```bash
   docker run -p 8000:8000 api-rate-limiter
   ```

The FastAPI application will be accessible at `http://localhost:8000`.

### **Accessing the API Documentation**
You can view the API documentation using the following URLs:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### **Registration Process for Customers**
You need to register customers before accessing the protected routes. Here are the instructions for registering different customers:

#### **Step 1: Register a Customer**

Use the `/auth/register` endpoint to register a new user.

| **Customer Type** | **Username**   | **Full Name**      | **Email**               | **Password** | **Role**     |
|-------------------|----------------|--------------------|-------------------------|--------------|--------------|
| Customer 1        | customer1_user | Customer One       | customer1@example.com   | password123  | customer1    |
| Customer 2        | customer2_user | Customer Two       | customer2@example.com   | password456  | customer2    |
| Customer 3        | customer3_user | Customer Three     | customer3@example.com   | password789  | customer3    |

**Example JSON for registering Customer 1:**
```json
{
  "username": "customer1_user",
  "full_name": "Customer One",
  "email": "customer1@example.com",
  "password": "password123",
  "phone_number": "1234567890",
  "role": "customer1"
}
```

- Use Postman or cURL to send this request to `http://localhost:8000/auth/register`.

#### **Step 2: Log In as a Customer**

Use the `/auth/login` endpoint to log in and obtain a JWT token. This token will be needed for accessing protected routes.

- Send a POST request to `http://localhost:8000/auth/login` with `Content-Type` as `application/x-www-form-urlencoded`.

**Example Login Data:**
```
username: customer1@example.com
password: password123
```

The response will provide you with an `access_token`:
```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

### **Using the API Endpoints**

#### **API Endpoint Details**

| **Endpoint**             | **Description**                          | **Method** | **Authorization** | **Rate Limit**                |
|--------------------------|------------------------------------------|------------|--------------------|-------------------------------|
| `/auth/register`         | Register a new user                      | POST       | None               | None                          |
| `/auth/login`            | Log in to obtain a JWT token             | POST       | None               | None                          |
| `/api/v1/users/{user_id}`| Retrieve user data                       | GET        | JWT Required       | Based on the customer type    |

#### **Rate Limit Information**

| **Customer Type** | **Rate Limit**                  |
|-------------------|---------------------------------|
| Customer 1        | 5 calls per minute              |
| Customer 2        | 10 calls per 30 seconds         |
| Customer 3        | No rate limiting                |

**Note:** If you exceed the rate limit, you will receive a `429 Too Many Requests` response.

### **Steps to Test the Application**

1. **Register Users:**
   - Use the `/auth/register` endpoint to register Customer 1, Customer 2, and Customer 3.

2. **Log In:**
   - Obtain JWT tokens for each registered user using the `/auth/login` endpoint.

3. **Access Protected Routes:**
   - Use the JWT token in the `Authorization` header (e.g., `Bearer your_jwt_token`) to access the `/api/v1/users/{user_id}` endpoint.

**Example cURL Command to Access a Protected Route:**
```bash
curl -H "Authorization: Bearer your_jwt_token" http://localhost:8000/api/v1/users/1
```

### **Environment Variables**

If you need to configure the database or any other settings, you can do so via environment variables. The `.env` file should be placed in the root directory, and it might include variables such as:
```
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### **Additional Notes**

- You can stop the running Docker container using `Ctrl + C` in the terminal where you started it.
- To stop all running containers, you can use:
  ```bash
  docker stop $(docker ps -q)
  ```

Feel free to explore the API and test the rate-limiting functionality based on your registered customer role!