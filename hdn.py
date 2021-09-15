
class Parser:
        
    def parse(self, file):
        file = open(file, 'r').read()
        items = []
        lines = []
        word = ''
        gather_item = False
        index = 0
        for x in file:
            if x == '"' and gather_item is False:
                gather_item = True
            elif x == '"' and gather_item is True:
                if file[index + 1] == ',':
                    gather_item = False
                    items.append(word)
                    word = ''
                else:
                    word += x

            elif gather_item:
                word += x
            elif x == ';':
                lines.append(items)
                items = []
            index += 1
        return lines

    def write_in_hdn(self, lines):
        file_str = ''
        for line in lines:
            for word in line:
                hdn_word = f'"{word}"'
                file_str += hdn_word + ','
            file_str += ';'
        return file_str
    
    def dump(self, hdn, file):
        hdn_file = open(file, 'w')
        hdn_file.write(hdn)        




