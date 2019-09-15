###Installation Guide : 
----
                
1. `pip install virtualenv`

2. install dependency using req.txt file

3. install mysql server db

4. set database ,user,password as mentioned in settings.py

5. `Python manage.py makemigrations`

6. `Python manage.py migrate`

7. create folder name logs in root dir. 


  
  
### APIS : 
| functionality   name       | api url                                   | method type | header                                                                                           | parameters                                                                                                                                                                                 | Success response                                                                                                                                                                                                                                                                      |
|----------------------------|-------------------------------------------|-------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SignUp                     | http://localhost:8000/auth/               | POST        | Not   required                                                                                   | {       "name":"alexa999",       "dob":"2088-01-12",       "email":"ponoki@simplemail.top",       "password":"ngdfcdhg@123",       "mobile":"76765757",        "roleid":5 (optional)     } | {       "message": "sign up   successfull & confirmation mail has been sent"     }                                                                                                                                                                                                    |
| Confirm-User               | http://localhost:8000/auth/confirm-user   | POST        | Key  =     Authorization     Value = Token {parsed token from url of email confirmation link}    | Not   required                                                                                                                                                                             | "user   confirmed and active"                                                                                                                                                                                                                                                         |
| Login                      | http://localhost:8000/auth/login          | POST        | Not   required                                                                                   | {       "email":"abc@xyz.com",       "password":"Passwords@1"     }                                                                                                                        | {       "message":   "login_success",       "user": {         "email":   "p@p.com",         "token":   "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OTYsImV4cCI6MTU2OTQxMjE5NSwidG9rZW5fdHlwZSI6Mn0.vXtOrFfE9UNJ-qFpHJvBhLBcThbl0eixMaHywHzOCoM",         "userid": 96       }     } |
| Forgot   Password          | http://localhost:8000/auth/generate-link  | POST        | Not   required                                                                                   | {               "email":"abc@xyz.com",               "request_type":3     }                                                                                                                | {       "message":   "email_sent_successfully"     }                                                                                                                                                                                                                                  |
| Resend   Confirm User Link | http://localhost:8000/auth/generate-link  | POST        | Not   required                                                                                   | {               "email":"abc@xyz.com",               "request_type":1     }                                                                                                                | {               "email":"abc@xyz.com",               "request_type":3     }                                                                                                                                                                                                           |
| Reset Password             | http://localhost:8000/auth/reset-password | POST        | Key  =     Authorization     Value = Token {parsed token from url of forgot password email link} | {     	"password":"D@D.coSSm1"     }                                                                                                                                                        | {       "message":   "reset_password_successfully"     }                                                                                                                                                                                                                              |
| Update User Details        | http://localhost:8000/auth/{user_id}/     | PUT         | Key  =     Authorization     Value = Token {login token}                                         | {       "name":   "Laurhtdhcen",              "mobile":   "9090909090"     }                                                                                                               | {       "message":   "successful_updated"     }                                                                                                                                                                                                                                       |
  
  
  
  
  
  
  
  
----
related links 
1. [Argon2 password hasher](https://docs.djangoproject.com/en/2.2/topics/auth/passwords/)
2. [Password upgrader](https://docs.djangoproject.com/en/2.2/topics/auth/passwords/#password-upgrades)
3. [performance](https://www.agiliq.com/blog/2017/11/how-performant-your-python-web-application/)
4. [settings](https://docs.djangoproject.com/en/2.2/ref/settings/#core-settings-topical-index)
