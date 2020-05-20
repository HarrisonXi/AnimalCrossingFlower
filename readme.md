# 《动物森友会》蓝玫瑰花卉杂交无歧义优化方案

### 引用资料

Google文档：

[花卉杂交指南：Animal Crossing Flower Genetics Guide](https://docs.google.com/document/d/1ARIQCUc5YVEd01D7jtJT9EEJF45m07NXhAm4fOpNvCs)

[花卉基因表现表格：ACNH/ACNL Flower Flags](https://docs.google.com/spreadsheets/d/11pRCX8G0xGizSYWgVhoUSu7pE-MV7AOprBcgSY1whB4)

微博大佬[阿丘不严肃](https://www.weibo.com/u/1949050703)翻译的译文：

[全花朵基因型及杂交原理参考（编译）](https://www.weibo.com/ttarticle/p/show?id=2309404493225317499148)

上一篇文章：

[《动物森友会》蓝玫瑰花卉杂交无歧义方案](https://github.com/HarrisonXi/AnimalCrossingFlower/blob/master/readme_old.md)

### 前言

前一篇文章给大家介绍了无歧义方案，但是因为概率太低没有什么卵用，所以今天要做的就是优化这个方案。关于什么是无歧义方案，请看上一篇！

### 另一种无歧义的可能性

前一篇文章我觉得同一种花色出现两个基因型，就会难以判断歧义。但是现在我觉得不完全是这样，类似于上一篇文章里提到的例子中，两种紫色就是可以区分的：

![old.png](https://github.com/HarrisonXi/AnimalCrossingFlower/raw/master/old.png)

所以我改良了算法，如果杂交结果中同颜色的花出现了**两种**基因型，那么我会把两种花都和三色原始种子花杂交一下，用以判断这个基因型是不是可消歧义的。用上图中的例子来说，rryywwss和黄色原始种子花杂交只能出白色，而rrYywwss和黄色原始种子花杂交是能额外出现黄色的。一旦能出黄色，它就一定是rrYywwss基因型，所以这里我就会认定rrYywwss也是无歧义的。（这个算法写起来有点烦，我承认第一版是因为我懒所以没好好实现这个。）

### 剔除低概率太并增加轮数

紧接着我尝试了剔除低概率的结果并增加的杂交的轮数，因为这样做可以对基因进行提纯。RrYyWwss如果能渐渐变成RrYywwss之类的，那肯定是极好的。

算法优化到这里之后，差不多4至6轮杂交（不含消歧义步骤）后，就能得到一些比较好的基因型用来培育蓝玫瑰了（完整结果：[output2.txt](https://github.com/HarrisonXi/AnimalCrossingFlower/blob/master/output2.txt)）：

```
RRYywwss(黑) + RRYywwss(黑) = RRYYwwss(蓝) 25.0%
RRYywwss(黑) + RrYYwwss(红) = RRYYwwss(蓝) 25.0%
RRYywwss(黑) + RRYYwwSs(红) = RRYYwwss(蓝) 25.0%
RRYywwss(黑) + RRYYWwss(橙) = RRYYwwss(蓝) 25.0%
RrYYwwss(红) + RrYYwwss(红) = RRYYwwss(蓝) 25.0%
RrYYwwss(红) + RRYYwwSs(红) = RRYYwwss(蓝) 25.0%
RrYYwwss(红) + RRYYWwss(橙) = RRYYwwss(蓝) 25.0%
RRYYwwSs(红) + RRYYwwSs(红) = RRYYwwss(蓝) 25.0%
RRYYwwSs(红) + RRYYWwss(橙) = RRYYwwss(蓝) 25.0%
RRYYWwss(橙) + RRYYWwss(橙) = RRYYwwss(蓝) 25.0%
```

### 计算种子得分

但是看一遍完整结果就会发现茫茫花海，要找个最优的杂交路线不容易。有些结果会使得基因纯度越来越低，类似RrYyWwSs这种动不动就能杂交出十几种基因型，所以也应该从流程里直接剔除掉它们。为了进一步优化，我给种子新增了评分系统。比如红色我们期望的基因型是RR，那么RR计3分，Rr计2分，rr计0分（关于为什么这么计分就不展开说了）。这样我们对四组基因做完评分，三色的原始种子还有蓝玫瑰的基因型得分就是：

```
rryyWwss(白) = 5分
rrYYWWss(黄) = 6分
RRyyWWSs(红) = 5分
RRYYwwss(蓝) = 12分
```

每次杂交完得到新的结果，我们不仅要选择无歧义的，还要期望得分更高的结果，来保证基因型越来越趋近于蓝玫瑰。

### 结论

再次改进后的算法（源代码：[flower.py](https://github.com/HarrisonXi/AnimalCrossingFlower/blob/master/flower.py)），运行一下就可以得到结果：[output3.txt](https://github.com/HarrisonXi/AnimalCrossingFlower/blob/master/output3.txt)。可以看到已经很简短了，从这里面剔除一些没用上的路线得到下面的结果，就可以按照这个路线尝试进行培育啦。

```
**** 第1轮 ****
rryyWwss(白) + rryyWwss(白) = rryywwss(紫) 25.0%(6)
rryyWwss(白) + rrYYWWss(黄) = rrYyWwss(白) 50.0%(7)
rryyWwss(白) + RRyyWWSs(红) = RryyWwss(红) 25.0% 歧(7)
rrYYWWss(黄) + RRyyWWSs(红) = RrYyWWss(橙) 50.0%(7)
RRyyWWSs(红) + RRyyWWSs(红) = RRyyWWss(黑) 25.0%(6)
**** 第2轮 ****
rryyWwss(白) + rrYyWwss(白) = rrYywwss(紫) 12.5% 歧(8)
RRyyWWSs(红) + RryyWwss(红) = RRyyWwss(黑) 12.5% 歧(8)
rryywwss(紫) + rrYyWwss(白) = rrYywwss(紫) 25.0% 歧(8)
rrYyWwss(白) + rrYyWwss(白) = rrYywwss(紫) 12.5% 歧(8)
RryyWwss(红) + RRyyWWss(黑) = RRyyWwss(黑) 25.0% 歧(8)
**** 第3轮 ****
rrYYWWss(黄) + rrYywwss(紫) = rrYYWwss(黄) 50.0%(8)
rrYyWwss(白) + rrYywwss(紫) = rrYYWwss(黄) 12.5%(8)
RrYyWWss(橙) + rrYywwss(紫) = rrYYWwss(黄) 12.5%(8)
RrYyWWss(橙) + rrYywwss(紫) = RrYYWwss(橙) 12.5%(10)
rrYywwss(紫) + rrYywwss(紫) = rrYYwwss(白) 25.0%(9)
**** 第4轮 ****
RRyyWwss(黑) + RrYYWwss(橙) = RRYywwss(黑) 12.5%(11)
rrYYWwss(黄) + RrYYWwss(橙) = RrYYwwss(红) 12.5%(11)
RrYYWwss(橙) + RrYYWwss(橙) = RrYYwwss(红) 12.5%(11)
RrYYWwss(橙) + rrYYwwss(白) = RrYYwwss(红) 25.0%(11)
**** 结果 ****
RRYywwss(黑) + RRYywwss(黑) = RRYYwwss(蓝) 25.0%
RRYywwss(黑) + RrYYwwss(红) = RRYYwwss(蓝) 25.0%
RrYYwwss(红) + RrYYwwss(红) = RRYYwwss(蓝) 25.0%
```

注：末尾含有“歧”字的就是需要二次杂交验证下消歧义。

整理下目前算出来较优的完整杂交步骤：

```
1. rryyWwss(白种子) + rrYYWWss(黄种子) = rrYyWwss(白1) 50.0%
2. 第一步里的白色花和白种子花杂交，可能会得出两种紫色：
   rryyWwss(白种子) + rrYyWwss(白1) = rryywwss(紫2A) 12.5%
   rryyWwss(白种子) + rrYyWwss(白1) = rrYywwss(紫2B) 12.5%
3. 将培育出来的紫色都和黄种子花杂交，可能得出以下结果：
   rrYYWWss(黄种子) + rryywwss(紫2A) = rrYyWwss(白1) 100.0%
   rrYYWWss(黄种子) + rrYywwss(紫2B) = rrYyWwss(白1) 50.0%
   rrYYWWss(黄种子) + rrYywwss(紫2B) = rrYYWwss(黄3) 50.0%
   注意这里产生的白色都是和第一步的白色是一样的基因型，可以重复利用。
   一旦产出了黄色花，那么这个紫色花就是rrYywwss(紫2B)基因型，这个黄色花后面还会用到，不要丢。
4. RRyyWWSs(红种子) + rrYYWWss(黄种子) = RrYyWWss(橙4) 50.0%
5. RrYyWWss(橙4) + rrYywwss(紫2B) = rrYYWwss(黄3) 12.5%
   RrYyWWss(橙4) + rrYywwss(紫2B) = RrYYWwss(橙5) 12.5%
   这两个都是无歧义的结果。
6-1. 这里得到的多个RrYYWwss(橙5)相互杂交，已经有6.2%的概率出蓝色了。没有出蓝色的话，还有挺大概率出现阿丘文章里提到的二代红：
   RrYYWwss(橙5) + RrYYWwss(橙5) = RrYYwwss(二代红) 12.5%
   RrYYWwss(橙5) + RrYYWwss(橙5) = RRYYwwss(蓝) 6.2%
   上面的结果都是无歧义的。不过不是很推荐这个方案，因为后面的方案可以持续优化概率。
6-2. 把RrYYWwss(橙5)和之前的rrYYWwss(黄3)进行杂交：
   RrYYWwss(橙5) + rrYYWwss(黄3) = rrYYwwss(白6) 12.5%
   RrYYWwss(橙5) + rrYYWwss(黄3) = RrYYwwss(二代红) 12.5%
   上面的结果都是无歧义的。这个rrYYwwss(白6)如果培育出来，也是有用的。
6-3. 如果得到了rrYYwwss(白6)，优先拿它和RrYYWwss(橙5)杂交：
   RrYYWwss(橙5) + rrYYwwss(白6) = rrYYWwss(黄3) 25.0%
   RrYYWwss(橙5) + rrYYwwss(白6) = rrYYwwss(白6) 25.0%
   RrYYWwss(橙5) + rrYYwwss(白6) = RrYYWwss(橙5) 25.0%
   RrYYWwss(橙5) + rrYYwwss(白6) = RrYYwwss(二代红) 25.0%
   相信你也发现了，出现的4种结果都是有用的。
7. RrYYwwss(二代红) + RrYYwwss(二代红) = RRYYwwss(蓝) 25.0%
   RrYYwwss(二代红) + RrYYwwss(二代红) = rrYYwwss(白6) 25.0%
   RrYYwwss(二代红) + RrYYwwss(二代红) = RrYYwwss(二代红) 50.0%
8. 为什么还有步骤8？哈哈哈，不要奇怪，完善的培育方案可不会教你只培育一朵蓝玫瑰。把蓝玫瑰和二代红种一起，可以提高培育更多蓝玫瑰的效率：
   RrYYwwss(二代红) + RRYYwwss(蓝) = RrYYwwss(二代红) 50.0%
   RrYYwwss(二代红) + RRYYwwss(蓝) = RRYYwwss(蓝) 50.0%
```

### 关于第一篇文章中的二代红

改进了新算法后，发现两步就能培育出第一篇文章中的二代红RrYyWwss，不想折腾那么多复杂步骤，可以用这个基因型搞花海战术。当然我只是瞎扯的，因为上一篇就说了概率太低导致几乎没有dio用。

![red.png](https://github.com/HarrisonXi/AnimalCrossingFlower/raw/master/red.png)