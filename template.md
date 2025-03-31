---
title: "awk基本使用"
description: "Awk 命令基本使用"
date: 2020-12-05
lastmod: 2020-12-05
tags:
- Linux
- Awk
draft: false
weight: # 输入1可以顶置文章
slug: "awk-usage"
showbreadcrumbs: true #顶部显示当前路径
---

### 快捷键

> awk 是 linux 上用于文本处理的脚本语言，你可以实现：
>
> - 定义变量
> - 使用字符串和算术运算符
> - 使用控制流程和循环
> - 生成格式化的输出

```shell
用法：awk [POSIX 或 GNU 风格选项] [--] '程序' 文件 ...
POSIX 选项：		GNU 长选项：(标准)
	-f 脚本文件		--file=脚本文件
	-F fs			--field-separator=fs
	-v var=val		--assign=var=val
```

#### 使用变量

- $0 整行
- $1 第一列字段
- $2 第二列字段
- $n 第 n 列字段

> 空格或者制表符是默认的列分隔符
> 可以通过-F 指定分隔符

```shell
awk -F: '{print $1}' /etc/passwd

cat /etc/passwd | awk -F: '{print $1}'
```

#### 使用脚本文件

> 将 awk 脚本保存在 testfile 文件中

```shell
{print $1 " home at " $6}
```

> 然后执行文件

```shell
awk -F: -f testfile /etc/passwd
```

#### 预处理和后处理

> 保存 testfile 如下

```shell
BEGIN {
print "Users and thier corresponding home"
print " UserName \t HomePath"
print "___________ \t __________"
FS=":"
}

{
print $1 "  \t  " $6
}

END {
print "The end"
}
```

> 执行脚本

```shell
awk -f testfile /etc/passwd
```

#### 内置变量

> 一些内置变量如下
>
> - FS 指定 field 段分隔符
> - OFS [Output Filed Separator]输出分隔符
> - ORS [Output Record Separator] 输出行分隔符
> - FIELDWIDTHS 按段长度分割
> - RS [Record Separator]记录分隔符，默认是换行符

**指定输出分隔符**

```shell
awk 'BEGIN{FS=":"; OFS="-"} {print $1,$6,$7}' /etc/passwd
```

**使用长度分割**

素材如下，保存为 testrecord：

```shell
1235.96521

927-8.3652

36257.8157
```

```shell
awk 'BEGIN{FIELDWIDTHS="3 4 3"}{print $1,$2,$3}' testrecord
```

输出如下：

```shell
123 5.96 521

927 -8.3 652

362 57.8 157
```

**使用 Record Separator**
素材如下，保存为 testrecord：

```shell
Person Name
123 High Street
(222) 466-1234

Another person
487 High Street
(523) 643-8754
```

```shell
awk 'BEGIN{FS="\n"; RS=""} {print $1,$3}' testrecord
```

输出如下：

```shell
Person Name (222) 466-1234
Another person (523) 643-8754
```

### 参考

[30 Examples For Awk Command In Text Processing](https://likegeeks.com/awk-command/)
