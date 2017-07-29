from music21 import *
import os


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


def keynum(x): #noteオブジェクトから鍵盤番号(0-87)に対応させる関数
    a_pre = x.pitch.pitchClassString
    if (a_pre == 'B'):
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

import pickle
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
    alltransobj.append(transnewobj)
#print(transnewobj)


#print(alltransobj)

#    print(obj)
#    print("")
'''
    dict_all={}
    j=0
    for i in list_all:
    dict_all[str(i)]=j
    j=1+j
    
    list1_num=[]
    for i in list1:
    list1_num=list1_num.append(dict_all[str(i)])
    
    '''

decompATObj =sum(alltransobj,[])
'''
    print("")
    print(decompALObj)
    print("")
    '''



def remove_duplicates(x):
    y=[]
    for i in x:
        if i not in y:
            y.append(i)
    return y

#decompATObj_str = [str(i) for i in decompATObj] #リストの文字列化

# print(decompALObj_str)

print("")


notDup_Obj = remove_duplicates(decompATObj)


dict_all={}
j=0
for i in notDup_Obj:
    dict_all[str(i)]=j
    j=1+j

chord2numbers = []
ind=0
for i in alltransobj:
    chord2numbers.append([])
    for j in i:
        chord2numbers[ind].append(dict_all[str(j)])
    ind=ind+1

print(chord2numbers)

import numpy as np
transition_mat=np.zeros((len(dict_all),len(dict_all)))

#training = []
ind=0
for i in chord2numbers:
    for j in range(0,(len(i)-1)):
        transition_mat[i[j]][i[j+1]]=1+transition_mat[i[j]][i[j+1]]
for i in range(len(dict_all)):
    transition_mat[i][i] = transition_mat[i][i] / 2



def chordnum1(list1):
    chordvec = np.array(list1)
    if set(list(chordvec % 12)) == {1, 4, 8}: #VIの和音
        return(4)
    elif set(list(chordvec % 12)) == {1,6,9}: #IIの和音
        return(1)
    elif set(list(chordvec % 12)) == {1,4,9}: #IVの和音
        return(2)
    elif set(list(chordvec % 12)).issubset({3,6,9,11}): #Vの和音
        return(3)
    else: #Iの和音
        return(0)
#    return(9999)





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
#    return(9999)
'''
    番号の対応
    C 4
    D 6
    E 8
    F 9
    G 11
    A 1
    H 3
    
    
    
    '''


'''
    #chordnum1を使って5*5の遷移行列を作る場合
    
    chordmaxnum1=5
    
    chordset1=[]
    for i in range(0,chordmaxnum1):
    chordset1.append([])
    print(chordset1)
    
    for i in range(0,len(notDup_Obj)):
    chordset1[chordnum1(notDup_Obj[i])].append(i)
    
    #print(chordset1)
    
    import itertools
    
    chord1_transition_mat=np.zeros((chordmaxnum1,chordmaxnum1))
    
    for i,j in itertools.product(range(0,chordmaxnum1),range(0,chordmaxnum1)):
    chord1_transition_mat[i,j]=sum(sum(transition_mat[np.ix_(chordset1[i],chordset1[j])]))
    
    '''




chordmaxnum2=16 #chordnum2を使って１５種類の和声記号を考える場合

chordset2=[]
for i in range(0,chordmaxnum2):
    chordset2.append([])
print(chordset2)

for i in range(0,len(notDup_Obj)):
    chordset2[chordnum2(notDup_Obj[i])].append(i)

print(notDup_Obj)
#print(chordset2) #生成された和音の空間1-82のそれぞれに対して，対応する和声記号を与える写像

import itertools

chord2_transition_mat=np.zeros((chordmaxnum2,chordmaxnum2))
all_chord_mat = [[[] for i in range(chordmaxnum2)] for i in range(chordmaxnum2) ] #和声記号の中身の和音も区別した二重リスト

for i,j in itertools.product(range(0,chordmaxnum2),range(0,chordmaxnum2)):
    chord2_transition_mat[i,j]=sum(sum(transition_mat[np.ix_(chordset2[i],chordset2[j])]))
    all_chord_mat[i][j].append(transition_mat[np.ix_(chordset2[i], chordset2[j])])

for i in range(16):
    print(all_chord_mat[2][i][0].shape)
    print(all_chord_mat[2][i])



