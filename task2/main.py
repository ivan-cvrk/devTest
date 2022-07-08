brackets = [
        ('(', ')'),
        ('[', ']'),
        ('{', '}')
    ]


def bracketsAreBalanced(file, brackets):

    # counter for bracketTypes
    bracketStack = []

    # map each bracket to its key
    openingBrackets = {}
    closingBrackets = {}
    for x in brackets:
        openingBrackets[x[0]] = x
        closingBrackets[x[1]] = x

    # evaluate brackets for a line
    def evalBrackets(line): 
        for c in line:
            if c in openingBrackets.keys():
                bracketStack.append(openingBrackets[c])
            elif c in closingBrackets.keys():
                if bracketStack[-1] == closingBrackets[c]:
                    bracketStack.pop()
                else:
                    raise Exception
            else:
                continue

    for line in file: 
        try:
            evalBrackets(line)
        except:
            return False

    return len(bracketStack) == 0


with open('file.txt') as file:
    if bracketsAreBalanced(file, brackets):
        print('Brackets are balanced!')
    else:
        print('Brackets are not balanced!')
