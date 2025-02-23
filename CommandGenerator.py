command = input('Enter Your command: ')

def generate_command(keys):
    command_parts = []

    for key in keys:
        key_value = ord(key)  # Converts the character to its ASCII value
        
        # Depending on the value, select the right prefix (2, 3)
        if key_value < 100:
            prefix = 2
        else:
            prefix = 3

        command_parts.append(f"3.key,{prefix}.{key_value},1.1;3.key,{prefix}.{key_value},1.0;")
    
    return ' '.join(command_parts)



command = generate_command(command)
print('Here is your equivalent command for onworks: ')
print(command)
input('Press Enter to Exit!!')
