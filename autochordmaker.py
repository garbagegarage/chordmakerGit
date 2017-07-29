from music21 import *
import os
import pickle
import numpy as np
import itertools
import random

def flatten_with_any_depth(nested_list):
    """深さ優先探索の要領で入れ子のリストをフラットにする関数"""
    # フラットなリストとフリンジを用意
    flat_list = []
    fringe = [nested_list]
    
    while len(fringe) > 0:
        node = fringe.pop(0)
        # ノードがリストであれば子要素をフリンジに追加
        # リストでなければそのままフラットリストに追加
        if isinstance(node, list):
            fringe = node + fringe
        else:
            flat_list.append(node)
    return flat_list


def keynum(x): #noteオブジェクトから鍵盤番号(1-88)に対応させる関数
    a_pre = x.pitch.pitchClassString
    if (a_pre == 'B'): #なぜかこれだけ読み込めなかったので
        a = 11
    else:
        a = int(x.pitch.pitchClassString)
    b = x.octave
    return (12*b+a-8)


files = os.listdir('/Users/karatsu/Desktop/Cmajdata/') #楽譜データ読み込み
files = files[1:len(files)]

alltransobj = [] #

for file in files:
    file = '/Users/karatsu/Desktop/Cmajdata/'+file
    mxml = converter.parse(file)
    
    len1 = len(mxml[4]) #ソプラノ声部
    key_states1 = []
    for i in range(1,len1):
        len2 = len(mxml[4][i])
        for j in range(0,len2):
            mobj = mxml[4][i][j]
            if ("Note" in mobj.classSet):
                key_states1.append([mobj.duration.quarterLength,keynum(mobj)])

    len1 = len(mxml[5]) #アルト声部
    key_states2 = []
    for i in range(1,len1):
        len2 = len(mxml[5][i])
        for j in range(0,len2):
            mobj = mxml[5][i][j]
            if ("Note" in mobj.classSet):
                key_states2.append([mobj.duration.quarterLength,keynum(mobj)])

    len1 = len(mxml[6]) #テノール声部
    key_states3 = []
    for i in range(1,len1):
        len2 = len(mxml[6][i])
        for j in range(0,len2):
            mobj = mxml[6][i][j]
            if ("Note" in mobj.classSet):
                key_states3.append([mobj.duration.quarterLength,keynum(mobj)])

    len1 = len(mxml[7]) #バス声部
    key_states4 = []
    for i in range(1,len1):
        len2 = len(mxml[7][i])
        for j in range(0,len2):
            mobj = mxml[7][i][j]
            if ("Note" in mobj.classSet):
                key_states4.append([mobj.duration.quarterLength,keynum(mobj)])

    with open('mobj4.pickle', 'wb') as f:
        pickle.dump([key_states1,key_states2,key_states3,key_states4], f)

    with open('mobj4.pickle', 'rb') as f:
        obj=pickle.load(f)
    
    newobj = []
    minunit = min(flatten_with_any_depth(obj))
    for i in range(0,4):
        partnote = []
        for j in range(0, len(key_states1)):
            for k in range(0, int(obj[i][j][0]/minunit)):
                partnote.append(obj[i][j][1])
        newobj.append(partnote)

    transnewobj = list(map(list, zip(*newobj)))
    alltransobj.append(transnewobj) #各曲の和音を４つ組の番号で表した三重リスト

decompATObj = sum(alltransobj,[]) #二重リスト化

def remove_duplicates(x):
    y=[]
    for i in x:
        if i not in y:
            y.append(i)
    return y


notDup_Obj = remove_duplicates(decompATObj) #decompATObjのうち，重複する和音を除去


dict_all={} #すべての曲中に出てくる和音を順に０からラベルづけ
j=0
for i in notDup_Obj:
    dict_all[str(i)]=j
    j=1+j

chord2numbers = [] #すべての曲の和音を上の辞書にしたがって，番号に変換する
ind=0
for i in alltransobj:
    chord2numbers.append([])
    for j in i:
        chord2numbers[ind].append(dict_all[str(j)])
    ind=ind+1

transition_mat=np.zeros((len(dict_all),len(dict_all))) #遷移行列


for i in chord2numbers: #連続する２つの和音を見て和音iから和音jにうつるとき，遷移行列(i,j)成分を1増やす
    for j in range(0,(len(i)-1)):
        transition_mat[i[j]][i[j+1]]=1+transition_mat[i[j]][i[j+1]]
