#!/usr/local/ieod-web/python/bin/python
# -*- coding: utf-8 -*-

#=============================================================================
#  @desc       
#  @version    1.0.0
#  @author     kylinshuang
#  @date       2017-12-04
#=============================================================================

import mysqltoken as token
import statement

class MySQLComponent(object):
    def __init__(self):
        self.status = 0
        self.token_list = []
        self.value = ''
    
    def __str__(self):
        return self.value
    
    def type(self):
        return type(self)
    
    def get_final_status(self):
        return 999
    
    def parse_by_fsm(self, token_list, special_final_status=[], verbose_func=None):
        fsm_map = self.get_fsm_map()
        final_status = self.get_final_status()
        start_term_pos = token_list.current_pos()
        last_term_pos = token_list.current_pos()
        last_token_list_pos = 0
        last_term_status = 0
        while not token_list.eof():
            try:
                t = token_list.next()
            except:
                break
            if verbose_func:
                verbose_func("COMPONENT NOW DEAL WITH {0}: {1}".format(t.type(), t.value), 3)
            if t.type() is token.MySQLCommentToken:
                self.token_list.append(t)
                self.value += t.value
                continue
            elif t.type() is token.MySQLSpaceToken:
                self.token_list.append(t)
                self.value += t.value
                continue
            elif t.type() is token.MySQLDelimiterToken and t.value == ';':
                break
            rule_founded = False
            for rule in fsm_map:
                status_match = (type(rule[0]) is int and self.status == rule[0]) or (type(rule[0]) is tuple and self.status in rule[0])
                if status_match and issubclass(rule[1], token.MySQLToken):
                    if verbose_func:
                        verbose_func("COMPONENT MATCH TOKEN RULE {0}".format(rule), 3)
                    if t.type() is rule[1] and (rule[2] is None or t.value == rule[2]):
                        rule_founded = True
                        self.status = rule[3]
                        if verbose_func:
                            verbose_func("COMPONENT CHANGE STATUS TO {0}".format(self.status), 3)
                        self.token_list.append(t)
                        self.value += t.value
                        if self.status == final_status:
                            if verbose_func:
                                verbose_func("COMPONENT STATUS END", 3)
                            return token_list.current_pos()
                        elif self.status in special_final_status:
                            last_term_pos = token_list.current_pos()
                            last_term_status = self.status
                            last_token_list_pos = len(self.token_list)
                            if verbose_func:
                                verbose_func("COMPONENT STATUS IN SPECIAL, SAVE POS {0}, STATUS {1}".format(last_term_pos, last_term_status), 3)
                        break
                elif status_match and (issubclass(rule[1], MySQLComponent) or issubclass(rule[1], statement.MySQLStatement)):
                    if verbose_func:
                        verbose_func("COMPONENT MATCH COMPLEX RULE {0}".format(rule), 3)
                    token_list.reset(token_list.current_pos() - 1)
                    c, token_list = rule[1].parse(token_list, verbose_func=verbose_func)
                    if c:
                        rule_founded = True
                        self.status = rule[3]
                        if verbose_func:
                            verbose_func("COMPONENT CHANGE STATUS TO {0}".format(self.status), 3)
                        self.token_list.append(c)
                        self.value += c.value
                        if self.status == final_status:
                            if verbose_func:
                                verbose_func("COMPONENT STATUS END", 3)
                            return token_list.current_pos()
                        elif self.status in special_final_status:
                            last_term_pos = token_list.current_pos()
                            last_term_status = self.status
                            last_token_list_pos = len(self.token_list)
                            if verbose_func:
                                verbose_func("COMPONENT STATUS IN SPECIAL, SAVE POS {0}, STATUS {1}".format(last_term_pos, last_term_status), 3)
                        break
                    else:
                        t = token_list.next()
            if not rule_founded:
                if last_term_status:
                    self.status = last_term_status
                    if verbose_func:
                        verbose_func("COMPONENT STATUS BACK TO {0}".format(self.status), 3)
                    self.token_list = self.token_list[:last_token_list_pos]
                    self.value = ''.join([x.value for x in self.token_list])
                    token_list.reset(last_term_pos)
                    return last_term_pos
                else:
                    token_list.reset(token_list.current_pos() - 1)
                    return None
        if self.status in special_final_status:
            return token_list.current_pos()
        return None
