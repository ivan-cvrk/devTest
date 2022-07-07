brackets = [
        ('(', ')'),
        ('[', ']'),
        ('{', '}')
    ]


def bracketsAreBalanced(file, brackets):

    # counter for bracketTypes
    bracketCount = { x: 0 for x in brackets }

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
                bracketCount[openingBrackets[c]] += 1
            elif c in closingBrackets.keys():
                bracketCount[closingBrackets[c]] -= 1

                if bracketCount[closingBrackets[c]] < 0:
                    raise Exception
            else:
                continue

    for line in file: 
        try:
            evalBrackets(line)
        except:
            return False

    return sum(bracketCount.values()) == 0


with open('file.txt') as file:
    if bracketsAreBalanced(file, brackets):
        print('Brackets are balanced!')
    else:
        print('Brackets are not balanced!')
