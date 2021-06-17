
from os import times
import sys
from pswd_gen import password_generator
import pyperclip

pg = password_generator('password_database.xlsx')
if sys.argv != 'help':
    function = input('function: ')
    if function == 'g':
        n_of_char = int(input('number of characters in your password: '))
        website_name = input('website name: ')
        password = pg.generate_pswd(n_of_char=n_of_char, website_name=website_name)
        print(password)
        pyperclip.copy(password)
    elif function == 'fp':
        website_name = input('website name: ')
        password = pg.find_password(website_name=website_name)
        if password != None:
            print(password)
            pyperclip.copy(password)
        else:
            
            websites_list = pg.get_all_websites()
            
            shortened_website_name = ''
            times_a = 0
            for w in website_name:
                shortened_website_name += w
                if times_a == 4:
                    break
                else:
                    pass
            
            for website in websites_list:
                shortened_websites_list_name = ''
                for w in website:
                    shortened_websites_list_name += w
                    if shortened_website_name == shortened_websites_list_name:
                        print(f'try using {website}')
        
    elif function == 'ep':
        website_name = input('website name: ')
        password_a = input('password: ')
        response = pg.enter_password(website_name=website_name, password=password_a)
        print(response)
        
           
    else:
        print('invalid function')
        print('type gp help for more information')
else:
    print("""in function type 'g' to generate and save password to database
             in function type 'fp' to find password of a website
             in function type 'ep' to enter website and password into the database""")
