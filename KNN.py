class Node:
    def __init__(self, word, wordcount):
        self.word = word
        self.wordcount = wordcount
        self.nextval = None


def knnselect(Knnlist):     # Method to check which Knn to choose over 5
    if Knnlist[2] == Knnlist[0]:
        return Knnlist[2]
    if Knnlist[2] == Knnlist[4]:
        return Knnlist[2]
    if Knnlist[0] == Knnlist[1]:
        return Knnlist[0]
    if Knnlist[1] == Knnlist[2]:
        return Knnlist[2]
    if Knnlist[2] == Knnlist[3]:
        return Knnlist[2]
    if Knnlist[3] == Knnlist[4]:
        return Knnlist[3]
    return "All types different"


docLast = []        # Saves the id of first document with type X
docName = []        # Saves document types with id X
Docs = (open('docs', 'r').readlines())

docName.append(Docs[1].split("\t")[1])      # Adds first document type to docName
docLast.append(0)
doccount = 0
for docloop in Docs:                        # Checks all values in docs
    doc = docloop.split("\t")
    if docName[-1] != doc[1]:               # If the next doc type has different name it appends new values in lists
        docName.append(doc[1])
        docLast.append(doccount)
    doccount += 1

traintext = (open('TrainData', 'r').readlines())     # reads temp file that contains worlds in id order.
count = 0
TrainData = []                                       # Holds train data as Node array(word, wordcount, nextval)
Totaltrue = 0
Totalguess = 0
for train in traintext:                              # Loops train data
    tabs = train.split("\t")
    if tabs[0] == "\n":                              # checks if tabs[0] is EOF
        continue
    Root = Node(tabs[0], tabs[1])                    # creates root tab[0] first word tab[1] first wordcounter
    TrainData.append(Root)                           # appends Root to TrainData
    for countTab in range(2, len(tabs), 2):          # adds other words and their counts to the root
        Root.nextval = Node(tabs[countTab], tabs[countTab+1])
        Root = Root.nextval
    count += 1                                       # Saves total train documents

test = (open('TestData', 'r').readlines())     # reads train file that contains worlds in id order.
for ttt in range(len(test)):
    testSplit = test[ttt].split("\t")     # Loops for each test document
    MinDest = []                               # saves closest 5 distances
    MinDestId = []                             # saves closest 5 distances Id in order to find
    for trainloop in range(count):      # Loops trained data
        temp = TrainData[trainloop]
        dist = 0
        testloop = 0                    # checks which text id we are in
        while True:                     # Loops until the words of train document or test documents finish

            if testloop >= len(testSplit)-2:     # If test data ends
                break
            if temp is None:    # If train data ends

                while True:
                    dist += int(testSplit[testloop + 1])
                    testloop += 2
                    if testloop >= len(testSplit) - 2:      # Loops until the rest of the word counts added to distance
                        break
                break

            if int(testSplit[testloop]) < int(temp.word):    # test id < train id. Word in test is not found.
                testloop += 2       # increment twice because odd numbers hold count
                dist += int(testSplit[testloop+1])
                continue

            if testSplit[testloop] == temp.word:    # same word excepted calculate distance.
                dist += abs(int(testSplit[testloop+1]) - int(temp.wordcount))
                testloop += 2
                temp = temp.nextval
                continue

            if int(testSplit[testloop]) > int(temp.word):  # test id > train id. Word in train is not in test ignore.
                temp = temp.nextval
                continue

        MinDest.append(dist)    # Adds last test doc to minimum destinations list
        MinDestId.append(trainloop*2+1)     # Adds id of that test doc
        if len(MinDest) == 6:   # If list extends KNN
            delete = MinDest.index(max(MinDest))
            # print("Delete", MinDest[delete])
            MinDest.pop(delete)
            MinDestId.pop(delete)

    KNNnames = []
    Answer = ""         # Real answer to check
    for dtr in range(len(docLast)):         # Detecting real answer.
        if docLast[dtr] > ttt*2:
            Answer = docName[dtr-1]
            break
    if Answer == "":
        Answer = docName[-1]

    for xx in range(5):                 # Sorts KNN
        for dtr in range(len(docLast)):
            if docLast[dtr] > MinDestId[xx]:
                KNNnames.append(docName[dtr-1])
                break
        if xx == len(KNNnames):
            KNNnames.append(docName[-1])

    foundAns = knnselect(KNNnames)
    Totalguess += 1
    if Answer == foundAns:
        Totaltrue += 1
    print("ID: ", ttt*2, " Answer found: ", foundAns, "\nReal Answer ", Answer)
    print("Ratio: ", (Totaltrue*100/Totalguess) / 1, "%\n")
