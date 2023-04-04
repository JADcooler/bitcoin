def deleteTxOutputs(txid, on):
        file = 'UTXO/UTXO.tmp'
        #by giving a txn, we remove an output from it as UTXO

        print("DELETING ",txid, " OUTPUT ", on)

        with open(file, 'r') as f:
                blocks = ast.literal_eval(f.read())

        blockF = ''
        for block in blocks:
                txns = blocks[block]
                txns = ast.literal_eval(txns)
                if( txid in txns):
                        blockF = block
                        break
        if(blockF == ''):
                print("NO BLOCK HAS REQUIRED TX")
                return False

        txns = ast.literal_eval(blocks[blockF])
        txn = ast.literal_eval(txns[txid])

        toPop = -1
        outputs = txn['outputs']
        for i in range(len(outputs)):
                if(outputs[i] is not None and outputs[i]['output_no']==on):
                        toPop = i
                        break
        if(toPop == -1):
                print("TXN DOES NOT HAVE REQUIRED OUTPUT INDEX")
                return False
        #we are now about to modify txns string in block dict


        modifyThis = blocks[blockF] #later used as l value
        modifyTxns = ast.literal_eval(modifyThis) #later as l value
        modifyTxn =ast.literal_eval( modifyTxns[txid]) #later uesd as l value


        modifyTxn['outputs'][toPop] = None

        modifyTxns[txid] = str(modifyTxn)
        blocks[blockF] = str(modifyTxns)

        with open(file, 'w') as f:
                f.write(str(blocks))

        print("SUCCESFULLY REMOVED OUTPUT",on," FROM",txid)
        return True


def handleError(args):
	if(args[0]  == (-1,-1)):
		print("[FATAL ERROR] INVALID OUTPUT INDEX REFERENCED, DOESN'T EXIST OR HAS BEEN USED \n\n")
		return False
	elif(args[0] == (-1,-2)):
		print("[FATAL ERROR] INPUT TXN AND OUTPUT INDEX DON'T EXIST IN UTXO SET")
		return False
	return True
