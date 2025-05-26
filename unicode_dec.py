def unicode_to_decimal():
    user_input = input("Enter a string: ")
    output_string = ''.join(f"{ord(char):03d}" for char in user_input)
    
    print(f"Converted string: {output_string}")
    print(f"Length of output string: {len(output_string)}")

unicode_to_decimal()
