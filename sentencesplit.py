import csv
import os
from nltk import tokenize

def tamToEng(string):

    # Distinguishes retroflex n and l, as well as alveolar trill from tap
    uyir = {"அ" : "a", "ஆ" : "aa",  "இ" : "i", "ஈ" : "ee", "உ" : "u", "ஊ" : "oo", "எ" : "e", "ஏ" : "E", "ஐ" : "ai", "ஒ" : "o", "ஓ" : "o", "ஔ" : "au"}
    mei = {"க" : ["ga", "ka"], "ங" : ["nga"], "ச" : ["sa", "cha"], "ஞ" : ["nya"], "ட" : ["da", "ta"], "ண" : ["Na"], "த" : ["dha", "tha"], "ந" : ["na"], "ப" : ["ba", "pa"], "ம" : ["ma"], "ய" : ["ya"], "ல" : ["la"], "ர" : ["ra"], "வ" : ["va"], "ழ" : ["zha"], "ள" : ["La"], "ற" : ["Ra", "tra"], "ன" : ["na"], "ஷ" : ["sha"], "ஸ" : ["sa"], "ஹ" : ["ha"], "ஜ" : ["ja"]}
    marks = {"ா" : "aa", "ி" : "i", "ீ" : "ee", "ு" : "u", "ூ" : "oo", "ெ" : "e", "ே" : "E", "ை" : "ai", "ொ" : "o", "ோ" : "o", "ௌ" : "au"}
    pulli = "்" 

    vallinam = ["க", "ச", "ட", "த", "ப", "ற"]

    processed = list(string.strip())
    final = []

    idx = 0
    pullied = False

    for i in range(len(processed)):

        letter = processed[i]
        
        # adds uyir ezhuthukkal
        if letter in uyir.keys():
            final.append(uyir[letter])
            idx += 1

        # adds mei ezhuthukkal
        elif letter in mei.keys():

            # checks for word-initial vallinam ezhuthukkal
            if letter in vallinam and (idx == 0 or processed[i-1] in ' !"#$%&\'()*+,-./0123456789:;<=>?[\\]^_`{|}~'):
                final.append(mei[letter][1])
                idx += 1

            # checks for rule changes
            elif pullied and letter in vallinam:

                # adding "nj"
                if processed[i-2] == "ஞ" and letter == "ச":
                    final[idx-1] = "n"; final.append("ja")
                    idx += 1

                # adding "ndr"
                elif processed[i-2] == "ன" and letter == "ற":
                    final[idx-1] = "n"; final.append("dra")
                    idx += 1

                # adding "tr"
                elif processed[i-2] == "ற" and letter == "ற":
                    final[idx-1] = "t"; final.append("ra")
                    idx += 1

                # geminated consonants
                elif processed[i-2] == letter:
                    if len(mei[letter][1]) == 2:
                        final.append(final[idx-1])
                        idx += 1
                    final[idx-1] += "a"
                    

                # double vallinam
                elif processed[i-2] in vallinam:
                    final.append(mei[letter][1])
                    idx += 1

                # regular consonant + vallinam  
                else:
                    final.append(mei[letter][0])
                    idx += 1

                pullied = False
                
            # adds regular mei ezhuthukkal
            else:
                final.append(mei[letter][0])
                idx += 1
        
        # adds diacritic vowel markings
        elif letter in marks.keys():

            # kutriyalugaram: shortening of the word-final "u"
            if letter == "ு" and (i == len(processed)-1 or processed[i+1] == " "):
                final[idx-1] = final[idx-1][:-1] + "u"

            # regular vowels
            else:
                final[idx-1] = final[idx-1][:-1] + marks[letter]

        # removes inherent vowels
        elif letter == pulli:
            pullied = True
            if processed[i-1] not in vallinam or processed[i-1] == "ற":
                final[idx-1] = final[idx-1][:-1]
            else:
                final[idx-1] = mei[processed[i-1]][1][:-1]
            
        # adds any not-letters
        else:
            final.append(letter)
            idx += 1
            pullied = False

    # returns final string
    return "".join(final)


dirname = os.path.dirname(os.path.dirname(__file__))
filename = os.path.join(dirname, 'videoDLs/Yarl0.txt')
csvname = os.path.join(dirname, 'videoDLs/test0.csv')
engname = os.path.join(dirname, 'videoDLs/Yarl0-Eng.txt')


file = open(filename, "r+")
text = file.read()

with open(csvname, "w", encoding='UTF8') as f:

    writer = csv.writer(f)
    writer.writerow(["tamil", "transliterated", "colloquial"])

    for token in tokenize.sent_tokenize(text):
        writer.writerow([token, tamToEng(token)])

with open(engname, "w", encoding="UTF8") as f: 
    for token in tokenize.sent_tokenize(text):
        f.write(tamToEng(token))

file.close()

