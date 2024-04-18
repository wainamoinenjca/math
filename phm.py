import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

f = open("output.txt", 'w')
df = pd.DataFrame()
index = pd.Series(i for i in range(1, 1001))

def sumOfDigits(num, base):
    quot = 1
    rem = 0
    sum = 0

    while quot > 0:
        quot, rem = divmod(num, base)
        num = quot
        sum += rem

    return sum

def genSODSeries(base, multiplicand, iterations):
    #base is the number base results should be evaluated in (e.g. base = 8, 5*7=43 SoD(43)= 7)
    #multiplicand is the number whose multiples you want to query (e.g. mult. = 2 yields evens, mult = 17 -> 17, 34, 51...)
    results = [0]
    for i in range(1, iterations+1):
        results.append(sumOfDigits(i * multiplicand, base))
    
    return pd.Series(results) #, ignore_index = True

def genSODDifferenceSeries(series):
    results = []
    for i in range (1, len(series) - 1):
        results.append(series[i] - series[i + 1])
        
    return pd.Series(results)
    
def displayChart(base, multiplicand, iterations):
    s = genSODSeries(base, multiplicand, iterations)
    plt.title(f"{base=}, {multiplicand=}, {iterations=}")
    plt.plot(s)
    plt.show()
    
def displayDiffChart(series, b, m, i):
    plt.title(f"SoD Difference:{b=}, {m=}, {i=}")
    plt.plot(series)
    plt.show()

def displayMultiChart(bmTuples=[]):
#for now works expecting exactly four bmTuples
#which are of form [b,m,i], base, multiplicand, iterations, respectively.
    t1 = genSODSeries(bmTuples[0][0], bmTuples[0][1], bmTuples[0][2] )
    t2 = genSODSeries(bmTuples[1][0], bmTuples[1][1], bmTuples[1][2],)
    t3 = genSODSeries(bmTuples[2][0], bmTuples[2][1], bmTuples[2][2],)
    t4 = genSODSeries(bmTuples[3][0], bmTuples[3][1], bmTuples[3][2],)

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(t1)
    base = bmTuples[0][0]
    multiplicand = bmTuples[0][1]
    iterations = bmTuples[0][2]
    axs[0, 0].set_title(f"{base=}, {multiplicand=}, {iterations=}")

    axs[0, 1].plot(t2, 'tab:orange')
    base = bmTuples[1][0]
    multiplicand = bmTuples[1][1]
    iterations = bmTuples[1][2]
    axs[0, 1].set_title(f"{base=}, {multiplicand=}, {iterations=}")

    axs[1, 0].plot(t3, 'tab:green')
    base = bmTuples[2][0]
    multiplicand = bmTuples[2][1]
    iterations = bmTuples[2][2]
    axs[1, 0].set_title(f"{base=}, {multiplicand=}, {iterations=}")

    axs[1, 1].plot(t4, 'tab:red')
    base = bmTuples[3][0]
    multiplicand = bmTuples[3][1]
    iterations = bmTuples[3][2]
    axs[1, 1].set_title(f"{base=}, {multiplicand=}, {iterations=}")

    for ax in axs.flat:
        ax.set(xlabel='multiple', ylabel='SoD output')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
        
    plt.show()


#displayMultiChart([[10, 101, 10000],[8, 57, 10000],[100, 10001, 1000000],[16, 257, 100000]])
displayChart(10, 10, 100000) #play around with base = 10 until you get a feel for it and then start exploring, you'll 
                                #develop a sense for how to navigate the landscape pretty quickly
displayChart(10, 100, 100000) #play around with base = 10 until you get a feel for it and then start exploring, you'll 
displayChart(10, 10000, 10000000) #play around with base = 10 until you get a feel for it and then start exploring, you'll 

#s = genSODSeries(10, 101, 100000)

#sDiff = genSODDifferenceSeries(s)
#displayDiffChart(sDiff, 10, 101, 100000)
#results = []
#for base in range(2, 6):
#    for i in range(1, 1001):
#        for j in range(1, 1001):
#            results.append(sumOfDigits(i * j, base))
#        f.write(str(i) + str(results) + '\n')
#        df = df.append(pd.Series(results), ignore_index = True)
#        results.clear()

#    df.to_csv('base' + str(base) + '_output.txt')
#    df = df.iloc[0:0]

#print(df)

#testRead = pd.read_csv('../../Users/jcalumba/Desktop/math/output.txt', names=index)
#testRead.from_csv('base2_output.txt')
#print(testRead.head(10))
#print(testRead.iloc[[4]])
#testRead = testRead.iloc[1:].reset_index(drop=True) #supposed to drop the first row so the x and y dimensions match
#plt.plot(index, testRead.get(5))
#plt.show()
#Curta mechanical calculator
