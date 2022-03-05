#This function returns the score of a word inputted
def score_word(word, wcUsed):
    '''
    This function takes a word and any wildcard characters used as input and 
    outputs the score based on the scrabble dictionary
    '''
    scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10}
    score = 0
    #another method I tried, which sometimes returned faster
    #for char in word:
    #    if char in wcUsed:
    #        continue 
    #    else:
    #        score += scores.get(char)
    #this sums the scores for each letter but skips a letter if it was a WC
    return sum(scores[letter] for letter in word if letter not in wcUsed)

def getValidWords(rack,ScrList,wcChars):
    '''
    This function loops through each word in the scrabble dictionary and checks if 
    it's a valid word for the rack to be able to make. It returns each valid word with
    the wc characters used in a list of tuples format
    '''
    WordsAndWcUsed = []
    for vWord in ScrList:
        #assign copies of rack and wcChars so we can manipulate them in the loops
        orgWcChars = wcChars
        orgRack = rack
        wcUsed = []
        Match = True
        #go through each letter in the current word to see if it's in the rack
        for letter in vWord:
            if letter in orgRack:   #if it is, take it out of the rack for the next iteration
                orgRack = orgRack.replace(letter, '', 1)
            else:   #if it's not, not a match so break
                Match = False
                break
            if letter in orgWcChars:    #if you use the WC to make the word, add it to the wcUsed list for scoring
                wcUsed.append(letter)
                orgWcChars = orgWcChars.replace(letter, '', 1)
        if Match == True:
            vWordLw = vWord.lower()
            wcString = ""
            wcString = wcString.join(wcUsed)
            wcStringFinal = wcString.lower()
            #this function will output a list of tuples with each element being
            #(valid word, wcChars that were used)
            data = (vWordLw,wcStringFinal)
            WordsAndWcUsed.append(data)
        else:
            continue    
    return WordsAndWcUsed

#this was another way I tried to implement the getValidWords to speed up execution,
#but it didn't produce much improvement 
def getValidWords2(rack,ScrList,wcChars):
    '''
    Deprecrated: Tried to speed up the getValidWords function with this alternate implementation
    but it didn't speed up overall execution time
    '''
    WordsAndWcUsed = []
    for vWord in ScrList:
        #orgWcChars = wcChars
        #orgRack = rack
        wcUsed = []
        if all(vWord.count(c) <= rack.count(c) for c in vWord) == True:
            vWordLw = vWord.lower()
            wcUsedSet = ''.join(sorted(set(vWord) & set(wcChars), key = vWord.index))
            wcUsed = str(wcUsedSet)
            #wcString = ""
            #wcString = wcString.join(wcUsed)
            wcStringFinal = wcUsed.lower()
            data = (vWordLw,wcStringFinal)
            WordsAndWcUsed.append(data)
        else:
            continue    
    return WordsAndWcUsed