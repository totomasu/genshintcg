import random
from itertools import product
from multiprocessing import Pool
from tqdm import tqdm


class Dice:
    def __init__(self):
        self.dice={'Omni':0,'Pyro':0,'Hydro':0,'Cryo':0,'Electro':0,'Geo':0,'Anemo':0,'Dendro':0}
        
    def addDie(self,die):
        self.dice[die] += 1
            
    def fillRandomDice(self):
        count = 8
        for i in self.dice.values():
            count -= i
        for _ in range(count):
            k = random.choice(list(self.dice.keys()))
            self.addDie(k)
    
    def reroll(self,repeat,evaluation_values):
        t0 = []
        for k,v in self.dice.items():
            if k == 'Omni':
                continue
            t0.append(tuple(range(v+1)))
        args=[]
        for l in product(*t0):
            t1 = ['Omni','Pyro','Hydro','Cryo','Electro','Geo','Anemo','Dendro']
            t2 = [self.dice['Omni']]+list(l)
            args.append((dict(zip(t1, t2)),repeat,evaluation_values))
        with Pool(4) as p:
                return list(tqdm(p.imap(wrap_multithread_func, args),total=len(args),ncols=100))
    def getDiceString(self):
        t = ''
        for k,v in self.dice.items():
            if v != 0:
                t += f"{k}:{v} "
        if t == '':
            t = 'None'
        return t
    
    def getDiceFigure(self):
        color = {
            'Omni':'\033[38;2;255;255;255m■ ',
            'Pyro':'\033[38;2;240;00;00m■ ',
            'Hydro':'\033[38;2;00;40;255m■ ',
            'Cryo':'\033[38;2;132;224;241m■ ',
            'Electro':'\033[35m■ ',
            'Geo':'\033[38;2;240;200;00m■ ',
            'Anemo':'\033[38;2;46;136;86m■ ',
            'Dendro':'\033[38;2;142;210;40m■ ',
            'reset':'\033[0m'
            }
        t = ''
        for k,v in self.dice.items():
            if v != 0:
                for i in range(v):
                    t+=color[k]
        if t == '':
            t = 'None'
        t+=color['reset']
        return t
    
    #パターンのマッチを判別するロジック
    def evaluate(self,evaluation_values):
        def particular_dice(dice,s,i):
            if i == 3:
                if dice[s] >= 3:
                        dice[s] -= 3
                elif dice[s] == 2 and dice['Omni'] >= 1:
                    dice[s] -= 2
                    dice['Omni'] -= 1
                elif dice[s] == 1 and dice['Omni'] >= 2:
                    dice[s] -= 1
                    dice['Omni'] -= 2
                elif dice[s] == 0 and dice['Omni'] >= 3:
                    dice['Omni'] -= 3
                else:
                    return False
                return True
            elif i == 2:
                if dice[s] >= 2:
                        dice[s] -= 2
                elif dice[s] == 1 and dice['Omni'] >= 1:
                    dice[s] -= 1
                    dice['Omni'] -= 1
                elif dice[s] == 0 and dice['Omni'] >= 2:
                    dice['Omni'] -= 2
                else:
                    return False
                return True
        
        def same_dice(dice,i):
            k,v = max(list(dice.items())[1:], key=lambda x: x[1])
            if i == 3:
                if dice[k] >= 3:
                    dice[k] -= 3
                elif dice[k] == 2 and dice['Omni'] >= 1:
                    dice[k] -= 2
                    dice['Omni'] -= 1
                elif dice[k] == 1 and dice['Omni'] >= 2:
                    dice[k] -= 1
                    dice['Omni'] -= 2
                elif dice[k] == 0 and dice['Omni'] >= 3:
                    dice['Omni'] -= 3
                else:
                    return False
                return True
            elif i == 2:
                if dice[k] >= 2:
                    dice[k] -= 2
                elif dice[k] == 1 and dice['Omni'] >= 1:
                    dice[k] -= 1
                    dice['Omni'] -= 1
                elif dice[k] == 0 and dice['Omni'] >= 2:
                    dice['Omni'] -= 2
                else:
                    return False
                return True
        
        def dif_dice(dice):
            for v in list(dice.values())[1:]:
                if v > 1:
                    return False
            return True
        
        score=0
        v=[]
        for i in evaluation_values.items():
            if i[0] == 'Pyro3Same3':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',3):
                    continue
                if not same_dice(d,3):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro2Same3':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',2):
                    continue
                if not same_dice(d,3):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro3Same2':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',3):
                    continue
                if not same_dice(d,2):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro3Same3Same2':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',3):
                    continue
                if not same_dice(d,3):
                    continue
                if not same_dice(d,2):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro2Same3Same2':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',2):
                    continue
                if not same_dice(d,3):
                    continue
                if not same_dice(d,2):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro3Same2Same2':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',3):
                    continue
                if not same_dice(d,2):
                    continue
                if not same_dice(d,2):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Same3Same2Same2':
                d=self.dice.copy()
                if not same_dice(d,3):
                    continue
                if not same_dice(d,2):
                    continue
                if not same_dice(d,2):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro3Same2Diff3':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',3):
                    continue
                if not same_dice(d,2):
                    continue
                if not dif_dice(d):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            #PyroHydro
            elif i[0] == 'Pyro3Hydro3':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',3):
                    continue
                if not particular_dice(d,'Hydro',3):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro3Hydro2':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',3):
                    continue
                if not particular_dice(d,'Hydro',2):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro2Hydro3':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',2):
                    continue
                if not particular_dice(d,'Hydro',3):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro2Hydro2':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',2):
                    continue
                if not particular_dice(d,'Hydro',2):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            #PyroDendro
            elif i[0] == 'Pyro3Dendro3':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',3):
                    continue
                if not particular_dice(d,'Dendro',3):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro3Dendro2':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',3):
                    continue
                if not particular_dice(d,'Dendro',2):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro2Dendro3':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',2):
                    continue
                if not particular_dice(d,'Dendro',3):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Pyro2Dendro2':
                d=self.dice.copy()
                if not particular_dice(d,'Pyro',2):
                    continue
                if not particular_dice(d,'Dendro',2):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            #HydroDendro
            elif i[0] == 'Hydro3Dendro3':
                d=self.dice.copy()
                if not particular_dice(d,'Hydro',3):
                    continue
                if not particular_dice(d,'Dendro',3):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Hydro3Dendro2':
                d=self.dice.copy()
                if not particular_dice(d,'Hydro',3):
                    continue
                if not particular_dice(d,'Dendro',2):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Hydro2Dendro3':
                d=self.dice.copy()
                if not particular_dice(d,'Hydro',2):
                    continue
                if not particular_dice(d,'Dendro',3):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
            elif i[0] == 'Hydro2Dendro2':
                d=self.dice.copy()
                if not particular_dice(d,'Hydro',2):
                    continue
                if not particular_dice(d,'Dendro',2):
                    continue
                if score <= i[1]:
                    score=i[1]
                v.append(i[0])
        return (score,v)
    