for i in range(len(dict_all)): #全終止や半終止などが多いため，I→I，V→V（同じ和音）に止まるものを半減
    transition_mat[i][i] = abs(transition_mat[i][i] // 2)


#今は使ってないけど，そのうち使うかも
#４つ組のベクトル（和音）を入力すると，その和音の和声記号を出力させる
#和声記号は下の通り0-15の数字に対応させて出力する
# ex.) chordnum([59, 52, 44, 40]) = 0
def chordnum2(list1):
    chordvec = np.array(list1)
    if set(list(chordvec % 12)) == {1, 4, 8}: #VIの和音
        return(15)
    elif set(list(chordvec % 12)) == {1,6,9}: #IIの和音
        if chordvec[3] % 12 == 6: #IIの基本形
            return(3)
        if chordvec[3] % 12 == 9: #IIの１転
            return(4)
    elif set(list(chordvec % 12)) == {1,4,9}: #IVの和音
        if chordvec[3] % 12 == 9: #IVの基本形
            return(5)
        elif chordvec[3] % 12 == 1: #IVの１転
            return(6)
        elif chordvec[3] % 12 == 4: #IVの２展
            return(7)
    elif set(list(chordvec % 12)) == {3,6,11}: #Vの和音
        if chordvec[3] % 12 == 11: #Vの基本形
            return(8)
        elif chordvec[3] % 12 == 3: #Vの１転
            return(9)
        elif chordvec[3] % 12 == 6: #Vの２転
            return(10)
    elif set(list(chordvec % 12)) == {3,6,9,11}: #V7の和音
        if chordvec[3] % 12 == 11: #V7の基本形
            return(11)
        elif chordvec[3] % 12 == 3: #V7の１転
            return(12)
        elif chordvec[3] % 12 == 6: #V7の２転
            return(13)
        elif chordvec[3] % 12 == 9: #V7の３転
            return(14)
    else:
        if chordvec[3] % 12 == 4: #Iの基本形
            return(0)
        if chordvec[3] % 12 == 8: #Iの１転
            return(1)
        if chordvec[3] % 12 == 11: #Iの２転
            return(2)

#ある和音を入力すると次に進む和音をあたえてくれる
#ex.) shiftchord([59, 52, 44, 40]) = [61, 52, 45, 40] 数字は適当
def shiftchord(i):
    chordnum = dict_all[(str(i))]
    cand=[]
    rowcomponent = transition_mat[chordnum]
    for j in range(0,len(rowcomponent)):
        cand.extend( [j]* int(rowcomponent[j]))
    random.shuffle(cand)
    return cand[0]

dict_all_inv={} #dict_allで定義した和音のラベルから元の４つ組のリストに戻す辞書
for i in notDup_Obj:
    dict_all_inv[dict_all[(str(i))]]=i

newmusic = [[59, 52, 44, 40]]

dict_note ={1:'A', 3:'H', 4:'C', 6:'D',8:'E',9:'F',11:'G'}


def numtonote(x):
    a = x // 12
    b = x % 12
    c = dict_note[b]
    print([a,c], end="")


for i in range(0,100):
    newmusic.append(dict_all_inv[shiftchord(newmusic[i])])
    for j in range(4):
        numtonote(newmusic[i][j])
    print("")
    if chordnum2(newmusic[(i+1)])==0 and chordnum2(newmusic[i])==0:
        break

for j in range(4):
    numtonote(newmusic[len(newmusic)-1][j])
print("")



'''
#和声記号出力のための関数
#今は使っていない
def ChNumtoCh(x):
    if x == 0:
        print("I")
    elif  x== 1:
        print("I^1")
    elif  x== 2:
        print("I^2")
    elif  x== 3:
        print("II")
    elif  x== 4:
        print("II^1")
    elif  x== 5:
        print("IV")
    elif  x== 6:
        print("IV^1")
    elif  x== 7:
        print("IV^2")
    elif  x== 8:
        print("V")
    elif  x== 9:
        print("V^1")
    elif  x== 10:
        print("V^2")
    elif  x== 11:
        print("V7")
    elif  x== 12:
        print("V7^1")
    elif  x== 13:
        print("V7^2")
    elif  x== 14:
        print("V7^3")
    elif  x== 15:
        print("VI")



def chordnumtochord(list):
    listnum = len(list)
    for i in range(listnum):
        list[i] = ChNumtoCh(list[i])
'''
