#!/usr/bin/python
# -*- coding: utf-8 -*-

#=============================================================================
#  @desc       
#  @version    2.0.0
#  @author     kylinshuang
#  @date       2017-11-21
#=============================================================================

import sys
import json
import mysqlparser

def usage():
    print "Usage:                                "
    print sys.argv[0] + " parse <SQL>"

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    sqlparser = mysqlparser.Parser()
    if sys.argv[1] == 'parse':
        result = sqlparser.parse(sys.argv[2])
        print [str(x) for x in sqlparser.sql_list]
        print result
    else:
        usage()
