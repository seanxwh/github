def createDataFromFile(filename):
    lines=[line for line in file(filename)]
    #hold all parsed words from the file into an array
    columnWords=lines[0].strip().split('\t')[:]
    #hold all names of all the owners/blogs that used the parserd words list
    rowNames=[]
    #array that holds the sub-array of the parsed words count for each owner/bloger
    data=[]
    for line in lines[1:]:
        p=line.strip().split('\t')
        rowNames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return rowNames,columnWords,data
