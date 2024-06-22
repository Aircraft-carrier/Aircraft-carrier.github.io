﻿﻿# 基于 MIPS 指令系统的处理器设计 

根据计算机组成原理课程所学的知识，设计一个基于 MIPS 指令系统的处理 器，深刻理解处理器结构和计算机系统的整体工作原理。 

## 🍆 0 实验要求

### 0.1 处理器功能及指令系统定义

​	本实验的任务是结合数据通路的思想，设计一个简单的基于 MIPS 指令系统 的 RISC 处理器，**选取有代表性的 R 类指令、I 类指令和 J 类指令，指令总的条数不少于 5 条**。 

​	**处理器的指令字长为 32 位，包含 32 个 32 位通用寄存器 R0~R31**，具体指令格式参考课件和 MIPS-课外阅读资料。  

### 0.2 设计要求

​	要求根据以上给定的指令系统设计处理器，处理器工作流程按**取指**、**译码**、 **运算**、**访存**、**写回**五个阶段进行（或自行设计）。

​	控制器设计方法**可选（组合逻辑设计或微程序设计方法）**  需完成的环节包括： 

1. 指令格式设计；
2. 微操作的定义；
3. 节拍的划分
4. 处理器结构设计框图及功能描述
5. 如采用微程序设计，写出每条机器指令对应的微指令序列，确定微指令字长和微指令格式，编写微指令码点

> **提交纸质版，统一 A4 纸，左侧装订。正文 5 号字宋体，西文用 Times  New Roman，1.2 倍行距。要求排版规范，图表规范**。 提交时间：2024 年 6 月 25 日提交。

## 🍉1.引言

### 1.1 MIPS指令概述

​	MIPS（Microprocessor without Interlocked Pipeline Stages，无互锁流水线微处 理器）是一种精简指令集（RISC）架构，由美国 MIPS 计算机系统公司（由斯坦 福大学团队于 1984 年创立，现为美普思科技）开发，以其高效、简洁和强大的 特性，在嵌入式系统、工作站和超级计算机等领域得到了广泛应用。 

​	MIPS 架构有多个版本，包括 MIPS I、II、III、IV，以及 MIPS V，这五个版本又分别分为 MIPS32/64 Release（即其 32 位/64 位实现）。截至 2017 年 4 月的 最新版本是 MIPS32/64 Release 6；2021 年 3 月，美普思科技宣布停止开发 MIPS 架构，并加入 RISC-V 基金会，未来的处理器设计将基于 RISC-V 架构。

**MIPS指令集有以下特点：**

1. 简单的Load/Store结构。
2. 易于流水线CPU设计。
3. 易于编译器开发。
4. MIPS指令的寻址方式非常简单，每条指令的操作也非常简单。

### 1.2 MIPS指令格式概述

> MIPS指令集的指令格式主要包括三种：R-Type、I-Type 和 J-Type。以下是这三种指令格式的详细介绍：

1. R-Type 指令格式：
R-Type 指令通常用于操作寄存器之间的操作，如加法、减法、逻辑运算等。其基本格式如下：
```
OP   rs   rt   rd   shamt   funct
```
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/6003b264be174af7b2c1a93d5d0a2651.png)

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/564f306eb45840c8bb6b0cd3c92c1884.png" width="100%" alt="window" /> </div>


- `OP`：指令操作码，用于表示指令的类型。
- `rs`、`rt`、`rd`：分别表示源寄存器、目标寄存器和目的寄存器。
- `shamt`：表示移位操作的偏移量，一般用于逻辑左移或右移等操作。
- `funct`：功能字段，用于指明具体的操作。

2. I-Type 指令格式：
I-Type 指令主要用于立即数操作或者内存读写操作。其基本格式如下：
```
OP   rs   rt   immediate
```
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/be166ae2e175468a8b266610ebc2c3e5.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/fd61eae0be8a472498cb3fcb41b2f669.png" width="100%" alt="window" /> </div>


- `OP`：指令操作码，表示指令类型。
- `rs`：源寄存器。
- `rt`：目标寄存器。
- `immediate`：立即数字段，用于存储立即数或者偏移量。

3. J-Type 指令格式：
J-Type 指令主要用于跳转指令，如无条件跳转或者函数调用等。其基本格式如下：
```
OP   address
```
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/b10ed6a932e7482d821633aa695e9195.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/395dbfc4e61d493bb5d1467cbac070dc.png" width="100%" alt="window" /> </div>


- `OP`：指令操作码，表示指令类型。
- `address`：跳转地址字段，用于存储跳转的目标地址。

总的来说，MIPS 指令集采用这三种不同的指令格式来支持不同类型的指令操作，使得指令编码简洁明了，有助于提高指令的执行效率。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/cb63cbad471942329a90e6eda72185e1.png" width="100%" alt="window" /> </div>


### 1.3 MIPS寄存器

> MIPS有32个通用寄存器。硬件上，这些寄存器并没有区别(除了 0 号以外)，区分的目的是为了不同的编译器产生的代码可以正常的互相调用。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/5a7bbe9febd8417b9774e22881d8f949.png" width="100%" alt="window" /> </div>


##  🍍2 指令格式的设计

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/973847a4a2f14e438c2ac8216a09c385.png" width="100%" alt="window" /> </div>


我们选择有代表性的`"ADD"，"SUB"，"LW"，"SW"，"J“`五条指令来进行处理器的设计。

### 2.1 ADD指令设计

```
ADD rd, rs, rt
// e.g. ADD $t2, $t0, $t1
```

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/c403e76178e7437e86a4696c3054f29e.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/1329633d77a741779501f9e78a5d7a51.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/7a0f66df9588480ebe2726cffdf34d77.png" width="100%" alt="window" /> </div>
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/3bd30d163f5c4778810dfa7776ec295a.png" width="100%" alt="window" /> </div>


> ADD指令的汇编格式为add rd，rs，rt，这实现了32位整数加的操作，加数与被加数分别置于rs和rd寄存器中，最后由ALU运算器计算出结果并存到rd寄存器中。

