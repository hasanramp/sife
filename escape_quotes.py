
def escape_special_char(word):
    special_char = ['$', '!', '&']
    index = 0
    times = 0
    for x in word:
        if x in special_char:
            word = word[0:index] + '\\' + word[index:]
            index += 1
        index +=1
    
    return word