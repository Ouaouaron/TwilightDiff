from sys import argv

class Prose:
    def __init__(self, location):
        self.text = []
        with open(location, encoding='utf-8') as file:
            for line in file:
                self.text += line.split()
                self.text.append('\n')
        self.head = 0


class ProseDiff:
    def __init__(self, taggedtext):
        """`taggedtext` should be a list of (text, tag) pairs where `tag` is
           a string 'same', 'original', 'altered', or 'newline'"""
        self.taggedtext = taggedtext

    def html(self):
        """Return an html file of the diff as a string."""
        htmlhead = "../resources/htmlhead.html"
        replacements = {'language' : 'en-US',
                        'encoding' : 'utf-8',
                        'title' : 'TwilightDiff'}

        with open(htmlhead, encoding='utf-8') as file
            result = file.read()
        for key, value in replacements:
            result.replace('[['+key+']]', value)

        result += "\t<p>"
        for text, tag in self.taggedtext:
            if tag == 'newline':
                result += '</p>\n\t<p>'
            elif tag == 'same':
                result += text
            elif tag == 'original' || tag == 'altered':
                result += '<span class="{}">{}</span>'.format(tag, text)
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