### 2.2 SUB指令设计

```
SUB rd, rs, rt
// e.g.  SUB $t2, $t0, $t1
```

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/a59654708d3c4758a2edbabd20ebf75f.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/e4104b570b08456989ecb7037173faef.png" width="100%" alt="window" /> </div>


> SUB指令的汇编格式为sub rd，rs，rt，这实现了32位整数减的操作，被减数与减数分别置于rs和rd寄存器中，最后由ALU运算器计算出结果并存到rd寄存器中。

### 2.3 LW指令设计：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/2576ac7c8b4e46b6bbd985bfd47a35d1.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/2f00ec66984d47d9875c8d861da8171e.png" width="100%" alt="window" /> </div>

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/ec6e5d2ed5504af3851ab58b3b2a021c.png" width="100%" alt="window" /> </div>


> LW指令的汇编格式为lw rt，offset(rs" width="100%" alt="window" /> </div>，这将offset进行位拓展后与rs寄存器中数据相加获得访存地址，然后从该地址取出数据并存到rt寄存器中。

### 2.4 SW设计

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/5242357ef2b447f797d7b3730943cf3f.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/9cd20781673f48c5aae0da497fb217e8.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/135258e9ffd34377b9796c37a438ff64.png" width="100%" alt="window" /> </div>


> SW指令的汇编格式为sw rt，offset(rs)，这将rt寄存器中的数据存到offset与rs寄存器中数据计算后得到的地址位置处。

### 2.5 J指令设计

```
J target
// e.g. J 0x00400020
```

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/409d07c54ca840418b99a0785b521302.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/228c9230b4c54eb597e69d1229f0e64d.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/b12ee2eab83440849a1dfd3fa39a1fd6.png" width="100%" alt="window" /> </div>


> J指令的汇编格式为j target，其分支目标地址的计算与条件分支指令不同，具体是将顺序指令地址 PC+4 的高 4 位作为高地址部分并与指令字中的 26 位立即数 Address 左移两位得到的 28 位数据进行拼接，生成一个 32 位的无条件转移目标地址。

### 2.6 BEQ设计
```
BEQ rs, rt, offset
// e.g. BEQ $t0, $t1, 16
```
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/18798381e5044201a62201406d68a960.png" width="100%" alt="window" /> </div>
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/426bf6402e4d4ec68356bff8a8eb468c.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/f52786b2920742c5b90da97542a78c3b.png" width="100%" alt="window" /> </div>
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/07cf960299854a629c468f2b11c2b628.png" width="100%" alt="window" /> </div>
> beq 指令用于比较两个寄存器的值是否相等，若相等则进行分支。指令字中的立即数字段为 16 位有符号数，是分支目标地址与顺序指令地址 PC+4 之间的字偏移，可正可负（既可向后跳转， 也可向前跳转）。由于指令长度为 4 字节，因此需要将 16 位立即数符号扩展成 32 位后并左移两 位生成 32 位字节偏移量，再加上顺序指令地址 PC+4 才能得到分支目标地址。为了避免资源冲突， 这里需要单独设置一个加法器。当比较条件满足时，用分支目标地址修改 PC 的内容，即产生分 支跳转；反之将PC的值更新为PC+4，程序顺序执行。这里PC输入端也需要增设一个多路选择器， 用于选择顺序执行还是跳转执行。

## 🍌3 微操作定义

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/4506c3e0850e4c409349d329ef9c112a.png" width="100%" alt="window" /> </div>


一下会基于CPU基本结构框架图与前面提到的MIPS寄存器来定义指令不同阶段的微操作。由于定义的五种指令均不存在间址周期，所以将指令执行周期设置为取指、取数、执行、访存、写回五个阶段。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/114511dcd3954ab099b8ddc7ef78f96c.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/d81aa38787844d23a62fc11df83257cf.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/3ee3bbd2d4a744b7b484b327b84036be.png" width="100%" alt="window" /> </div>
同时会结合单周期 MIPS 处理器的数据通路来分析每条指令的实际情形下的具体执行过程。辅助理解位操作。

### 3.1 ADD指令的位操作定义

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/2a7547a49f2a4c308321b0f88f2b12fa.png" width="100%" alt="window" /> </div>


- 1 取指阶段：

| 微操作        |                   描述                   | 微命令       |
| ------------- | :--------------------------------------: | ------------ |
| $(PC)$ | `PC→Bus`,`Bus→MAR`,取当前指令地址`→MAR` | `PCo，MARi`  |
| $1 → R$       |                  读主存                  | `MemR=1`     |
| $M(MAR)→MDR$ |         从`MAR`的地址中读取指令          | `MARo，MDRi` |
| $MDR → IR$    |              把指令送到`IR`              | `MDRo，IRi`  |
| $(PC)+4 → PC$ |                  `PC+4`                  | `+4`         |

- 2 取数阶段

| 微操作           | 描述                            | 微命令             |
| ---------------- | ------------------------------- | ------------------ |
| $R(IR[21~25])→Y$ | 把`rs`寄存器中的加数先存到`Y`中 | `R(IR(21~25)o，Yi` |

- 3 执行阶段

| 微操作              | 描述                                                         | 微命令                    |
| ------------------- | ------------------------------------------------------------ | ------------------------- |
| $(Y)+R(IR(16~20)→Z$ | 把`(Y)`与`rt`寄存器中的操作数求和并送入`Z`，其中`rt`寄存器中的操作数直接通过`Bus`送到`ALU` | `Yo`，`Ro`，`ALUi`+，`Zi` |

- 4 写回阶段

| 微操作            | 描述                                            | 微命令     |
| ----------------- | ----------------------------------------------- | ---------- |
| $(Z)→R(IR(11~15)$ | 把暂存器`Z`中存储的运算结果写入目的寄存器`rd`中 | `Ri`，`Zo` |



### 3.2 SUB指令的位操作定义

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/8487211c264c409c88dcc715da8dc1b1.png" width="100%" alt="window" /> </div>


- 取指阶段

| 微操作        |                   描述                   | 微命令       |
| ------------- | :--------------------------------------: | ------------ |
| $(PC)$ | `PC→Bus`,`Bus→MAR`,取当前指令地址`→MAR` | `PCo，MARi`  |
| $1 → R$       |                  读主存                  | `MemR=1`     |
| $M(MAR)→MDR$ |         从`MAR`的地址中读取指令          | `MARo，MDRi` |
| $MDR → IR$    |              把指令送到`IR`              | `MDRo，IRi`  |
| $(PC)+4 → PC$ |                  `PC+4`                  | `+4`         |

- 取数阶段

| 微操作            | 描述                                | 微命令             |
| ----------------- | ----------------------------------- | ------------------ |
| $(R(IR[21~25])→Y$ | 把`rs`寄存器中的被减数数先存到`Y`中 | `R(IR(21~25)o，Yi` |

- 执行阶段

| 微操作               | 描述                                                         | 微命令                |
| -------------------- | ------------------------------------------------------------ | --------------------- |
| $(Y)-R(IR(16~20))→Z$ | 把`(Y)`与`rt`寄存器中的操作数计算并送入`Z`，其中`rt`寄存器中的操作数直接通过`Bus`送到`ALU` | `Yo，Ro，ALUi“-”，Zi` |

- 写回阶段

| 微操作             | 描述                                            | 微命令  |
| ------------------ | ----------------------------------------------- | ------- |
| $(Z)→R(IR(11~15))$ | 把暂存器`Z`中存储的运算结果写入目的寄存器`rd`中 | `Ri，Z` |

- R型指令的数据通路

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/a58c00e6eeba4d3f906313a0c3a13cdf.png" width="100%" alt="window" /> </div>
>指令执行过程中涉及的功能部件主要包括寄存器堆和 ALU。其只需将从指令存储器读出的指令字中的源寄存器字段 rs、rt 分别送入寄存器堆的两个读寄存器编号端 R1#、R2#，将目的 寄存器字段 rd 送入寄存器堆的写寄存器编号端 W#，将从寄存器堆读出的两个源寄存器的值经 R1、R2 端口输出到运算器；指令字中的 funct 字段决定 AluOp 控制 ALU 进行相应的运算（这里 应选择加法），运算结果被送入寄存器堆的写数据端口 WD，时钟上跳沿到来时会将运算结果写入目的寄存器 rd 中。

### 3.3 LW指令的位操作定义

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/0e15aff4b0984a2a85cc6cb50524797e.png" width="100%" alt="window" /> </div>


- 取指阶段

| 微操作        |                   描述                   | 微命令       |
| ------------- | :--------------------------------------: | ------------ |
| $(PC)$ | `PC→Bus`,`Bus→MAR`,取当前指令地址`→MAR` | `PCo，MARi`  |
| $1 → R$       |                  读主存                  | `MemR=1`     |
| $M(MAR)→MDR$ |         从`MAR`的地址中读取指令          | `MARo，MDRi` |
| $MDR → IR$    |              把指令送到`IR`              | `MDRo，IRi`  |
| $(PC)+4 → PC$ |                  `PC+4`                  | `+4`         |

- 取数阶段

| 微操作             | 描述                            | 微命令              |
| ------------------ | ------------------------------- | ------------------- |
| $(R(IR[21~25]))→Y$ | 把`rs`寄存器中的地址先存到`Y`中 | `R(IR(21~25))o，Yi` |

- 执行阶段

| 微操作                     | 描述                                 | 微命令            |
| -------------------------- | ------------------------------------ | ----------------- |
| $(Y)+Extended(IR(0~15))→Z$ | 把`(Y)`与`offset`偏移量求和并送入`Z` | `Yo，ALUi“+”，Zi` |

- 访存阶段

| 微操作                         | 描述                                                         | 微命令                         |
| ------------------------------ | ------------------------------------------------------------ | ------------------------------ |
| $(Z)→MAR、\\1→R、\\M(MAR)→MDR$ | 把暂存器`Z`中存储的运算地址送到`MAR`并发出读命令，并取出该地址的数据存到MDR | `Zo，MARi，MemR=1，MDRi，MARo` |

- 写回阶段

| 微操作             | 描述                            | 微命令     |
| ------------------ | ------------------------------- | ---------- |
| $MDR→R(IR(16~20))$ | 把`MDR`的数放入目标寄存器`rt`中 | `MDRo，Ri` |

- LW指令的数据通路
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/e751bbe8e91e4af6a30b3e90ca2b4132.png" width="100%" alt="window" /> </div>
> lw 访存指令需要使用的操作数包括变址寄存器 rs、目的寄存器 rt 和 16 位地址偏移量 imm16，将指令字中的 rs 字段仍然送入寄存器堆的 R1# 端；将目的寄存器字段 rt 送入寄存器堆的 写寄存器编号端 W#；另外要将 16 位立即数 imm16 通过符号扩展单元转换成 32 位后送入 ALU， 与变址寄存器 rs 的值相加形成最终的访存地址后读取数据存储器中的数据并送入寄存器堆写数据 端口 WD。如图所示为 lw 指令操作的部分数据通路，其数据通路涉及的功能部件包括指令存储器、寄存器堆、符号扩展单元、ALU、数据存储器等，需要注意的是 lw 指令中 rt 字段变成了 目的寄存器。寄存器堆的写使能控制信号 RegWrite 应设置为 1，用于控制数据写回；AluOp 应 该设置为加法操作；而数据存储器写使能控制信号 WE 应该为 0，用于控制存储器进行读操作。

### 3.4 SW指令的位操作定义

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/26ee6b5be7654c7eae4f3744820857f1.png" width="100%" alt="window" /> </div>


- 取指阶段

| 微操作        |                   描述                   | 微命令       |
| ------------- | :--------------------------------------: | ------------ |
| $(PC)$ | `PC→Bus`,`Bus→MAR`,取当前指令地址`→MAR` | `PCo，MARi`  |
| $1 → R$       |                  读主存                  | `MemR=1`     |
| $M(MAR)→MDR$ |         从`MAR`的地址中读取指令          | `MARo，MDRi` |
| $MDR → IR$    |              把指令送到`IR`              | `MDRo，IRi`  |
| $(PC)+4 → PC$ |                  `PC+4`                  | `+4`         |

- 取数阶段

| 微操作            | 描述                            | 微命令             |
| ----------------- | ------------------------------- | ------------------ |
| $(R(IR[21~25])→Y$ | 把`rs`寄存器中的地址先存到`Y`中 | `R(IR(21~25)o，Yi` |

- 执行阶段

| 微操作                    | 描述                                 | 微命令            |
| ------------------------- | ------------------------------------ | ----------------- |
| $(Y)+Extended(IR(0~15)→Z$ | 把`(Y)`与`offset`偏移量求和并送入`Z` | `Yo，ALUi“+”，Zi` |

- 访存阶段

| 微操作                                                       | 描述                                                         | 微命令                             |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------------------- |
| $(Z)→MAR、\\(R(IR[16~20])→MDR、\\1→W、\\MDR→M(MAR" width="100%" alt="window" /> </div>$ | 把`Z`中计算的地址送至`MAR`，并把rt寄存器中的数据送到`MDR`，把`MDR`的数据写入主存 | `Zo，MARi，Ro，MemW=1，MDRi，MDRo` |
- SW指令的数据通路
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/74cfde7debe14848b48418143ebbc9b2.png" width="100%" alt="window" /> </div>
> sw 访存指令需要使用的操作数包括变址寄存器 rs、源寄存器 rt 和 16 位地址偏移量 imm16，将指令字中的 rs、rt 字段分别送入寄存器堆的 R1#、R2# 端；将 16 位立即数通过符号 扩展单元转换成 32 位后送入 ALU，与变址寄存器 rs 的值相加后形成最终的主存地址；将从寄 存器堆读出的 rt 寄存器的值送入数据存储器写数据端口 WD。如图所示为 sw 指令的数据通路。 寄存器堆不需要写入，所以 RegWrite 设置为 0；AluOp 应设置为加法操作；而数据存储器写使 能控制信号 MemWrite 应该为 1，用于控制存储器进行写操作。

###  补充-混合型数据通路
- 支持 R 型运算指令和访存指令的混合数据通路
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/734c7445298d4941bb072ea22041d415.png" width="100%" alt="window" /> </div>
>	访存指令数据通路中寄存器堆写寄存器编号端口 W#、写数据端口 WD 的输入来源，ALU 第二个操作数的输入来源与 R 型运算类指令数据通路均不同。为了将不同的数据通路统一到同 一个电路中以支持两种不同类型的指令，可在有多个输入来源的端口处增加多路选择器，从而 得到如图所示的混合数据通路。
>	​每增加一个多路选择器就会额外引入一个控制信号，这里分别增加了 RegDst、AluSrc、 MemToReg 三个控制信号。其中 RegDst 用于决定指令字中的 rt、rd 哪个字段作为目的寄存器进 行写入；AluSrc 用于从寄存器或立即数扩展值中选择一个操作数送入 ALU；MemToReg 用于从 ALU 的运算结果或主存访问数据中选择一路写回寄存器堆。通过设置这些控制信号的值就可以形成适合不同指令的数据通路，这些控制信 号都应该由操作控制器根据指令译码自动生成。


### 3.5 J指令的位操作定义

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/deea39b282a7416b9ca9db6845998bab.png" width="100%" alt="window" /> </div>


- 取指阶段

| 微操作        |                   描述                   | 微命令       |
| ------------- | :--------------------------------------: | ------------ |
| $(PC)$ | `PC→Bus`,`Bus→MAR`,取当前指令地址`→MAR` | `PCo，MARi`  |
| $1 → R$       |                  读主存                  | `MemR=1`     |
| $M(MAR)→MDR$ |         从`MAR`的地址中读取指令          | `MARo，MDRi` |
| $MDR → IR$    |              把指令送到`IR`              | `MDRo，IRi`  |
| $(PC)+4 → PC$ |                  `PC+4`                  | `+4`         |

- 执行阶段

| 微操作             | 描述               | 微命令 |
| ------------------ | ------------------ | ------ |
| ${PC,IR[0~25]}→PC$ | 计算得到跳转后的PC | PCi    |
- 无条件跳转指令的数据通路
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/94451d722b71468b8c74a4df307d5801.png" width="100%" alt="window" /> </div>
### 3.6 BEQ指令的位操作定义
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/0869001751eb43d48e10b2cbc1cd5cc0.png" width="100%" alt="window" /> </div>
- 有条件跳转指令的数据通路
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/b91a0330e5194cd4aaeb24a9815da438.png" width="100%" alt="window" /> </div>
> 条件分支指令是否发生分支跳转取决于两个操作数的比较情况，为此，条件分支指令数据通路需要同时完成计算分支目标地址和比较寄存器内容的工作。如图所示为 beq 指令的数据 通路。这里 beq 指令会译码生成条件分支指令译码信号 Branch，将其与 ALU 的运算结果标志 equal（两数相等）进行逻辑与后生成分支跳转信号 BranchTaken，BranchTaken 用于选择 PC 的 数据来源。

## 🫐4 微操作节拍的划分与微指令的确定

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/5368915c40ce4b45b5b02ae20445c102.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/3d946c2d31304d7296b296429b40a139.png" width="100%" alt="window" /> </div>


### 4.1 取指阶段微操作节拍划分与微指令的确定

> 在取指阶段各指令微操作格式相同

| 节拍 | 微操作                              | 说明    |
| ---- | ----------------------------------- | ------- |
| T0   | $PC →MAR , 1 → R$                   | 微指令1 |
| T1   | $Ad(CMDR)→CMAR$                     |         |
| T2   | $M(MAR)→ MDR , (PC)+1 → PC$         | 微指令2 |
| T3   | $Ad(CMDR)→ CMAR$                    |         |
| T4   | $MDR → IR , OP(IR)→$ 微地址生成部件 | 微指令3 |
| T5   | 微地址生成部件 $→ CMAR$ 下地址      |         |

### 4.2 取数阶段微操作节拍划分与微指令的确定

| 节拍 | 微操作            | 说明    |
| ---- | ----------------- | ------- |
| T0   | $(R(IR[21~25])→Y$ | 微指令4 |
| T1   | $Ad(CMDR)→ CMAR$  |         |

### 4.3 执行阶段微操作节拍划分与微指令的确定

> 在执行（运算）阶段各指令微操作格式不同

- ADD指令

| 节拍 | 微操作              | 说明    |
| ---- | ------------------- | ------- |
| T0   | $(Y)+R(IR(16~20)→Z$ | 微指令5 |
| T1   | $Ad(CMDR)→ CMAR$    |         |

- SUB指令

| 节拍 | 微操作              | 说明    |
| ---- | ------------------- | ------- |
| T0   | $(Y)-R(IR(16~20)→Z$ | 微指令6 |
| T1   | $Ad(CMDR)→ CMAR$    |         |

- LW指令

| 节拍 | 微操作                    | 说明    |
| ---- | ------------------------- | ------- |
| T0   | $(Y)+Extended(IR(0~15)→Z$ | 微指令7 |
| T1   | $Ad(CMDR)→ CMAR$          |         |

- SW指令

| 节拍 | 微操作                    | 说明    |
| ---- | ------------------------- | ------- |
| T0   | $(Y)+Extended(IR(0~15)→Z$ | 微指令7 |
| T1   | $Ad(CMDR)→CMAR$           |         |

- J指令

| 节拍 | 微操作             | 说明    |
| ---- | ------------------ | ------- |
| T0   | ${PC,IR[0~25]}→PC$ | 微指令8 |
| T1   | $Ad(CMDR)→ CMAR$   |         |

### 4.4 访存阶段微操作节拍划分与微指令的确定

- LW指令

| 节拍 | 微操作           | 说明     |
| ---- | ---------------- | -------- |
| T0   | $(Z)→MAR，1→R$   | 微指令9  |
| T1   | $Ad(CMDR)→ CMAR$ |          |
| T2   | $M(MAR)→ MDR$    | 微指令10 |
| T3   | $Ad(CMDR)→ CMAR$ |          |

- SW指令

| 节拍 | 微操作                                            | 说明     |
| ---- | ------------------------------------------------- | -------- |
| T0   | $(Z)→MAR，\\(R(IR[16~20])→MDR，\\1→W$             | 微指令11 |
| T1   | $Ad(CMDR)→ CMAR$                                  |          |
| T2   | $MDR →M(MAR" width="100%" alt="window" /> </div>$ | 微指令12 |
| T3   | $Ad(CMDR)→ CMAR$                                  |          |

### 4.5 写回阶段微操作节拍划分与微指令的确定

- ADD指令

| 节拍 | 微操作            | 说明     |
| ---- | ----------------- | -------- |
| T0   | $(Z)→R(IR(11~15)$ | 微指令13 |
| T1   | $Ad(CMDR)→ CMAR$  |          |

- SUB指令

| 节拍 | 微操作            | 说明     |
| ---- | ----------------- | -------- |
| T0   | $(Z)→R(IR(11~15)$ | 微指令13 |
| T1   | $Ad(CMDR)→ CMAR$  |          |

- LW指令

| 节拍 | 微操作            | 说明     |
| ---- | ----------------- | -------- |
| T0   | $MDR→R(IR(16~20)$ | 微指令14 |
| T1   | $Ad(CMDR)→ CMAR$  |          |

## 🥖5 处理器结构设计框图及功能描述
### 5.1 简单CPU模型

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/e7d7794aa8f54722b4dd1bb858451bda.png" width="100%" alt="window" /> </div>
#### 5.1.1 CPU 中的主要寄存器
- 程序计数器
程序计数器（Program Counter，PC）保存将要执行的指令的字节地址，Intel x86 系列中称为指令指针寄存器（Instruction Pointer，IP）。PC 位宽与主存地址总线位宽相同。CPU 取指令时，会利用 PC 的内容作为地址访问主存，并将从主存取出的指令字送入指令寄存器中，然后还需要修改 PC 的值以形成下一条指令的地址。当程序顺序执行时，PC 的新值等于 PC 值加上当前指令的字节长度，可以通过简单的加法器实现。注意变长指令系统中指令的字节长度需要指令译码后才能确定；当程序出现分支跳转时，用分支指令提供的分支地址修改 PC 的值，形成跳转后的新指令地址。

- 存储器地址寄存器
存储器地址寄存器（Memory Address Register，AR）也可简称为地址寄存器，在 CPU 中AR 通常用来保存 CPU 访问主存的单元地址，无论 CPU 是取指令还是存取数据，都必须先将要访问地址送入 AR，直到读写操作完成。AR 位宽和主存地址总线位宽相同。注意 AR 并不是必需的，部分计算机中可直接将访存地址加载在地址总线上实现访存。

- 存储器数据寄存器
存储器数据寄存器（Memory Data Register，DR）也可简称为数据寄存器，在 CPU 中 DR 用于存放从主存中读出的数据或准备写入主存的数据，其数据位宽与机器字长相同。作为 CPU 和主存之间的缓冲寄存器也可用于存放运算器 ALU 的操作数、运算结果或中间结果，以减少访问主存的次数，具体见图中 DR 与 ALU 输入输出端之间的通路。同样，DR 作为存储器的访问接口也不是必需的，具体与 CPU 结构有关。

- 指令寄存器
指令寄存器（Instruction Register，IR）用于保存当前正在执行的指令。从主存中取出的指令字存放在 IR 中，其位宽和指令字相同。指令字由指令译码器（ID）翻译成若干个指令译码信号（每一个指令译码信号表示一条不同的指令，同一时刻只有一个信号有效）。指令字中的地址码部分由地址生成逻辑对寻址方式进行译码并生成目标地址或数据，根据寻址方式的不同将目标地址送入程序计数器 PC、地址寄存器 AR 或运算部件。有的计算机将指令寻址方式暗含在操作码字段中，有的计算机将操作码和地址码一并送入指令译码器，有的计算机将操作码和地址码一并送入地址生成逻辑，以决定地址码的作用。操作控制器根据指令译码信号生成最终的
控制信号序列控制各功能部件进行相应动作。

- 通用寄存器组
通用寄存器组（General Registers，GR）是指运算器内部的若干寄存器，又称寄存器堆；通用的含义是指这些寄存器的功能有多种用途，可作为 ALU 的累加器、变址寄存器、基址寄存器、地址指针、数据缓冲器，用于存放操作数、中间结果以及各种地址信息等。在 Intel x86 指令集中这些寄存器为 EAX、EBX……EDX 等，在 MIPS 32 指令集中这些寄存器为 $0 ～ $31，这些寄存器都对程序员可见，每个寄存器均有对应的地址编号，寄存器地址由指令字中的地址码部分提供。增加通用寄存器的数量，既可减少访问主存的次数，从而提高 CPU 的处理效率，又可以方
便汇编编程以及编译器生成代码

- 程序状态字寄存器
程序状态字寄存器（Program Status Word/Register，PSW/PSR）用于保存由算术运算指令、逻辑运算指令、测试指令等建立的各种条件标志。常见的状态信息包括进位标志（C）、溢出标志（V）、结果为负数标志（S）及结果为零标志（Z）等，通常条件分支指令利用 PSW 的值实现分支条件。另外程序状态字寄存器还可用于保存中断和系统工作的状态信息，以便 CPU 能及时了解计算机运行的状态，从而便于控制程序。不同类型的计算机可能设置不同的条件标志位和状态信息。Intel x86 指令集中状态寄存器为 EFLAGS，MIPS 指令集中没有状态寄存器，所以其条件分支指令与 x86 指令有较大区别。CPU 中的寄存器的具体设置与指令集以及具体实现方式有较大关系，其中 AR、DR、IR 寄存器并不是必需的，另外运算器内部的通用寄存器组 GR 和程序状态字寄存器 PSW 属于用户可见存储器，在汇编编程时可以直接使用。其他寄存器为控制器内部使用，用于控制指令的执行。

#### 5.1.2 操作控制器
操作控制器接收指令译码器（ID）送来的指令译码信息，与时序信号、条件及状态信息进行组合，形成各种具有严格时间先后顺序的操作控制信号（即微操作控制信号序列），并连接到计算机各功能部件的控制端，控制相应部件按指令的功能依序进行动作，从而实现指令的功能。CPU 执行指令的过程就是 CPU 控制信息流的过程，操作控制器是控制的决策机构，其产生的微操作控制信号序列就是控制流。信息流的控制就是将操作控制器生成的微操作控制信号序列送到各功能部件的控制门、多路选择器、触发器或锁存器处，依时间先后顺序打开或关闭某些特定的门电路，使数据信息按完成指令功能需要经过的路径——数据通路从一个功能部件传
送到另一个功能部件，实现对数据加工处理的控制。
### 5.2 微程序控制器
#### 5.2.1基本概念
- 微命令与微操作:

​	控制部件向执行部件发出的各种控制命令称为微命令，执行部件收到微命令后所进行的操 作称为微操作。图 6.8 所示的由控制器产生的 PCin、PCout、IRin、RegDst、ADD、Rin、Rout 等控 制信号就属于微命令。收到微命令后，PC、IR、多路选择器、运算器、寄存器堆等执行部件会 执行相应的微操作，如 PC 写入新的地址、IR 接收新指令、多路选择器根据选择端的值选择对应 的输入输出等。

​	其中相容性微操作是指能同时或在同一个机器周期内并行执 行的微操作，不能在同一个机器周期并行执行的微操作就是互斥性微操作。

> 信号 Read、Write 就属于互斥性微操作，所有内总线的输出控制信号 PCout、DRout、Zout、DRout、 IR(A" width="100%" alt="window" /> </div>out、IR(I" width="100%" alt="window" /> </div>out、Rout 等都是互斥性微操作，运算器的运算控制信号 ADD、+4、SUB 等也属于 互斥性微操作；从总线向寄存器锁存数据的使能信号 PCin、ARin、IRin、Xin、Rin 等就属于相容性微操作。

- 微指令与微程序

​	在计算机的一个机器周期中，一组实现一定操作功能的相容性微命令称为微指令。这些微 命令组合产生的一组控制信号，控制执行相应的一组微操作，实现一条指令的部分功能。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/1bbbf53483e041219c9116b3b0420e6f.png" width="100%" alt="window" /> </div>
> 微指令包括操作控制字段和顺序控制字段两部分。其中操作控制字段是主体，由若干微命 令位组成，每一位均对应表中的一个微操作控制信号，有多少个微操作控制信号，这里就对 应有多少个比特位；微指令是否含某个微命令，由对应位的状态 1 或 0 决定。微程序控制器向 执行部件发出的微命令就是通过微指令的操作控制字段发出的

​	实现一条指令功能的若干条微指令的集合称为微程序，微程序中多条微指令的先后关系由微指令格式中的顺序控制字段决定。

> 顺序控制字段包括判别测试字段和下址字段两部分。判别 测试字段（图中 P0 ～ P2）指出微指令执行过程中需要测试的外部条件，如是否要根据指令译码 进行微程序分支、进位、运算结果是否为零、是否是当前微程序的最后一条微指令等。下址字 段存放的是下条微指令的地址，位宽与微程序规模有关，最终是否按照该地址执行微程序与判 别测试结果有关。　

#### 5.2.2微程序控制器组成原理
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/5c53b070cbbf412d86f41139e4a8cc8b.png" width="100%" alt="window" /> </div>
- 控制存储器

​	控制存储器用于存放全部指令的所有微程序。控制存储器的字长等于微指令的长度，其存 储容量取决于指令系统，即等于所有指令的微程序包含的微指令数量。从控制存储器中取出的 数据就是微指令字，微指令字包括操作控制字段、判别测试字段、下址字段 3 部分。操作控制 字段经控制存储器取出后通过控制总线传输到所有执行部件的控点，控制相应部件进行适当的 微操作；判别测试字段用于实现地址逻辑转移；下址字段用于指示即将访问的下一条微指令的 地址。注意图中下方给出的微指令字只是用来表示指令格式的，并不是一个寄存器部件，它用 于表示微指令字中不同字段送往不同部件

- 微地址

​	微地址寄存器 μAR 为控制存储器提供微指令地址，初始化时为 0，所以控制存储器 0 号单 元应该为取指令微程序的第一条微指令，这样系统上电复位时计算机就可以访问控制存储器中的 取指微程序并开始取指令的操作。μAR 输入来源为地址转移逻辑的输出。它靠时钟控制其地址 更新，每一次时钟控制端的触发都会重新锁存新的微地址，从而取出并执行下一条微指令。在 三级时序中，这个时钟控制端应在机器周期的最后一个节拍结束时触发；在现代时序中这个时 钟控制端应该在当前时钟周期结束时触发。如果 CPU 中需要时序配合的控制信号是上跳沿有效， 那么这里的时钟控制端就应该是下跳沿触发。

- 地址转移逻辑

​	地址转移逻辑用于产生后续地址（下一条微指令的地址）。地址转移逻辑根据指令字的译 码情况、外部状态条件、微指令判别测试字段、下址字段等共同决定微地址寄存器的输入，生 成后续微指令的地址并送入 μAR，时钟触发到来时 μAR 更新为后续地址的值。后续微指令地址 形成常用的方法有下址字段法和计数器法。

### 5.3 MIPS处理器的流水线设计方案
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/495650edd62d4c7a965ca7eb8414641b.png" width="100%" alt="window" /> </div>
- 取指令
>如图：程序第一条指令 lw 指令进入 IF 段取指令的示意图，lw 指令在当前时钟节拍所使用的数据通路用深色表示，lw 指令字由程序计数器 PC 提供的地址访问指 令存储器得到，并将指令存储器 RD 输出端的 lw 指令字送 IF/ID 流水寄存器输入端；另外 程序计数器 PC 的值与 4 相加形成顺序指令地址 PC+4，送 PC 输入端以便下一个时钟周期 可以取出下一条指令。注意虽然 lw 指令在后续功能段并不会使用 PC+4，但 PC+4 还是会 传送给 IF/ID 流水寄存器，以备其他指令（如 beq）使用。流水线各功能段并不区分指令的 功能，所有数据信息和操作控制信号都来自段首的流水寄存器输出，所以只要是后续功能 段有可能要用到的数据和控制信号都要向后传递。时钟到来时指令字将锁存在 IF/ID 流水 寄存器中，同时 PC 更新为 PC+4 的值，lw 指令进入 ID 段，同时 IF 段取出下一条指令 sw。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/7133b7779c224d14b1dc5b136fc9ea95.png" width="100%" alt="window" /> </div>
- 指令译码、取操作数
> 如图： lw 指令进入 ID 段译码的示意图，具体数据通路用 深色表示，ID 段由操作控制器根据 IF/ID 流水寄存器中的指令字生成以后各段所需要的操 作控制信号并向后传输，具体见图 7.8；另外 ID 段还会根据指令字中的 rs、rt 字段读取寄 存器堆中的 rs 和 rt 寄存器的值 RS、RT；符号扩展单元会将指令字中的 16 位立即数符号扩 展为 32 位；多路选择器根据指令字生成指令可能的写寄存器编号 WriteReg#（有些指令并不需要写寄存器）。这 4 个数据连同顺序指令地址 PC+4 一起传输给 ID/EX 流水寄存器，时 钟到来时这些数据信息连同操作控制器产生的操作控制信号都会锁存在 ID/EX 流水寄存器 中，lw 指令进入 EX 段，同时 sw 指令进入 ID 段、beq 指令进入 IF 段。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/ef95911998ed4c948fa39bcf73518b75.png" width="100%" alt="window" /> </div>
- 执行或访存地址运算：
> 如图：lw 指令进入 EX 段的示意图，具体数据通路用深 色表示。对于 lw 指令来说，EX 段主要用于计算访存地址，将 ID/EX 流水寄存器中的 RS 的值与符号扩展后的立即数相加得到访存地址送 EX/MEM 流水寄存器；如果是 beq 指令 EX 段还需要计算分支目标地址，生成分支跳转信号 BranchTaken。ID/EX 流水寄存器中 RT 的值会在 MEM 段作为写入数据使用，所以 RT 的值会作为写入数据 WriteData 送 EX/MEM 流水寄存器；另外 ID/EX 流水寄存器中的写寄存器编号 WriteReg#也将直接传送给 EX/MEM 流水寄存器。同样时钟到来后这些数据信息连同后段所需要的操作控制信号都会锁存在 EX/MEM 流水接口中的寄存器中，lw 指令进入 MEM 段，sw、beq、add 指令分别进入 EX、 ID、IF 段。


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/331af39339a343af82f025b3879a058e.png" width="100%" alt="window" /> </div>
- 存储器访问
> 如图：为 lw 指令进入 MEM 段的示意图，具体数据通路用深色表示。 该阶段功能比较单一，主要根据 EX/MEM 流水寄存器中锁存的 ALU 运算结果---访存地址 和写入数据对于存储器进行读或写操作，EX/MEM 流水寄存器中的 ALU 运算结果、 WriteReg#、数据存储器读出的数据都会送 MEM/WB 流水寄存器输入端，同样时钟到来后 这些数据信息连同后段所需要的操作控制信号都会锁存在 MEM/WB 流水寄存器中，lw 指 令进入 WB 段，sw、beq、add、addi 指令分别进入 MEM、EX、ID、IF 段，此时指令流水线充满。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/e9d934f4252f40b5adeb97cd521e8761.png" width="100%" alt="window" /> </div>
- 结果写回
> 如图：为 lw 指令进入 WB 段的示意图，具体数据通路用深色表示。 WB 段从 MEM/WB 流水寄存器中选择 ALU 运算结果或内存访问数据写回到寄存器堆指定 寄存器 WriteReg#中，时钟到来时寄存器堆会完成数据写入，lw 指令离开流水线。注意此 时 sw 指令也进入了最后阶段 MEM 段，同时 beq 指令也进入了最后阶段 EX 段，同一时刻 实际上有 3 条指令执行完毕，当然这些指令即使执行完成也需要在流水线中继续向后传递 直至 WB 段。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/274812fb05964a1d8873884e78e5d8eb.png" width="100%" alt="window" /> </div>







##  🥕 6 微程序设计
> 微命令编码方法：因为一共采用了17个微操作，故种类较少，采用直接编码的方式。

> 	直接表示法：直接表示法的基本思想是：将微指令操作控制字段的每个二进制位定义为一个微命令，用“1”或“0”表示相应的微命令的“有”或“无”；一条微指令从控制存储器中取出时，它所包含的微命令可直接用于控制数据通路中的执行部件。这种方法的优点是简单、微操作的并行能力强、操作速度快；缺点是微指令过长，一般来说，有多少个微命令，微指令的操作控制字段就需要多少位。较为复杂的计算机系统微命令可能有上百个，此时就需要采用其他方法来缩短微指令字。 
### 6.1 控制字段

> 因为一共采用了17个微操作，故种类较少，采用直接编码方式。

| 比特位的位置（从左向右） | 微操作                                            |
| ------------------------ | ------------------------------------------------- |
| 1                        | $(PC)→MAR$                                        |
| 2                        | $(PC)+1 → PC$                                     |
| 3                        | $M(MAR)→ MDR$                                     |
| 4                        | $MDR → IR$                                        |
| 5                        | $OP(IR)→$ 微地址生成部件                          |
| 6                        | $MDR →M(MAR" width="100%" alt="window" /> </div>$ |
| 7                        | $(Z)→MAR$                                         |
| 8                        | $MDR→R(IR(16~20)$                                 |
| 9                        | $(Z)→R(IR(11~15)$                                 |
| 10                       | $(Y)+Extended(IR(0~15)→Z$                         |
| 11                       | $(Y)+R(IR(16~20)→Z$                               |
| 12                       | $(Y)-R(IR(16~20)→Z$                               |
| 13                       | $(R(IR[21~25])→Y$                                 |
| 14                       | ${PC,IR[0~25]}→PC$                                |
| 15                       | $(R(IR[16~20])→MDR$                               |
| 16                       | $1→R$                                             |
| 17                       | $1→W$                                             |

### 6.2 下地址字段与微指令序列的确定
> 本次设计32位MIPS模型机微指令
> 考虑到有17个微操作，可以设计操作控制字段22位，顺序控制之端10位包括3位判别测试位和7位下地址字段。

- 取指阶段

| 微指令序号 | 操作控制              | 下地址             |
| ---------- | --------------------- | ------------------ |
| 1(0000)    | 1000 0000 0000 0001 0 | 0001               |
| 2(0001)    | 0110 0000 0000 0000 0 | 0010               |
| 3(0010)    | 0001 1000 0000 0000 0 | 0011（有可能跳转） |

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/a88a639a1d8e4e6d8a04fe5b6ef0614e.png" width="100%" alt="window" /> </div>


- 取数阶段

| 微指令序号 | 操作控制              | 下地址             |
| ---------- | --------------------- | ------------------ |
| 4(0011)    | 0000 0000 0000 1000 0 | 0100（有可能跳转） |

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/bf9708d0644649fdaa34048a60ac2c18.png" width="100%" alt="window" /> </div>


- ADD指令

| 微指令序号 | 操作控制              | 下地址 |
| ---------- | --------------------- | ------ |
| 5(0100)    | 0000 0000 0010 0000 0 | 0101   |
| 13(0101)   | 0000 0000 1000 0000 0 | 0000   |

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/6e7036b15f9b47fb9ee515b4188890c6.png" width="100%" alt="window" /> </div>


- SUB指令

| 微指令序号 | 操作控制              | 下地址 |
| ---------- | --------------------- | ------ |
| 6(0110)    | 0000 0000 0001 0000 0 | 0111   |
| 13(0111)   | 0000 0000 1000 0000 0 | 0000   |


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/a0b979a06a864f11a8ffddc850863d12.png" width="100%" alt="window" /> </div>

- LW指令

| 微指令序号 | 操作控制              | 下地址 |
| ---------- | --------------------- | ------ |
| 7(1000)    | 0000 0000 0100 0000 0 | 1001   |
| 9(1001)    | 0000 0010 0000 0001 0 | 1010   |
| 10(1010)   | 0010 0000 0000 0000 0 | 1011   |
| 14(1011)   | 0000 0001 0000 0000 0 | 0000   |

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/c3900ea716f44b1eb41eab1524aa7535.png" width="100%" alt="window" /> </div>


- SW指令

| 微指令序号 | 操作控制              | 下地址 |
| ---------- | --------------------- | ------ |
| 7(1100)    | 0000 0000 0100 0000 0 | 1101   |
| 11(1101)   | 0000 0010 0000 0010 1 | 1110   |
| 12(1110)   | 0000 0100 0000 0000 0 | 0000   |

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/12bac8e66254459880b26a69594f5c31.png" width="100%" alt="window" /> </div>


- J指令

| 微指令序号 | 操作控制              | 下地址 |
| ---------- | --------------------- | ------ |
| 8(1111)    | 0000 0000 0000 0100 0 | 0000   |



<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/2fea60ddd3a049a38f6912baec2f39dc.png" width="100%" alt="window" /> </div>







