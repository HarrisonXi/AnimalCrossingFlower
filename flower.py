# -*- coding:utf-8 -*- 
import sys, os
from termcolor import colored

colors = ['白', '白', '白', '白', '白', '白', '紫', '紫', '紫', '黄', '黄', '黄', '白', '白', '白', '紫', '紫', '紫', '黄', '黄', '黄', '黄', '黄', '黄', '白', '白', '白', '红', '粉', '白', '红', '粉', '白', '红', '粉', '紫', '橙', '黄', '黄', '红', '粉', '白', '红', '粉', '紫', '橙', '黄', '黄', '橙', '黄', '黄', '红', '粉', '白', '黑', '红', '粉', '黑', '红', '粉', '黑', '红', '粉', '橙', '橙', '黄', '红', '红', '白', '黑', '红', '紫', '橙', '橙', '黄', '橙', '橙', '黄', '蓝*', '红', '白']
redF = ['rr', 'Rr', 'RR']
yellowF = ['yy', 'Yy', 'YY']
whiteF = ['ww', 'Ww', 'WW']
satF = ['ss', 'Ss', 'SS']

# 0 - 0 - 1 - 0 白
# 0 - 2 - 0 - 0 黄
# 2 - 0 - 0 - 1 红
seeds = ['0010', '2001', '0200'] # 默认的三色种子
round = 1

def color_mix(color1, color2):
    c = color1 * 10 + color2
    if c == 0:
        return [0]
    elif c == 1:
        return [0, 1]
    elif c == 2:
        return [1]
    elif c == 10:
        return [0, 1]
    elif c == 11:
        return [0, 1, 2]
    elif c == 12:
        return [1, 2]
    elif c == 20:
        return [1]
    elif c == 21:
        return [1, 2]
    elif c == 22:
        return [2]
    return []

def flower_mix(seed1, seed2, distinct):
    red1 = int(seed1[0])
    red2 = int(seed2[0])
    redM = color_mix(red1, red2)
    yellow1 = int(seed1[1])
    yellow2 = int(seed2[1])
    yellowM = color_mix(yellow1, yellow2)
    white1 = 2 - int(seed1[2])
    white2 = 2 - int(seed2[2])
    whiteM = color_mix(white1, white2)
    sat1 = int(seed1[3])
    sat2 = int(seed2[3])
    satM = color_mix(sat1, sat2)
    expDict = {} # 记录只出一种结果（无歧义）的花色
    dupKeys = [] # 记录重复出现的花色
    for r in redM:
        for y in yellowM:
            for w in whiteM:
                for s in satM:
                    index = r * 27 + y * 9 + (2 - w) * 3 + s
                    key = colors[index]
                    if distinct:
                        if key not in dupKeys:
                            if key in expDict.keys():
                                dupKeys.append(key)
                                expDict.pop(key)
                            else:
                                desc = '{}{}{}{} = {}'.format(redF[r], yellowF[y], whiteF[w], satF[s], key) # 用来打印的文本
                                seed = '{}{}{}{}'.format(r, y, 2 - w, s) # 种子序列号
                                expDict[key] = (desc, seed)
                    else:
                        desc = '{}{}{}{} = {}'.format(redF[r], yellowF[y], whiteF[w], satF[s], key) # 用来打印的文本
                        seed = '{}{}{}{}'.format(r, y, 2 - w, s) # 种子序列号
                        expDict[index] = (desc, seed)
    newSeeds = []
    if len(expDict) > 0:
        print(colored('==== {}{}{}{} + {}{}{}{} ===='.format(redF[red1], yellowF[yellow1], whiteF[white1], satF[sat1], redF[red2], yellowF[yellow2], whiteF[white2], satF[sat2]), 'blue'))
        for value in expDict.values():
            print(value[0])
            newSeeds.append(value)
    return(newSeeds)

def flower():
    print(colored('**** 第{}轮 ****'.format(round), 'red'))
    roundNewSeeds = []
    count = len(seeds)
    for index1 in range(count):
        seed1 = seeds[index1]
        for index2 in range(index1, count):
            seed2 = seeds[index2]
            newSeeds = flower_mix(seed1, seed2, True)
            roundNewSeeds.extend(newSeeds)
    for seed in roundNewSeeds:
        if seed[1] not in seeds:
            print(colored('添加种子: {}'.format(seed[0]), 'blue'))
            seeds.append(seed[1])

if len(sys.argv) >= 3:
    flower_mix(sys.argv[1], sys.argv[2], False)
else:
    while '2220' not in seeds:
        flower()
        round = round + 1