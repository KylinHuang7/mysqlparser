#!/usr/local/ieod-web/python/bin/python
# -*- coding: utf-8 -*-

#=============================================================================
#  @desc       
#  @version    1.0.0
#  @author     kylinshuang
#  @date       2017-12-04
#=============================================================================

import os
import re
import itertools
import codecs

import mysqltoken as token
import statement.create
import statement.alter
import statement.drop
import statement.rename
import statement.truncate
import statement.select
import statement.insert
import statement.replace
import statement.update
import statement.delete
import statement.set
import statement.show
import statement.explain
import statement.use

class Parser(object):
    def __init__(self):
        self.log_level = 1
    
    def verbose(self, content, level=0):
        if self.log:
            if level <= self.log_level:
                self.log(content)
    
    def parse_single_sql(self, token_list, log_func=None):
        token_starts = token_list.get_next_valid_token(2)
        if not token_starts or len(token_starts) != 2:
            return None
        s = None
        if token_starts[0].value == 'CREATE':
            if token_starts[1].value in ['DATABASE', 'SCHEMA']:
                s, token_list = statement.create.CreateDatabaseStatement.parse(token_list, verbose_func=self.verbose)
            elif token_starts[1].value in ['TEMPORARY', 'TABLE']:
                s, token_list = statement.create.CreateTableStatement.parse(token_list, verbose_func=self.verbose)
            elif token_starts[1].value in ['ONLINE', 'OFFLINE', 'UNIQUE', 'FULLTEXT', 'SPATIAL', 'INDEX']:
                s, token_list = statement.create.CreateIndexStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value == 'ALTER':
            if token_starts[1].value in ['DATABASE', 'SCHEMA']:
                s, token_list = statement.alter.AlterDatabaseStatement.parse(token_list, verbose_func=self.verbose)
            elif token_starts[1].value in ['ONLINE', 'OFFLINE', 'IGNORE', 'TABLE']:
                s, token_list = statement.alter.AlterTableStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value == 'DROP':
            if token_starts[1].value in ['DATABASE', 'SCHEMA']:
                s, token_list = statement.drop.DropDatabaseStatement.parse(token_list, verbose_func=self.verbose)
            elif token_starts[1].value in ['TEMPORARY', 'TABLE']:
                s, token_list = statement.drop.DropTableStatement.parse(token_list, verbose_func=self.verbose)
            elif token_starts[1].value in ['ONLINE', 'OFFLINE', 'INDEX']:
                s, token_list = statement.drop.DropIndexStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value == 'RENAME':
            s, token_list = statement.rename.RenameTableStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value == 'TRUNCATE':
            s, token_list = statement.truncate.TruncateTableStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value in ['SELECT', '(']:
            if token_list.has_token(token.MySQLKeywordToken, 'UNION'):
                s, token_list = statement.select.UnionStatement.parse(token_list, verbose_func=self.verbose)
            if not s:
                s, token_list = statement.select.SelectStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value == 'INSERT':
            s, token_list = statement.insert.InsertStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value == 'REPLACE':
            s, token_list = statement.replace.ReplaceStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value == 'UPDATE':
            s, token_list = statement.update.UpdateStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value == 'DELETE':
            s, token_list = statement.delete.DeleteStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value == 'SET':
            s, token_list = statement.set.SetStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value == 'SHOW':
            s, token_list = statement.show.ShowStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value in ['EXPLAIN', 'DESCRIBE', 'DESC']:
            s, token_list = statement.explain.ExplainStatement.parse(token_list, verbose_func=self.verbose)
        elif token_starts[0].value == 'USE':
            s, token_list = statement.use.UseStatement.parse(token_list, verbose_func=self.verbose)
        else:
            return None
        return s
        
    def parse(self, sql, log_func=None):
        self.log = log_func
        try:
            self.token_list = token.MySQLTokenList(sql, verbose_func=self.verbose)
        except Exception as e:
            self.verbose("Parse error {0}".format(e), 1)
            return False
            
        self.verbose("Token List: {0}".format(self.token_list), 3)
        
        self.sql_token_list = self.token_list.divide()
        self.verbose("SQL Token List: {0}".format([str(x) for x in self.sql_token_list]), 3)
        
        self.sql_list = []
        for token_list in self.sql_token_list:
            s = self.parse_single_sql(token_list, log_func=None)
            if s:
                self.sql_list.append(s)
                self.verbose("SQL Type: {0}".format(s.type()), 4)
                if hasattr(s, 'database') and hasattr(s, 'table') and hasattr(s, 'from_database') and hasattr(s, 'from_table'):
                    self.verbose("Table: {0}, {1}, from {2}, {3}".format(s.database, s.table, s.from_database, s.from_table), 4)
                elif hasattr(s, 'database') and hasattr(s, 'table'):
                    self.verbose("Table: {0}, {1}".format(s.database, s.table), 4)
                elif hasattr(s, 'database'):
                    self.verbose("Database: {0}".format(s.database), 4)
            else:
                self.verbose("SQL List: {0}".format(self.sql_list), 3)
                self.verbose("Syntax error on {0}".format(token_list), 1)
                return False
        self.verbose("SQL List: {0}".format(["{0}: {1}".format(x.type(), x.value) for x in self.sql_list]), 1)
        if not self.sql_token_list[-1].eof() and self.sql_token_list[-1].get_next_valid_token():
            self.verbose("Syntax error by truncated", 1)
            return False
        return True
