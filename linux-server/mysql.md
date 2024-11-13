# Mysql commands

```sql
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';

CREATE DATABASE mydb;

GRANT ALL PRIVILEGES ON mydb.* TO 'myuser'@'localhost';

FLUSH PRIVILEGES;
```