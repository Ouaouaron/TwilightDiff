from sys import argv

class Prose:
    def __init__(self, location):
        self.text = []
        with open(location, encoding='utf-8') as file:
            for line in file:
                # Separate words and keep (but isolate) line endings
                self.text += line.split() 
                self.text.append('\n')
    def __getitem__(self, key):
        return self.text[key]

    def diff(self, altered):
        taggedtext = []
        LOOKAHEAD = 30
        altindex = 0

        result = ProseDiff()
        for word in self.text:
            matched = False
            if word == '\n':
                for i in range(LOOKAHEAD):
                    if altered[altindex+i] == '\n':
                        result.push(altered[altindex:altindex+i], 'altered')
                        result.push('', 'newline')
                        altindex += i + 1
                        matched = True
                        break
                continue
            for i in range(LOOKAHEAD):
                if word.lower() == altered[altindex+i].lower():
                    result.push(altered[altindex:altindex+i], 'altered')
                    result.push(word, 'same')
                    altindex += i + 1
                    mathced = True
                    break
            if matched == False:
                result.push(word, 'original')
                continue



class ProseDiff:
    def __init__(self):
        self.taggedtext = []
        # variables for push()
        self.originaltext = ''
        self.alteredtext = ''
        self.sametext = ''

    def push(self, text, tag):
        if tag == 'newline':
            self.flush()
            taggedtext.append( ('', 'newline') )
        elif tag == 'same':
            if self.sametext == '':
                self.flush()
            self.sametext += ' ' + text
        elif tag == 'original':
            self.originaltext += ' ' + text
        elif tag == 'altered':
            self.alteredtext += ' ' + text
        else:
            raise TagError(tag, text)

            
    def flush(self):
        if self.originaltext != '':
            taggedtext.append( (self.originaltext.lstrip(), 'original') )
        if self.alteredtext != '':
            taggedtext.append( (self.alteredtext.lstrip(), 'altered') )
        if self.sametext != '':
            taggedtext.append( (self.sametext.lstrip(), 'same') )


    def html(self):
        """Return an html file of the diff as a string."""
        htmlhead = "../resources/htmlhead.html"
        replacements = {'language' : 'en-US',
                        'encoding' : 'utf-8',
                        'title' : 'TwilightDiff'}

        with open(htmlhead, encoding='utf-8') as file:
            result = file.read()
        for key, value in replacements:
            result.replace('[['+key+']]', value)

        result += "\t<p>"
        for text, tag in self.taggedtext:
            if tag == 'newline':
                result += '</p>\n\t<p>'
            elif tag == 'same':
                result += text
            elif tag in ['original', 'altered']:
                result += '<span class="{}"> {} </span>'.format(tag, text)
            else:
                raise TagError(tag, text)
        result += "</p>\n</article>\n</body>\n</html>"

        return result


class TagError(Exception):
    def __init__(self, tag, text):
        self.tag = tag
        self.text = text

if __name__ == "__main__":
    # Load original and altered
    original = Prose(argv[1])
    altered = Prose(argv[2])
    
    result = original.diff(altered)

    file = open('output.html', mode='w')
    file.write(result.html())
    file.close()
