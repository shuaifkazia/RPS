
# Rock-Paper-Scissors API

This is the backend API for the Rock-Paper-Scissors game, implemented using Django Rest Framework. The API handles user management, game sessions, and payment transactions using PayPal.


## Clone

Clone the Repository

```bash
git clone https://github.com/shuaifkazia/RPS.git 

```

```bash
cd RPS
```

## Setup
Create A Virtual Environment and acitivate it

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

## Install the Dependencies
once you activate the virtual Environment install the dependecies for the project
```bash
pip install -r requirements.txt
```

## Database Configuration
```bash
1. Install PostgreSQL if not installed already and create a Database.

2. Goto Project setting file under RPS/settings.py

3. Got to the DB section in the file and change the NAME,USER and PASSWORD values to match to your Postgres username as USER and password as PASSWORD and DB name as NAME(you created

```

now once you had configured the DB you need to apply the migrations to the Database (apllying all the chnages like creating the table)
NOTE :  Before enterting the below command in termnial manage.py file must be in your current directy (RPS)

## Database Migrations

```bash
python manage.py migrate
```

## Run Server

```bash
python manage.py runserver
```

## SWAGGER
For easy Reference the API is incorporated with Swagger to build beautiful and interactive API documentation
To access the swagger documentation, use the endpoint
http://127.0.0.1:8000/doc/





## Tech Stack

**Server:** Django Rest Framework

**Database:** PostgreSQL

**Payment Gateway:** Paypal
## API Endpoints
### 1. USER Endpoints

| Endpoint  | Description | Method | Payload | Note |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| /user/register  | Register New User  | POST | {"fullName": "string","username": "string","email": "string","password": "string"}| | 
| /user/login  | Authenticate the User  | POST | {"username": "string","password": "string"}| |
| /user/resetpassword | Reset Password  | POST |{"username": "string","password": "string"}| Bearer Token in header is Required|

### 1. GAME Endpoints

| Endpoint  | Description | Method | Payload | Note |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| /game/start-game-session/  | To Start a Game Session  | POST | {} | Bearer Token in header is Required| 
| /game/record-player-move/{session_id}  | To Record A players move and getv game result  | POST | {"playerMove": "string"} |***playerMove:*** •ROCK,•PAPER,•SCISSORS , Bearer Token in header is Required|
| /game/user-game-history/ | Reset Password  | GET | | Bearer Token in header is Required|


### 1. PAYMENT Endpoints

| Endpoint  | Description | Method | Payload | Note |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| /payment/initiate-payment/  | To Initiate the Payment  | POST | {"amount": "string","currency": "string","transaction_type": "string"}| ***transaction_type:*** •Deposit ,***currency:***USD , Bearer Token in header is Required  | 
| /payment/user-transaction_history/  | To Get Users Payment History  | GET | | Bearer Token in header is Required|
| /payment/success/ | Redirection endpoint for paypal to approve the payment  | GET | | Bearer Token in header is Required|
| /payment/cancel/ | Redirection endpoint for paypal to handle cancellation  | GET | | Bearer Token in header is Required|


## Support

For support, email shuaifkazia@gmail.com

