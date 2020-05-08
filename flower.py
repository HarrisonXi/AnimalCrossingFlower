# -*- coding:utf-8 -*- 
import sys, os, time
from termcolor import colored

colors = ['白', '白', '白', '白', '白', '白', '紫', '紫', '紫',
          '黄', '黄', '黄', '白', '白', '白', '紫', '紫', '紫',
          '黄', '黄', '黄', '黄', '黄', '黄', '白', '白', '白',
          '红', '粉', '白', '红', '粉', '白', '红', '粉', '紫',
          '橙', '黄', '黄', '红', '粉', '白', '红', '粉', '紫',
          '橙', '黄', '黄', '橙', '黄', '黄', '红', '粉', '白',
          '黑', '红', '粉', '黑', '红', '粉', '黑', '红', '粉',
          '橙', '橙', '黄', '红', '红', '白', '黑', '红', '紫',
          '橙', '橙', '黄', '橙', '橙', '黄', '蓝', '红', '白']
redFlag = ['rr', 'Rr', 'RR']
yellowFlag = ['yy', 'Yy', 'YY']
whiteFlag = ['WW', 'Ww', 'ww']
satFlag = ['ss', 'Ss', 'SS']

class FlowerResult:
    def __init__(self, index, color, seed, desc):
        self.index = index
        self.color = color
        self.seed = seed
        self.desc = desc

def mixColor(color1, color2):
    c = color1 * 10 + color2
    if c == 0:
        return [0]
    elif c == 22:
        return [2]
    elif c == 2 or c == 20:
        return [1]
    elif c == 1 or c == 10:
        return [0, 1]
    elif c == 12 or c == 21:
        return [1, 2]
    elif c == 11:
        return [0, 1, 2]
    return []

def mixFlower(seed1, seed2):
    red1 = seed1 // 1000
    red2 = seed2 // 1000
    redMixed = mixColor(red1, red2)
    yellow1 = seed1 % 1000 // 100
    yellow2 = seed2 % 1000 // 100
    yellowMixed = mixColor(yellow1, yellow2)
    white1 = seed1 % 100 // 10
    white2 = seed2 % 100 // 10
    whiteMixed = mixColor(white1, white2)
    sat1 = seed1 % 10
    sat2 = seed2 % 10
    satMixed = mixColor(sat1, sat2)
    seedResults = [] # 记录可以杂交出的种子列表
    for r in redMixed:
        for y in yellowMixed:
            for w in whiteMixed:
                for s in satMixed:
                    index = r * 27 + y * 9 + w * 3 + s # 颜色表现的索引号
                    color = colors[index] # 表现出的颜色
                    seed = r * 1000 + y * 100 + w * 10 + s # 种子序列号
                    desc = '{}{}{}{}({}) + {}{}{}{}({}) = {}{}{}{}({})'.format(
                        redFlag[red1], yellowFlag[yellow1], whiteFlag[white1], satFlag[sat1],
                        colors[red1 * 27 + yellow1 * 9 + white1 * 3 + sat1],
                        redFlag[red2], yellowFlag[yellow2], whiteFlag[white2], satFlag[sat2],
                        colors[red2 * 27 + yellow2 * 9 + white2 * 3 + sat2],
                        redFlag[r], yellowFlag[y], whiteFlag[w], satFlag[s], color
                    ) # 用来打印的文本
                    seedResults.append(FlowerResult(index, color, seed, desc))
    return seedResults

# 无歧义培育法 - 提取无歧义的种子
def mixFlower_distinct(seed1, seed2):
    seedResults = mixFlower(seed1, seed2)
    newResults = {}
    dupColors = []
    for result in seedResults:
        if result.color not in dupColors:
            if result.color in newResults.keys():
                # 已经出现过的颜色，容易引起歧义，添加到dupColors
                dupColors.append(result.color)
                newResults.pop(result.color)
            else:
                # 新出现的颜色，记录到newSeeds
                newResults[result.color] = result
    return newResults.values()

# 无歧义培育法 - 主循环体
def flowerDistinct():
    # 默认的三色种子:
    # 0 - 0 - 1 - 0 白
    # 0 - 2 - 0 - 0 黄
    # 2 - 0 - 0 - 1 红
    seeds = [10, 200, 2001]
    round = 1
    while 2220 not in seeds:
        print(colored('**** 第{}轮 ****'.format(round), 'red'))
        newResults = []
        count = len(seeds)
        for index1 in range(count):
            seed1 = seeds[index1]
            for index2 in range(index1, count):
                seed2 = seeds[index2]
                newResults.extend(mixFlower_distinct(seed1, seed2))
        newSeeds = []
        for result in newResults:
            if result.seed not in seeds:
                newSeeds.append(result.seed)
                seeds.append(result.seed)
        for result in newResults:
            if result.seed in newSeeds:
                print(result.desc)
        round = round + 1


if len(sys.argv) >= 3:
    for result in mixFlower(int(sys.argv[1]), int(sys.argv[2])):
        print(result.desc)
else:
    flowerDistinct()
