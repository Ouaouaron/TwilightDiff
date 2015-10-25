from sys import argv

if __name__ == "__main__":
    # Load original and altered
    original = Prose(argv[1])
    altered = Prose(argv[2])
    
    result = original.diff(altered)

    file = open('output.txt', mode='w')
    file.write(str(result))
    file.close()