def multithread_func(l,repeat,evaluation_values):
    t3 = Dice()
    t3.dice = l.copy()
    t4 = t3.getDiceFigure()
    score=0
    percentages={k:0 for k in evaluation_values.keys()}
    
    for i in range(repeat):
        t3.dice = l.copy()
        t3.fillRandomDice()
        s,v = t3.evaluate(evaluation_values)
        score += s
        for _v in v:
            percentages[_v]+=1
            
    for k,v in percentages.items():
        percentages[k]=v/repeat
    score/=repeat
    return (t4,score,percentages)

def wrap_multithread_func(args):
    return multithread_func(*args)

def simulate(repeat,first_roll,evaluation_values):
    """
    サイコロを振りなおす時の残すサイコロのパターン全てでそれぞれ試行回数分サイコロを振りなおす。
    サイコロのパターンに評価値をつけ、マッチする最も評価値の高いパターンの評価値の平均値と、評価値を設定したサイコロのパターンを満たす確率を出力する。
    残すサイコロパターンのうち期待値が高いものを出力する。
    
    Parameters
    ----------
    repeat : int
        試行回数
    first_roll : dict
        1回目のダイスロールでのサイコロ
    evaluation_values : dict
        それぞれのパターンの評価値
    """
    d = Dice()
    for i in first_roll:
        d.addDie(i)
    print(f'First roll  {d.getDiceFigure()}')
    print(f'repeat:{repeat}')
    
    scores = d.reroll(repeat,evaluation_values)
    scores = sorted(scores, key=lambda x: x[1],reverse=True)
    
    sk=''
    for i in evaluation_values.keys():
        sk+= f'{i} '
    print(f'Evaluate {sk}   Keep')
    
    for i in scores[:20]:
        a='{:.2f}'.format(i[1])
        b=''
        for k,v in i[2].items():
            c='{:.0%}'.format(v)
            b+=f'\033[48;2;00;00;{int(255*v)}m{c.center(13)}\033[0m'
        print(f'{a.rjust(6)}  {b}  {i[0]}') 

