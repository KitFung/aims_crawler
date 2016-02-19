# -*- coding: utf-8 -*-
import re


def custom_escape(s_arr):
    if not s_arr:
        return ''
    result = s_arr[0].replace('&nbsp', '')
    return result if len(result) > 0 else ''


def multiple_replace(string, rep):
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], string)


def string_to_element_array(s):
    """
    s: input string, space around each operator, not space for '(', ')'
    """
    if not s:
        return []
    replacements = {'(': '( ', ')': ' )'}
    s = multiple_replace(s, replacements)
    s_arr = s.split(' ')
    return s_arr


def convert_to_reverse_polish_notation(s_arr, operators):
    """"
    s: input element array
    e.g.: ['(', '1', '+', '1', ')', '-', '2']
    ordered_operators: dictionary of operator with order
    e.g.: {
        'AND': 1,
        'OR': 2,
        'COR': 2,
    }
    """
    result_arr = []
    tmp_arr = []

    for ele in s_arr:
        if ele == '(':
            tmp_arr.append('(')
        elif ele == ')':
            for symbol in reversed(tmp_arr):
                if symbol == '(':
                    tmp_arr.pop()
                    break
                result_arr.append(tmp_arr.pop())
        elif ele in operators:
            if len(tmp_arr) == 0 or tmp_arr[-1] == '(':
                tmp_arr.append(ele)
            elif operators[tmp_arr[-1]] > operators[ele]:
                tmp_arr.append(ele)
            else:
                for symbol in reversed(tmp_arr):
                    if symbol in operators and\
                       operators[symbol] > operators[ele]:
                        result_arr.append(tmp_arr.pop())
                    else:
                        tmp_arr.append(ele)
                        break
        else:
            result_arr.append(ele)
    for symbol in tmp_arr:
        result_arr.append(symbol)
    return result_arr
