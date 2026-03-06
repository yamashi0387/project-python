import streamlit as st
import random

st.title("🎲 ヨットで遊ぼう")

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
    st.session_state.turn = 1 #1ゲーム13ターンなのでターンも毎回1ターン目にされたら困る.
    st.session_state.roles=["エース","デュース","トレイ","フォー","ファイブ","シックス","チョイス","フォーダイス","フルハウス","S.ストレート","B.ストレート","ヨット"] #役は一度使用したら使えないので、使ったらここから消していく.
    st.session_state.bonusscore = 0 #ボーナススコアの条件判定に使う
    st.session_state.bonusstatus = False #ボーナススコア

st.title(f"🎲 Turn {st.session_state.turn}/12") #turn数の表示.titleはh1.
st.write(f"### 現在の合計点: {st.session_state.total_score}") #合計点の表示.###はh3みたいなもの.

if st.session_state.roles:
    if 'current_dice' not in st.session_state:
        if st.button("サイコロを振る"): #ボタンを設置して、ボタンが押されるとサイコロが振られる.
            st.session_state.current_dice = [random.randint(1,6) for _ in range(5)] #サイコロをランダムで生成する.
            st.session_state.roll_count=0 #サイコロがリセットされたら振り直しの回数もリセット.
            st.rerun()

    if 'current_dice' in st.session_state:
        dice=st.session_state.current_dice
        dice_icons = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"} #数字で表示するよりサイコロで表示したいので、数字と絵文字を対応させて、絵文字を画面に表示させる.
        icons = [dice_icons[d] for d in dice] #出目をアイコンに変換する.
        st.write(f"# {' '.join(icons)}") #現在のサイコロを表示.' 'join()で、リストの中身を半角空きで並べる.

        cols=st.columns(5) #5k個に分割
        keeps = [] #振り直さないサイコロを選ぶ.
        for i in range(5):
            with cols[i]: #分割した各々の設定
                st.write(f"# {dice_icons[dice[i]]}") #サイコロの目を表示
                keep = st.checkbox("Keep", key=f"keep_{i}") #keyはcheckboxの名前と理解している.名前をつけておくと、rerunしたときにsession_stateのように、状態が保持できる.つまり、2回目の振り直しのときに、さきほど保持したサイコロは自動的にチェックが付く
                keeps.append(keep) #keep_{i}がtrueかfalseかをリストとして管理している.

        st.divider() #真ん中に水平線引く

        col1, col2=st.columns(2) #2つに分割

        with col1: #振り直す操作を定義
            if st.session_state.roll_count <2 : #振り直しは2回まで.回数は st.session_state.roll_countで管理している.
                if st.button(f"### 1.振り直す(残り{2-st.session_state.roll_count}回)"): #振り直すボタン
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
                st.session_state.turn += 1 #ターン数を1増やす.
                st.session_state.roles.remove(selected_role) #選んだ役を次のターンからは選べないようにする.
            
                if selected_role in ["エース","デュース","トレイ","フォー","ファイブ","シックス"] :
                    st.session_state.bonusscore += scores[selected_role]
                
                if st.session_state.bonusscore >= 63 and st.session_state.bonusstatus==False:
                    st.session_state.total_score += 35
                    st.session_state.bonusstatus = True


                for i in range(5): #チェックボックスの状態を初期化
                    key=f"keep_{i}"
                    if key in st.session_state:
                        del st.session_state[key]

                del st.session_state.current_dice #サイコロを初期化.
                st.rerun() #これで1ターン
else:
    st.balloons()
    st.success(f"全12ラウンド終了！最終スコアは **{st.session_state.total_score}点** でした！")

    if st.button("新しくゲームを始める"): #12ターン終わったら、状態を初期化する.
        st.session_state.clear() #これが初期化の命令.
        st.rerun()