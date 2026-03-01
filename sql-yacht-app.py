import streamlit as st
import random
import pandas as pd

from supabase import create_client #supbaseにアクセスするための窓口

url = st.secrets["SUPABASE_URL"]#プロジェクトのURL
key = st.secrets["SUPABASE_KEY"]#DBに接続するためのキー
supabase = create_client(url, key)

def save_score(score: int): #点数を保存する関数
    supabase.table("scores").insert({"score": score}).execute() #scoresというテーブルのscoreというカラムにデータを保存する.idとcreated_at(他のカラム)は自動的に埋まる.execute()でDBの変更を実行する

def get_top5():
    data = supabase.table("scores").select("score").order("score", desc=True).limit(5).execute() #scoresというテーブルからscoreというカラムをscoreが大きい順(降順)にtop5を要求する.
    return data.data #data自体は複数の要素からなり、表はdataの中のdataという要素にある.

#役の成立判定と、点数の配分を定義する.
def get_scores(dice): #サイコロを受け取って点数を決める.
    scores={} #辞書に役と点数を記録する.
    counts = [dice.count(i) for i in range(1,7)] #サイコロの出目をリストで受け取り、各目が何個ずつ出ているかを保持する.
    #以下、辞書の作成
    scores["エース"]=counts[0]*1
    scores["デュース"]=counts[1]*2
    scores["トレイ"]=counts[2]*3
    scores["フォー"]=counts[3]*4
    scores["ファイブ"]=counts[4]*5
    scores["シックス"]=counts[5]*6
    scores["チョイス"]=sum(dice)
    scores["フォーダイス"]=sum(dice) if max(counts) >= 4 else 0
    scores["フルハウス"]=sum(dice) if not (1 in counts) else 0
    scores["S.ストレート"]=15 if (all(counts[i] >= 1 for i in range(0, 4)) or all(counts[i] >= 1 for i in range(1, 5)) or all(counts[i] >= 1 for i in range(2, 6))) else 0
    scores["B.ストレート"]=30 if (all(counts[i] >= 1 for i in range(0, 5)) or all(counts[i] >= 1 for i in range(1, 6))) else 0
    scores["ヨット"]=50 if max(counts)==5 else 0

    return scores

#ゲームの初期状態の定義
if 'total_score' not in st.session_state: #記憶させたいことを用意できるのがsession_state.
    st.session_state.total_score = 0 #scoreがサイコロを振るたびに0にされたら困る.
    st.session_state.turn = 0 #1ゲーム12ターンなのでターンも毎回1ターン目にされたら困る.
    st.session_state.roles=["エース","デュース","トレイ","フォー","ファイブ","シックス","チョイス","フォーダイス","フルハウス","S.ストレート","B.ストレート","ヨット"] #役は一度使用したら使えないので、使ったらここから消していく.
    st.session_state.bonusscore = 0 #ボーナススコアの条件判定に使う
    st.session_state.bonusstatus = False #ボーナススコア
    st.session_state.score_saved = False #スコアが一度だけ保存されるようにする.

st.title("🎲 ヨットで遊ぼう") #タイトル

if 'current_dice' in st.session_state: #タイトル画面では非表示にする
    st.title(f"🎲 Turn {st.session_state.turn}/12") #turn数の表示.

if 'current_dice' in st.session_state:
    st.write(f"### 現在の合計点: {st.session_state.total_score}") #合計点の表示.###はh3みたいなもの.
    if not st.session_state.bonusstatus :
        st.write(f" (ボーナススコア獲得まで{63-st.session_state.bonusscore}点)")
    else:
        st.write("(ボーナススコア獲得🎉)")

if st.session_state.turn == 0:
    st.write("### ランキングtop5")
    top5 = get_top5()
    if top5: 
        for i, row in enumerate(top5, start=1): #ランキング作成
                st.write(f"{i}位: {row['score']}点")
    else:
        st.write("まだスコアが登録されていません。")

