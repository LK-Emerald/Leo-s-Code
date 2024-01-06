import csv, re

def extract_numbers(input_string):
    entries=input_string.split(',')
    match=[]
    i = 0
    for entry in entries:
        if i==0:
            pass
        if i!=0:
            match.append(re.sub(r'[^0-9]', '', entry))
        i+=1
        # match = re.sub(r'[^0-9]', '', append_match[0])
        # match += re.sub(r'[^0-9]', '', append_match[1])

    return match
    #pattern = r'^=createWord\(\$C(\d+),?(\d*)\)'
    #match = re.match(pattern, input_string)
    

with open("Fira.tsv") as file:  
    seg1,seg1line,seg2,seg2line = None,None,None,None

    tsv_file = csv.reader(file, delimiter="\t")  
    translate = input('Word to translate\n\n')
    for line in tsv_file:  
        if line[0] == translate:
            instructions = line[2]
            original_line = line
            instructionslist = instructions.split(" ")
            for line in tsv_file:
                if instructionslist[0] == line[0]:
                    seg1 = line[1]
                if instructionslist[2] == line[0]:
                    seg2 = line[1]
    print(seg1,seg2)
    resultline = extract_numbers(original_line[3])
    print(resultline)
    wrdremove1,wrdremove2= int(resultline[0]),int(resultline[0])+1
    seg1=seg1[:wrdremove1]+seg1[wrdremove2:]
    wrdremove1,wrdremove2 = int(resultline[1]),int(resultline[1])+1
    seg2=seg2[:wrdremove1]+seg2[wrdremove2:]
    seg1=seg1[1:]
    seg2=seg2[1:]
    print(resultline[0])
  
    finalword = seg1+seg2
    print(finalword)

        












    
            



































































