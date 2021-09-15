def verify_for_illegal_password(password):
    index = 0
    for p in password:
        if p == '"':
            if password[index + 1] == ',':
                print('reached here')
                password = password.replace(',', '|')
                return password
        index += 1
    

a_word = 'kdjf",fdk'

password = verify_for_illegal_password(a_word)
print(password)