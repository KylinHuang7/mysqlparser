#!/usr/local/ieod-web/python/bin/python
# -*- coding: utf-8 -*-

#=============================================================================
#  @desc       
#  @version    1.0.0
#  @author     kylinshuang
#  @date       2017-12-04
#=============================================================================

import mysqltoken as token
import component
import component.identifier

class MySQLExpressionComponent(component.MySQLComponent):
    support_keyword = [
        'AND',              'BETWEEN',          'BINARY',               'CASE',                 'COLLATE',
        'CURRENT_DATE',     'CURRENT_TIME',     'CURRENT_TIMESTAMP',    'CURRENT_USER',         'DIV',
        'ELSE',             'END',              'EXISTS',               'IN',                   'INTERVAL',
        'IS',               'LAST_DAY',         'LIKE',                 'LOCALTIME',            'LOCALTIMESTAMP',
        'MATCH',            'MOD',              'NOT',                  'OR',                   'REGEXP',
        'RLIKE',            'SOUNDS',           'THEN',                 'WHEN',                 'XOR',
    ]
    support_in_function_keyword = [
        'AS',               'ASC',              'BY',                   'DESC',                 'DISTINCT',
        'GROUP',            'ORDER',            'SEPARATOR',            'USING',
    ]
    support_function = [
        'ABS',              'ACOS',                 'ADDDATE',              'ADDTIME',          'AES_DECRYPT',
        'AES_ENCRYPT',      'ASCII',                'ASIN',                 'ATAN',             'ATAN2',
        'AVG',              'BENCHMARK',            'BIN',                  'BIT_AND',          'BIT_COUNT',
        'BIT_LENGTH',       'BIT_OR',               'BIT_XOR',              'CAST',             'CEIL', 
        'CEILING',          'CHAR',                 'CHARACTER_LENGTH',     'CHARSET',          'CHAR_LENGTH', 
        'COERCIBILITY',     'COLLATION',            'COMPRESS',             'CONCAT',           'CONCAT_WS',
        'CONNECTION_ID',    'CONV',                 'CONVERT',              'CONVERT_TZ',       'COS',
        'COT',              'COUNT',                'CRC32',                'CURDATE',          'CURRENT_DATE',
        'CURRENT_TIME',     'CURRENT_TIMESTAMP',    'CURRENT_USER',         'CURTIME',          'DATABASE',
        'DATE',             'DATEDIFF',             'DATE_ADD',             'DATE_FORMAT',      'DATE_SUB',
        'DAY',              'DAYNAME',              'DAYOFMONTH',           'DAYOFWEEK',        'DAYOFYEAR',
        'DECODE',           'DEFAULT',              'DEGREES',              'DES_DECRYPT',      'DES_ENCRYPT',
        'ELT',              'ENCODE',               'ENCRYPT',              'EXP',              'EXPORT_SET',
        'EXTRACT',          'FIELD',                'FIND_IN_SET',          'FLOOR',            'FORMAT',
        'FORM_UNIXTIME',    'FOUND_ROWS',           'FROM_DAYS',            'GET_FORMAT',       'GET_LOCK',
        'GROUP_CONCAT',     'HEX',                  'HOUR',                 'IF',               'IFNULL',
        'INET_ATON',        'INET_NTOA',            'INSERT',               'INSTR',            'IS_FREE_LOCK',
        'IS_USED_LOCK',     'LAST_INSERT_ID',       'LCASE',                'LEFT',             'LENGTH',
        'LN',               'LOAD_FILE',            'LOCALTIME',            'LOCALTIMESTAMP',   'LOCATE',
        'LOG',              'LOG10',                'LOG2',                 'LOWER',            'LPAD',
        'LTRIM',            'MAKEDATE',             'MAKETIME',             'MAKE_SET',         'MASTER_POS_WAIT',
        'MAX',              'MD5',                  'MICROSECOND',          'MID',              'MIN',
        'MINUTE',           'MOD',                  'MONTH',                'MONTHNAME',        'NAME_CONST',
        'NOW',              'NULLIF',               'OCT',                  'OCTET_LENGTH',     'OLD_PASSWORD',
        'ORD',              'PASSWORD',             'PERIOD_ADD',           'PERIOD_DIFF',      'PI', 
        'POSITION',         'POW',                  'POWER',                'QUARTER',          'QUOTE',
        'RADIANS',          'RAND',                 'RELEASE_LOCK',         'REPEAT',           'REPLACE',
        'REVERSE',          'RIGHT',                'ROUND',                'ROW_COUNT',        'RPAD',
        'RTRIM',            'SCHEMA',               'SECOND',               'SESSION_USER',     'SET_TO_TIME',
        'SHA',              'SHA1',                 'SHA2',                 'SIGN',             'SIN', 
        'SLEEP',            'SOUNDEX',              'SPACE',                'SQRT',             'STD',
        'STDDEV',           'STDDEV_POP',           'STDDEV_SAMP',          'STRCMP',           'STR_TO_DATE',
        'SUBDATE',          'SUBSTR',               'SUBSTRING',            'SUBSTRING_INDEX',  'SUM',
        'SYSDATE',          'SYSTEM_USER',          'TAN',                  'TIME',             'TIMEDIFF',
        'TIMESTAMP',        'TIMESTAMPADD',         'TIMESTAMPDIFF',        'TIME_FORMAT',      'TIME_TO_SEC',
        'TO_DAYS',          'TO_SECONDS',           'TRIM',                 'TRUNCATE',         'UCASE',
        'UNCOMPRESS',       'UNCOMPRESSED_LENGTH',  'UNHEX',                'UNIX_TIMESTAMP',   'UPPER',
        'USER',             'UTC_DATE',             'UTC_TIME',             'UTC_TIMESTAMP',    'UUID',
        'UUID_SHORT',       'VALUES',               'VARIANCE',             'VAR_POP',          'VAR_SAMP',
        'VERSION',          'WEEK',                 'WEEKDAY',              'WEEKOFYEAR',       'YEAR',
        'YEARWEEK',
    ]
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLExpressionComponent()
        in_bracket = 0
        bracket_token_list = []
        bracket_value = ''
        last_term_pos = token_list.current_pos()
        in_function = False
        while not token_list.eof():
            try:
                t = token_list.next()
            except:
                break
            if verbose_func:
                verbose_func("EXPRESSION DEAL WITH {0}: {1}".format(t.type(), t.value), 3)
            if t.type() is token.MySQLDelimiterToken and t.value == ';':
                token_list.reset(token_list.current_pos() - 1)
                break
            elif t.type() is token.MySQLDelimiterToken and t.value == ',':
                if in_bracket == 0:
                    token_list.reset(token_list.current_pos() - 1)
                    break
                else:
                    bracket_token_list.append(t)
                    bracket_value += t.value
                    last_term_pos = token_list.current_pos()
                    if verbose_func:
                        verbose_func("EXPRESSION IN ',' {0}, {1}, {2}, {3}".format(bracket_token_list, bracket_value, last_term_pos, in_bracket), 3)
            elif t.type() is token.MySQLOperatorToken and t.value == '(':
                next_token = token_list.get_next_valid_token(1)
                if verbose_func:
                    verbose_func("EXPRESSION IN '(' {0}: {1}".format(next_token[0].type(), next_token[0].value), 3)
                if next_token[0].type() is token.MySQLKeywordToken and next_token[0].value == 'SELECT':
                    token_list.reset(token_list.current_pos() - 1)
                    subquery, token_list = component.reference.SubQueryComponent.parse(token_list, verbose_func=verbose_func)
                    if subquery:
                        if in_bracket > 0 :
                            bracket_token_list.append(subquery)
                            bracket_value += subquery.value
                            if verbose_func:
                                verbose_func("EXPRESSION IN SUBQUERY {0}, {1}, {2}, {3}".format(bracket_token_list, bracket_value, last_term_pos, in_bracket), 3)
                        else:
                            c.token_list.append(subquery)
                            c.value += subquery.value
                            last_term_pos = token_list.current_pos()
                            if verbose_func:
                                verbose_func("EXPRESSION IN SUBQUERY {0}, {1}, {2}, {3}".format(c.token_list, c.value, last_term_pos, in_bracket), 3)
                    else:
                        token_list.reset(token_list.current_pos() - 1)
                        break
                else:
                    bracket_token_list.append(t)
                    bracket_value += t.value
                    in_bracket += 1
                    if verbose_func:
                        verbose_func("EXPRESSION IN '(' {0}, {1}, {2}, {3}".format(bracket_token_list, bracket_value, last_term_pos, in_bracket), 3)
            elif t.type() is token.MySQLOperatorToken and t.value == ')':
                if in_bracket == 0:
                    token_list.reset(token_list.current_pos() - 1)
                    break
                bracket_token_list.append(t)
                bracket_value += t.value
                in_bracket -= 1
                if in_bracket == 0:
                    c.token_list.extend(bracket_token_list)
                    bracket_token_list = []
                    c.value += bracket_value
                    bracket_value = ''
                    last_term_pos = token_list.current_pos()
                    if verbose_func:
                        verbose_func("EXPRESSION IN ')' {0}, {1}, {2}, {3}".format(c.token_list, c.value, last_term_pos, in_bracket), 3)
            elif t.type() is token.MySQLKeywordToken and t.value in cls.support_in_function_keyword:
                if in_bracket > 0:
                    bracket_token_list.append(t)
                    bracket_value += t.value
                    if verbose_func:
                        verbose_func("EXPRESSION IN ELSE {0}, {1}, {2}, {3}".format(bracket_token_list, bracket_value, last_term_pos, in_bracket), 3)
                else:
                    token_list.reset(token_list.current_pos() - 1)
                    break
            elif t.type() is token.MySQLKeywordToken and t.value not in cls.support_keyword and t.value not in cls.support_function and t.value not in token.MySQLKeywordToken.keywords:
                token_list.reset(token_list.current_pos() - 1)
                break
            else:
                if in_bracket > 0 :
                    bracket_token_list.append(t)
                    bracket_value += t.value
                    if verbose_func:
                        verbose_func("EXPRESSION IN ELSE {0}, {1}, {2}, {3}".format(bracket_token_list, bracket_value, last_term_pos, in_bracket), 3)
                else:
                    c.token_list.append(t)
                    c.value += t.value
                    if t.type() not in [token.MySQLCommentToken, token.MySQLSpaceToken]:
                        last_term_pos = token_list.current_pos()
                    if verbose_func:
                        verbose_func("EXPRESSION IN ELSE {0}, {1}, {2}, {3}".format(c.token_list, c.value, last_term_pos, in_bracket), 3)
        if verbose_func:
            verbose_func("EXPRESSION END {0}, {1}, {2}, {3}".format(start_pos, last_term_pos, bracket_token_list, token_list.eof()), 3)
        if last_term_pos == start_pos:
            token_list.reset(start_pos)
            return None, token_list
        elif bracket_token_list:
            token_list.reset(last_term_pos)
            return c, token_list
        return c, token_list

