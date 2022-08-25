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

class MySQLIdentifierComponent(component.MySQLComponent):
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLIdentifierComponent()
        while not token_list.eof():
            try:
                t = token_list.next()
            except:
                break
            if t.type() is token.MySQLCommentToken:
                c.token_list.append(t)
                c.value += t.value
                continue
            elif t.type() is token.MySQLSpaceToken:
                c.token_list.append(t)
                c.value += t.value
                continue
            elif t.type() is token.MySQLQuotedIdentifierToken:
                c.token_list.append(t)
                c.value += t.value
                return c, token_list
            elif t.type() is token.MySQLUnquotedIdentifierToken:
                c.token_list.append(t)
                c.value += t.value
                return c, token_list
            elif t.type() is token.MySQLKeywordToken and t.value in token.MySQLKeywordToken.keywords:
                c.token_list.append(t)
                c.value += t.value
                return c, token_list
            else:
                break
        token_list.reset(start_pos)
        return None, token_list

class MySQLDatabaseNameComponent(component.MySQLComponent):
    def __init__(self):
        super(MySQLDatabaseNameComponent, self).__init__()
        self.database = ''
    
    def get_fsm_map(self):
        return (
            (0, MySQLIdentifierComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLDatabaseNameComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in c.token_list:
                if type(t) is MySQLIdentifierComponent:
                    c.database = t.value.strip('`')
            token_list.reset(end_pos)
            return c, token_list

class MySQLTableNameComponent(component.MySQLComponent):
    def __init__(self):
        super(MySQLTableNameComponent, self).__init__()
        self.database = ''
        self.table = ''
    
    def get_fsm_map(self):
        return (
            (0, MySQLIdentifierComponent, None, 1),
            ((0, 1), token.MySQLOperatorToken, '.', 2),
            (2, MySQLIdentifierComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLTableNameComponent()
        end_pos = c.parse_by_fsm(token_list, [1], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            #print "MySQLTableNameComponent: {0}, {1}, {2}".format(c.token_list, c.value, c)
            for t in c.token_list:
                if type(t) is MySQLIdentifierComponent:
                    if c.table:
                        c.database = c.table
                        c.table = t.value.strip('`')
                    else:
                        c.table = t.value.strip('`')
            token_list.reset(end_pos)
            return c, token_list

class MySQLTableNameListComponent(component.MySQLComponent):
    def __init__(self):
        super(MySQLTableNameListComponent, self).__init__()
        self.table_list = []
    
    def get_fsm_map(self):
        return (
            ((0, 2), MySQLTableNameComponent, None, 1),
            (1, token.MySQLDelimiterToken, ',', 2),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLTableNameListComponent()
        end_pos = c.parse_by_fsm(token_list, [1], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in c.token_list:
                if type(t) is MySQLTableNameComponent:
                    c.table_list.append(t)
            token_list.reset(end_pos)
            return c, token_list

class MySQLColumnNameComponent(component.MySQLComponent):
    def __init__(self):
        super(MySQLColumnNameComponent, self).__init__()
        self.database = ''
        self.table = ''
    
    def get_fsm_map(self):
        return (
            (0, MySQLIdentifierComponent, None, 1),
            (1, token.MySQLOperatorToken, '.', 2),
            (2, MySQLIdentifierComponent, None, 3),
            (3, token.MySQLOperatorToken, '.', 4),
            (4, MySQLIdentifierComponent, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLColumnNameComponent()
        end_pos = c.parse_by_fsm(token_list, [1, 3], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            column_name = ''
            for t in c.token_list:
                if type(t) is MySQLIdentifierComponent:
                    if column_name and c.table:
                        c.database = c.table
                        c.table = column_name
                        column_name = t.value.strip('`')
                    elif column_name:
                        c.table = column_name
                        column_name = t.value.strip('`')
                    else:
                        column_name = t.value.strip('`')
            token_list.reset(end_pos)
            return c, token_list

class MySQLColumnNameListComponent(component.MySQLComponent):
    def __init__(self):
        super(MySQLColumnNameListComponent, self).__init__()
        self.column_list = []
    
    def get_fsm_map(self):
        return (
            ((0, 2), MySQLColumnNameComponent, None, 1),
            (1, token.MySQLDelimiterToken, ',', 2),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLColumnNameListComponent()
        end_pos = c.parse_by_fsm(token_list, [1], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in c.token_list:
                if type(t) is MySQLColumnNameComponent:
                    c.column_list.append(t)
            token_list.reset(end_pos)
            return c, token_list

# index_col_name:
#   col_name [(length)] [ASC | DESC]
class MySQLIndexColumnNameComponent(component.MySQLComponent):
    def get_fsm_map(self):
        return (
            (0, MySQLColumnNameComponent, None, 1),
            (1, token.MySQLOperatorToken, '(', 2),
            (2, token.MySQLNumericToken, None, 3),
            (3, token.MySQLOperatorToken, ')', 4),
            ((1, 4), token.MySQLKeywordToken, 'ASC', self.get_final_status()),
            ((1, 4), token.MySQLKeywordToken, 'DESC', self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLIndexColumnNameComponent()
        end_pos = c.parse_by_fsm(token_list, [1, 4], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            token_list.reset(end_pos)
            return c, token_list

class MySQLIndexColumnNameListComponent(component.MySQLComponent):
    def __init__(self):
        super(MySQLIndexColumnNameListComponent, self).__init__()
        self.name_list = []
    
    def get_fsm_map(self):
        return (
            ((0, 2), MySQLIndexColumnNameComponent, None, 1),
            (1, token.MySQLDelimiterToken, ',', 2),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLIndexColumnNameListComponent()
        end_pos = c.parse_by_fsm(token_list, [1], verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            for t in c.token_list:
                if type(t) is MySQLIndexColumnNameComponent:
                    c.name_list.append(t)
            token_list.reset(end_pos)
            return c, token_list

class MySQLCharsetNameComponent(component.MySQLComponent):
    support_charsets = [
        'big5',     'dec8',     'cp850',    'hp8',      'koi8r',
        'latin1',   'latin2',   'swe7',     'ascii',    'ujis',
        'sjis',     'hebrew',   'tis620',   'euckr',    'koi8u',
        'gb2312',   'greek',    'cp1250',   'gbk',      'latin5',
        'armscii8', 'utf8',     'ucs2',     'cp866',    'keybcs2',
        'macce',    'macroman', 'cp852',    'latin7',   'utf8mb4',
        'cp1251',   'utf16',    'cp1256',   'cp1257',   'utf32',
        'binary',   'geostd8',  'cp932',    'eucjpms',
    ]
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLUnquotedIdentifierToken, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLCharsetNameComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            charset = ''
            for t in c.token_list:
                if type(t) is token.MySQLUnquotedIdentifierToken:
                    charset = t.value.lower()
            if charset not in cls.support_charsets:
                token_list.reset(start_pos)
                return None, token_list
            else:
                token_list.reset(end_pos)
                return c, token_list

class MySQLCollationNameComponent(component.MySQLComponent):
    support_suffix = ['ai', 'as', 'ci', 'cs', 'bin'];
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLUnquotedIdentifierToken, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLCollationNameComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            collation = ''
            for t in c.token_list:
                if type(t) is token.MySQLUnquotedIdentifierToken:
                    collation = t.value.lower()
            collation_piece = collation.split('_')
            if collation_piece[0] not in MySQLCharsetNameComponent.support_charsets:
                token_list.reset(start_pos)
                return None, token_list
            elif collation_piece[-1] not in cls.support_suffix:
                token_list.reset(start_pos)
                return None, token_list
            else:
                token_list.reset(end_pos)
                return c, token_list

class MySQLEngineNameComponent(component.MySQLComponent):
    support_engine = [
        'INNODB',       'MyISAM',   'MEMORY',   'CSV',  'ARCHIVE',
        'BLACKHOLE',    'MERGE',    'FEDERATED',
    ]
    
    def get_fsm_map(self):
        return (
            (0, token.MySQLUnquotedIdentifierToken, None, self.get_final_status()),
            (0, token.MySQLKeywordToken, None, self.get_final_status()),
        )
    
    @classmethod
    def parse(cls, token_list, verbose_func=None):
        start_pos = token_list.current_pos()
        c = MySQLEngineNameComponent()
        end_pos = c.parse_by_fsm(token_list, verbose_func=verbose_func)
        if end_pos is None:
            token_list.reset(start_pos)
            return None, token_list
        else:
            engine = ''
            for t in c.token_list:
                if type(t) in [token.MySQLUnquotedIdentifierToken, token.MySQLKeywordToken]:
                    engine = t.value.upper()
            if engine not in cls.support_engine:
                token_list.reset(start_pos)
                return None, token_list
            else:
                token_list.reset(end_pos)
                return c, token_list
