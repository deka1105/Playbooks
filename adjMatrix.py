import pandas as pd
allCol = ['0A','1B','2C','3D','4E','5F','6G','7H','8I','9J','10K','12L','12M','13N']
sol = {
    0:[11,],
    1:[2,6,7,8,9,10,11],
    3:[6,7,8,9,10,11],
    4:[4,], 5:[11,], 7:[6,9],
    10:[11,], 12:[2,9,10,11]}
adj_matrix = pd.DataFrame()
adj_matrix['Row Names'] = allCol
def createAdj():
    global adj_matrix
    for i in range (0, len(allCol)-1):
        ls = []
        for j in allCol:
            ls.append('-')
        try:
            solList = sol[i]
            for j in solList:
                ls[j] = 'X'
        except:
            pass
        adj_matrix[allCol[i]] = ls

createAdj()        
adj_matrix
