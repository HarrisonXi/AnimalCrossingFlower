# 《动物森友会》蓝玫瑰花卉杂交无歧义方案

### 引用资料

Google文档：

[花卉杂交指南：Animal Crossing Flower Genetics Guide](https://docs.google.com/document/d/1ARIQCUc5YVEd01D7jtJT9EEJF45m07NXhAm4fOpNvCs)

[花卉基因表现表格：ACNH/ACNL Flower Flags](https://docs.google.com/spreadsheets/d/11pRCX8G0xGizSYWgVhoUSu7pE-MV7AOprBcgSY1whB4)

微博大佬[阿丘不严肃](https://www.weibo.com/u/1949050703)翻译的译文：

[全花朵基因型及杂交原理参考（编译）](https://www.weibo.com/ttarticle/p/show?id=2309404493225317499148)

### 前言

我这篇文章暂时可能没有什么dio用，所以可以先看看图一乐。因为概率太低所以实际应用价值偏低，后面会改改程序看看有没有更有效的方案，可以期待我的更新。

### 什么是无歧义方案

上面的杂交原理文章看完后，大家应该就能明白花卉杂交是怎么一回事了，但是这篇指南里提供的杂交路线是可能产生歧义的。什么意思呢？拿第三步做成图给大家看：

![old.png](https://github.com/HarrisonXi/AnimalCrossingFlower/raw/master/old.png)

![old.png](/Users/harrisonxi/Desktop/AnimalCrossingFlower/old.png)

白色加紫色会杂交出四种花：两个紫色两个白色，但是其中只有一个紫色是我们需要的。所以我们需要二次验证，把杂交出的紫色花跟黄色种子花种一起，看看能不能杂交出黄色花来判断是不是我们要的紫色基因型。这就是我所说的有歧义方案。

这种情况算好的，有歧义方案偶尔可能会出现一些我们没法判断花朵基因型的情况，我没有仔细深究有没有这种可能，有空的时候我会再（继）研（续）究（偷）下（懒）。

### 程序计算无歧义方案

无歧义的意思就是杂交结果里，只要花朵出了对应的颜色，就一定是确定的基因型。

```
rryyWwss(白) + rryyWwss(白) = rryyWWss(白)
rryyWwss(白) + rryyWwss(白) = rryyWwss(白)
rryyWwss(白) + rryyWwss(白) = rryywwss(紫)
```

参照上面白色玫瑰种子的杂交结果，可能出现两种白色花，就叫做有歧义；只会出现一种紫色花，那就是无歧义。

整个无歧义方案用人肉来算肯定不现实，所以写了个python3脚本，最新版本的脚本放在这里了：[flower.py](https://github.com/HarrisonXi/AnimalCrossingFlower/blob/master/flower.py)

![output.gif](https://github.com/HarrisonXi/AnimalCrossingFlower/raw/master/output.gif)

![output](/Users/harrisonxi/Desktop/AnimalCrossingFlower/output.gif)

运行的结果：[output.txt](https://github.com/HarrisonXi/AnimalCrossingFlower/blob/master/output.txt)，精简后的有效无歧义培育路线：[result.txt](https://github.com/HarrisonXi/AnimalCrossingFlower/blob/master/result.txt)

![result.png](https://raw.githubusercontent.com/HarrisonXi/AnimalCrossingFlower/master/result.png)

![result](/Users/harrisonxi/Desktop/AnimalCrossingFlower/result.png)

标记成“(种)”的就是商店买的种子。

这里前面的路线概率都还可以，就是最后一步概率太低了，考虑花海战术来培育的话，兴许才能有点希望，不然非洲人可能一个月都等不到出蓝玫瑰。另外找朋友来帮忙浇水可以提高杂交触发率，大家应该都知道了。

比较有趣的是最上面的一个万能粉基因型，这个基因型自交或者两朵同基因型杂交，是可以杂交出所有玫瑰花色的（金色比较特殊我没算）。有兴趣感受随机性惊喜的朋友可以试试，1/256=0.39%的概率可以得到蓝玫瑰。