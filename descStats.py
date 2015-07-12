import pandas as pd
import re
import os

class static:

    notContUS = ["GU","PR","FM","AS","VI","AK","HI",'AE']

    kwords = [
            # these are my personal terms of interest
           'microbiology', 'botany', 'mycology', 'fungus', 'fungi',
            'microbe', 'microbes','biosystems', 'biosystem', 'rhizobia',
            'mycorrhizae', 'mycorrhizal', 'microbiome', 'mycobiome',
            'phytopathology', 'pathology','dna','evolution', 'genetics',
            'ecology','bioinformatics', 'plant', 'fungal', 'plants',
            'herbarium','herbaria','geospatial','gis'
           ]

    def __init__(self):
        # assigns and sorts either the new keyword set or keeps the old one
        userTerms = self.__userInput()
        if userTerms != []:
            self.kwords = userTerms
        self.kwords = sorted(self.kwords)

    def __userInput(self):

        # optionally takes user selected keword terms
        print 'Enter the terms you want to search for, or just press return for default terms.'
        arr = []
        term = raw_input()

        while (term != ''):
            term = term.lower()
            arr.append(term)
            term = raw_input()
        return(arr)

    #we can probably put in something to bin data here

class AbstractExtract(static):
    def __init__(self,abstract,kwords):
        self.kwords = kwords
        self.abstract = abstract
        self.tokens = self.__tokenize()
        self.matches = self.__tokenMatch()

    def __tokenize(self):
        # splits abstract into discrete words
        try:
            abNums = re.sub('\d','',self.abstract)
            abLower = abNums.lower()
            abNoPunct = re.sub('[^a-z ]','',abLower)
            tokens = abNoPunct.split(' ')
        except:
            return([])
        return(tokens)

    def __tokenMatch(self):
        # finds term matches inside abstract
        matches = []
        for term in self.kwords:
            if term in self.tokens:
                matches.append(term)
        return(matches)

class dfProcessor(static):
    def __init__(self,df):
        self.name = df
        static.__init__(self)
        self.__df = pd.read_csv(df)
        self.__cleanDF = self.__process()
        self.freqTable = self.__stateFreq()
        self.__transformPrep()
        self.transDF = self.__transform()

    def __process(self):
        # creates column with arrays of extracted terms
        self.__df['AbstractTokens'] = map(lambda x:
            AbstractExtract(x,self.kwords).matches, self.__df['Abstract at Time of Award'])
        reducedDF = self.__df[self.__df['AbstractTokens'].map(lambda x: len(x)>0)]
        reducedDF.drop(["Abstract at Time of Award"],inplace=True,axis=1)
        return(reducedDF.reset_index().drop('index', axis=1))

    def __stateFreq(self):
        # makes dictonary for how many awards each state won
        stateFreqTable = {}
        for state in self.__cleanDF['Primary State']:
            if state in self.notContUS:
                next
            elif type(state) != str:
                next
            else:
                stateFreqTable[state] = stateFreqTable.get(state,0)+1

        stateStates = sorted(stateFreqTable.keys())
        stateVals = map(lambda x: stateFreqTable[x],stateStates)
        return(stateFreqTable)

    def __transformPrep(self):
        # acts on existing self.__cleanDF to add term counts
        for kword in self.kwords: self.__cleanDF[kword] = 0
        for i in self.__cleanDF.index:
            for term in self.__cleanDF.loc[i,"AbstractTokens"]:
                if term == self.__cleanDF.loc[i,"AbstractTokens"][-1]: break
                self.__cleanDF.loc[i,term]+=1

    def __transform(self):
        # subset the dataframe to make matrix of counts
        matrix = self.__cleanDF.drop(['Year','AbstractTokens'],1)
        matrix = matrix.groupby("Primary State").sum()
        for x in self.notContUS:
            try:
                matrix = matrix.drop(x)
            except:
                next

        return(matrix.T)

    def exportMatrix(self):
        # exports matrix of term counts
        abspath = os.path.abspath(self.name)
        filename = re.search('/(\w*\.csv)$',abspath)
        newName = 'awardMatrices/'+filename.group(1)

        if os.path.isdir('awardMatrices/') == False:
            os.makedirs('awardMatrices/')

        self.transDF.to_csv(newName)
