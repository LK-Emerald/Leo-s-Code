import csv, re
with open("/Users/leokirk/Downloads/Copy of Fira - Lexicon.tsv") as file:  
     
    tsv_file = csv.reader(file, delimiter="\t")  
     
    for line in tsv_file:  
        print(line)  

def combineStr(word1, word2, trimVal=0, trim2Val=0):
  word1 = word1+"" # Converts iable type to string
  word2 = (word2+"").toLowerCase()
  if trimVal > 0:
    word1 = word1.slice(0, -trimVal)
  
  if trim2Val > 0:
    word2 = word2.slice(trim2Val)
  
  return word1+word2


def getIndexOf(key, range):
  key = key.toLowerCase()
  counter = 0
  for counter in len(range)-1:
    counter+=1
    if (range[counter]+"").toLowerCase() == key:
      return counter
    
  
  return -1


def engToFira(wordEng, ignorePunctuation=False):
  print("engToFira "+wordEng)
  # If no word is passed, return
  if len(wordEng) == 0:
    return wordEng
  
  # Manage punctuation
  if ignorePunctuation == False:
    punctuation = ["!", ",", ".", "?", "-", "+", "<", ">", "/", "(", ")", "[", "]", ":", "", ":", "", "@", "'", '"', "%"]
    foundPunctuation = ["", ""]
    if punctuation.indexOf(wordEng[0]) >= 0:
      return wordEng[0]+"0"+engToFira(wordEng.slice(1))
    
    if punctuation.indexOf(wordEng[len(wordEng)-1]) >= 0:
      return engToFira(wordEng[len(wordEng)-1])+"1"+wordEng.slice(0, -1)
    
  

  # Check for numbers
  if isNumber(wordEng):
    print("eTF isNumber True")
    return numberWord(wordEng)
  
  print("eTF isNumber False")

  if wordEng.toLowerCase() == "_place":
    return "iami"
  spreadsheet = SpreadsheetApp.getActive()
  currIndex = getIndexOf(wordEng, spreadsheet.getRange("wordBankEng").getValues())
  if currIndex >= 0:
    return spreadsheet.getRange("wordBankFira").getValues()[currIndex]
  else:
    currIndex = getIndexOf(wordEng, spreadsheet.getRange("wordBankEngExtended").getValues())
  if currIndex >= 0:
    return spreadsheet.getRange("wordBankFiraExtended").getValues()[currIndex]
  else:
    currIndex = getIndexOf(wordEng, spreadsheet.getRange("wordBankEngPlural").getValues())
    if currIndex >= 0:
        return spreadsheet.getRange("wordBankFiraPlural").getValues()[currIndex]
    else:
        return wordEng
      
    
  


def compoundWord(word1, word2, trim=2, trim2=0):
  word1 = translate((word1+"").replace(" ","")().toLowerCase())
  word2 = translate((word2+"").replace(" ","")().toLowerCase())
  return combineStr(word1, word2, trim, trim2)


def isNumber(s):
  print("isNumber "+s)
  i = 0
  for i in len(s):
    i+=1
    print("iN i "+i+" s[i] "+s[i])
    if s[i] < '0' or s[i] > '9':
      print("isNumber = False")
      return False
    
  
  print("isNumber = True")
  return True


def multiCompoundWord(*args):
  print("multiCompoundWord")
  counterStart = 0
  startFound = False
  trim = 2
  endSlice = 0
  if (isNumber(args[0])): # Check for an inital trim value
    trim = parseInt(args[0])
    counterStart = 1
  
  if (isNumber(args[len(args)-1])): # Check for a number at the end, which is used as the endSlice value
    endSlice = args.pop()
  counter = counterStart
  for counter in len(args):
    counter += 1
    if (isNumber(args[counter])):
      trim = parseInt(args[counter])
    else:
      if (startFound == False):
        currStr = translate(args[counter])
        startFound = True
      else:
        if (counter == len(args)-1):
          currStr = combineStr(currStr, translate(args[counter]).slice(endSlice), trim)
        else:
          currStr = combineStr(currStr, translate(args[counter]), trim)
        
      
    
  
  return currStr


