Certainly! I apologize for misunderstanding your initial request. Here's the updated README.md file with the information organized in a table format:

```markdown
# Project Documentation for Rock-Paper-Scissors API

This is the backend API for the Rock-Paper-Scissors game, implemented using Django Rest Framework. The API handles user management, game sessions, and payment transactions using PayPal.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/SkyLandd/Rock_Paper_Backend_test.git
   cd rock-paper-scissors-game
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv env
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Install PostgreSQL and create a database.

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Run the project:
   ```
   python manage.py runserver
   ```

## API Documentation

For easy reference, the API is incorporated with Swagger to build beautiful and interactive API documentation. To access the Swagger documentation, use the endpoint:
```
http://127.0.0.1:8000/doc/
```

Note: All the API endpoints have been integrated with token authentication. Before using any API endpoint, log in and obtain the token. Then include it in the header section of the request as `Authorization: Bearer <token>`.

### Applications and Endpoints

| Endpoint                               | Description                               | Method | Payload                                                                                   | Note                                                |
|----------------------------------------|-------------------------------------------|--------|-------------------------------------------------------------------------------------------|-----------------------------------------------------|
| `/user/register`                       | Create new user                           | POST   | `{ "fullName": "string", "username": "string", "email": "string", "password": "string" }` |                                                     |
| `/user/login`                          | Authenticate user                         | POST   | `{ "username": "string", "password": "string" }`                                           |                                                     |
| `/user/resetpassword`                  | Reset password                            | POST   | `{ "username": "string", "password": "string" }`                                           | Bearer Token in header required for password change |
| `/game/start-game-session/`            | Start a new game session                  | POST   | `{}`                                                                                      | Bearer Token in header required                     |
| `/game/record-player-move/{session_id}`| Record player move in a game              | POST   | `{ "playerMove": "string" }`                                                               | Options: ROCK, PAPER, SCISSORS; Bearer Token in header required |
| `/game/user-game-history/`             | Get user's game history                   | GET    | `{}`                                                                                      | Bearer Token in header required                     |
| `/payment/initiate-payment/`           | Initiate payment                          | POST   | `{ "amount": "string", "currency": "string", "transaction_type": "string" }`                | Bearer Token in header required                     |
| `/payment/user-transaction-history/`   | Get user payment history                  | GET    | `{}`                                                                                      | Bearer Token in header required                     |
| `/payment/success/`                    | Redirection endpoint for PayPal approval  | GET    |                                                                                           | None                                                |
| `/payment/cancel/`                     | Redirection endpoint for PayPal cancellation | GET |                                                                                           | None                                                |



Feel free to use this table as a reference for your project! 🚀🎮
```

If you need any further adjustments or additional details, feel free to let me know! 😊