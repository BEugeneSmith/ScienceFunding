import pandas as pd

# import all of the datasets
awards2010 = pd.read_csv('Data/exportAwards-2010.csv')
awards2011 = pd.read_csv('Data/exportAwards-2011.csv')
awards2012 = pd.read_csv('Data/exportAwards-2012.csv')
awards2013 = pd.read_csv('Data/exportAwards-2013.csv')
awards2014 = pd.read_csv('Data/exportAwards-2014.csv')

def awardTrim(df,year):
    # makes subset of data frame and adds column for year
    terms = ['Doing Business as Name','Estimated Total Award Amount','Primary State','Abstract at Time of Award']
    df = df[terms]

    l = []
    for i in range(len(df)):
        l.append(str(year))
    df['Year'] = l

    return df

#trim the csvs
awards2010 = awardTrim(awards2010,2010).dropna()
awards2011 = awardTrim(awards2011,2011).dropna()
awards2012 = awardTrim(awards2012,2012).dropna()
awards2013 = awardTrim(awards2013,2013).dropna()
awards2014 = awardTrim(awards2014,2014).dropna()

#export the csvs
awards2010.to_csv('awards2010.csv',index=False)
awards2011.to_csv('awards2011.csv',index=False)
awards2012.to_csv('awards2012.csv',index=False)
awards2013.to_csv('awards2013.csv',index=False)
awards2014.to_csv('awards2014.csv',index=False)

#combine and export an aggregate of the data
allAwards = pd.concat([awards2010,awards2011,awards2012,awards2013,awards2014])
allAwards.to_csv('allAwards.csv',index=False)