# subpartitioning expr:
#     [LINEAR] HASH(expr)
#   | [LINEAR] KEY [ALGORITHM={1|2}] (column_list)
class MySQLSubPartitioningExpressionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'LINEAR', 1),
            ((0, 1), token.MySQLKeywordToken, 'HASH', 2),
            (2, token.MySQLOperatorToken, '(', 3),
            (3, MySQLExpressionComponent, None, 4),
            (4, token.MySQLOperatorToken, ')', self.get_final_status()),
            ((0, 1), token.MySQLKeywordToken, 'KEY', 5),
            (5, token.MySQLKeywordToken, 'ALGORITHM', 6),
            (6, token.MySQLOperatorToken, '=', 7),
            (7, token.MySQLNumericToken, 1, 8),
            (7, token.MySQLNumericToken, 2, 8),
            ((5, 8), token.MySQLOperatorToken, '(', 9),
            (9, component.identifier.MySQLColumnNameListComponent, None, 10),
            (10, token.MySQLOperatorToken, ')', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLSubPartitioningExpressionComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list


# partitioning expr:
#     [LINEAR] HASH(expr)
#   | [LINEAR] KEY [ALGORITHM={1|2}] (column_list)
#   | RANGE{(expr) | COLUMNS(column_list)}
#   | LIST{(expr) | COLUMNS(column_list)}
class MySQLPartitioningExpressionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, token.MySQLKeywordToken, 'LINEAR', 1),
            ((0, 1), token.MySQLKeywordToken, 'HASH', 2),
            (2, token.MySQLOperatorToken, '(', 3),
            (3, MySQLExpressionComponent, None, 4),
            (4, token.MySQLOperatorToken, ')', self.get_final_status()),
            ((0, 1), token.MySQLKeywordToken, 'KEY', 5),
            (5, token.MySQLKeywordToken, 'ALGORITHM', 6),
            (6, token.MySQLOperatorToken, '=', 7),
            (7, token.MySQLNumericToken, 1, 8),
            (7, token.MySQLNumericToken, 2, 8),
            ((5, 8), token.MySQLOperatorToken, '(', 9),
            (9, component.identifier.MySQLColumnNameListComponent, None, 10),
            (10, token.MySQLOperatorToken, ')', self.get_final_status()),
            (0, token.MySQLKeywordToken, 'RANGE', 11),
            (0, token.MySQLKeywordToken, 'LIST', 11),
            (11, token.MySQLOperatorToken, '(', 3),
            (11, token.MySQLKeywordToken, 'COLUMNS', 8),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLPartitioningExpressionComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

# assignment:
#    col_name = value
class MySQLAssignmentExpressionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, component.identifier.MySQLColumnNameComponent, None, 1),
            (1, token.MySQLOperatorToken, '=', 2),
            (2, MySQLExpressionComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLAssignmentExpressionComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list
#
# assignment_list:
#    assignment [, assignment] ...
class MySQLAssignmentListExpressionComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            ((0, 2), MySQLAssignmentExpressionComponent, None, 1),
            (1, token.MySQLDelimiterToken, ',', 2),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLAssignmentListExpressionComponent()
        end_pos = c.parse_by_fsm(token_list, [1], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list
