#!/usr/local/ieod-web/python/bin/python
# -*- coding: utf-8 -*-

#=============================================================================
#  @desc       
#  @version    1.0.0
#  @author     kylinshuang
#  @date       2017-12-04
#=============================================================================

import re

class MySQLToken(object):
    def __init__(self):
        self.value = ''
    
    def __str__(self):
        return self.value
    
    def type(self):
        return type(self)

class MySQLStringToken(MySQLToken):
    @classmethod
    def parse(cls, sql):
        if sql[0] not in ['N', '"', "'"]:
            return None, sql
        token = MySQLStringToken()
        single_quotes_regex = re.compile(r"N?'(''|\\\\|\\'|[^'])*'", re.I)
        double_quotes_regex = re.compile(r'N?(""|".*?[^\\]")', re.S | re.I)
        m_1 = single_quotes_regex.match(sql)
        m_2 = double_quotes_regex.match(sql)
        if m_1:
            token.value = m_1.group(0)
            sql = sql[len(m_1.group(0)):]
        elif m_2:
            token.value = m_2.group(0)
            sql = sql[len(m_2.group(0)):]
        else:
            return None, sql
        return token, sql

class MySQLNumericToken(MySQLToken):
    @classmethod
    def parse(cls, sql):
        if sql[0] not in ['+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            return None, sql
        token = MySQLNumericToken()
        numeric_regex = re.compile(r"[+-]?(\d+(\.\d*)?|\.\d+)(E[+-]?\d+)?", re.I)
        m = numeric_regex.match(sql)
        if m:
            token.value += m.group(0)
            sql = sql[len(m.group(0)):]
        else:
            return None, sql
        return token, sql

class MySQLHexadecimalToken(MySQLToken):
    @classmethod
    def parse(cls, sql):
        if sql[0] not in ['0', 'X', 'x']:
            return None, sql
        token = MySQLHexadecimalToken()
        x_regex = re.compile(r"X'([0-9A-F][0-9A-F])+'", re.I)
        d_regex = re.compile(r"0x([0-9A-Fa-f][0-9A-Fa-f])+")
        m_1 = x_regex.match(sql)
        m_2 = d_regex.match(sql)
        if m_1:
            token.value += m_1.group(0)
            sql = sql[len(m_1.group(0)):]
        elif m_2:
            token.value += m_2.group(0)
            sql = sql[len(m_2.group(0)):]
        else:
            return None, sql
        return token, sql

class MySQLBitToken(MySQLToken):
    @classmethod
    def parse(cls, sql):
        if sql[0] not in ['0', 'B', 'b']:
            return None, sql
        token = MySQLBitToken()
        b_regex = re.compile(r"B'[01]+'", re.I)
        d_regex = re.compile(r"0b[01]+")
        m_1 = b_regex.match(sql)
        m_2 = d_regex.match(sql)
        if m_1:
            token.value += m_1.group(0)
            sql = sql[len(m_1.group(0)):]
        elif m_2:
            token.value += m_2.group(0)
            sql = sql[len(m_2.group(0)):]
        else:
            return None, sql
        return token, sql

class MySQLNullToken(MySQLToken):
    @classmethod
    def parse(cls, sql):
        if sql[0] not in ['N', 'n', '\\']:
            return None, sql
        token = MySQLNullToken()
        if sql.startswith('\\N'):
            token.value = '\\N'
            sql = sql[2:]
            return token, sql
        else:
            keyword, sql = MySQLKeywordToken.parse(sql, expect_keywords=['NULL'])
            if keyword:
                token.value = keyword.value
                return token, sql
        return None, sql

class MySQLQuotedIdentifierToken(MySQLToken):
    @classmethod
    def parse(cls, sql):
        if sql[0] not in ['`']:
            return None, sql
        token = MySQLQuotedIdentifierToken()
        regex = re.compile(r"`(``|[\u0001-\u005f\u0061-\uffff])+`")
        m = regex.match(sql)
        if m:
            token.value += m.group(0)
            sql = sql[len(m.group(0)):]
            return token, sql
        return None, sql

class MySQLUnquotedIdentifierToken(MySQLToken):
    @classmethod
    def parse(cls, sql, allow_keyword=False):
        token = MySQLUnquotedIdentifierToken()
        """ for perfomance, not need
        if not allow_keyword:
            keyword, sql = MySQLKeywordToken.parse(sql, expect_keywords=MySQLKeywordToken.reserved_keywords)
            if keyword:
                return None, sql
        number, sql = MySQLNumericToken.parse(sql)
        if number:
            return None, sql
        """
        regex = re.compile(r"\b[0-9a-zA-Z$_\u0080-\uffff]+\b", re.UNICODE)
        m = regex.match(sql)
        if m:
            token.value += m.group(0)
            sql = sql[len(m.group(0)):]
            return token, sql
        return None, sql

class MySQLVariableToken(MySQLToken):
    @classmethod
    def parse(cls, sql):
        if sql[0] not in ['@']:
            return None, sql
        token = MySQLVariableToken()
        user_single_quotes_regex = re.compile(r"@'(''|\\\\|\\'|[^'])*'", re.I)
        user_double_quotes_regex = re.compile(r'@(""|".*?[^\\]")', re.S | re.I)
        user_quotes_regex = re.compile(r"@`(``|[\u0001-\u005f\u0061-\uffff])+`")
        user_unquotes_regex = re.compile(r"@[0-9a-z_.$]+", re.I)
        system_regex = re.compile(r"@@(global\.|session\.)?[a-zA-Z-_]+")
        m_1 = user_single_quotes_regex.match(sql)
        m_2 = user_double_quotes_regex.match(sql)
        m_3 = user_quotes_regex.match(sql)
        m_4 = user_unquotes_regex.match(sql)
        m_5 = system_regex.match(sql)
        if m_1:
            token.value = m_1.group(0)
            sql = sql[len(m_1.group(0)):]
        elif m_2:
            token.value = m_2.group(0)
            sql = sql[len(m_2.group(0)):]
        elif m_3:
            token.value = m_3.group(0)
            sql = sql[len(m_3.group(0)):]
        elif m_4:
            token.value = m_4.group(0)
            sql = sql[len(m_4.group(0)):]
        elif m_5:
            token.value = m_5.group(0)
            sql = sql[len(m_5.group(0)):]
        else:
            return None, sql
        return token, sql

class MySQLCommentToken(MySQLToken):
    @classmethod
    def parse(cls, sql):
        if sql[0] not in ['-', '/', '#']:
            return None, sql
        token = MySQLCommentToken()
        singleline_regex = re.compile(r'(--\s+|#).*?(\r\n|\r|\n|$)')
        multiline_regex = re.compile(r'/\*.*?\*/', re.M)
        m_1 = singleline_regex.match(sql)
        m_2 = multiline_regex.match(sql)
        if m_1:
            token.value = m_1.group(0)
            sql = sql[len(m_1.group(0)):]
            return token, sql
        elif m_2:
            token.value = m_2.group(0)
            sql = sql[len(m_2.group(0)):]
            return token, sql
        return None, sql

class MySQLSpaceToken(MySQLToken):
    @classmethod
    def parse(cls, sql):
        if sql[0] not in [' ', '\t', '\n', '\r']:
            return None, sql
        token = MySQLSpaceToken()
        regex = re.compile(r"\s+")
        m = regex.match(sql)
        if m:
            token.value = m.group(0)
            sql = sql[len(m.group(0)):]
            return token, sql
        return None, sql

class MySQLDelimiterToken(MySQLToken):
    @classmethod
    def parse(cls, sql):
        if sql[0] not in [',', ';']:
            return None, sql
        token = MySQLDelimiterToken()
        if sql.startswith(';') or sql.startswith(','):
            token.value = sql[0]
            sql = sql[1:]
            return token, sql
        return None, sql

class MySQLOperatorToken(MySQLToken):
    operators = [
        '&&',   '&',    '||',   '|',    '~',
        '<<',   '<=>',  '>>',   '<=',   '>=',
        '<>',   '>',    '<',    '!=',   '!',
        '+',    '-',    '*',    '/',    '^',
        '%',    '=',    ':=',   '(',    ')',
        '.',
    ]
    @classmethod
    def parse(cls, sql):
        if sql[0] not in ['&', '|', '~', '<', '>', '!', '+', '-', '*', '/', '^', '%', '=', ':', '(', ')', '.']:
            return None, sql
        token = MySQLOperatorToken()
        for k in cls.operators:
            if sql.startswith(k):
                token.value = k
                sql = sql[len(k):]
                return token, sql
        return None, sql

class MySQLKeywordToken(MySQLToken):
    keywords = [
        'ABS',                      'ACOS',                         'ACTION',                   'ADDDATE',              'ADDTIME', 
        'AES_DECRYPT',              'AES_ENCRYPT',                  'AFTER',                    'AGAINST',              'AGGREGATE', 
        'ALGORITHM',                'ANY',                          'ASCII',                    'ASIN',                 'AT', 
        'ATAN',                     'ATAN2',                        'AUTHORS',                  'AUTO_INCREMENT',       'AUTOEXTEND_SIZE', 
        'AVG',                      'AVG_ROW_LENGTH',               'BACKUP',                   'BEGIN',                'BENCHMARK', 
        'BIN',                      'BINLOG',                       'BIT',                      'BIT_AND',              'BIT_COUNT', 
        'BIT_LENGTH',               'BIT_OR',                       'BIT_XOR',                  'BLOCK',                'BOOL', 
        'BOOLEAN',                  'BTREE',                        'BYTE',                     'CACHE',                'CASCADED', 
        'CAST',                     'CATALOG_NAME',                 'CCONCAT_WS',               'CEIL',                 'CEILING', 
        'CHAIN',                    'CHANGED',                      'CHAR_LENGTH',              'CHARACTER_LENGTH',     'CHARSET', 
        'CHECKSUM',                 'CIPHER',                       'CLASS_ORIGIN',             'CLIENT',               'CLOSE', 
        'COALESCE',                 'CODE',                         'COERCIBILITY',             'COLLATION',            'COLUMN_NAME', 
        'COLUMNS',                  'COMMENT',                      'COMMIT',                   'COMMITTED',            'COMPACT', 
        'COMPLETION',               'COMPRESS',                     'COMPRESSED',               'CONCAT',               'CONCURRENT', 
        'CONNECTION',               'CONNECTION_ID',                'CONSISTENT',               'CONSTRAINT_CATALOG',   'CONSTRAINT_NAME', 
        'CONSTRAINT_SCHEMA',        'CONTAINS',                     'CONTEXT',                  'CONTRIBUTORS',         'CONV', 
        'CONVERT_TZ',               'COS',                          'COT',                      'COUNT',                'CPU', 
        'CRC32',                    'CUBE',                         'CURDATE',                  'CURSOR_NAME',          'CURTIME', 
        'DATA',                     'DATAFILE',                     'DATE',                     'DATE_ADD',             'DATE_FORMAT', 
        'DATE_SUB',                 'DATEDIFF',                     'DATETIME',                 'DAY',                  'DAYNAME', 
        'DAYOFMONTH',               'DAYOFWEEK',                    'DAYOFYEAR',                'DEALLOCATE',           'DECODE', 
        'DEFINER',                  'DEGREES',                      'DELAY_KEY_WRITE',          'DES_DECRYPT',          'DES_ENCRYPT', 
        'DES_KEY_FILE',             'DIRECTORY',                    'DISABLE',                  'DISCARD',              'DISK', 
        'DO',                       'DUMPFILE',                     'DUPLICATE',                'DYNAMIC',              'ELT', 
        'ENABLE',                   'ENCODE',                       'ENCRYPT',                  'END',                  'ENDS', 
        'ENGINE',                   'ENGINES',                      'ENUM',                     'ERROR',                'ERRORS', 
        'ESCAPE',                   'EVENT',                        'EVENTS',                   'EVERY',                'EXECUTE', 
        'EXP',                      'EXPANSION',                    'EXPORT_SET',               'EXTENDED',             'EXTENT_SIZE', 
        'EXTRACT',                  'FAST',                         'FAULTS',                   'FIELD',                'FIELDS', 
        'FILE',                     'FIND_IN_SET',                  'FIRST',                    'FIXED',                'FLOOR', 
        'FLUSH',                    'FORM_UNIXTIME',                'FORMAT',                   'FOUND',                'FOUND_ROWS', 
        'FRAC_SECOND',              'FROM_DAYS',                    'FULL',                     'FUNCTION',             'GEOMETRY', 
        'GEOMETRYCOLLECTION',       'GET_FORMAT',                   'GET_LOCK',                 'GLOBAL',               'GRANTS', 
        'GROUP_CONCAT',             'HANDLER',                      'HASH',                     'HELP',                 'HEX', 
        'HOST',                     'HOSTS',                        'HOUR',                     'IDENTIFIED',           'IFNULL', 
        'IGNORE_SERVER_IDS',        'IMPORT',                       'INDEXES',                  'INET_ATON',            'INET_NTOA', 
        'INITIAL_SIZE',             'INNOBASE',                     'INNODB',                   'INSERT_METHOD',        'INSTALL', 
        'INSTR',                    'INTERNAL',                     'INTO', 'INVOKER',          'IO',                   'IO_THREAD', 
        'IPC',                      'IS_FREE_LOCK',                 'IS_USED_LOCK',             'ISOLATION',            'ISSUER', 
        'KEY_BLOCK_SIZE',           'LANGUAGE',                     'LAST',                     'LAST_DAY',             'LAST_INSERT_ID', 
        'LCASE',                    'LEAVES',                       'LENGTH',                   'LESS',                 'LEVEL', 
        'LINESTRING',               'LIST',                         'LN',                       'LOAD_FILE',            'LOCAL', 
        'LOCATE',                   'LOCKS',                        'LOG',                      'LOG10',                'LOG2', 
        'LOGFILE',                  'LOGS',                         'LOWER',                    'LPAD',                 'LTRIM', 
        'MAKE_SET',                 'MAKEDATE',                     'MAKETIME',                 'MASTER',               'MASTER_CONNECT_RETRY', 
        'MASTER_HEARTBEAT_PERIOD',  'MASTER_HOST',                  'MASTER_LOG_FILE',          'MASTER_LOG_POS',       'MASTER_PASSWORD', 
        'MASTER_PORT',              'MASTER_POS_WAIT',              'MASTER_SERVER_ID',         'MASTER_SSL',           'MASTER_SSL_CA', 
        'MASTER_SSL_CAPATH',        'MASTER_SSL_CERT',              'MASTER_SSL_CIPHER',        'MASTER_SSL_KEY',       'MASTER_USER', 
        'MAX',                      'MAX_CONNECTIONS_PER_HOUR',     'MAX_QUERIES_PER_HOUR',     'MAX_ROWS',             'MAX_SIZE', 
        'MAX_UPDATES_PER_HOUR',     'MAX_USER_CONNECTIONS',         'MD5',                      'MEDIUM',               'MEMORY', 
        'MERGE',                    'MESSAGE_TEXT',                 'MICROSECOND',              'MID',                  'MIGRATE', 
        'MIN',                      'MIN_ROWS',                     'MINUTE',                   'MODE',                 'MODIFY', 
        'MONTH',                    'MONTHNAME',                    'MULTILINESTRING',          'MULTIPOINT',           'MULTIPOLYGON', 
        'MUTEX',                    'MYSQL_ERRNO',                  'NAME',                     'NAME_CONST',           'NAMES', 
        'NATIONAL',                 'NCHAR',                        'NDB',                      'NDBCLUSTER',           'NEW', 
        'NEXT',                     'NO',                           'NO_WAIT',                  'NODEGROUP',            'NONE', 
        'NOW',                      'NULLIF',                       'NVARCHAR',                 'OCT',                  'OCTET_LENGTH', 
        'OFFSET',                   'OJ',                           'OLD_PASSWORD',             'ONE',                  'ONE_SHOT',
        'OPEN',                     'OPTIONS',                      'ORD',                      'OWNER',                'PACK_KEYS',
        'PAGE',                     'PARSER',                       'PARTIAL',                  'PARTITION',            'PARTITIONING',
        'PARTITIONS',               'PASSWORD',                     'PERIOD_ADD',               'PERIOD_DIFF',          'PHASE',
        'PI', 'PLUGIN',             'PLUGINS',                      'POINT',                    'POLYGON',              'PORT', 
        'POSITION',                 'POW',                          'POWER',                    'PREPARE',              'PRESERVE', 
        'PREV',                     'PRIVILEGES',                   'PROCESSLIST',              'PROFILE',              'PROFILES', 
        'PROXY',                    'QUARTER',                      'QUERY',                    'QUICK',                'QUOTE', 
        'RADIANS',                  'RAND',                         'READ_ONLY',                'REBUILD',              'RECOVER', 
        'REDO_BUFFER_SIZE',         'REDOFILE',                     'REDUNDANT',                'RELAY',                'RELAY_LOG_FILE', 
        'RELAY_LOG_POS',            'RELAY_THREAD',                 'RELAYLOG',                 'RELEASE_LOCK',         'RELOAD', 
        'REMOVE',                   'REORGANIZE',                   'REPAIR',                   'REPEATABLE',           'REPLICATION', 
        'RESET',                    'RESTORE',                      'RESUME',                   'RETURNS',              'REVERSE', 
        'ROLLBACK',                 'ROLLUP',                       'ROUND',                    'ROUTINE',              'ROW', 
        'ROW_COUNT',                'ROW_FORMAT',                   'ROWS',                     'RPAD',                 'RTREE', 
        'RTRIM',                    'SAVEPOINT',                    'SCHEDULE',                 'SCHEMA_NAME',          'SECOND', 
        'SECURITY',                 'SERIAL',                       'SERIALIZABLE',             'SERVER',               'SESSION', 
        'SESSION_USER',             'SET_TO_TIME',                  'SHA',                      'SHA1',                 'SHA2', 
        'SHARE',                    'SHUTDOWN',                     'SIGN',                     'SIGNED',               'SIMPLE', 
        'SIN',                      'SLAVE',                        'SLEEP',                    'SNAPSHOT',             'SOCKET', 
        'SOME',                     'SONAME',                       'SOUNDEX',                  'SOUNDS',               'SOURCE', 
        'SPACE',                    'SQL_BUFFER_RESULT',            'SQL_CACHE',                'SQL_NO_CACHE',         'SQL_THREAD', 
        'SQL_TSI_DAY',              'SQL_TSI_FRAC_SECOND',          'SQL_TSI_HOUR',             'SQL_TSI_MINUTE',       'SQL_TSI_MONTH', 
        'SQL_TSI_QUARTER',          'SQL_TSI_SECOND',               'SQL_TSI_WEEK',             'SQL_TSI_YEAR',         'SQRT', 
        'START',                    'STARTS',                       'STATUS',                   'STD',                  'STDDEV', 
        'STDDEV_POP',               'STDDEV_SAMP',                  'STOP',                     'STORAGE',              'STR_TO_DATE', 
        'STRCMP',                   'STRING',                       'SUBCLASS_ORIGIN',          'SUBDATE',              'SUBJECT', 
        'SUBPARTITION',             'SUBPARTITIONS',                'SUBSTR',                   'SUBSTRING',            'SUBSTRING_INDEX', 
        'SUM',                      'SUPER',                        'SUSPEND',                  'SWAPS',                'SWITCHES', 
        'SYSDATE',                  'SYSTEM_USER',                  'TABLE_CHECKSUM',           'TABLE_NAME',           'TABLES', 
        'TABLESPACE',               'TAN',                          'TEMPORARY',                'TEMPTABLE',            'TEXT', 
        'THAN',                     'TIME',                         'TIME_FORMAT',              'TIME_TO_SEC',          'TIMEDIFF', 
        'TIMESTAMP',                'TIMESTAMPADD',                 'TIMESTAMPDIFF',            'TO_DAYS',              'TO_SECONDS', 
        'TRANSACTION',              'TRIGGERS',                     'TRIM',                     'TRUNCATE',             'TYPE', 
        'TYPES',                    'UCASE',                        'UNCOMMITTED',              'UNCOMPRESS',           'UNCOMPRESSED_LENGTH', 
        'UNDEFINED',                'UNDO_BUFFER_SIZE',             'UNDOFILE',                 'UNHEX',                'UNICODE', 
        'UNINSTALL',                'UNIX_TIMESTAMP',               'UNKNOWN',                  'UNTIL',                'UPGRADE', 
        'UPPER',                    'USE_FRM',                      'USER',                     'USER_RESOURCES',       'UUID', 
        'UUID_SHORT',               'VALUE',                        'VAR_POP',                  'VAR_SAMP',             'VARIABLES', 
        'VARIANCE',                 'VERSION',                      'VIEW',                     'WAIT',                 'WARNINGS', 
        'WEEK',                     'WEEKDAY',                      'WEEKOFYEAR',               'WORK',                 'WRAPPER', 
        'X509',                     'XA',                           'XML',                      'YEAR',                 'YEARWEEK',
    ]
    reserved_keywords = [
        'ACCESSIBLE',               'ADD',                  'ALL',                  'ALTER',                            'ANALYZE',
        'AND',                      'AS',                   'ASC',                  'ASENSITIVE',                       'BEFORE',
        'BETWEEN',                  'BIGINT',               'BINARY',               'BLOB',                             'BOTH',
        'BY',                       'CALL',                 'CASCADE',              'CASE',                             'CHANGE',
        'CHAR',                     'CHARACTER',            'CHECK',                'COLLATE',                          'COLUMN',
        'CONDITION',                'CONSTRAINT',           'CONTINUE',             'CONVERT',                          'CREATE',
        'CROSS',                    'CURRENT_DATE',         'CURRENT_TIME',         'CURRENT_TIMESTAMP',                'CURRENT_USER',
        'CURSOR',                   'DATABASE',             'DATABASES',            'DAY_HOUR',                         'DAY_MICROSECOND',
        'DAY_MINUTE',               'DAY_SECOND',           'DEC',                  'DECIMAL',                          'DECLARE',
        'DEFAULT',                  'DELAYED',              'DELETE',               'DESC',                             'DESCRIBE',
        'DETERMINISTIC',            'DISTINCT',             'DISTINCTROW',          'DIV',                              'DOUBLE',
        'DROP',                     'DUAL',                 'EACH',                 'ELSE',                             'ELSEIF',
        'ENCLOSED',                 'ESCAPED',              'EXISTS',               'EXIT',                             'EXPLAIN',
        'FALSE',                    'FETCH',                'FLOAT',                'FLOAT4',                           'FLOAT8',
        'FOR',                      'FORCE',                'FOREIGN',              'FROM',                             'FULLTEXT',
        'GENERAL',                  'GRANT',                'GROUP',                'HAVING',                           'HIGH_PRIORITY',
        'HOUR_MICROSECOND',         'HOUR_MINUTE',          'HOUR_SECOND',          'IF',                               'IGNORE',
        'IN',                       'INDEX',                'INFILE',               'INNER',                            'INOUT',
        'INSENSITIVE',              'INSERT',               'INT',                  'INT1',                             'INT2',
        'INT3',                     'INT4',                 'INT8',                 'INTERGER',                         'INTERVAL',
        'INFO',                     'IS',                   'ITERATE',              'JOIN',                             'KEY',
        'KEYS',                     'KILL',                 'LEADING',              'LEAVE',                            'LEFT',
        'LIKE',                     'LIMIT',                'LINEAR',               'LINES',                            'LOAD',
        'LOCALTIME',                'LOCALTIMESTAMP',       'LOCK',                 'LONG',                             'LONGBLOB',
        'LONGTEXT',                 'LOOP',                 'LOW_PRIORITY',         'MASTER_SSL_VERIFY_SERVER_CERT',    'MATCH',
        'MAXVALUE',                 'MEDIUMBLOB',           'MEDIUMINT',            'MEDIUMTEXT',                       'MIDDLEINT',
        'MINUTE_MICROSECOND',       'MINUTE_SECOND',        'MOD',                  'MODIFIES',                         'NATURAL',
        'NOT',                      'NO_WRITE_TO_BINLOG',   'NULL',                 'NUMERIC',                          'ON',
        'OPTIMIZE',                 'OPTION',               'OPTIONALLY',           'OR',                               'ORDER',
        'OUT',                      'OUTER',                'OUTFILE',              'PRECISION',                        'PRIMARY',
        'PROCEDURE',                'PURGE',                'RANGE',                'READ',                             'READS',
        'READ_WRITE',               'REAL',                 'REFERENCES',           'REGEXP',                           'RELEASE',
        'RENAME',                   'REPEAT',               'REPLACE',              'REQUIRE',                          'RESIGNAL',
        'RESTRICT',                 'RETURN',               'REVOKE',               'RIGHT',                            'RLIKE',
        'SCHEMA',                   'SCHEMAS',              'SECOND_MICROSECOND',   'SELECT',                           'SENSITIVE',
        'SEPARATOR',                'SET',                  'SHOW',                 'SIGNAL',                           'SLOW',
        'SMALLINT',                 'SPATIAL',              'SPECIFIC',             'SQL',                              'SQLEXCEPTION',
        'SQLSTATE',                 'SQLWARNING',           'SQL_BIG_RESULT',       'SQL_CALC_FOUND_ROWS',              'SQL_SMALL_RESULT',
        'SSL',                      'STARTING',             'STRAIGHT_JOIN',        'TABLE',                            'TERMINATED',
        'THEN',                     'TINYBLOB',             'TINYINT',              'TINYTEXT',                         'TO',
        'TRAILING',                 'TRIGGER',              'TRUE',                 'UNDO',                             'UNION',
        'UNIQUE',                   'UNLOCK',               'UNSIGNED',             'UPDATE',                           'USAGE',
        'USE',                      'USING',                'UTC_DATE',             'UTC_TIME',                         'UTC_TIMESTAMP',
        'VALUES',                   'VARBINARY',            'VARCHAR',              'VARCHARACTER',                     'VARYING',
        'WHEN',                     'WHERE',                'WHILE',                'WITH',                             'WRITE',
        'XOR',                      'YEAR_MONTH',           'ZEROFILL',
    ]
    
    @classmethod
    def parse(cls, sql, expect_keywords=[]):
        if sql[0].lower() not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
            return None, sql
        token = MySQLKeywordToken()
        if expect_keywords:
            regex = re.compile(r"\b(" + '|'.join(expect_keywords) + r")\b", re.I)
            m = regex.match(sql)
            if m:
                token.value = m.group(0).upper()
                sql = sql[len(m.group(0)):]
                return token, sql
            return None, sql
        regex = re.compile(r"\b(" + '|'.join(cls.reserved_keywords) + r")\b", re.I)
        m = regex.match(sql)
        if m:
            token.value = m.group(0).upper()
            sql = sql[len(m.group(0)):]
            return token, sql
        regex = re.compile(r"\b(" + '|'.join(cls.keywords) + r")\b", re.I)
        m = regex.match(sql)
        if m:
            token.value = m.group(0).upper()
            sql = sql[len(m.group(0)):]
            return token, sql
        return None, sql

class MySQLTokenList(object):
    def __init__(self, sql, verbose_func=None):
        self.token_list = []
        self.cur_index = 0
        self.is_eof = False
        parse_list = [MySQLDelimiterToken, MySQLNullToken, MySQLSpaceToken, MySQLCommentToken, MySQLStringToken, MySQLQuotedIdentifierToken, MySQLOperatorToken, MySQLNumericToken, MySQLHexadecimalToken, MySQLBitToken, MySQLVariableToken, MySQLKeywordToken, MySQLUnquotedIdentifierToken]
        while len(sql) > 0:
            parsed = False
            for parser in parse_list:
                token, sql = parser.parse(sql)
                if token:
                    self.token_list.append(token)
                    if verbose_func:
                        verbose_func("PARSED TOKEN {0}: {1}".format(token.type(), token.value), 3)
                    parsed = True
                    break
            if not parsed:
                raise Exception('parse error on: {0}'.format(sql))
    
    def __iter__(self):
        return self
    
    def __str__(self):
        str_list = []
        for token in self.token_list:
            str_list.append("<{0}: {1}>".format(token.type(), str(token)))
        return "\n".join(str_list)
    
    def next(self):
        self.cur_index += 1
        if self.cur_index > len(self.token_list):
            raise StopIteration
        return self.token_list[self.cur_index - 1]
    
    def reset(self, pos=0):
        self.cur_index = pos
    
    def current_pos(self):
        return self.cur_index
    
    def eof(self):
        if self.cur_index > len(self.token_list):
            return True
        else:
            return False
    
    def divide(self):
        token_list_list = []
        start_pos = self.current_pos()
        self.reset()
        status = 0
        start = 0
        end = 0
        while not self.eof():
            current_token_list = MySQLTokenList('')
            try:
                t = self.next()
            except:
                break
            if type(t) == MySQLDelimiterToken and t.value == ';':
                if start != end:
                    current_token_list.token_list = self.token_list[start:end]
                    token_list_list.append(current_token_list)
                    current_token_list = MySQLTokenList('')
                    start = end
                status = 0
            elif status == 0:
                start = self.current_pos()
                end = self.current_pos()
                if type(t) != MySQLSpaceToken:
                    start = self.current_pos() - 1
                    status = 1
            else:
                if type(t) != MySQLSpaceToken:
                    end = self.current_pos()
        if start != end:
            current_token_list.token_list = self.token_list[start:end]
            token_list_list.append(current_token_list)
        return token_list_list
    
    def has_token(self, type=None, value=None):
        if len(filter(lambda x: x.type() is type and x.value == value, self.token_list)):
            return True
        return False
    
    def get_next_valid_token(self, num=1):
        return_val = []
        for token in self.token_list[self.cur_index:]:
            if type(token) in [MySQLSpaceToken, MySQLCommentToken]:
                continue
            else:
                return_val.append(token)
            if len(return_val) == num:
                return return_val
        return return_val
