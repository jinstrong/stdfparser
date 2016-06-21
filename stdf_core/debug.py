import pandas as pd
import os
from pandas import DataFrame
import numpy as np
import ast


def get_yield(file):
    with pd.ExcelFile(file) as xls:
        data = pd.read_excel(xls, 'yield', index_col=[0]).transpose()
    return data


def get_dict(file):
    new_dict = get_yield(file).to_dict()
    my_dict = {}
    basename = os.path.basename(file)
    name_front = basename.find('_') + 1
    name_end = basename.find('---') - 12
    name = basename[name_front:name_end]

    for key, value in new_dict.iteritems():
        my_dict[key] = {}
        my_dict[key][name] = {}
        for key1, value1 in value.iteritems():
            #         print key,key1,value1
            my_dict[key][name][key1] = value1
            #     print my_dict
    return my_dict


def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


# folder = 'D:\Test_results_validating\ESP8266\ESP8266EX_PA5H13.0A#A_ESP1617001AC000'
# dump_excel = os.path.join(folder, 'yield_all.xlsx')
# std_excel = list(filter(lambda s: s.endswith('std.gz.xlsx'), os.listdir(folder)))
# std_excel_path = list(map(lambda s: os.path.join(folder, s), std_excel))
# list_dict = list(map(lambda s: get_dict(s), std_excel_path))
# new_dict = reduce(merge, list_dict)
# df = pd.DataFrame.from_dict(new_dict).transpose()
# df = df.replace(np.nan, {column: {} for column in df.columns})
# dfs = [pd.DataFrame([x for x in df[col]]) for col in df.columns]
# df1 = pd.concat(dfs, axis=1, keys=df.columns)
# print (df1)

