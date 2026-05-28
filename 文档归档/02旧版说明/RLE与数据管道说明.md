# RLE 与数据管道说明

> 负责人：数据分析同学。你需要把这部分讲明白，因为它是这个赛题区别于普通图像分类的关键。

## 一句话解释

Severstal 的标注不是直接给一张 mask 图片，而是把缺陷区域压缩成 RLE 字符串放在 `train.csv` 里。我们的数据管道要做的事是：

```text
train.csv 中的 RLE 字符串 -> 解码成每类二维 Mask -> 合并成 4 通道 Mask -> 和原图一起送入 U-Net
```

## 原始 train.csv 长什么样

核心列：

| 列名 | 含义 |
|---|---|
| `ImageId_ClassId` | 图片名和类别编号，例如 `0002cc93b.jpg_1` |
| `EncodedPixels` | RLE 编码后的缺陷区域，空值表示该图片该类别没有缺陷 |

同一张图片会出现 4 行，分别对应 4 类缺陷。

## 为什么要聚合

模型训练时更方便使用：

```text
一张图片 -> 一个 RGB 输入 -> 一个 4 通道 Mask 标签
```

所以代码会把原始表格整理成：

| image_id | class_1 | class_2 | class_3 | class_4 | has_defect |
|---|---|---|---|---|---|
| xxx.jpg | RLE/空 | RLE/空 | RLE/空 | RLE/空 | 0 或 1 |

对应代码：

```text
../03_模型训练与代码实现/src/severstal/data.py
```

## RLE 解码要注意什么

Kaggle 的 RLE 有两个关键点：

- 像素从 1 开始计数。
- 展开顺序是列优先，也就是 Fortran order。

如果顺序写错，mask 会旋转或错位，模型训练和提交都会出问题。

对应代码：

```text
../03_模型训练与代码实现/src/severstal/rle.py
```

## Dataset 输出什么

训练时 Dataset 输出：

```text
image: 形状为 (3, H, W) 的 RGB 图片张量
mask:  形状为 (4, H, W) 的四通道缺陷 Mask
```

4 个 mask 通道分别对应 4 类缺陷。模型最后也输出 4 个通道。

对应代码：

```text
../03_模型训练与代码实现/src/severstal/dataset.py
```

## 数据增强做什么

数据增强用来提高泛化能力，当前包括：

- 水平翻转。
- 轻微平移、缩放、旋转。
- 亮度和对比度扰动。
- 更强配置中包含噪声和颜色扰动。

对应代码：

```text
../03_模型训练与代码实现/src/severstal/transforms.py
```

消融实验中会有 `w/o Augmentation`，用于验证数据增强是否真的有效。

## 你需要产出的解释

最终报告/PPT 中，你需要讲清楚：

1. 原始标注为什么是 RLE。
2. RLE 如何变成 mask。
3. 为什么每张图要生成 4 通道 mask。
4. 数据类别不平衡有什么影响。
5. 数据增强为什么可能提升模型泛化。

## 答辩简短回答模板

如果老师问“RLE 是什么”，可以答：

```text
RLE 是 Run-Length Encoding，用起点和连续长度来压缩二值 Mask。Severstal 中每类缺陷区域都用 RLE 存在 train.csv 里。我们训练前要把 RLE 解码成二维 Mask，再把 4 类 Mask 合并成 4 通道标签。
```

如果老师问“为什么这是分割不是分类”，可以答：

```text
分类只判断图片有没有缺陷或是哪类缺陷，但这个任务要定位缺陷在哪些像素上，并输出像素级 Mask，所以属于语义分割。
```