if st.session_state.roles:
    if 'current_dice' not in st.session_state: #サイコロが生成されていないときにはこの画面を表示
        if st.button("サイコロを振る"): #ボタンを設置して、ボタンが押されるとサイコロが振られる.
            st.session_state.turn += 1
            st.session_state.current_dice = [random.randint(1,6) for _ in range(5)] #サイコロをランダムで生成する.
            st.session_state.roll_count=0 #サイコロがリセットされたら振り直しの回数もリセット.
            st.rerun()

    if 'current_dice' in st.session_state: #サイコロが生成されているときにはこの画面を表示
        dice=st.session_state.current_dice
        dice_icons = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"} #数字で表示するよりサイコロで表示したいので、数字と絵文字を対応させて、絵文字を画面に表示させる.
        icons = [dice_icons[d] for d in dice] #出目をアイコンに変換する.
        st.write(f"# {' '.join(icons)}") #現在のサイコロを表示.' 'join()で、リストの中身を半角空きで並べる.

        st.write("振り直さないサイコロにチェックを入れてください")

        cols=st.columns(5) #5k個に分割
        keeps = [] #振り直さないサイコロを選ぶ.
        for i in range(5):
            with cols[i]: #分割した各々の設定
                st.write(f"# {dice_icons[dice[i]]}") #サイコロの目を表示
                keep = st.checkbox("Keep", key=f"keep_{i}") #keyはcheckboxの名前と理解している.名前をつけておくと、rerunしたときにsession_stateのように、状態が保持できる.つまり、2回目の振り直しのときに、さきほど保持したサイコロは自動的にチェックが付く
                keeps.append(keep) #keep_{i}がtrueかfalseかをリストとして管理している.

        st.divider() #真ん中に水平線引く

        col1, col2=st.columns(2) #2つに分割(サイコロの振り直しと、役の確定の2つを左右に表示)

        with col1: #振り直す操作を定義
            st.write("### 1.振り直す")
            if st.session_state.roll_count <2 : #振り直しは2回まで.回数は st.session_state.roll_countで管理している.
                if st.button(f"### 振り直す(残り{2-st.session_state.roll_count}回)"): #振り直すボタン
                    for i in range(5):
                        if not keeps[i]: #keepされてないもののみ振り直す.keeps[i]がfalseなら実行されるということ.
                            st.session_state.current_dice[i]=random.randint(1,6) #再生成
                    st.session_state.roll_count += 1 #振り直しをカウント
                    st.rerun()

            else: #振り直せないときはこのボタンを出す.押せないボタン.
                st.write("振り直しはもうできません")
        
        with col2: #振り直しが済んだら、これでどの役を使うか決める.
            st.write("### 2.確定する")
            scores=get_scores(dice) #各役を選んだときのスコアを計算させる.
            selected_role = st.selectbox("どの役にしますか？", st.session_state.roles) #役を選ぶ.

            if st.button("この役で確定する"): #選んだ役で確定させる.
                st.session_state.total_score += scores[selected_role] #選んだ役のスコアを足す
                st.session_state.roles.remove(selected_role) #選んだ役を次のターンからは選べないようにする.
            
                if selected_role in ["エース","デュース","トレイ","フォー","ファイブ","シックス"] :
                    st.session_state.bonusscore += scores[selected_role]
                
                if st.session_state.bonusscore >= 63 and st.session_state.bonusstatus==False: #一度しかボーナスが足されないように、フラグをつけている
                    st.session_state.total_score += 35
                    st.session_state.bonusstatus = True


                for i in range(5): #チェックボックスの状態を初期化
                    key=f"keep_{i}"
                    if key in st.session_state:
                        del st.session_state[key]

                del st.session_state.current_dice #サイコロを初期化.
                st.rerun() #これで1ターン
        st.divider() #真ん中に水平線を引く

        #ルール説明を作成
        with st.expander("ルール説明"):
            st.write("### ルール説明")
            st.write("ヨットは、サイコロで遊ぶポーカーのようなものです。")
            st.write("サイコロ5つを使って役を成立させて、合計得点を競います。")
            st.write("役と得点については、下の 役の説明を見る ボタンから確認してください。")
            st.write("出目と選んだ役に応じて、得点が入ります。")
            st.write("1ゲーム12ターンで全ての役を一度ずつ選ぶ必要があり、もし不成立の役を選んだ場合は、その役の得点は0点となります。")
            st.write("各ターン2回まで選んだサイコロを振り直すことができます(複数選択可)。")
            st.write("'振り直さない'サイコロのチェックボックスにチェックをいれて、振り直しボタンを押せば好きなサイコロを振り直せます。")
            st.write("振り直す必要がなければ、そのままセレクトボックスから役を確定させてください。")
            st.write("エース、デュース、トレイ、フォー、ファイブ、シックスの合計点数が63点に達すると、35点のボーナススコアが加算されます。")
            st.write("ランクインを目指して遊んでみてください！")


        #役の説明テーブルを作成
        role_table = {
                    "役名": ["エース", "デュース", "トレイ", "フォー", "ファイブ", "シックス", "チョイス", "フォーダイス", "フルハウス", "S.ストレート", "B.ストレート", "ヨット"],
                     "役の説明": ["1の目の数×1点", "2の目の数×2点", "3の目の数×3点", "4の目の数×4点", "5の目の数×5点", "6の目の数×6点", "出目の合計点", "⚄⚄⚄⚄⚅のように、ある目が四回以上でていれば、出目の合計が得点", "⚄⚄⚄⚅⚅や⚄⚄⚄⚄⚄のように、全ての出目が2回以上出ているとき、出目の合計が得点", "⚀⚁⚂⚃のように連続した4つの目が出目に含まれるならば15点", "⚀⚁⚂⚃⚄のように連続した5つの目が出目に含まれるならば30点", "⚄⚄⚄⚄⚄のように5個全て同じ目がでたら50点"]
                     }
        df = pd.DataFrame(role_table)
        with st.expander("役の説明をみる"):
            st.table(df.set_index("役名"))

            
else:
    st.balloons()
    st.success(f"全12ラウンド終了！最終スコアは **{st.session_state.total_score}点** でした！")
    if  not  st.session_state.score_saved : #新しくゲームを始めるボタンを押したときに再度スコアが保存されるバグを回避.
        save_score(st.session_state.total_score)
        st.session_state.score_saved = True
        st.write("### ランキングtop5")
        top5 = get_top5()  # db.py の関数を呼び出す
        if top5:
            for i, row in enumerate(top5, start=1):
                st.write(f"{i}位: {row['score']}点")
        else:
            st.write("まだスコアが登録されていません。")
    if st.button("新しくゲームを始める"): #12ターン終わったら、状態を初期化する.
        st.session_state.clear() #これが初期化の命令.
        st.rerun()