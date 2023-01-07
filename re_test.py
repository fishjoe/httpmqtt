import re

# As re doesn't support escapes itself, use of r"" strings is not
# recommended.
regex = re.compile("[\r\n]")


print(regex.split("line1\rline2\nline3\r\n"))
# Result:
# ['line1', 'line2', 'line3', '', '']