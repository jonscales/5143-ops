# Define ANSI escape codes as variables
RED = "\033[91m"
RESET = "\033[0m"

# Use the variables to format text
text_to_format = "This text will be in red."
formatted_text = f"{RED}{text_to_format}{RESET}"

# Print the formatted text
print(formatted_text)