def stringWord(word1, word2, join="-") :
  return translate(word1) + join + translate(word2)


def addGender(word, gender, replaceLast=False):
  gender = (gender+"").toLowerCase()
  if (replaceLast):
    word = word.slice(0, -1)+""
  
  if (["m", "masc", "masculine", "male"].indexOf(gender) >= 0): # Masculine
    return word + translate("_Masculine")
  elif (["f", "fem", "feminine", "female"].indexOf(gender) >= 0): # Feminine
    return word + translate("_Feminine")
  elif (["p", "plur", "plural"].indexOf(gender) >= 0): # Plural
    return word + translate("_Plural")
  elif (["n", "neut", "neutral"].indexOf(gender) >= 0): # Neutral/Unknown
    return word + translate("_Neutral")
  elif (["v", "verb"].indexOf(gender) >= 0): # Verb
    return word + translate("_Verb")
  elif (gender == ""): # N/A
    return word
  else:
    return "Gender not found"
  


def deriveWord(word, type, gender="", sliceStart = 0, sliceEnd = 0):
  type = (type+"").toLowerCase() # Parses to string and converts to lowercase
  sliceStart = parseInt(sliceStart)
  sliceEnd = parseInt(sliceEnd)
  #return "word: "+word+" | type: "+type+" | gender: "+gender+" | sliceStart: "+sliceStart+" | sliceEnd"+sliceEnd
  wordFira = sliceWord(translate(word), sliceStart, sliceEnd)
  if (type == "instance") : # To Hunt -> Hunting / A Hunt
    wordFira = wordFira + translate("_Instance")
  elif (type == "object") : # To Hunt -> Hunter
    wordFira = wordFira + translate("_Object")
  elif (type == "subject") : # To Hunt -> Hunted
    wordFira = wordFira + translate("_Subject")
  elif (type == "place") : # To Hunt -> Hunting Grounds
    wordFira = wordFira + translate("_Place")
  elif (type == "verb") : # A Hunt -> To Hunt
    return (wordFira+"").slice(0, -1) + translate("_Verb")
  elif (type == "plural") : # A Hunt -> To Hunt
    return addGender(wordFira, gender, True)
  elif (type == "gender") : # Used for gender only
    pass
  else:
    wordFira = "Derive type not found"
  

  wordFira = addGender(wordFira, gender)
  return wordFira


def sliceWord(string, startIndex, endIndex = 0) :
  startIndex = parseInt(startIndex)
  endIndex = parseInt(endIndex)
  if (endIndex == 0) :
    return string.slice(startIndex)
  
  return string.slice(startIndex, endIndex)


def trimArray(inputArray, toLower=True) :
  c=0
  for c in len(inputArray):
    c+=1
    inputArray[c] = (inputArray[c]+"").replace(" ","")()
    if (toLower) :
      inputArray[c].toLowerCase()
    
  
  return inputArray


def createWord(location, trim1=2, trim2=0) :
   words = trimArray((location+"").split("+"))
   if (len(words) == 2) : # If the input info requires compoundWord
    return compoundWord(words[0], words[1], trim1, trim2)
   elif (len(words) > 2) : # for multiCompoundWord
    #return words[0]+words[1]+words[2]
    return multiCompoundWord(trim1, *words, trim2) 
   elif len(words) == 1 :
    words = words[0].split("of")
    words = trimArray(words)
    if (len(words) > 1) : # for deriveWord
      if (["verb", "plural"].indexOf(words[0].toLowerCase()) >= 0) : # Checks to see if words[0].toLowerCase() is "verb" or "plural"
        return deriveWord(words[1], words[0], "p", trim1, trim2)
      
      data = words[0].split(" ")
      #return words[1]+"|"+data[1]+"|"+data[0]+"|"+trim1+"|"+trim2
      return deriveWord(words[1], data[1], data[0], trim1, trim2)
    
  
    return len(words)


