import random
answer= str(random.randint(100,999)) #推測する数字をランダムに生成する #何番目の桁かがあとでほしいので文字列に変換した.
ans_list= list(answer) #答えを一桁づつに分割しておきたいので、リスト化する
ans_counter=[0]*10 #答えに含まれる数字と、その数を記録する.BITE数の判定に使う.
for element in ans_list: #実際にリストにそのデータを記録している.
    ans_counter[int(element)] += 1

def get_guess():
    while True:
        guess=input("３桁の数字(100-999)を入力してください") #推測する数字を入力させる.以下、フールプルーフ.
        try: #先に数値型判定をしないとintでエラーが出るので、例外処理を先に書く.
            num = int(guess)
        except ValueError:
             print("数字を入力してください.")
             continue
        if (num<100):   #数値であることが保証されたので、安全に大小関係が比較できる.
            print("数字が小さすぎます.")
            continue
        if (999<num):
            print("数字が大きすぎます.")
            continue
        break  #ここまでこれたらguessが確定する.
    gue_list= list(guess) #answerと同様の処理をする
    gue_counter=[0]*10 
    for element in gue_list:
        gue_counter[int(element)] += 1
    return num,gue_list,gue_counter
    
def count_HIT_BITE():
    num,gue_list,gue_counter=get_guess()
    a_c=[element for element in ans_counter]
    g_c=[element for element in gue_counter]  #このあと、これらのリストを書き換えるが、次の推測ではその書き換えは取り消さないと、BITEが判定できない.
    #HITを数える
    HIT=0
    for i in range(0,3):
        if gue_list[i]==ans_list[i]:
            HIT += 1
            a_c[int(gue_list[i])] -=1 #BITE数えるための操作
            g_c[int(gue_list[i])] -=1 #BITE数えるための操作
    #これでHIT数が記録できた.
    #次にBITE数を数える.BITEは、2つのcounter-listを比較することで数えられる.
    BITE=0
    for i in range(0,10):
        if a_c[i] != 0 and g_c[i] != 0:
            BITE += min(a_c[i],g_c[i])
    return HIT,BITE

def numeron():
    while True:
        HIT,BITE=count_HIT_BITE()
        print(HIT,"HIT,BITE",BITE,"です.")
        if HIT==3:
            print("3HITです.おめでとう!")
            break