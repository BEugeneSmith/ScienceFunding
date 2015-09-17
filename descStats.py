import pandas as pd
import re
import os
pd.options.mode.chained_assignment= None

class static:

    notContUS = ["GU","PR","FM","AS","VI","AK","HI",'AE']

    kwords = [
            # default values
           'microbiology', 'botany', 'mycology', 'fungus', 'fungi',
            'microbe', 'microbes','biosystems', 'biosystem', 'rhizobia',
            'mycorrhizae', 'mycorrhizal', 'microbiome', #'mycobiome',
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
        # print 'Enter the terms you want to search for, or just press return for default terms.'
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

class dfAbstractProcessor(static):
    def __init__(self,dfName):
        self.name = dfName
        static.__init__(self)
        self.__df = pd.read_csv(dfName)
        self.__cleanDF = self.__process()
        self.freqTable = self.__stateFreq()
        self.__transformPrep()
        self.transDF = self.__transform() # not normailzed matrix
        self.abstractMax = self.__maxExtract()
        self.normDF = self.__valueNormalize()

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
        matrix = self.__cleanDF.drop(['Year','AbstractTokens','Estimated Total Award Amount'],1)
        matrix = matrix.groupby("Primary State").sum()
        for x in self.notContUS:
            try:
                matrix = matrix.drop(x)
            except:
                next

        return(matrix.T)

    def __maxExtract(self):
        # extracts maximum value from dataframe
        totals = []
        for i in self.transDF.index:
            for j in self.transDF.columns:
                totals.append(self.transDF.loc[i,j])
        maxVal = max(totals)

        return(maxVal)

    def __valueNormalize(self):
        # normalize values in a given array
        mx = self.abstractMax
        matrix = self.transDF

        for i in matrix.index:
            for j in matrix.columns:
                matrix.loc[i,j] = float(matrix.loc[i,j])/mx
        return(matrix)

    def exportMatrix(self):
        # exports matrix of term counts
        abspath = os.path.abspath(self.name)
        filename = re.search('/(\w*\.csv)$',abspath)
        newName = 'awardMatrices/'+filename.group(1)

        if os.path.isdir('awardMatrices/') == False:
            os.makedirs('awardMatrices/')

        self.transDF.to_csv(newName)

class dfFundsProcessor(static):

    def __init__(self,dfName):
        self.name = dfName
        static.__init__(self)
        self.__df = pd.read_csv(dfName)
        self.__cleanDF = self.__process()
        self.__fundMatrixPrep()
        self.fundMatrix = self.__fundMatrixTransform()
        self.fundMax = self.__maxExtract()
        self.__valueNormalize()

    def __process(self):
        # creates column with arrays of extracted terms
        self.__df['AbstractTokens'] = map(lambda x:
            AbstractExtract(x,self.kwords).matches, self.__df['Abstract at Time of Award'])
        reducedDF = self.__df[self.__df['AbstractTokens'].map(lambda x: len(x)>0)]
        reducedDF.drop(["Abstract at Time of Award"],inplace=True,axis=1)
        return(reducedDF.reset_index().drop('index', axis=1))

    def __fundMatrixPrep(self):
        # acts on existing self.__cleanDF to add term counts
        for kword in self.kwords: self.__cleanDF[kword] = 0
        for i in self.__cleanDF.index:
            for term in self.__cleanDF.loc[i,"AbstractTokens"]:
                if term == self.__cleanDF.loc[i,"AbstractTokens"][-1]: break
                self.__cleanDF.loc[i,term]+=self.__cleanDF.loc[i,'Estimated Total Award Amount']

    def __fundMatrixTransform(self):
        # subset the dataframe to make matrix of counts
        matrix = self.__cleanDF.drop(['Year','AbstractTokens','Estimated Total Award Amount'],1)
        matrix = matrix.groupby("Primary State").sum()
        for x in self.notContUS:
            try:
                matrix = matrix.drop(x)
            except:
                next

        return(matrix.T)

    def __maxExtract(self):
        # extracts maximum value from dataframe
        totals = []
        for i in self.fundMatrix.index:
            for j in self.fundMatrix.columns:
                totals.append(self.fundMatrix.loc[i,j])
        maxVal = max(totals)

        return(maxVal)

    def __valueNormalize(self):
        # normalize values in a given array
        mx = self.fundMax
        matrix = self.fundMatrix

        for i in matrix.index:
            for j in matrix.columns:
                matrix.loc[i,j] = float(matrix.loc[i,j])/mx


    def exportMatrix(self):
        # exports matrix of term counts
        abspath = os.path.abspath(self.name)
        filename = re.search('/(\w*\.csv)$',abspath)
        newName = 'fundMatrices/'+filename.group(1)

        if os.path.isdir('fundMatrices/') == False:
            os.makedirs('fundMatrices/')

        self.fundMatrix.to_csv(newName)

class matrixCollate:
    def __init__(self,df1,df2,df1mx,df2mx):
        self.df1 = df1
        self.df2 = df2
        self.df1mx = df1mx
        self.df2mx = df2mx

        if len(df1) != len(df2) or df1.size != df2.size:
            pass

        # denormalized dataframes
        self.__df1denorm = self.__dfDenormalize(self.df1,self.df1mx)
        self.__df2denorm = self.__dfDenormalize(self.df2,self.df2mx)

        # create new dataframe
        self.collDF = self.__collate()
        self.rateDF = self.__rateCalc()


    def __dfDenormalize(self,df,mx):
        # normalizes dataframes
        for i in df.columns.tolist():
            for j in df.index.tolist():
                df.loc[j,i] = (mx * df.loc[j,i])
        return(df)

    def __collatePrep(self,df):
        # creates new empty dataframe
        newDF = pd.DataFrame(
            index = df.index,
            columns = df.columns
        )
        return(newDF)

    def __collate(self):
        newDF = self.__collatePrep(self.df1)
        for i in newDF.columns.tolist():
            for j in newDF.index.tolist():
                vals = [self.__df1denorm.loc[j,i],self.__df2denorm.loc[j,i]]
                newDF.loc[j,i] = vals
        return(newDF)

    def __rateCalc(self):
        newDF = self.__collatePrep(self.df1)
        for i in newDF.columns.tolist():
            for j in newDF.index.tolist():
                val = self.__df2denorm.loc[j,i]/self.__df1denorm.loc[j,i]
                newDF.loc[j,i] = vals
        return(newDF)

class rateCalc:
    # this will extract the ratio of funds to number of awards.
    pass