d = {1: {u'FT1': u"{0.0: 19732, 1.0: 20495, 'total': 40227, 'yield': '93.34%'}",
         u'FT3': u"{0.0: 9285, 1.0: 9629, 'total': 18914, 'yield': '92.93%'}",
         u'FT2': u"{0.0: 1412, 1.0: 1480, 'total': 2892, 'yield': '93.87%'}",
         u'FT': u"{0.0: 82, 1.0: 6517, 'total': 6599, 'yield': '92.70%'}",
         u'FT_R1': u"{0.0: 1262, 1.0: 1418, 'total': 2680, 'yield': '53.73%'}",
         u'QA_R2': u"{0.0: 2, 'total': 2, 'yield': '100.00%'}", u'QA_R1': u"{0.0: 6, 'total': 6, 'yield': '75.00%'}",
         u'QA': u"{1.0: 750, 'total': 750, 'yield': '98.94%'}",
         u'BIN2_R1': u"{0.0: 23, 1.0: 31, 'total': 54, 'yield': '13.01%'}"},
     2: {u'FT1': u"{0.0: 246, 1.0: 110, 'total': 356, 'yield': '0.83%'}",
         u'FT3': u"{0.0: 81, 1.0: 54, 'total': 135, 'yield': '0.66%'}",
         u'FT2': u"{0.0: 9, 1.0: 3, 'total': 12, 'yield': '0.39%'}",
         u'FT': u"{0.0: 51, 1.0: 173, 'total': 224, 'yield': '3.15%'}",
         u'FT_R1': u"{0.0: 138, 1.0: 86, 'total': 224, 'yield': '4.49%'}",
         u'QA_R1': u"{0.0: 1, 'total': 1, 'yield': '12.50%'}", u'QA': u"{1.0: 5, 'total': 5, 'yield': '0.66%'}",
         u'BIN2_R1': u"{0.0: 81, 1.0: 70, 'total': 151, 'yield': '36.39%'}"},
     3: {u'FT1': u"{0.0: 72, 1.0: 47, 'total': 119, 'yield': '0.28%'}",
         u'FT3': u"{0.0: 35, 1.0: 25, 'total': 60, 'yield': '0.29%'}",
         u'FT2': u"{0.0: 1, 1.0: 1, 'total': 2, 'yield': '0.06%'}",
         u'FT': u"{0.0: 0, 1.0: 13, 'total': 13, 'yield': '0.18%'}",
         u'FT_R1': u"{0.0: 93, 1.0: 98, 'total': 191, 'yield': '3.83%'}",
         u'BIN2_R1': u"{0.0: 92, 1.0: 97, 'total': 189, 'yield': '45.54%'}"},
     4: {u'FT1': u"{0.0: 132, 1.0: 174, 'total': 306, 'yield': '0.71%'}",
         u'FT3': u"{0.0: 35, 1.0: 36, 'total': 71, 'yield': '0.35%'}",
         u'FT2': u"{0.0: 8, 1.0: 11, 'total': 19, 'yield': '0.62%'}",
         u'FT': u"{0.0: 1, 1.0: 37, 'total': 38, 'yield': '0.53%'}",
         u'FT_R1': u"{0.0: 179, 1.0: 167, 'total': 346, 'yield': '6.94%'}",
         u'BIN2_R1': u"{0.0: 1, 1.0: 1, 'total': 2, 'yield': '0.48%'}"},
     5: {u'FT1': u"{0.0: 27, 1.0: 28, 'total': 55, 'yield': '0.13%'}",
         u'FT_R1': u"{0.0: 41, 1.0: 34, 'total': 75, 'yield': '1.50%'}",
         u'FT3': u"{0.0: 11, 1.0: 9, 'total': 20, 'yield': '0.10%'}",
         u'FT2': u"{0.0: 2, 1.0: 0, 'total': 2, 'yield': '0.06%'}",
         u'FT': u"{0.0: 0, 1.0: 4, 'total': 4, 'yield': '0.06%'}"},
     8: {u'FT1': u"{0.0: 76, 1.0: 77, 'total': 153, 'yield': '0.35%'}",
         u'FT3': u"{0.0: 40, 1.0: 42, 'total': 82, 'yield': '0.40%'}",
         u'FT2': u"{0.0: 5, 1.0: 8, 'total': 13, 'yield': '0.42%'}",
         u'FT': u"{0.0: 0, 1.0: 20, 'total': 20, 'yield': '0.28%'}",
         u'FT_R1': u"{0.0: 131, 1.0: 133, 'total': 264, 'yield': '5.29%'}",
         u'BIN2_R1': u"{0.0: 1, 1.0: 2, 'total': 3, 'yield': '0.72%'}"},
     9: {u'FT1': u"{0.0: 199, 1.0: 158, 'total': 357, 'yield': '0.83%'}",
         u'FT3': u"{0.0: 90, 1.0: 62, 'total': 152, 'yield': '0.75%'}",
         u'FT2': u"{0.0: 8, 1.0: 8, 'total': 16, 'yield': '0.52%'}",
         u'FT': u"{0.0: 0, 1.0: 36, 'total': 36, 'yield': '0.51%'}",
         u'FT_R1': u"{0.0: 238, 1.0: 238, 'total': 476, 'yield': '9.54%'}",
         u'BIN2_R1': u"{0.0: 2, 1.0: 2, 'total': 4, 'yield': '0.96%'}"},
     10: {u'FT1': u"{0.0: 56, 1.0: 38, 'total': 94, 'yield': '0.22%'}",
          u'FT3': u"{0.0: 25, 1.0: 33, 'total': 58, 'yield': '0.28%'}",
          u'FT2': u"{0.0: 5, 1.0: 1, 'total': 6, 'yield': '0.19%'}",
          u'FT': u"{0.0: 0, 1.0: 11, 'total': 11, 'yield': '0.15%'}",
          u'FT_R1': u"{0.0: 77, 1.0: 66, 'total': 143, 'yield': '2.87%'}",
          u'BIN2_R1': u"{0.0: 2, 1.0: 0, 'total': 2, 'yield': '0.48%'}"},
     11: {u'FT1': u"{0.0: 2, 1.0: 0, 'total': 2, 'yield': '0.00%'}",
          u'FT3': u"{0.0: 1, 1.0: 0, 'total': 1, 'yield': '0.00%'}",
          u'BIN2_R1': u"{0.0: 1, 1.0: 0, 'total': 1, 'yield': '0.24%'}"},
     12: {u'FT1': u"{0.0: 6, 1.0: 0, 'total': 6, 'yield': '0.01%'}",
          u'FT3': u"{0.0: 2, 1.0: 0, 'total': 2, 'yield': '0.01%'}",
          u'FT_R1': u"{0.0: 1, 1.0: 0, 'total': 1, 'yield': '0.02%'}"},
     13: {u'FT1': u"{0.0: 953, 1.0: 422, 'total': 1375, 'yield': '3.19%'}",
          u'FT3': u"{0.0: 544, 1.0: 292, 'total': 836, 'yield': '4.11%'}",
          u'FT2': u"{0.0: 88, 1.0: 28, 'total': 116, 'yield': '3.77%'}",
          u'FT': u"{0.0: 21, 1.0: 147, 'total': 168, 'yield': '2.36%'}",
          u'FT_R1': u"{0.0: 289, 1.0: 225, 'total': 514, 'yield': '10.30%'}",
          u'QA_R1': u"{0.0: 1, 'total': 1, 'yield': '12.50%'}", u'QA': u"{1.0: 3, 'total': 3, 'yield': '0.40%'}",
          u'BIN2_R1': u"{0.0: 4, 1.0: 5, 'total': 9, 'yield': '2.17%'}"},
     14: {u'FT1': u"{0.0: 31, 1.0: 18, 'total': 49, 'yield': '0.11%'}",
          u'FT_R1': u"{0.0: 35, 1.0: 39, 'total': 74, 'yield': '1.48%'}",
          u'FT3': u"{0.0: 16, 1.0: 7, 'total': 23, 'yield': '0.11%'}",
          u'FT2': u"{0.0: 2, 1.0: 1, 'total': 3, 'yield': '0.10%'}",
          u'FT': u"{0.0: 0, 1.0: 6, 'total': 6, 'yield': '0.08%'}"}}
df = pd.DataFrame.from_dict(d, orient='index')
df = df.fillna('{}')
for col in df.columns:
    df[col] = df[col].map(lambda d: ast.literal_eval(d))
dfs = [pd.DataFrame([x for x in df[col]]) for col in df.columns]
df2 = pd.concat(dfs, axis=1, keys=df.columns)
# print (df2.keys)
# print (df2)
print df.columns
for col in df.columns:

    for x in df[col]:
        for key0,value0 in x.iter
# with pd.ExcelWriter(dump_excel) as writer:
#     # df2.to_excel(writer, sheet_name='yield')
#     df1.to_excel(writer, sheet_name='new_yield')
