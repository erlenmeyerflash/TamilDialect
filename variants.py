# create colloquial variants

def plural(text):
    
    text = text.split()

    for i in range(len(text)):
        if text[i][-4:] in ["ngal", "rgal"]:
            text[i] = text[i][:-4] + "nga"
        elif "rgal" in text[i]:
            idx = text[i].find("rgal")
            text[i] = text[i][:idx] + "ngal" + text[i][idx+4:]

    return " ".join(text)


def locative(text): 

    text = text.split()

    for i in range(len(text)):
        if text[i][-3:] == "yil":
            text[i] = text[i][:-3] + 'le'
        elif text[i][-2:] == "il":
            text[i] = text[i][:-2] + "le"

    return " ".join(text)


def accusative(text):

    text = text.split()

    for i in range(len(text)):
        if text[i][-2:] == "ai":
            text[i] = text[i][:-2] + "e"

    return " ".join(text)


def gemination(text):

    geminate = ["thth", "tt", "pp", "kk"]

    changed = []
    
    for gem in geminate:
        ungem = gem[:int(len(gem)/2)]
        replaced = text.replace(gem, ungem)
        if replaced != text:
            changed.append(replaced)

    return changed


def vowel_orth(text):

    vows = {"ee" : "ii",
            "oo" : "uu",
            "aa" : "a",
            "ae" : "e"}
    
    changed = []

    for vow in vows:
        replaced = text.replace(vow, vows[vow])
        if replaced != text:
            changed.append(replaced)

    return changed


def h_g(text):

    vowels = ("a", "e", "i", "o", "u")
    idx = 0

    store = text

    while text[idx+1:].find("h") != -1:

        idx += text[idx:].find("h")
        
        if idx > 0 and idx < len(text) - 1:
            if text[idx-1] in vowels and text[idx+1] in vowels:
                text = text[:idx] + "g" + text[idx+1:]
            else: 
                idx += 1
        else:
            idx += 1

        if idx+1 >= len(text):
            break
   
    return text if text != store else None


def ch_s(text):

    text = text.split()

    for i in range(len(text)):
        if text[i][:2] == "ch":
            text[i] = "s" + text[i][2:]

    changed = " ".join(text)
    return changed if text != changed else None

def zh_l(text):
    changed = text.replace("zh", "l")
    return changed if text != changed else None

def le_la(text):
    changed = text.replace("le ", "la ")
    return changed if text != changed else None

## Dialectic Alterations

def nrVariants(text):
    changed = []

    # Should n N be distinguished?
    variants = {
        "ndr" : ["nn", "nd", "nr"]
    }
    
    for original, replacements in variants.items():
        if original in text:
            for replacement in replacements:
                changed.append(text.replace(original, replacement))
    
    return changed if changed else None

# One problem is that not all words with "tr" will be changed this way, should this variation be handled with a word-level dictionary?
def tr_tt(text):
    # patri vs patti
    changed = text.replace("tr", "thth")
    return changed if changed != text else None

test = "changar mattrum ivargal taj mahalil thamizh puththagangalai saappittu padippaargal"

# print(test)
# #print(h_g(ch_s(orth_replace(orth_replace(gemination(accusative(locative(plural(test))), ["thth", "pp"]), ("zh", "l")), ("th", "t")))))

# print(ch_s(test))
# print(gemination(test))
# print(h_g(test))
# print(locative(test))
# print(le_la(locative(test)))