def simulate_random(repeat,evaluation_values):
    """
    １回目のダイスロールからランダムに試行
    
    Parameters
    ----------
    repeat : int
        試行回数
    evaluation_values : dict
        それぞれのパターンの評価値
    """
    d = Dice()
    d.fillRandomDice()
    s=[]
    for k,v in d.dice.items():
        for _ in range(v):
            s.append(k)
    simulate(repeat,s,evaluation_values)
    
if __name__ == "__main__":
    e1={
        'Pyro3Same3':20,
        'Pyro2Same3':15,
        'Pyro3Same2':10,
        'Pyro3Same3Same2':24,
        'Pyro2Same3Same2':20,
        'Pyro3Same2Same2':16,
        # 'Same3Same2Same2':18,
        # 'Pyro3Same2Diff3':20,
        # 'Pyro3Hydro3':20,
        # 'Pyro3Hydro2':14,
        # 'Pyro2Hydro3':14,
        # 'Pyro2Hydro2':8,
        # 'Pyro3Dendro3':20,
        # 'Pyro3Dendro2':14,
        # 'Pyro2Dendro3':14,
        # 'Pyro2Dendro2':8,
        # 'Hydro3Dendro3':18,
        # 'Hydro3Dendro2':12,
        # 'Hydro2Dendro3':12,
        # 'Hydro2Dendro2':6
    }
    e2={
        # 'Pyro3Same3':20,
        # 'Pyro2Same3':15,
        # 'Pyro3Same2':10,
        # 'Pyro3Same3Same2':24,
        # 'Pyro2Same3Same2':20,
        # 'Pyro3Same2Same2':16,
        # 'Same3Same2Same2':18,
        # 'Pyro3Same2Diff3':20,
        'Pyro3Hydro3':20,
        'Pyro3Hydro2':14,
        'Pyro2Hydro3':14,
        'Pyro2Hydro2':8,
        'Pyro3Dendro3':20,
        'Pyro3Dendro2':14,
        'Pyro2Dendro3':14,
        'Pyro2Dendro2':8,
        'Hydro3Dendro3':18,
        'Hydro3Dendro2':12,
        'Hydro2Dendro3':12,
        'Hydro2Dendro2':6
    }
    
    #simulate(10000,['Geo','Geo','Hydro','Cryo','Cryo','Cryo','Anemo','Dendro'],e1)
    #simulate(10000,['Omni','Hydro','Electro','Electro','Geo','Geo','Geo','Dendro'],e2)
    simulate_random(20000,e1)