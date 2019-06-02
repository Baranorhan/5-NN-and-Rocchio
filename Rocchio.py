import numpy as np

docLast = []  # Saves the id of first document with type X
docName = []  # Saves document types with id X
Docs = (open('docs', 'r').readlines())

docName.append(Docs[1].split("\t")[1])  # Adds first document type to docName
docLast.append(0)
doccount = 0  # Counts the documents passed
Totaltrue = 0  # Check how many answer we found right
Totalguess = 0  # How many answer we found at total

traintext = (open('TrainData', 'r').readlines())  # reads temp file that contains worlds in id order.
traindata = list()  # hold np values for each centroids

traindata.append(np.zeros(125754, dtype=int))  # each centroid will hold a np array each words position shows how many
# times its repeat value over document number
# I didn't implement a linked list because the number of centroids are limited enough to support all words
# and it can work much more faster than checking all words in a linked list implementation
for docloop in range(0, len(Docs) - 1, 2):  # Checks all values in docs

    doc = Docs[docloop].split("\t")  # converts document as arrays separated with tab
    if docName[-1] != doc[1]:  # If the next doc type has different name it appends new values in lists
        docName.append(doc[1])
        docLast.append(doccount)

        traindata[-1] = np.divide(traindata[-1], (docLast[-1] - docLast[-2]))  # when new article categories found
        # divide each word count to the document number
        traindata.append(np.zeros(125754, dtype=int))
    splitted = traintext[doccount].split("\t")  # Loops train data and adds all words to the current centroid
    for x in range(0, len(splitted) - 1, 2):
        traindata[-1][int(splitted[x])] += int(splitted[x + 1])     # Array implementation also speeds train process

    doccount += 1


traindata[-1] = np.divide(traindata[-1], (doccount - docLast[-2]))        # divides last centroid

test = (open('TestData', 'r').readlines())  # reads train file that contains worlds in id order.
for ttt in range(len(test)):
    testSplit = test[ttt].split("\t")   # Loops for each test document
    mindisttemp = np.inf                # minimum distance in each centroid
    tempans = docName[0]                # name of minimum distance centroid

    for trainloop in range(len(traindata)):  # Loops for each centroid
        dist = 0        # Total dist between centroid and test doc
        testloop = 0    # checks which text word we are in

        while True:     # Loops for each word in the test document

            if testloop >= len(testSplit) - 2:  # If test data ends
                break
            # print("old", dist)
            # print(testSplit[testloop + 1], traindata[trainloop][int(testSplit[testloop])])

            dist += abs(int(testSplit[testloop + 1]) - traindata[trainloop][int(testSplit[testloop])])
            # testSplit[testloop + 1] number of repeat in test
            # traindata[trainloop][int(testSplit[testloop])] number of repeat in centroid for same word
            # print("new", dist)
            testloop += 2

        if dist <= mindisttemp:      # If this centroid has smaller distance it becomes new temp
            mindisttemp = dist
            tempans = docName[trainloop]

    Answer = ""  # Real answer to check
    for dtr in range(len(docLast)):  # Detecting real answer.
        if docLast[dtr] > ttt * 2:
            Answer = docName[dtr - 1]
            break
    if Answer == "":            # Check if the answer we found is true
        Answer = docName[-1]
    Totalguess += 1
    if Answer == tempans:
        Totaltrue += 1

    print("ID: ", ttt * 2, " Answer found: ", tempans, "\nReal Answer ", Answer)
    print("Ratio: ", (Totaltrue * 100 / Totalguess) / 1, "%\n")
