# Database

Variables surrounded by '{}' are requierd.

## Procedures

<details>
<summary>Register New User</summary>

<br>

Creates a new user.

``` sql
CALL register_new_user({username}, {password hash}, {salt})
```

```python
cursor.callproc("register_new_user", ({username}, {hash}, {salt}))
```
  
</details>

<details>
<summary>Update User Auth</summary>

<br>

Updates the password hash, salt and last login, call at every login

``` sql
CALL update_user_auth({uid}, {salt})
```

```python
cursor.callproc("update_user_auth", ({uid}, {salt}))
```
  
</details>

## Tables

<details>
<summary>User table</summary>

<br>

Table containing all user credentials.

- **created**: date and time of creation, *datetime*.
- **last_login**: date and time of last login, *datetime*.
- **username**: users name, *varchar(40)*.
- **password_hash**: hashed password, *varchar(100)*.
- **salt**: salt for the password, *varchar(16)*.
- ***uid***: user id, *varchar(36)*.
  
</details>