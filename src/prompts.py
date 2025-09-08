def build_regex_footer(examples):
    return f"""
I want you to generate a Python regular expression that matches page footers.
Input data are some examples to build the regular expression.
Your regex should:
* Match exactly this footer structure to match the whole string.
* Be written in Python syntax using the re module.
Please provide ONLY the regex pattern, withouth the leading 'r' Not the code nor the result.

An example is show here:
Input text: "pag 7 | 103"  
Desired output: "pag\s+\d+\s*\|\s*\d+"

Input text: {examples}
"""