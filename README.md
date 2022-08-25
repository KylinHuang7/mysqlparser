# mysqlparser

`mysqlparser` is a python lib for parsing [MySQL](http://dev.mysql.com) statements.

## Usage

```python
import mysqlparser

sqlparser = mysqlparser.Parser()

sql = 'SELECT * FROM `dbData`.`tbTest` WHERE `iId` > 100 LIMIT 10'
result = sqlparser.parse(sql)
print(sqlparser.sql_list)
print(sqlparser.sql_list[0].database)
print(sqlparser.sql_list[0].table)

```