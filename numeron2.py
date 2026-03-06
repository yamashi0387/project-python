import random

def get_digit(): #遊ぶ桁数を選ぶ関数.
    while True:
        try:
            digit=int(input("遊びたい桁数を半角数字で入力してください:"))
            if digit < 1:
                print("1以上の数字を入力してください")
                continue
            return digit
        except ValueError:
            print("数字を半角で入力してください")

def get_answer(digit):
    answer= str(random.randint(10**(digit-1),10**digit-1)) #推測する数字をランダムに生成する #何番目の桁かがあとでほしいので文字列に変換した.
    ans_list= list(answer) #答えを一桁づつに分割しておきたいので、リスト化する
    ans_counter=[0]*10 #答えに含まれる数字と、その数を記録する.BITE数の判定に使う.
    for element in ans_list: #実際にリストにそのデータを記録している.
        ans_counter[int(element)] += 1
    return ans_list,ans_counter

def get_guess(digit):
    while True:
        guess=input(f"{digit}桁の数字を半角で入力してください: ") #推測を入力させる.以下、フールプルーフの実装.
        try: #先に数値型判定をしないとintでエラーが出るので、例外処理を先に書く.
            num = int(guess)
        except ValueError:
             print("数字を入力してください.")
             continue
        if (num<10**(digit-1)):   #数値であることが保証されたので、安全に大小関係が比較できる.
            print("数字が小さすぎます.")
            continue
        if (10**digit-1<num):
            print("数字が大きすぎます.")
            continue
        break  #ここまでこれたらguessが確定する.
    gue_list= list(guess) #answerと同様の処理をする
    gue_counter=[0]*10 
    for element in gue_list:
        gue_counter[int(element)] += 1
    return gue_list,gue_counter
    
def count_HIT_BITE(digit,ans_list,ans_counter,gue_list,gue_counter): 
    copy_of_ans=[element for element in ans_counter]
    copy_of_gue=[element for element in gue_counter]  #このあと、これらのリストを書き換えるが、次の推測ではその書き換えは取り消さないと、BITEが判定できない.
    #HITを数える
    HIT=0
    for i in range(0,digit):
        if gue_list[i]==ans_list[i]:
            HIT += 1
            copy_of_ans[int(gue_list[i])] -=1 #BITE数えるための操作 #HITで使われた数値を取り除いてる.
            copy_of_gue[int(gue_list[i])] -=1 #BITE数えるための操作
    #これでHIT数が記録できた.
    #次にBITE数を数える.BITEは、2つのcounter-listを比較することで数えられる.
    BITE=0
    for i in range(0,10):
        if copy_of_ans[i] != 0 and copy_of_gue[i] != 0:
            BITE += min(copy_of_ans[i],copy_of_gue[i])
    return HIT,BITE

def numeron():
    digit=get_digit()
    ans_list,ans_counter=get_answer(digit) #答えを生成する.
    while True:
        gue_list,gue_counter=get_guess(digit)
        HIT,BITE=count_HIT_BITE(digit,ans_list,ans_counter,gue_list,gue_counter)
        if HIT==digit:
            break
        print(f"{HIT}HIT,{BITE} BITEです.")
    print(f"{digit}HITです.おめでとう!")
numeron()