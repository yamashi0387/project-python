import random

def saikoro( ):
    x_1=random.randint(1,6)
    x_2=random.randint(1,6)
    x_3=random.randint(1,6)
    x_4=random.randint(1,6)
    x_5=random.randint(1,6)
    return list((x_1,x_2,x_3,x_4,x_5))

def resaikoro():
    y=saikoro()
    print(y)
    j=1
    while j<=2:
        print("左から1,4,5番目のサイコロを振り直したければ1 4 5のように半角スペース区切りで半角数字を入力してください")
        reroll=input("振り直したいサイコロを入力してください")
        p=False
        while True:
            if reroll == "": #振り直さないなら即break
                p=True
                break
            reroll_list=reroll.split()
            try:
                reroll_int = [int(x) for x in reroll_list] #入力値をリスト化
            except ValueError: #数字以外が入力されたときの例外処理
                print("数字で入力してください")
                reroll=input("振り直したいサイコロを入力してください")
                continue
            if (max(reroll_int)>=6 or min(reroll_int)<=0): #入力された数値が1-5でないときの対処
                print("数値が大きすぎるか小さすぎます")
                reroll=input("振り直したいサイコロを入力してください")
                continue
            break
        if p == True:
            break      
        for element in set(reroll_int): #setにしているのは、1 1 2と入力されたようなときに、1が2回振り直されないようにするため.
            y[element-1]=random.randint(1,6)
        print(y)
        j=j+1        
    return y

def decide_role(result,player_num): 
    now_player_role=player_role[player_num]
    #同じ役は一度のみ使用可能にする
    #役の入力ミス対策
    while True:
      w=input("役を入力してください")
      k=0
      p=False
      if not (w in role):
        print("役の名前が誤っています")
        continue
      while k<=11:
        if w==role[k] and now_player_role[k]!=" ":
            print("その役は使用済みです")
            p=True
        k=k+1
      if p==True:
          continue    
      break

    #点数計算
    if w=="エース":
        n=result.count(1)
        now_player_role[0]=n*1
       

    elif w=="デュース":
        n=result.count(2)
        now_player_role[1]=n*2

    elif w=="トレイ":
        n=result.count(3)
        now_player_role[2]=n*3

    elif w=="フォー":
        n=result.count(4)
        now_player_role[3]=n*4

    elif w=="ファイブ":
        n=result.count(5)
        now_player_role[4]=n*5

    elif w=="シックス":
        n=result.count(6)
        now_player_role[5]=n*6

    elif w=="チョイス":
        sum_choice=sum(result)
        now_player_role[6]=sum_choice

    elif w=="フォーダイス":
        c_four=[result.count(i) for i in range(1,7)] #各目がいくつ出ているかを数えるリスト
        if max(c_four) >=4: #全て同じ目でも成立する条件にする
          sum_fourdice=sum(result)
          now_player_role[7]=sum_fourdice
        else:
            now_player_role[7]=0 #役が不成立なら０点

    elif w=="フルハウス":
       c_full=[result.count(i) for i in range(1,7)] #各目がいくつ出ているかを数えるリスト
       if all(c_full_element==0 or c_full_element >=2 for c_full_element in c_full): #５個全て同じ目でも成立する条件にする
             sum_full=sum(result)
             now_player_role[8]=sum_full
       else:
           now_player_role[8]=0 #役が不成立なら０点

    elif w=="S.ストレート":
        c_S=[result.count(i) for i in range(1,7)] #各目がいくつ出ているかを数えるリスト
        if (all(c_S[i] >=1 for i in range(0,4)) or all(c_S[i] >=1 for i in range(1,5)) or all(c_S[i] >=1 for i in range(2,6))): #1,2,3,4がでるか2,3,4,5がでるか、3,4,5,6がでるかの３パターン
            now_player_role[9]=15
        else:
            now_player_role[9]=0 #役が不成立なら０点
    elif w=="B.ストレート":
        c_B= [result.count(i) for i in range(1,7)] #各目がいくつ出ているかを数えるリスト
        if (all(c_B[i] >=1 for i in range(0,5)) or all(c_B[i] >=1 for i in range(1,6))): #1,2,3,4,5か2,3,4,5,6の２パターン
            now_player_role[10]=30
        else:
            now_player_role[10]=0 #役が不成立なら０点

    elif w=="ヨット":
      c_yacht=[result.count(i) for i in range(1,7)] #各目がいくつ出ているかを数えるリスト
      if max(c_yacht)==5:
          now_player_role[11]=50
      else:
        now_player_role[11]=0       
    print(now_player_role)
    return now_player_role


role=["エース","デュース","トレイ","フォー","ファイブ","シックス","チョイス","フォーダイス","フルハウス","S.ストレート","B.ストレート","ヨット"]
player1_role=[" "," "," "," "," "," "," "," "," "," "," "," "]
player2_role=[" "," "," "," "," "," "," "," "," "," "," "," "]
player_role=[player1_role,player2_role]

def vs_yacht():
    for i in range (0,12):
        for j in range(0,2):
            print(f"player{j+1}の番です")
            print(player_role[j])
            z=resaikoro()
            decide_role(z,j)
    total_point_1=sum(player1_role)
    total_point_2=sum(player2_role)
    if sum(player1_role[i] for i in range(0,6))>=63:
        total_point_1 +=35
    if sum(player2_role[i] for i in range(0,6))>=63:
        total_point_2 +=35
    print(f"Player1の点数は、{total_point_1}です")
    print(f"Player2の点数は、{total_point_2}です")
    if total_point_2 < total_point_1:
        print("player1の勝ち!")
    
    elif total_point_1 < total_point_2:
        print("player2の勝ち!")
    
    else:
        print("引き分け!")
    for i in range (0,12):
        player1_role[i]=" "#次のゲームのために初期化する
        player2_role[i]=" "

vs_yacht()