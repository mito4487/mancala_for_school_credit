import evaluate
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
#ゲームの勝敗判定
def judge(mancala_seed,player_num):
    player=[0]*2
    if(player_num==0):
        enemy=1
    else:
        enemy=0
    for i in range(7):
        player[0]+=mancala_seed[i]
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
    PlayersPoints=player
    mancala_seeds[st]=0
    nextturn=False
    if (player==1):
        Rotate(mancala_seeds)
        
    for i in range(1,seeds):
        if(st+i>13):
            i=st+i-14
        mancala_seeds[st+i]+=1
    if(mancala_seeds[st+i]==1 and st+i!=0 and st+i!=7):#steeling
        mancala_seeds[PlayersPoints]+=mancala_seeds[face[st+i]]
        mancala_seeds[face[st+i]]=0
    elif(st+i==PlayersPoints):
        nextturn=True
        
    if (player==1):
        Rotate(mancala_seeds)
        
    return nextturn
    
#player2に番を渡す
def Rotate(mancala):
    tmp=[0]*7
    for i in range(7):
        tmp[i]=mancala[i]
    for i in range(7):
        mancala[i]=mancala[i+7]
        mancala[i+7]=tmp[i]        

with(mancala[1]==mancala[2]==mancala[3] ==mancala[4] ==mancala[5] ==mancala[6] ==0 or 
     mancala[8]==mancala[9]==mancala[10]==mancala[11]==mancala[12]==mancala[13]==0):
    
    #player1 turn
    copy=mancala
    hoge,start=evaluate.tree_selecting(copy,0,0,0,100000,-100000,0)
    SowingSeeds(0,start,mancala)
    
    #player2 turn
    copy=mancala
    hoge,start=evaluate.tree_selecting(copy,0,0,0,100000,-100000,1)
    SowingSeeds(1,start,mancala)
    
win=judge(mancala,0)
if(win==1):
    print("player1 win")
elif(win==0):
    print("draw")
else:
    print("player2 win")