
// identify UTXOs

-> UTXOs() #gives txid and output index
## IMPLEMENTAION FOR ARBITRARY BLOCK - INPROGRESS - ONHOLD	
// choose amount and receiver pubkey

-> neededUTXO(amount)
   
-> make_inp()

-> pay(amount, to)

// transaction is now made, we broadcast

-> broadcast(tr)

// we listen to transaction
// [ISSUE] sometimes tx length exceeds, is it ok to inc recFrom?
## TESTING RECVFROM 2048 IN ACTUAL LAN -- ONHOLD

-> we check its signature, reject if invalid  
// we decrypt the signature, we check prev txn , output index.
// we use that amount, to check if outputs <= input
## TESTING FOR MULTIPLE VERIFY SIGNATURE -- DONE

## TESTING FOR ACTUAL TRANSACTION DATA IN MEMPOOL/ BLOCK -- DONE
## by verifying if input referenced exists in UTXO set

## REMOVE REFFERENCED PREV TRAN OUTPUT IF VALID FROM UTXO -- DONE

// then we update available UTXOs by removing ones we used as inp
// we update utxo.tmp if transaction. UTXOs.txt if block
// if UTXO isn't available, we reject.

## MAKE MAIN TO USE UTXO.tmp for available UTXO -- DONE
	#-> subtask clean output index reference bug -- DONE

## CLEAN MAIN -- okayish progress, IN HOLD

## UPDATE UTXO.tmp from received transactions --DONE
	#-> add mempool UTXOs to UTXO.tmp

## FIX NEGATIVE FEE AMOUNT BUG ON SPENDING LAST UTXO -- DONE

## DISPLAY BALANCE -- HOLD

## PRETTY PRINT EVERYWHERE -- DONE

## use multiple keys to test -- DONE

## MINING

## add coinbase txn -- DONE
##	-> add coinbase, with sum of fees, and current block reward -- DONE


sort desc by fees, THEN check valid ones and remove invalid ones.
from the valid ones that are sorted by fees, select X amount of txns to include
## Implement SORT Fee Approach -- DONE


## broadcast block once mined -- DONE

## MAIN_F update where it receives blocks -- DONE
##	-> validate -- DONE
##		-> merkleroot, block reward, sum of fees of txns -- DONE
##	-> uses transactions inside the block txns to update UTXOs.txt -- DONE
##	-> python reset to have UTXO.tmp use for mempool -- DONE
##	-> Replay tx input deletion of mempool in UTXO.tmp 
##		-> Show and disregard newly discovered invalid inputs
## CODE CLEANUP Import common functions from a py avoid duplicates - HOLD
      
## CHECK PLACES WHERE AMOUNT USED IS VALIDATED -- DONE
it's important to validate transactions such that input - output amount is positive
## VALIDATE AMOUNT USED IN validateTr -- DONE

## ADD BLOCK_HASH : STR( TXNS) IN BLOCKHEADERS.txt -- DONE

leave rest of unmined tx from mempool to be in mempool [MAINB]
## leave rest of unmined tx from mempool to be in mempool [MAIN_F] -- DONE
both these tasks are the same and this means that main_f should ALWAYS 
be acive even in miners as even if mempool and UTXO.tmp is updated when he's
mining, the mining process is unaffected
-> This is done by removing txn from mempool which has any txn from mined block
by comparing set of txids of mempool and mined block
if txid in mem:
   del mempool[txid] //potential solution


## STRESS TEST -- IN PROGRESS
## basic single node test - Done

## SEND current state of blockchain for nodes requesting it by -- HOLD
## sending blockHeaders.txt
## sending UTXOs.txt
## sending mempool.txt

-> start mining (miner.py)

// in script, we can choose arbitrary time to start mining.
// mining is done with current mempool.txt txs.

-> add coinbase, with sum of fees, and current block reward

-> mine with bruteforcing nonce, if ok send block data with coinbase

-> //mempool is limited in size, how many characters can I send?
   //tr tr ah we can send instead of in bulk. in case some
   //new node requests it.

## REVERT TO PAST FILE (EITHER UTXO.tmp or UTXOs.txt) from backup, if exception
have UTXOs.txt.b file, blockHeaders.txt.b file, at start of exception prone parts of code
REVERT once exception is found by copy pasting such that changes made are nullified

# CLEAN ECC DIRECTORY .PY FILES 
## EXPLAIN HANDLE MESSAGE ERRORS AND ALL EXCEPTIONS IN DOCS FOR KIDS
## VISUAL REPRESENTATION OF ALL METHODS AND FLOW IN DOCS
--------------------------------------------------------------------

intermediary steps/plans

// so.. I'm removing an UTXO after entering it to mempool
// then I get a block that has already added the tx.


// I have to add a mechanism to make permanent changes to
// UTXO.txt only after block is added.

-> UTXO.tmp

// when there's a block received. we deleteUTXO() in UTXO.txt
// if some input doesn't exist, we reject block

### BUGS
# MAIN.py shows balance where MAIN_F does not. -- in progress
	#UTXO.tmp has different block ID but same coinbase????
