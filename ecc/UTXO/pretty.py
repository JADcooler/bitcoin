import ast
from pprint import pprint
import sys


def func(file):
    dic = {}
    choice = 0
    if(file == "UTXO.tmp"):
        choice = 1


    if(choice== '1'):
        print("\033[1;31m PRINTING UTXO.tmp \033[1;\n")
    else:
        print("\033[1;31m PRINTING UTXOs.txt \033[1;\n")

    with open(file) as f:
        w = f.read()

    w = ast.literal_eval(w)

    for block in w:        

        dic[block] = []

        print("\033[1;35mNOW ANALYSING BLOCK ",end='')
        print("\033[3;33m",block, "\033[0;\\")
                
        txns = ast.literal_eval(w[block])
        print("no of transactions ", len(txns))
        for tx in txns:
            print("\033[1;33m txid:\033[1;\033[0;37m;",tx,"\033[0;\\")
            dic[block].append(tx)

        print()
    return dic


## DIFF SECTION 


def seqw(t, s):
    blockDiff = set(t.keys()) - set(s.keys()) #since UTXO.tmp should always be derived from UTXOs.txt
    #we should expect that they always haev the same block.
    #in case they do not, UTXO.tmp might not have updated properly

    t1 = []
    [t1.extend(t[txns]) for txns in t]

    t2 = []    
    [t2.extend(s[txns]) for txns in s]

    TXDiff = set(t1) - set(t2)

    print("BLOCK DIFF ",blockDiff)
    print("TX DIFF ",TXDiff)
    

#print(t1,t2)

#We fully expect every tx in UTXOs.txt to be part of UTXO.tmp
#We just check the tx in mempool through this (unvalidated txs)

tmp = func('UTXO.tmp') #tmp for temporary
per = func('UTXOs.txt') #per for permenant

print("------------------------------------------\n\n")
print("WHAT UTXOs.txt has that UTXO.tmp does not")
seqw(per, tmp)

print("\n\nWHAT UTXOs.tmp has that UTXOs.txt does not")
seqw(tmp, per)
