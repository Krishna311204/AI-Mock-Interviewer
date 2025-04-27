import language_tool_python

# Initialize the grammar checking tool
tool = language_tool_python.LanguageTool('en-US')

# Read the text from script.txt
with open('script.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Check for grammar and sentence errors
matches = tool.check(text)

# Prepare the analysis report
error_count = len(matches)
error_details = []

for match in matches:
    error_details.append({
        'sentence': match.context,
        'error': match.message,
        'suggestions': match.replacements
    })

# Display the report
print(f"Total Errors Found: {error_count}\n")
for idx, error in enumerate(error_details, 1):
    print(f"Error {idx}:")
    print(f"  Sentence   : {error['sentence']}")
    print(f"  Issue      : {error['error']}")
    print(f"  Suggestions: {error['suggestions']}\n")

# Optionally close the tool
tool.close()
