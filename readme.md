https://docs.google.com/spreadsheets/d/13KDITzV5F0D-_dOVp5ZiHeFLWGx1e0V6SV9oRrzeODw/edit#gid=1401260553
Your task is to port this code to python
You can access the code via Extensions -> Apps Script (You might need to make a copy of the file)
- The words are found in the Lexicons, for example 'Castle' in English is 'Krytiamī' in Fira, and you can determine this using `CreateWord("Protection + House", 3, 2)`, where the "Protection + House" part is specified in the Logic column. Please note that not all words use CreateWord so watch out for that.
  - The Extended and Plural lexicons work in much the same way, and they always use the same formula
- The lexicon should be stored in a text file (I would recommend using File -> Download -> .tsv to easily export the lexicon - a .tsv is exactly the same as .txt as far as Python is concerned.
  - I recommend using the Rainbow CSV extension for VSCode to make the tsv more readable
  - This could mean a file for each lexicon or you could just combine them into one, I don't mind
  - IMPORTANT: I do not want any Fira words to be stored except for the 'root' words - those with a '-' in the Logic column. All of these should have no formula in the Formula column, or with some super simple formula that basically just holds a string, such as addGender()
    - Actually I'm okay with a cache of words being stored, but there needs to be some function that causes them to all be recalculated (recursion will likely be needed owing to dependencies)
    - This means that the tsv file will need to store some equivalent of the formula column - I'd recommend making a new system based on but not the exact same as the fomulas on the sheet. Ultimately, you can choange whatever you want about how the translation works as long as it still transaltes correctly in the end
      - It would also be nice to keep the notes column to help me organise
  - It needs to be quick and painless to add new words to the stored lexicon
- The program does not need to worry about sentence ordering or anything like that, just translate the words one-by-one. With that in mind, you do still need to worry about preserving punctuation!
- The program mush be able to translate any number (e.g. '30') using Fira's number system. It's explained on the Fira Explained page but I ran provide more clarification if needed.
- The way I would expect it to work is that the user can type a word into the terminal and the program will then print the translation of the word.




## Example 1: Standard Word
```'Armour    multicompoundword    ["Protection", "Cloth"]    [0, 1]    [3, 0], "-"'```
A word may be stored like this in the .tsv, depends how you want to do it.
After processing the string you would end up with this:
```py
["Armour", "create_word", ["Protection", "Cloth"], [0, 1], [3, 0], "-"]
```
The Fira word for Armour can be created by using the multicompoundword function:
- Take the Fira word for protection, 'Kryevī'
- Slice it by [:-3] to get 'Kry'
- Take the Fira word for cloth, 'Załurī'
- Slice it by [1:] to get 'ałurī'
- Then stick the two words together to get 'Kryałurī'

## Example 2: Root Word
(After processing string:)
```py
["Colour", "Cr̄oma", "add_gender", ["Cr̄om", "f"])
```
This is an example of a root word: It stores a string (Cr̄om) directly in Fira, rather than in English. For this reason, I would reccomend putting the root words in a different file.
The word can be created using the add_gender function:
- Take the body of the word, 'Cr̄om'
- 'F' indicated that you should add the feminine ending, stored as '_Feminine' in the lexicon, currently as 'a'.
- Then stick the two words together to get 'Cr̄oma'




- **addGender** (defined as `addGender(word, gender, replaceLast=false)`)
  - It takes a 'word', i.e. a direct string that shouldn't be translated (hence why I count it as a base word) 
  - Then adds a gendered word ending to it, as specified by the gender parameter: 'm' for masculine, 'n' for neutral, 'f' for feminine, 'p' for plural. 
    - These are stored as root words under '_masculine', etc.
  - replaceLast is false by default. If set to true, it should remove the last letter of the word before adding the gendered word ending
- **concatenate** is a default spreadsheet function that takes any number of strings and puts them together, so `concatenate("a", "b", "c")` is tha same as `"a"+"b"+"c"` in python.
- **engToFira** is a depreciated function. Just treat it as translate() instead.
  - **translate** is essentially your code: it takes a string and translates it, accounting for 'combined words' where multiple word in English translate to one word in Fira, such as 'Solar System' and verbs that may or may not be preceded by a 'to'.
### **createWord**
createWord decides whether to use compoundWord, multiCompoundWord, or deriveword.
- When used on a logic of 'word1 + word2', e.g. Protection + Cloth, it uses compoundWord/multiCompoundWord (they do the same thing basically) to translate the words and stick them together, as explained here: https://discord.com/channels/@me/1155044108704940032/1192086218415034369.
  - The two numbers are the number of letters to remove from each word.
    - The first number tells you how many letters to remove from the end of the first word.
    - The second number tells you how many letters to remove from the start of the second word.
  - Please note that there may be more than two words such as for Cat. My code for this is a non-functional mess but to keep it the same as the spreadsheet for now, it should work as follows:
    - The first number tells you how many letters to remove from the end of all word but the last.
    - The second number tells you how many letters to remove from the start of the last word.
    - So using the system I suggested in my previous message, Cat (`=createWord("Rodent + Killer + Animal", 3, 0)`) would be `["Cat", "create_word" ["Rodent", "Killer", "Animal"], [0, 0, 0], [3, 3, 0]`
- When used on a logic of 'X of Y', e.g. Speaker is 'F Subject of To Speak', deriveWord is used
  - The rules for deriving a wort (i.e. turning a verb into a noun, etc.) are explained in the Fira Explained section of the spreadsheet.
  - `deriveWord(word, type, gender="", sliceStart = 0, sliceEnd = 0)`
    - word is the word to be derived from
    - type is the type to change the word to, e.g. 'subject'. The valid types are:
      - object (e.g. To Hunt -> A Hunt)
      - subject (e.g. To Hunt -> Hunted)
      - place (e.g. To Hunt -> Hunting Grounds)
      - verb (e.g. A Hunt -> To Hunt)
      - This should go without saying but just because an example here starts with a verb or whatever, doesn't mean that that will always be the case.
      - The endings to use for each type are stored in the root words as '_object', etc.
    - gender is the gender to add to the new word as per the addGender function, a blank input means none should be added.
    - sliceStart and sliceEnd are how many characters to remove from the word after translation but before adding the derivation letter or gender. This works as `word = translate(word)[sliceStart:sliceEnd]`.




1. You have pointed out something but not what the problem with it is.
2. I'm assuming that you're still talking about cat here. Here's an example I've come up with off the top of my head to show which number goes where: `=createWord("A + B + C", 1, 2)` would be `["Elephant", "compoundword" ["A", "B", "C"], [0, 0, 1], [0, 2, 2]`
I suspect that it would be easier to use compoundword instead of createword in cases where it would just use compoundwork anyway. It's up to you.
3. What brackets? What word? Please elaborate
4. I am deeply sorry for making such atrocious errors, I will attempt to avoid making further spelling mistakes ever again.
5. Because the lists allow you to control how much you remove from the start and end of each word individually.
