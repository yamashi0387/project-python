import random
a=str(random.randint(100,1000))
answer=list(a)

def num_guess_HIT_BITE():
    b=str(input("3桁の数字を入力してください"))
    guess=list(b)
    j=0
    HIT=0
    while j<=2:
      if guess[j]==answer[j]:
          HIT += 1
      j=j+1
    print(HIT,"HIT")
    if HIT==3:
      return 3
    i=0
    #通常のバイト
    if ((guess[0] ==  answer[1] or guess[0] == answer[2]) and (guess[0] != answer[0])):
        i=i+1
    if ((guess[1] ==  answer[0] or guess[1] == answer[2]) and (guess[1] != answer[1])):
       i=i+1
    if ((guess[2] ==  answer[0] or guess[2] == answer[1]) and (guess[2] != answer[2])):
       i=i+1
    #答えが123で推測が114のとき,1HIT1BITEにならないように調整する.
    if (guess[0]==answer[0] and guess[1]!= answer[1] and guess[1]==answer[0] and guess[1] != answer[2]):
       i=i-1
    if (guess[0]==answer[0] and guess[2]!= answer[2] and guess[2]==answer[0] and guess[2] != answer[1]):
       i=i-1
    if (guess[1]==answer[1] and guess[0]!= answer[0] and guess[0]==answer[1] and guess[0] != answer[2]):
       i=i-1
    if (guess[1]==answer[1] and guess[2]!= answer[2] and guess[2]==answer[1] and guess[2] != answer[0]):
       i=i-1
    if (guess[2]==answer[2] and guess[0]!= answer[0] and guess[0]==answer[2] and guess[1] != answer[1]):
       i=i-1
    if (guess[2]==answer[2] and guess[1]!= answer[1] and guess[1]==answer[2] and guess[2] != answer[0]):
       i=i-1  
    #答えが121推測が111のとき,2HIT1BITEにならないように調整する.
    if (guess[0]==answer[0] and guess[1]!= answer[1] and guess[1]==answer[0] and guess[1] == answer[2] and guess[2]==answer[2]):
      i=i-1 
    if (guess[0]==answer[0] and guess[2]!= answer[2] and guess[2]==answer[0] and guess[2] == answer[1] and guess[1]==answer[1]):
      i=i-1
    if (guess[1]==answer[1] and guess[0]!= answer[0] and guess[0]==answer[1] and guess[0] == answer[2] and guess[2]==answer[2]):
      i=i-1
    #答えが320で推測が133のとき,0HIT2BITEにならないように調整する.
    if (guess[0]!=answer[0] and guess[1]==guess[2] and guess[1]!=answer[1] and guess[2]!=answer[2]):
      i=i-1
    if (guess[1]!=answer[1] and guess[0]==guess[2] and guess[0]!=answer[0] and guess[2]!=answer[2]):
      i=i-1
    if (guess[2]!=answer[2] and guess[0]==guess[1] and guess[0]!=answer[0] and guess[1]!=answer[1]):
      i=i-1
    
    print(i,"BITE")


def numeron():
    while True:
        result = num_guess_HIT_BITE()
        if result == 3:
            break

numeron()