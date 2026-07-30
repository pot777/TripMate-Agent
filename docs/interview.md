# Agent Interview Notes


## Q1: 什么是大语言模型？


答案：

大语言模型是一类基于Transformer架构，
通过大规模数据训练得到的概率生成模型。

模型通过预测下一个token学习语言规律，
从而实现文本生成和理解。



## Q2: Token是什么？


答案：

Token是模型处理文本的基本单位。

模型输入和输出都会转换成token序列。

Context Window限制的是token数量。



## Q3: Context Window是什么？


答案：

Context Window表示模型一次能够处理的信息容量。

包括：

- 输入Prompt
- 历史对话
- 输出内容