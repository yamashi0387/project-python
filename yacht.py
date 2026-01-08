import random
role=["エース","デュース","トレイ","フォー","ファイブ","シックス","チョイス","フォーダイス","フルハウス","S.ストレート","B.ストレート","ヨット"]
your_role=[" "," "," "," "," "," "," "," "," "," "," "," "]

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
        w=input("振り直したいサイコロを入力してください")
        i=1
        while i<=5:
            if  f"x_{i}" in w:
                y[i-1]=random.randint(1,6)
            i=i+1
        print(y)
        j=j+1        
    return y

def decide_role(result):

    #同じ役は一度のみ使用可能にする
    #役の入力ミス対策
    while True:
      w=input("役を入力してください")
      k=0
      p=False
      while k<=11:
        if w==role[k] and your_role[k]!=" ":
            print("その役は使用済みです")
            p=True
        k=k+1
      if p==True:
        continue    
      if not (w in role):
        print("役の名前が誤っています")
        continue
      break

    #点数計算
    if w=="エース":
        n=result.count(1)
        your_role[0]=n*1
       

    if w=="デュース":
        n=result.count(2)
        your_role[1]=n*2

    if w=="トレイ":
        n=result.count(3)
        your_role[2]=n*3

    if w=="フォー":
        n=result.count(4)
        your_role[3]=n*4
        print(your_role)

    if w=="ファイブ":
        n=result.count(5)
        your_role[4]=n*5

    if w=="シックス":
        n=result.count(6)
        your_role[5]=n*6

    if w=="チョイス":
        sum_choice=sum(result)
        your_role[6]=sum_choice

    if w=="フォーダイス":
        c_four=[result.count(i) for i in range(1,7)]
        if max(c_four) >=4:
          sum_fourdice=sum(result)
          your_role[7]=sum_fourdice
        else:
            your_role[7]=0

    if w=="フルハウス":
       c_full=[result.count(i) for i in range(1,7)]
       if all(c_full_element==0 or c_full_element >=2 for c_full_element in c_full):
             sum_full=sum(result)
             your_role[8]=sum_full
       else:
           your_role[8]=0

    if w=="S.ストレート":
        c_S=[result.count(i) for i in range(1,7)]
        if (all(c_S[i] >=1 for i in range(0,4)) or all(c_S[i] >=1 for i in range(1,5)) or all(c_S[i] >=1 for i in range(2,6))):
            your_role[9]=15
        else:
            your_role[9]=0
    if w=="B.ストレート":
        c_B= [result.count(i) for i in range(1,7)]
        if (all(c_B[i] >=1 for i in range(0,5)) or all(c_B[i] >=1 for i in range(1,6))):
            your_role[10]=30
        else:
            your_role[10]=0

    if w=="ヨット":
      c_yacht=[result.count(i) for i in range(1,7)]
      if max(c_yacht)==5:
          your_role[11]=50
      else:
        your_role[11]=0       
    print(your_role)
    return your_role

#ヨット関数の定義
def yacht():
  i=0
  while i<=11:
      i=i+1
      z=resaikoro()
      decide_role(z)
  total_point=sum(your_role)
  if sum(your_role[i] for i in range(0,6))>=63:
    total_point +=35
  return total_point

yacht()
