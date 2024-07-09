import main

keisuu=10#勝敗が決まったときの評価値の重み
ban={1:0,0:1}
def evaluate(mancala_seeds):
    return mancala_seeds[0]

def tree_selecting(mancala_seeds,startingPosition,firstselect,nowdepth,turn,alpha,beta):
    nowdepth+=1
    if(nowdepth==main.depth):
        return evaluate(mancala_seeds),firstselect
    if(mancala_seeds[1]==mancala_seeds[2]==mancala_seeds[3] ==mancala_seeds[4] ==mancala_seeds[5] ==mancala_seeds[6] ==0 or 
     mancala_seeds[8]==mancala_seeds[9]==mancala_seeds[10]==mancala_seeds[11]==mancala_seeds[12]==mancala_seeds[13]==0):
        return main.judge(mancala_seeds,turn)*keisuu,firstselect
    
    for i in range(6):
        if(nowdepth==1):
            firstselect=i
        now_mancala_seeds=mancala_seeds
        nextturn=main.SowingSeeds(turn,startingPosition,now_mancala_seeds)
        if(nextturn):
            score,hoge=-tree_selecting(now_mancala_seeds,i,firstselect,nowdepth,turn,alpha,beta)
        else:
            turn=ban[turn]
            score,hoge=-tree_selecting(now_mancala_seeds,i,firstselect,nowdepth,turn,alpha=-beta,beta=-alpha)
        if(score>alpha):
            alpha=score
    
    if(alpha >= beta):
            return alpha,firstselect

    return alpha,firstselect
    