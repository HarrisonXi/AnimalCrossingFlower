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

class Flower:
    def __init__(self, index, color, seed, percent, desc):
        self.index = index
        self.color = color
        self.seed = seed
        self.percent = percent
        self.desc = desc

# 混合两个颜色
# color1, color2：为0至2的数字
# 返回：可能混合出的颜色列表
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

# 计算颜色列表里出现对应颜色的概率
# colorList：颜色列表，例：[0, 1, 2]
# color：为0至2的数字
# 返回：计算出的概率
def colorPercent(colorList, color):
    if len(colorList) == 3:
        if color == 1:
            return 0.5
        else:
            return 0.25
    elif len(colorList) == 2:
        return 0.5
    else:
        return 1

# 将seed1和seed2两个种子进行杂交，并计算出结果
# seed1, seed2：个十百千位都为0-2的数字
# 返回：元素为Flower的数组
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
    flowers = [] # 记录可以杂交出的种子列表
    for r in redMixed:
        rPercent = colorPercent(redMixed, r)
        for y in yellowMixed:
            yPercent = colorPercent(yellowMixed, y)
            for w in whiteMixed:
                wPercent = colorPercent(whiteMixed, w)
                for s in satMixed:
                    sPercent = colorPercent(satMixed, s)
                    index = r * 27 + y * 9 + w * 3 + s # 花卉在颜色表里的索引号
                    color = colors[index] # 花卉表现出的颜色
                    seed = r * 1000 + y * 100 + w * 10 + s # 花卉种子序列号
                    color1 = colors[red1 * 27 + yellow1 * 9 + white1 * 3 + sat1] # 原花卉种子1的颜色
                    color2 = colors[red2 * 27 + yellow2 * 9 + white2 * 3 + sat2] # 原花卉种子2的颜色
                    percent = rPercent * yPercent * wPercent * sPercent # 杂交出这个花卉的概率
                    desc = '{}{}{}{}({}) + {}{}{}{}({}) = {}{}{}{}({}) {:.1%}'.format(
                        redFlag[red1], yellowFlag[yellow1], whiteFlag[white1], satFlag[sat1], color1,
                        redFlag[red2], yellowFlag[yellow2], whiteFlag[white2], satFlag[sat2], color2,
                        redFlag[r], yellowFlag[y], whiteFlag[w], satFlag[s], color, percent
                    ) # 用来打印的文本
                    flowers.append(Flower(index, color, seed, percent, desc))
    return flowers

# 无歧义培育法 - 提取无歧义的种子
# seed1, seed2：个十百千位都为0-2的数字
# 返回：元素为Flower的数组
def mixFlower_distinct(seed1, seed2):
    flowers = mixFlower(seed1, seed2)
    newFlowers = {}
    dupColors = []
    for flower in flowers:
        if flower.color not in dupColors:
            if flower.color in newFlowers.keys():
                # 已经出现过的颜色，引起歧义，添加到dupColors
                dupColors.append(flower.color)
                newFlowers.pop(flower.color)
            else:
                # 新出现的颜色，记录到newSeeds
                newFlowers[flower.color] = flower
    return newFlowers.values()

# 无歧义培育法 - 和原始3色种子合成判断能不能出额外颜色
# flower1, flower2：Flower
# seed：个十百千位都为0-2的数字
# 返回：会培育出额外颜色的Flower的列表，可能会为空
def mixFlower_tryDisambiguation_(flower1, flower2, seed):
    flowers1 = mixFlower(flower1.seed, seed)
    colors1 = []
    for flower in flowers1:
        if flower.percent < 0.2:
            # 会出现概率太低的花色，这种先略过
            return []
        if flower.color not in colors1:
            colors1.append(flower.color)
    flowers2 = mixFlower(flower2.seed, seed)
    colors2 = []
    for flower in flowers2:
        if flower.percent < 0.2:
            # 会出现概率太低的花色，这种先略过
            return []
        if flower.color not in colors2:
            colors2.append(flower.color)
    newFlowers = []
    for color in colors1:
        if color not in colors2:
            newFlowers.append(flower1)
            break
    for color in colors2:
        if color not in colors1:
            newFlowers.append(flower2)
            break
    return newFlowers

# 无歧义培育法 - 和原始3色种子合成判断能不能出额外颜色
# flower1, flower2：Flower
# 返回：会培育出额外颜色的Flower的列表，可能会为空
def mixFlower_tryDisambiguation(flower1, flower2):
    for round in [2, 1]:
        for seed in [200, 10, 2001]:
            newFlowers = mixFlower_tryDisambiguation_(flower1, flower2, seed)
            if len(newFlowers) >= round:
                return newFlowers
    return []

