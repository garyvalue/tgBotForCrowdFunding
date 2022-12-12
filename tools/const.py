createSqlSponsor = '''
create table "sponsor"(
  title VARCHAR(250) NOT NULL,
  link VARCHAR(100) unique NOT NULL,
  author VARCHAR(20),
  money decimal(5, 2),
  date TEXT,
  num int,
  status int,
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
)
'''
createSqlFinish = '''
create table "finish" (
  id int PRIMARY KEY NOT NULL,
  link VARCHAR(100) NOT NULL,
  pwd VARCHAR(10),
  password VARCHAR(50),
  data TEXT
)
'''
createSqlJoin = '''
create table "join" (
  id int NOT NULL,
  user VARCHAR(100) NOT NULL
)
'''
insertSponsorSql = 'INSERT INTO sponsor VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',1,%d,null)'
delSponsorSql = 'DELETE FROM sponsor WHERE id=\'%s\''
setJoinNumSql = 'UPDATE sponsor SET num=\'%s\' WHERE id=\'%s\''
finishSponsorSql = 'UPDATE sponsor SET status=1 WHERE id=\'%s\''
insertFinishSql = 'INSERT INTO finish VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'
updateFinishSql = 'UPDATE finish SET link=\'%s\',pwd=\'%s\',password=\'%s\' WHERE id=\'%s\''
delFinishSql = 'DELETE FROM finish WHERE id=\'%s\''
joinItemSql = 'INSERT INTO join VALUES (\'%s\',\'%s\')'
exitItemSql = 'DELETE FROM join WHERE id=\'%s\' AND user=\'%s\''
