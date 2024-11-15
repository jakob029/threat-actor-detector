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
<summary>Update User Salt</summary>

<br>

Updates the salt and last login, call at every login

``` sql
CALL update_user_salt({username}, {salt})
```

```python
cursor.callproc("update_user_salt", ({username}, {salt}))
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

<details>
<summary>Session table</summary>

<br>

Table containing all active user sessions.

- **created**: date and time of creation, *datetime*.
- **last_access**: date and time of last access, *datetime*.
- **death_time**: last valid use date and time, *datetime*.
- ***sid***: session id / token, *varchar(36)*.
- ***uid***: user id, *varchar(36)*.
  
</details>

<details>
<summary>Chat table</summary>

<br>

Table containing all user credentials.

- **message**: message, *varchar(12288)*.
- **role**: role of the sender, *varchar (36)*.
- **index**: message index in chat, *int*.
- ***uid***: user id, *varchar(36)*.
- ***cid***: chat id, *varchar(36)*.
  
</details>
