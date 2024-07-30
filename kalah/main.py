#import evaluate
#import sys
#import threading

#sys.setrecursionlimit(67108864)
#　2^20のstackメモリを確保
#threading.stack_size(1024*1024)
mancala=[0,4,4,4,4,4,4,0,4,4,4,4,4,4]
face={1:13,2:12,3:11,4:10,5:9,6:8,13:1,12:2,11:3,10:4,9:5,8:6}
depth=5

"""
start seed
  4  4  4  4  4  4
0                  0
  4  4  4  4  4  4
 
index 
  1  2  3  4  5  6  
0                  7
  13 12 11 10 9  8      
"""
#end
def end(mancala_seeds):
    end_f=False
    for i in range(1,7):
        if(mancala_seeds[i]!=0):
            end_f=True
    if(end_f):
        return end_f
    end_f=False
    for i in range(8,14):
        if(mancala_seeds[i]!=0):
            end_f=True       
    if(end_f):
        return end_f
    return end_f
#ゲームの勝敗判定
def judge(mancala_seed,player_num):
    player=[0]*2
    if(player_num==0):
        enemy=1
    else:
        enemy=0
    for i in range(1,8):
        player[0]+=mancala_seed[i]
        if(i+7==14):
            i=-7
        player[1]+=mancala_seed[i+7]
    if(player[player_num]>player[enemy]):
        return 1
    elif(player[player_num]<player[enemy]):
        return -1
    else:
        return 0


#種まき操作関数
#次の番が自分のときTrueを返す    
#player: 1 or 2
def SowingSeeds(player,startposition,mancala_seeds):
    st=startposition
    seeds=mancala_seeds[st]
    PlayersPoints=abs((player-1)*7)
    mancala_seeds[st]=0
    nextturn=False
    #if (player==1):
    #    Rotate(mancala_seeds)
        
    for i in range(1,seeds+1):
        if(st+i>13):
            i=i-14
        mancala_seeds[st+i]+=1
    if(st+seeds>13):
            seeds=seeds-14
    if(mancala_seeds[st+seeds]==1 and st+seeds>0 and st+seeds<7 and st+seeds!=7):#steeling
        
        mancala_seeds[PlayersPoints]+=mancala_seeds[face[st+seeds]]
        mancala_seeds[face[st+seeds]]=0
    elif(st+seeds==7):
        nextturn=True
        
    #if (player==1):
    #    Rotate(mancala_seeds)
        
    return nextturn
    
#player2に番を渡す
def Rotate(mancala_seeds):
    tmp=[0]*7
    for i in range(7):
        tmp[i]=mancala_seeds[i]
    for i in range(7):
        mancala_seeds[i]=mancala_seeds[i+7]
        mancala_seeds[i+7]=tmp[i]        


keisuu=10#勝敗が決まったときの評価値の重み
ban={1:0,0:1}
def evaluate_1(mancala_seeds):
    eva=mancala_seeds[0]-mancala_seeds[7]+(mancala_seeds[1]+mancala_seeds[2]+mancala_seeds[3]+mancala_seeds[4]+mancala_seeds[5]+mancala_seeds[6]-mancala_seeds[10]-mancala_seeds[11]-mancala_seeds[9]-mancala_seeds[8]-mancala_seeds[12]-mancala_seeds[13])
    return eva

def evaluate_2(mancala_seeds):
    eva=mancala_seeds[0]-mancala_seeds[7]-(mancala_seeds[1]+mancala_seeds[2]+mancala_seeds[3]+mancala_seeds[4]+mancala_seeds[5]+mancala_seeds[6]-mancala_seeds[10]-mancala_seeds[11]-mancala_seeds[9]-mancala_seeds[8]-mancala_seeds[12]-mancala_seeds[13])
    return eva

