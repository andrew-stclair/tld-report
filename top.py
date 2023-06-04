"""Json Module"""
import json

with open("results.json", 'r', encoding='utf-8') as results_file:
    items_dict = json.loads(results_file.read())

def select_percent(tld_object):
    """Returns the percent for a tld"""
    return items_dict[tld_object]['percent']

def select_badness(tld_object):
    """Returns the percent for a tld"""
    return items_dict[tld_object]['badness']

BADNESS_COUNT = 0
BADNESS_OUTPUT = 'tld,badness\n'
for tld in reversed(sorted(items_dict, key=select_badness)):
    if BADNESS_COUNT < 10:
        BADNESS_OUTPUT += f"{tld},{items_dict[tld]['badness']}\n"
    BADNESS_COUNT += 1
print(BADNESS_OUTPUT)

with open("reports/top_badness.csv", "w", encoding='utf-8') as badness_file:
    badness_file.write(BADNESS_OUTPUT)

PERCENT_COUNT = 0
PERCENT_OUTPUT = 'tld,percent\n'
for tld in reversed(sorted(items_dict, key=select_percent)):
    if PERCENT_COUNT < 10:
        PERCENT_OUTPUT += f"{tld},{items_dict[tld]['percent']}\n"
    PERCENT_COUNT += 1
print(PERCENT_OUTPUT)

with open("reports/top_percent.csv", "w", encoding='utf-8') as percent_file:
    percent_file.write(PERCENT_OUTPUT)
