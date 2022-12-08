createSql = 'create table "item" ( title VARCHAR(250) NOT NULL, link VARCHAR(100) unique NOT NULL, author VARCHAR(20), money decimal(5,2), date TEXT, status int, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)'
insertSql = 'INSERT INTO \"item\" VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%d, null)'