def tree_selecting(mancala_seeds,startingPosition,nowdepth,turn,player,alpha,beta):
    nowdepth+=1
    endf=not((mancala[1]==0 and mancala[2]==0 and mancala[3]==0 and mancala[4]==0 and mancala[5]==0 and mancala[6]==0) or (mancala[8]==0 and mancala[9]==0 and mancala[10]==0 and mancala[11]==0 and mancala[12]==0 and mancala[13]==0))
    
    if(nowdepth==depth):
        if(player):
            return evaluate_1(mancala_seeds)
        else:
            return evaluate_2(mancala_seeds)
    if(not endf):
        return judge(mancala_seeds,turn)*keisuu
    
    for i in range(1,6):
        if(mancala_seeds[i]!=0):
            now_mancala_seeds=mancala_seeds[:]
        #連続して番を取れるか判定
            nextturn=SowingSeeds(turn,startingPosition,now_mancala_seeds)
            if(nextturn):
                score=tree_selecting(now_mancala_seeds,i,nowdepth-1,turn,player,alpha,beta)
            else:
                turn=ban[turn]
                Rotate(now_mancala_seeds)
                score=-tree_selecting(now_mancala_seeds,i,nowdepth,turn,player,alpha=-beta,beta=-alpha)
            if(score>alpha):
                alpha=score
    
    if(alpha >= beta):
            return alpha

    return alpha
    



endf=True
#print(sys.getrecursionlimit())
while(endf):
    #player1 turn
    copy=mancala[:]
    print(copy)
    for i in range(1,7):
        if(copy[i]!=0):
            non_pass=i
            break
    score=tree_selecting(copy,non_pass,0,0,True,0,100000)
    start=non_pass
    non_pass+=1
    for i in range(non_pass,7):
        if(copy[i]!=0):
            hiscore=tree_selecting(copy,i,0,0,True,0,100000)
            #print(copy)
            if(score<hiscore):
                score=hiscore
                start=i    
    SowingSeeds(0,start,mancala)
    print("  "+str(mancala[1])+"  "+str(mancala[2])+"  "+str(mancala[3])+"  "+str(mancala[4])+"  "+str(mancala[5])+"  "+str(mancala[6])+"\n"
          +str(mancala[0])+"         st"+str(start)+"         "+str(mancala[7])+"       *1\n"
          +"  "+str(mancala[13])+"  "+str(mancala[12])+"  "+str(mancala[11])+"  "+str(mancala[10])+"  "+str(mancala[9])+"  "+str(mancala[8])+"\n\n")
    
    Rotate(mancala)
    endf=not((mancala[1]==0 and mancala[2]==0 and mancala[3]==0 and mancala[4]==0 and mancala[5]==0 and mancala[6]==0) or (mancala[8]==0 and mancala[9]==0 and mancala[10]==0 and mancala[11]==0 and mancala[12]==0 and mancala[13]==0))
    
    if (not endf):
        Rotate(mancala)
        break
    #player2 turn
    copy=mancala[:]
    score=tree_selecting(copy,1,0,1,False,0,100000)
    start=1
    for i in range(1,7):
        if(copy[i]!=0):
            non_pass=i
            break
    score=tree_selecting(copy,non_pass,0,0,True,0,100000)
    start=non_pass
    non_pass+=1
    for i in range(non_pass,7):
        if(copy!=0):
            hiscore=tree_selecting(copy,i,0,1,False,0,100000)
            if(score<hiscore):
                score=hiscore
                start=i    
    SowingSeeds(0,start,mancala)
    Rotate(mancala)
    endf=not((mancala[1]==0 and mancala[2]==0 and mancala[3]==0 and mancala[4]==0 and mancala[5]==0 and mancala[6]==0) or (mancala[8]==0 and mancala[9]==0 and mancala[10]==0 and mancala[11]==0 and mancala[12]==0 and mancala[13]==0))
    
    print("  "+str(mancala[1])+"  "+str(mancala[2])+"  "+str(mancala[3])+"  "+str(mancala[4])+"  "+str(mancala[5])+"  "+str(mancala[6])+"\n"
          +str(mancala[0])+"        st"+str(start)+"           "+str(mancala[7])+"     *2\n"
          +"  "+str(mancala[13])+"  "+str(mancala[12])+"  "+str(mancala[11])+"  "+str(mancala[10])+"  "+str(mancala[9])+"  "+str(mancala[8])+"\n\n")
    
win=judge(mancala,0)
if(win==1):
    print("player1 win")
elif(win==0):
    print("draw")
else:
    print("player2 win")