#!/usr/local/ieod-web/python/bin/python
# -*- coding: utf-8 -*-

#=============================================================================
#  @desc       
#  @version    1.0.0
#  @author     kylinshuang
#  @date       2017-12-04
#=============================================================================

import mysqltoken as token
import component.identifier
import component.expression
import component.reference
import statement

# 13.7.5 SHOW Syntax
# SHOW AUTHORS
# SHOW {BINARY | MASTER} LOGS
# SHOW BINLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
# SHOW CHARACTER SET [like_or_where]
# SHOW COLLATION [like_or_where]
# SHOW [FULL] {COLUMNS | FIELDS} {FROM | IN} tbl_name [{FROM | IN} db_name] [like_or_where]
# SHOW CONTRIBUTORS
# SHOW CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
# SHOW CREATE EVENT event_name
# SHOW CREATE FUNCTION func_name
# SHOW CREATE PROCEDURE proc_name
# SHOW CREATE TABLE tbl_name
# SHOW CREATE TRIGGER trigger_name
# SHOW CREATE VIEW view_name
# SHOW {DATABASES | SCHEMAS} [like_or_where]
# SHOW ENGINE engine_name {STATUS | MUTEX}
# SHOW [STORAGE] ENGINES
# SHOW ERRORS [LIMIT [offset,] row_count]
# SHOW COUNT(*) ERRORS
# SHOW EVENTS [{FROM | IN} db_name} [like_or_where]
# SHOW FUNCTION CODE func_name
# SHOW FUNCTION STATUS [like_or_where]
# SHOW GRANTS [FOR user]
# SHOW {INDEX | INDEXES | KEYS} {FROM | IN} tbl_name [{FROM | IN} db_name] [like_or_where]
# SHOW MASTER STATUS
# SHOW OPEN TABLES [{FROM | IN} db_name] [like_or_where]
# SHOW PLUGINS
# SHOW PROCEDURE CODE proc_name
# SHOW PROCEDURE STATUS [like_or_where]
# SHOW PRIVILEGES
# SHOW [FULL] PROCESSLIST
# SHOW PROFILE [types] [FOR QUERY n] [LIMIT row_count [OFFSET offset]]
# SHOW PROFILES
# SHOW RELAYLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
# SHOW SLAVE HOSTS
# SHOW SLAVE STATUS
# SHOW [GLOBAL | SESSION] STATUS [like_or_where]
# SHOW TABLE STATUS [{FROM | IN} db_name] [like_or_where]
# SHOW [FULL] TABLES [{FROM | IN} db_name] [like_or_where]
# SHOW TRIGGERS [{FROM | IN} db_name] [like_or_where]
# SHOW [GLOBAL | SESSION] VARIABLES [like_or_where]
# SHOW WARNINGS [LIMIT [offset,] row_count]
# SHOW COUNT(*) WARNINGS
#
# like_or_where:
#    LIKE 'pattern'
#  | WHERE expr
class ShowStatement(statement.MySQLStatement):
    def __init__(self):
        super(ShowStatement, self).__init__()
        self.database = []
        self.table = []
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'SHOW', 1),
            (1, token.MySQLKeywordToken, 'AUTHORS', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'BINARY', 2),
            (1, token.MySQLKeywordToken, 'MASTER', 2),
            (2, token.MySQLKeywordToken, 'LOGS', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'BINLOG', 3),
            (3, token.MySQLKeywordToken, 'EVENTS', 4),
            (4, token.MySQLKeywordToken, 'IN', 5),
            (5, token.MySQLStringToken, None, 6),
            ((4, 6), token.MySQLKeywordToken, 'FROM', 7),
            (7, token.MySQLNumericToken, None, 8), # [LIMIT [offset,] row_count]
            ((4, 6, 8), token.MySQLKeywordToken, 'LIMIT', 9),
            (9, token.MySQLNumericToken, None, 10),
            (10, token.MySQLDelimiterToken, ',', 11),
            (11, token.MySQLNumericToken, None, self.get_final_status()),
            (1, token.MySQLKeywordToken, 'CHARACTER', 12),
            (12, token.MySQLKeywordToken, 'SET', 13), # [like_or_where]
            (1, token.MySQLKeywordToken, 'CHARSET', 13),
            ((13, 19), token.MySQLKeywordToken, 'LIKE', 14),
            (14, token.MySQLStringToken, None, self.get_final_status()),
            ((13, 19), token.MySQLKeywordToken, 'WHERE', 15),
            (15, component.expression.MySQLExpressionComponent, None, self.get_final_status()),
            (1, token.MySQLKeywordToken, 'COLLATION', 13),
            (1, token.MySQLKeywordToken, 'FULL', 16),
            ((1, 16), token.MySQLKeywordToken, 'COLUMNS', 17), # {FROM | IN} tbl_name [{FROM | IN} db_name] [like_or_where]
            ((1, 16), token.MySQLKeywordToken, 'FIELDS', 17),
            (17, token.MySQLKeywordToken, 'FROM', 18),
            (17, token.MySQLKeywordToken, 'IN', 18),
            (18, component.identifier.MySQLTableNameComponent, None, 19), # [{FROM | IN} db_name] [like_or_where]
            (19, token.MySQLKeywordToken, 'FROM', 20),
            (19, token.MySQLKeywordToken, 'IN', 20),
            (20, component.identifier.MySQLDatabaseNameComponent, None, 13),
            (1, token.MySQLKeywordToken, 'CONTRIBUTORS', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'CREATE', 21),
            (21, token.MySQLKeywordToken, 'DATABASE', 22),
            (21, token.MySQLKeywordToken, 'SCHEMA', 22),
            (22, token.MySQLKeywordToken, 'IF', 32),
            (32, token.MySQLKeywordToken, 'NOT', 33),
            (33, token.MySQLKeywordToken, 'EXISTS', 34),
            ((22, 34), component.identifier.MySQLDatabaseNameComponent, None, self.get_final_status()),
            (21, token.MySQLKeywordToken, 'EVENT', 23),
            (23, component.identifier.MySQLIdentifierComponent, None, self.get_final_status()),
            (21, token.MySQLKeywordToken, 'FUNCTION', 23),
            (21, token.MySQLKeywordToken, 'PROCEDURE', 23),
            (21, token.MySQLKeywordToken, 'TABLE', 24),
            (24, component.identifier.MySQLTableNameComponent, None, self.get_final_status()),
            (21, token.MySQLKeywordToken, 'TRIGGER', 23),
            (21, token.MySQLKeywordToken, 'VIEW', 23),
            (1, token.MySQLKeywordToken, 'DATABASES', 13),
            (1, token.MySQLKeywordToken, 'SCHEMAS', 13),
            (1, token.MySQLKeywordToken, 'ENGINE', 25),
            (25, component.identifier.MySQLEngineNameComponent, None, 26),
            ((26, 42, 56), token.MySQLKeywordToken, 'STATUS', self.get_final_status()),
            (26, token.MySQLKeywordToken, 'MUTEX', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'STORAGE', 27),
            ((1, 27), token.MySQLKeywordToken, 'ENGINES', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'ERRORS', 8),
            (1, token.MySQLKeywordToken, 'COUNT', 35),
            (35, token.MySQLOperatorToken, '(', 36),
            (36, token.MySQLOperatorToken, '*', 37),
            (37, token.MySQLOperatorToken, ')', 38),
            (38, token.MySQLKeywordToken, 'ERRORS', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'EVENTS', 19),
            (1, token.MySQLKeywordToken, 'FUNCTION', 28),
            (28, token.MySQLKeywordToken, 'CODE', 29),
            (29, component.identifier.MySQLIdentifierComponent, None, self.get_final_status()),
            (28, token.MySQLKeywordToken, 'STATUS', 13),
            (1, token.MySQLKeywordToken, 'GRANTS', 30),
            (30, token.MySQLKeywordToken, 'FOR', 31),
            (31, token.MySQLKeywordToken, 'CURRENT_USER', 39),
            (39, token.MySQLOperatorToken, '(', 40),
            (40, token.MySQLOperatorToken, ')', self.get_final_status()),
            (31, token.MySQLStringToken, None, 41),
            (41, token.MySQLVariableToken, None, self.get_final_status()),
            (1, token.MySQLKeywordToken, 'INDEX', 17),
            (1, token.MySQLKeywordToken, 'INDEXES', 17),
            (1, token.MySQLKeywordToken, 'KEYS', 17),
            (1, token.MySQLKeywordToken, 'MASTER', 42),
            (1, token.MySQLKeywordToken, 'OPEN', 43),
            (43, token.MySQLKeywordToken, 'TABLES', 19),
            (1, token.MySQLKeywordToken, 'PLUGINS', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'PRIVILEGES', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'PROCEDURE', 28),
            ((1, 16), token.MySQLKeywordToken, 'PROCESSLIST', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'PROFILE', 44),
            ((44, 49), token.MySQLKeywordToken, 'ALL', 45),
            ((44, 49), token.MySQLKeywordToken, 'BLOCK', 46),
            (46, token.MySQLKeywordToken, 'IO', 45),
            ((44, 49), token.MySQLKeywordToken, 'CONTEXT', 47),
            (47, token.MySQLKeywordToken, 'SWITCHES', 45),
            ((44, 49), token.MySQLKeywordToken, 'CPU', 45),
            ((44, 49), token.MySQLKeywordToken, 'IPC', 45),
            ((44, 49), token.MySQLKeywordToken, 'MEMORY', 45),
            ((44, 49), token.MySQLKeywordToken, 'PAGE', 48),
            (48, token.MySQLKeywordToken, 'FAULTS', 45),
            ((44, 49), token.MySQLKeywordToken, 'SOURCE', 45),
            ((44, 49), token.MySQLKeywordToken, 'SWAPS', 45),
            (45, token.MySQLDelimiterToken, ',', 49),
            ((44, 45), token.MySQLKeywordToken, 'FOR', 50),
            (50, token.MySQLKeywordToken, 'QUERY', 51),
            (51, token.MySQLNumericToken, None, 52),
            ((44, 45, 52), token.MySQLKeywordToken, 'LIMIT', 53),
            (53, token.MySQLNumericToken, None, 54),
            (54, token.MySQLKeywordToken, 'OFFSET', 55),
            (55, token.MySQLNumericToken, None, self.get_final_status()),
            (1, token.MySQLKeywordToken, 'PROFILES', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'RELAYLOG', 3),
            (1, token.MySQLKeywordToken, 'SLAVE', 56),
            (56, token.MySQLKeywordToken, 'HOSTS', self.get_final_status()),
            (1, token.MySQLKeywordToken, 'GLOBAL', 57),
            (1, token.MySQLKeywordToken, 'SESSION', 57),
            ((1, 57), token.MySQLKeywordToken, 'STATUS', 13),
            (1, token.MySQLKeywordToken, 'TABLE', 58),
            (58, token.MySQLKeywordToken, 'STATUS', 19),
            ((1, 16), token.MySQLKeywordToken, 'TABLES', 19),
            (1, token.MySQLKeywordToken, 'TRIGGERS', 19),
            ((1, 57), token.MySQLKeywordToken, 'VARIABLES', 13),
            (1, token.MySQLKeywordToken, 'WARNINGS', 8),
            (38, token.MySQLKeywordToken, 'WARNINGS', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        s = ShowStatement()
        end_pos = s.parse_by_fsm(token_list, [4, 6, 8, 10, 13, 19, 30, 39, 44, 45, 52, 54], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in s.token_list:
                if type(t) is component.identifier.MySQLDatabaseNameComponent:
                    s.database.append(t.database)
                    s.table.append('')
                elif type(t) is component.identifier.MySQLTableNameComponent:
                    s.database.append(t.database)
                    s.table.append(t.table)
                elif type(t) is component.expression.MySQLExpressionComponent:
                    for tt in filter((lambda x: type(x) is component.reference.SubQueryComponent), t.token_list):
                        s.database.extend(tt.database)
                        s.database.extend(tt.table)
            token_list.reset(end_pos)
            return s, token_list

