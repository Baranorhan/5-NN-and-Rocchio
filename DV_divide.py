f = (open('DV', 'r').readlines())
Even = True
with open('TestData', 'a+') as test, open('TrainData', 'a+') as train:
    for line in f:
        term = line.rstrip()
        if Even:
            test.write(term + "\n")
            Even = False
            continue
        else:
            train.write(term + "\n")
            Even = True