# 无歧义培育法 - 高级无歧义
# seed1, seed2：个十百千位都为0-2的数字
# 返回：元素为Flower的数组
def mixFlower_distinctA(seed1, seed2):
    flowers = mixFlower(seed1, seed2)
    colorDict = {}
    for flower in flowers:
        if flower.color in colorDict.keys():
            # 已经出现过的颜色
            colorDict[flower.color].append(flower)
        else:
            # 新出现的颜色
            colorDict[flower.color] = [flower]
    newFlowers = []
    for flowers in colorDict.values():
        if len(flowers) == 1:
            newFlowers.append(flowers[0])
        elif len(flowers) == 2:
            for flower in mixFlower_tryDisambiguation(flowers[0], flowers[1]):
                flower.desc = flower.desc + ' 歧'
                newFlowers.append(flower)
    return newFlowers

# 无歧义培育法 - 主循环体
def flowerDistinct():
    # 默认的三色种子:
    # 0 - 0 - 1 - 0 白
    # 0 - 2 - 0 - 0 黄
    # 2 - 0 - 0 - 1 红
    seeds = [10, 200, 2001]
    round = 1
    while round <= 16:
        newFlowers = []
        count = len(seeds)
        for index1 in range(count):
            seed1 = seeds[index1]
            for index2 in range(index1, count):
                seed2 = seeds[index2]
                for flower in mixFlower_distinctA(seed1, seed2):
                    if flower.percent > 0.1:
                        newFlowers.append(flower)
        newSeeds = []
        for flower in newFlowers:
            if flower.seed not in seeds and flower.seed != 2220:
                newSeeds.append(flower.seed)
                seeds.append(flower.seed)
        if len(newSeeds) == 0:
            break
        print(colored('**** 第{}轮 ****'.format(round), 'red'))
        for flower in newFlowers:
            if flower.seed in newSeeds:
                print(flower.desc)
        round = round + 1
    print(colored('**** 结果 ****', 'red'))
    for flower in newFlowers:
        if flower.seed == 2220 and flower.percent > 0.2:
            print(flower.desc)

# 得分培育法 - 计算得分
def score(seed):
    score = 0
    red = seed // 1000
    if red == 2:
        score = score + 3
    elif red == 1:
        score = score + 2
    yellow = seed % 1000 // 100
    if yellow == 2:
        score = score + 3
    elif yellow == 1:
        score = score + 2
    white = seed % 100 // 10
    if white == 2:
        score = score + 3
    elif white == 1:
        score = score + 2
    sat = seed % 10
    if sat == 0:
        score = score + 3
    elif sat == 1:
        score = score + 2
    return score

# 得分培育法 - 主循环体
def flowerScore():
    # 默认的三色种子:
    # 0 - 0 - 1 - 0 白
    # 0 - 2 - 0 - 0 黄
    # 2 - 0 - 0 - 1 红
    seeds = [10, 200, 2001]
    round = 1
    while round <= 16:
        newFlowers = []
        count = len(seeds)
        for index1 in range(count):
            seed1 = seeds[index1]
            for index2 in range(index1, count):
                seed2 = seeds[index2]
                for flower in mixFlower_distinctA(seed1, seed2):
                    if flower.percent > 0.1 and score(flower.seed) > (score(seed1) + score(seed2)) / 2:
                        newFlowers.append(flower)
        newSeeds = []
        for flower in newFlowers:
            if flower.seed not in seeds and flower.seed != 2220:
                newSeeds.append(flower.seed)
                seeds.append(flower.seed)
        if len(newSeeds) == 0:
            break
        print(colored('**** 第{}轮 ****'.format(round), 'red'))
        for flower in newFlowers:
            if flower.seed in newSeeds:
                print('{}({})'.format(flower.desc, score(flower.seed)))
        round = round + 1
    print(colored('**** 结果 ****', 'red'))
    for flower in newFlowers:
        if flower.seed == 2220 and flower.percent > 0.2:
            print(flower.desc)

if len(sys.argv) >= 3:
    for flower in mixFlower(int(sys.argv[1]), int(sys.argv[2])):
        print(flower.desc)
elif len(sys.argv) == 2:
    for flower in mixFlower(10, int(sys.argv[1])):
        print(flower.desc)
    for flower in mixFlower(200, int(sys.argv[1])):
        print(flower.desc)
    for flower in mixFlower(2001, int(sys.argv[1])):
        print(flower.desc)
else:
    flowerScore()
