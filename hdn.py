
class Parser:
    def __init__(self, file):
        self.file = file
    def parse(self):
        file = open(self.file, 'r').read()
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

    def replace_value(self, original, final):
        lines = self.parse()
        for line in lines:
            index = 0
            for item in line:
                if item == original:
                    line[index] = final
                index += 1
        print(lines)
        hdn_str = self.write_in_hdn(lines)
        self.dump(hdn_str, self.file)



