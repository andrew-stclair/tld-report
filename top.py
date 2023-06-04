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

badness_count = 0
badness_output = 'tld,badness\n'
for tld in reversed(sorted(items_dict, key=select_badness)):
    if badness_count < 10:
        badness_output += f"{tld},{items_dict[tld]['badness']}\n"
    badness_count += 1
print(badness_output)

with open("top_badness.csv", "w", encoding='utf-8') as badness_file:
    badness_file.write(badness_output)

percent_count = 0
percent_output = 'tld,percent\n'
for tld in reversed(sorted(items_dict, key=select_percent)):
    if percent_count < 10:
        percent_output += f"{tld},{items_dict[tld]['percent']}\n"
    percent_count += 1
print(percent_output)

with open("top_percent.csv", "w", encoding='utf-8') as percent_file:
    percent_file.write(percent_output)
