# -*- coding:utf-8 -*-
# python for data analysis  6 XML and HTML
from lxml.html import parse
from urllib2 import urlopen
from pandas.io.parsers import TextParser
parsed = parse(urlopen('http://finance.yahoo.com/q/op?s=AAPL+Options'))
doc = parsed.getroot()
urls = [lnk.get('href') for lnk in doc.findall('.//a')]  # 找出所有网址
tables = doc.findall('.//table')  # 找出数据表格
calls = tables[0]
puts = tables[1]
rows = calls.findall('.//tr')


def _unpack(row, kind='td'):
    elts = row.findall('.//%s' % kind)
    return [val.text_content() for val in elts]
_unpack(rows[0], kind='th')
_unpack(rows[1], kind='td')


def parse_options_data(table):
    rows = table.findall('.//tr')
    header = _unpack(rows[0], kind='th')
    data = [_unpack(r) for r in rows[1:]]
    return TextParser(data, names=header).get_chunk()
call_data = parse_options_data(calls)
put_data = parse_options_data(puts)