def _join_number_word(finalString, newString, join, last_was_stop) :
  if (last_was_stop) :
    finalString = finalString + " " + newString
    last_was_stop = False
  else:
    finalString = finalString + join + newString
  
  return finalString, last_was_stop



def numberWord(userInput) :
  print("numberWord "+userInput)
  numberWordArray = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
  join = "-"
  zeroStop = translate("And")
  last_was_stop = False

  userInput = userInput+"" # Convert to string
  finalString = translate(numberWordArray[parseInt(userInput[0])])
  userInput = userInput.slice(1)
  #return [finalString, userInput]
  zeroCount = 0
  while (len(userInput) > 0) :
    print("userInput "+userInput)
    if (userInput[0] == 0) :
      zeroCount += 1
    else:
      if (zeroCount > 0) :
        finalString, last_was_stop = _join_number_word(finalString, translate(numberWordArray[0]), join, last_was_stop)
        if (zeroCount > 1) :
          finalString, last_was_stop = _join_number_word(finalString, numberWord(zeroCount), join, last_was_stop)
        
        finalString, last_was_stop = _join_number_word(finalString, zeroStop, join, last_was_stop)
        last_was_stop = True
        zeroCount = 0
      
      finalString, last_was_stop = _join_number_word(finalString, translate(numberWordArray[parseInt(userInput[0])]), join, last_was_stop)
    
    userInput = userInput.slice(1)
  
  if (zeroCount > 0) :
    finalString, last_was_stop = _join_number_word(finalString, translate(numberWordArray[0]), join, last_was_stop)
    if (zeroCount > 1) :
      finalString, last_was_stop = _join_number_word(finalString, numberWord(zeroCount), join, last_was_stop)
    
  
  return finalString


def translate(text) :
  print("Translate "+text)
  if (text == "") : # Check for empty input
    return ""
  
  # Check for numbers
  if (isNumber(text)) :
    print("Number found")
    return numberWord(text)
  else:
    print("Number not found")
  

  text = trimArray((text+"").split(" "))
  finalText = ""
  currWord = ""
  keepEng = False
  c=len(text)-2
  for c in 0 :
    c-=1
    keepEng = False
    currWord = text[c] + " " + text[c+1]
    print("c", c, "currWord", currWord)
    if (engToFira(currWord, True) == currWord) : # If it's not a combined word (e.g. "one hundred")
      currWord = text[c+1]
      if (engToFira("to " + currWord) == "to " + currWord) : # If it's not a verb without the 'to' at the start
        if (engToFira(currWord) == currWord) : # If it's not a recognised word
          keepEng = True
        
      else:
        currWord = "to "+currWord
      
      
    else :
      c-=1
    
    if (keepEng) :
      finalText = currWord + " " + finalText 
    elif (engToFira(currWord) != "") :
      finalText = engToFira(currWord) + " " + finalText 
    
  
  if (c > -2) : # If the last two words were not a combined word
    if (engToFira("to " + text[0]) == "to " + text[0]) : # If it's not a verb without the 'to' at the start
      currWord = engToFira(text[0])
      if (currWord == text[0]) : # If it's not a recognised word
        finalText = text[0] + " " + finalText
      elif (currWord != "") :
        finalText = currWord + " " + finalText
      
      else:
        finalText = engToFira("to " + text[0]) + " " + finalText
    
  
  if (finalText.slice(-1) == " ") :
    finalText = finalText.slice(0, -1)
  
  print("finalText "+finalText)
  return finalText


def testfunc() :
  #print(translate("and"))
  print(translate("1001"))
  #print(translate("Reflect"))




























def parseInt(headline):
  re.search('[0-9]+', headline).group()