#for i j in itertools.product(range(0,chordmaxnum2),range(0,chordnum))

#print(chord1_transition_mat)
#print("")


chord2_transition_mat[0,0]=chord2_transition_mat[0,0]-50 #Iの和音は最後に伸びて無駄に増えているので，１曲あたり２個減らす
np.set_printoptions(linewidth=200)
print(chord2_transition_mat)

import random
def shiftharmony(i):
    cand=[]
    rowcomponent = chord2_transition_mat[i]
    for j in range(0,len(rowcomponent)):
        cand.extend( [j]*rowcomponent[j])
    random.shuffle(cand)
    return cand[0]


newmusic=[0]
for i in range(0,100):
    newmusic.append(shiftharmony(newmusic[i]))
    if newmusic[(i+1)]==0 and newmusic[i]==0:
        break

print(transition_mat)
transition_mat.shape
print(newmusic)







def shiftchord(i):
    chordnum = dict_all[(str(i))]
    cand=[]
    rowcomponent = transition_mat[chordnum]
    for j in range(0,len(rowcomponent)):
        cand.extend( [j]*rowcomponent[j])
    random.shuffle(cand)
    return cand[0]

dict_all_inv={}
for i in notDup_Obj:
    dict_all_inv[dict_all[(str(i))]]=i

newmusic2 = [[59, 52, 44, 40]]
print(shiftchord(newmusic2[0]))
print(newmusic2[0])

dict_note ={1:'A', 3:'H', 4:'C', 6:'D',8:'E',9:'F',11:'G'}


def numtonote(x):
    a = x // 12
    b = x % 12
    c = dict_note[b]
    print([a,c], end="")


for i in range(0,100):
    newmusic2.append(dict_all_inv[shiftchord(newmusic2[i])])
    for j in range(4):
        numtonote(newmusic2[i][j])
    print("")
    if chordnum2(newmusic2[(i+1)])==0 and chordnum2(newmusic2[i])==0:
        break

for j in range(4):
    numtonote(newmusic2[len(newmusic2)-1][j])
print("")

for i in range(0,100):
    newmusic2.append(dict_all_inv[shiftchord(newmusic2[i])])
    for j in range(4):
        numtonote(newmusic2[i][j])
    print("")
    if chordnum2(newmusic2[(i+1)])==0 and chordnum2(newmusic2[i])==0:
        break

for j in range(4):
    numtonote(newmusic2[len(newmusic2)-1][j])
print("")


#newmusic2[0]=0

#print(newmusic2)
#for i in newmusic2:
#print(dict_all_inv[newmusic2[i]])





#print(dict_all_inv[0])
#print(dict_all_inv['abc'])
#for i in newmusic2:
#    print(dict_all_inv[newmusic2[i]])

'''
    def shiftchord(i):
    cand = []
    rowcomponent =
    
    newmusic2 = [[59, 52, 44, 40]]
    for i in range(0,100):
    new2music.append(shiftchordnewmusic)
    '''

'''
    和音記号
    0 I
    1 I^1
    2 I^2
    3 II
    4 II^1
    5 IV
    6 IV^1
    7 IV^2
    8 V
    9 V^1
    10 V^2
    11 V7
    12 V7^1
    13 V7^2
    14 V7^3
    15 VI
    '''

'''
    def ChNumtoCh(x):
    if x == 0:
    return("I")
    elif  x== 1:
    return("I^1")
    elif  x== 2:
    return("I^2")
    elif  x== 3:
    return("II")
    elif  x== 4:
    return("II^1")
    elif  x== 5:
    return("IV")
    elif  x== 6:
    return("IV^1")
    elif  x== 7:
    return("IV^2")
    elif  x== 8:
    return("V")
    elif  x== 9:
    return("V^1")
    elif  x== 10:
    return("V^2")
    elif  x== 11:
    return("V7")
    elif  x== 12:
    return("V7^1")
    elif  x== 13:
    return("V7^2")
    elif  x== 14:
    return("V7^3")
    elif  x== 15:
    return("VI")
    '''

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


#newmusicchord = []
#newmusicchord = chordnumtochord(newmusic)
#print(newmusicchord)

#np.savetxt('chordtransitionmat.csv',chord2_transition_mat,fmt ='%f0')


