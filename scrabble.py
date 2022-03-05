import sys 
import wordscore

#will track execution time for debugging - commenting out to match with autograder
#import time
#start_time = time.time()

#Checks that a rack is entered
if len(sys.argv) < 2:
    raise Exception("Please define your rack")
    exit()
#initializing variables
myRack = str(sys.argv[1])
myRackUp = myRack.upper()
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
WordsAndWcUsed = []
WAndWcWithDup = []
check_val = set()   # This will be used to help deduplicate the data for a 2 WC use case

#Checks against length of rack
if len(myRack) < 2 or len(myRack) > 7:
    raise Exception("Must enter between 2 and 7 letters")
    exit()
#Checks that no numbers are entered
if any(char.isdigit() for char in myRackUp) == True:
    raise Exception("Do not include numbers in rack")
    exit()
#Checks that no special characters are entered
spChr = [-1 for i in myRackUp if i in '[@_!#$%^\'\"&()<>/\|}{~:]']
if -1 in spChr:
    raise Exception("No special Characters allowed")
    exit()    
#Checks if more than 1 kind of widlcard are being used
if myRack.count('*') > 1 or myRack.count('?') > 1:
    raise Exception("You're limited to only one of each wildcard (*,?)")
    exit()
#code given - open data and save as list 
with open("sowpods.txt","r") as infile:
    raw_input = infile.readlines()
    data = [datum.strip('\n') for datum in raw_input]

#get count of wildcard characters used and the indices of each
wcCount = myRackUp.count('*') + myRackUp.count('?')
qmark = myRackUp.find('?')  #Returns index of question mark
star = myRackUp.find('*')   #Returns index of star

#if no wildcard characters in the rack
if wcCount == 0:
    #Call getValidWord which will return a list of tuples
    #each element = (valid word, which wildcard chars were used)
    #because this case statement has no wildcards, pass in a blank string to 3rd arguement
    WordsAndWcUsed = wordscore.getValidWords(myRackUp,data,'')
#if one wildcard character in the rack
elif wcCount == 1:
    i = max(qmark,star) #returns the index of the wc, 1 will return -1
    #because there was one WC, generate a word for each letter in the alphabet and 
    #pass that into the getValidWordsFunction
    for a in alphabet:
        word = myRackUp[0:i] + a + myRackUp[i+1:]   #slice the word based on found WC index
        iterWordsAndWc = wordscore.getValidWords(word,data,a)
        #add any generated valid words to final output at each generation
        WAndWcWithDup = WAndWcWithDup + iterWordsAndWc
    #this block removes any duplicate tuples from the list 
    for i in WAndWcWithDup:
        if i[0] not in check_val:
            WordsAndWcUsed.append(i)
            check_val.add(i[0])
#if 2 wc characters are in the rack
elif wcCount == 2:
    i = min(qmark,star) #will be the first index to slice on
    j = max(qmark,star) #will be the second index to slice on
    words = []
    #use two for loops to generate all the combinations of words that can be formed from the rack
    for a in alphabet:
        for b in alphabet:
            word = myRackUp[0:i]+ a + myRackUp[i+1:j] + b + myRackUp[j+1:] #slice the word based on WC indices
            wcString = a + b    #concatenate the wc characters to pass into getValidWords
            #each iteration, only add a word in if it hasn't already been generated
            if word not in words:
                iterWordsAndWc = wordscore.getValidWords(word,data,wcString)
                WAndWcWithDup = WAndWcWithDup + iterWordsAndWc
                words.append(word)  #keep words list updated each iteration to ensure no unnecessary runs 
            else:
                continue
    #deduplication (same as in case wcCount = 1)
    for i in WAndWcWithDup:
        if i[0] not in check_val:
            WordsAndWcUsed.append(i)
            check_val.add(i[0])

#create a new list of tuples with (score, word) calling the score function for each word in the previous list
ScoresAndWords = []
ScoresAndWords = [(wordscore.score_word(ele[0],ele[1]), ele[0]) for ele in WordsAndWcUsed]
#This was another method I tried, but list comprehension was faster obviously
#for ele in WordsAndWcUsed:
#    toAdd = (wordscore.score_word(ele[0],ele[1]), ele[0])
#    ScoresAndWords.append(toAdd)

#The two required sortings using lambda functions
ScoresAndWords.sort(key=lambda x:x[1])
ScoresAndWords.sort(key=lambda x:x[0], reverse = True)

#Below was the first print method I tried, but was not successful in removing the quotation marks
# #print(*ScoresAndWords, sep = "\n")
#This emthod below successfully removed the quotes from the string in tuple and suprisingly sped up
#the execution despite it being a for loop
for ele in ScoresAndWords:
    ele1Print = ele[1].strip("'")
    print(f"({ele[0]}, {ele1Print})", sep = "\n")
print(f"Total number of words: {len(WordsAndWcUsed)}", sep = "\n")

#Commenting out time print to match autograder
#end_time = time.time()
#print(f"Total execution time was {end_time-start_time} seconds")