createSqlSponsor = '''
create table "sponsor"(
  title VARCHAR(250) NOT NULL,
  link VARCHAR(100) unique NOT NULL,
  author VARCHAR(20),
  money decimal(5, 2),
  date TEXT,
  status int,
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
)
'''
createSqlFinish = '''
create table "finish" (
  id int PRIMARY KEY NOT NULL,
  link VARCHAR(100) NOT NULL,
  pwd VARCHAR(10),
  password VARCHAR(50)
)
'''
insertSponsorSql = 'INSERT INTO sponsor VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%d, null)'
delSponsorSql = 'DELETE FROM sponsor WHERE id=\'%s\''
insertFinishSql = 'INSERT INTO finish VALUES (\'%s\',\'%s\',\'%s\',\'%s\')'
updateFinishSql = 'UPDATE finish SET link=\'%s\',pwd=\'%s\',password=\'%s\' WHERE id=\'%s\''
delFinishSql = 'DELETE FROM finish WHERE id=\'%s\''
