#! /usr/bin/python

import sys
import re

def main(argv):
# Take the first input
    diff = argv[0]
# Split it into lines
	diff_list = diff.splitlines()
	files_and_functions = {}
	file_name = ""
	for line in diff_list:
# Check for any renames
		line_rename_from = ""
		rename_from = "rename from (.*)"
		rename_to = "rename to (.*)"
		file_regexp = "--- a/(.*)"
		function_regexp = "@@.*@@ def ([\\w|\\d|_]*)"
		new_function = "\\+\\s+def\\s+(.*):"
# Check line if it is an addition to the file take note of the file name
		match = re.search(rename_from, line)
		if match is not None:
			line_rename_from = match.group(1)
		match = re.search(rename_to, line)
		if match is not None:
			files_and_functions[line_rename_from]["rename"] = match.group(1)
		match = re.search(file_regexp, line)
		if match is not None:
			file_name = match.group(1)
		match = re.search(function_regexp, line)
		if match is not None:
			files_and_functions[file_name][match.group(1)] = ""
		match = re.search(new_function, line)
		if match is not None:
			files_and_functions[file_name][match.group(1)] = ""
# Check line if it is an addition to a function add the function name to a dictionary {"filename" : {"function_name" : "" }}
# Collate functions and filename togeather
	collated = collate(files_and_functions)
# Print/return list of tests to run
	print collated

def collate(dictionary):
    keys = dictionary.keys()
    collated = []
    for key in keys:
	functions = dictionary[key].keys()
	for function in functions:
	    collated.append(key+"."+function)
    return collated

if __name__ == "__main__":
    main(sys.argv[1:])
