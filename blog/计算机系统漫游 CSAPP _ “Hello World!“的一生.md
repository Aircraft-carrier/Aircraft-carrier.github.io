﻿﻿<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/9e51e41373c642189570c6eb19757fea.png" width="100%" alt="window" /> </div>


# 第1章 概述🍉

## 1.1 Hello简介

​	hello 的 P2P 过程是 gcc 调用 cpp(预处理器" width="100%" alt="window" /> </div>/cc1(编译器" width="100%" alt="window" /> </div>/as(汇编器" width="100%" alt="window" /> </div>/ld(连接器" width="100%" alt="window" /> </div>，将 C 语言源文件预处理、编译、汇编、链接，最终生成可执行文件保存在磁盘中，最后得以作为进程在计算机系统中运行。

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/91637de4f77b456da8f61102de2b8e99.jpeg)

​	hello 的 020 是 hello 可执行目标程序从运行到最后被回收的过程。在 Shell 中运行该程序时，Shell 调用 fork 函数创建子进程，创建完毕后，操作系统内核提供的 execve 函数会创建虚拟内存的映射，即 mmp，然后开始加载物理内存，进入到 main 函数当中执行相关的代码，打印出信息。在进程中，TLB、4级页表、3级 Cache，Pagefile等等设计会加快程序的运行。程序运行完成后，Shell 回收子进程，操作系统内核删除相关数据结构，释放其占据的资源。至此，hello 的一生就结束了。

## 1.2 环境与工具

### 1.2.1 硬件环境

CPU：IntelR CoreTM i7-10875H CPU @ 2.30GHz 2.30 GHz

RAM：16.0 GB

### 1.2.2 操作系统

Windows 11 21H2、Windows Subsystem for Linux2 Ubuntu 20.04 LTS

### 1.2.3 开发工具

vscode、vim、gcc、gdb、edb

## 1.3 中间结果

为编写本论文，生成的中间结果文件以及它们的作用如下：

|      文件       | 作用                  |
| :-------------: | --------------------- |
|     hello.c     | 源代码                |
|     hello.i     | 预处理后的代码        |
|     hello.s     | 汇编代码              |
|     hello.o     | 可重定位目标文件      |
| hello.o.elf.txt | hello.o的ELF          |
|    hello.o.s    | hello.o反汇编后的代码 |
|      hello      | 链接后的可执行文件    |
|  hello.elf.txt  | hello的ELF            |
|   obj_hello.s   | hello的反汇编代码     |

## 1.4 本章小结

本章大致介绍了 hello 的 P2P 和 020 过程，描述了使用的环境与工具，并列出了生成的中间结果文件以及它们的作用



# 第2章 预处理🥑

## 2.1 预处理的概念与作用

### 2.1.1 什么是预处理

​	在编译和链接 hello.c 之前，需要对源文件进行一些文本方面的操作，比如文本替换、文件包含、删除部分代码等，这个过程叫做预处理，由预处理程序完成。

### 2.1.2 预处理的作用

​	预处理根据以字符 # 开头的命令，修改原始的 C 程序。比如我们初学 C 语言时记忆最深刻的代码：

```c
#include<stdio.h>
```

 它就利用了预处理：引用头文件。它告诉预处理器读取系统头文件 stdio.h 的内容，预处理器把它插入程序文本中。

## 2.2在Ubuntu下预处理的命令

 Linux 下使用 gcc 预处理的命令为：

```bash
gcc -E hello.c -o hello.i
```

-E 表示只激活预处理过程

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/7f2d1cd8d3e04a7795fc5cd4cfcee440.png" width="100%" alt="window" /> </div>


## 2.3 Hello的预处理结果解析

###  2.3.1 生成文件对比

使用 vscode 打开文件，hello.c 源程序只有24行，如下

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/0d535c6517a6451b8ef65c2a14ac270d.png" width="100%" alt="window" /> </div>


打开生成的 hello.i 文件，发现有 3057行，并且我们原始的main代码部分被放在最后

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/602568407f3848838dbcc5b36684c1f0.png" width="100%" alt="window" /> </div>


### 2.3.2 预处理后的文件解析

1. 外部库文件

   首先，开始部分有一系列外部库 .h 文件路径

   <div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/64ddbf5ac4f64674a86595217c96ef11.png" width="100%" alt="window" /> </div>


2. 数据类型名称替换

   <div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/ec595bfec9b648199e8f767dfabd35ba.png" width="100%" alt="window" /> </div>


3. 内部函数声明

   中间部分是很多内部函数的声明，包括系统内核提供的接口的封装：

   <div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/06a36d99df1c4a28bed8650776ae1e93.png" width="100%" alt="window" /> </div>


4. 主体代码

   而一直到最后，才是我们写的main函数代码部分，注意到此时已经没有注释代码存在了。

   <div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/b3c7c5aabaa74a47a8a788ec8df19c57.png" width="100%" alt="window" /> </div>


## 2.4 本章小结

​	本章介绍了 hello.c 的预处理过程，并分析了预处理的结果文件 hello.i。

​	从程序员的角度来说，利用宏定义指令可以让我们轻松写出可读性更好的代码，利用条件编译指令可以让我们更加方便快捷的调试代码。

​	从hello程序的角度来说，hello.c 是残缺的，不完整的，预处理阶段进行的头文件包含、宏替换、条件编译、注释去除、行连接补全了hello缺失的部分,打通了程序和系统的通信渠道，为后续的编译，汇编做准备。最终得以运行在操作系统的上下文中。

# 第3章 编译🥖

## 3.1 编译的概念与作用

### 3.1.1什么是编译

​	汇编语言是对硬件的抽象，而 C 语言又是对汇编语言的抽象，C 语言对人友好，但对机器并不友好。编译阶段正是将高级语言编写的源代码转换为计算机能够理解和执行的机器语言代码的过程在hello的人生中，编译代表着：把完整的代码 hello.i 翻译成对应的汇编语言程序 hello.s。

## 3.2 在 Ubuntu 下编译的命令

Linux下使用 gcc 编译的命令为：

```bash
gcc -S hello.i -o hello.s 
```

-S 表示只激活到编译过程

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/3698d5b611d64a53ad416c35c0057c6c.png" width="100%" alt="window" /> </div>


## 3.3 Hello的编译结果解析

 hello.i 编译生成了对应的汇编代码，在这一节中，我将对 C 语言中数据类型及各式操作如何编译到汇编代码中逐个解析

### 3.3.1 常量

1. 字符型常量

   <div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/572ebbe569e54065b67936a59f521bad.png" width="100%" alt="window" /> </div>


   printf 打印了一个字符串，这个字符串常量存在 .LC0 中：

   <div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/24e62b56a61d4127800a10b942a56a5b.png" width="100%" alt="window" /> </div>


   在汇编语言中，`.LC0` 是一个标签，用来标识某个位置或数据的引用点。这里的`.LC0` 是一个用来表示字符串常量的标签。接下来的`.string`指令用来定义一个字符串常量，字符串常量是被双引号包围的字符序列，在这里包含了一些转义字符和非 ASCII 字符。最后的`.align 3`指令是用来将当前位置对齐到一个特定的字节边界。这样的对齐操作有时用于优化内存访问速度。

   <div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/6a6bbf23fcbc44aaa1372fdbe47ee3dd.png" width="100%" alt="window" /> </div>


   printf 打印了一个字符串，这个字符串常量存在 .LC1中

   <div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/d435331c4ca84f19b36ab7b6df18e13b.png" width="100%" alt="window" /> </div>


2. 其他常量

   还有一些其它常量直接在汇编代码中以立即数的身份出现，例如这段代码，有一个整型常量5

   <div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/63a2414cbf184384b023894056bff674.png" width="100%" alt="window" /> </div>


   它对应的汇编代码如下：
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/c9c5f67ada464859a5ac250de02b202f.png" width="100%" alt="window" /> </div>

   

### 3.3.2 变量与运算

1. 局部变量

局部变量存储在寄存器或者栈中。

hello.c中有一个局部变量：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/87b3e1bee8374819ada1b8d602b4dbf1.png" width="100%" alt="window" /> </div>


i 是在一个 for 循环语句中作为循环变量，这段代码如下：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/c1fc985cbfe14f74b6aaa1fb990564d4.png" width="100%" alt="window" /> </div>


可以看到，i 存储在栈中。

### 3.3.3 数组/指针操作

main 函数的参数中，有一个字符串数组：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/9fcf1cc3e84442959f0ebaa6f4ab616a.png" width="100%" alt="window" /> </div>


其中，argc 是输入的参数的个数，也就是字符串数组 argv 中的元素个数

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/37a04f02ab894e0ca1b06a4019ef1f6b.png" width="100%" alt="window" /> </div>


找到其对应的汇编代码为：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/ae31b8fddf0e45bdbfebe870ded51ac3.png)


​	`%rbp` 通常用作基地址指针，先将 `-32(%rbp)` 处的值加载到 `%rax` 寄存器中，这个值为`argv`的首地址。再将 `%rax` 寄存器中的值加上32，32为了访问`argv`数组第5个指针元素的偏移量处的值。将`argv[4]`从内存中取出并保存在`%rdi`中作为代用`atoi`函数的参数。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/0e0fde12332d4c698c1d8cc5f827032c.png" width="100%" alt="window" /> </div>


​	同理这个`printf`的请求也用到了`argv`数组的参数

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/7e14e2937d42433b859471a829b164df.png" width="100%" alt="window" /> </div>


### 3.3.4 控制转移

​	同样还是以上述那段 `for` 循环的代码为例，循环变量 `i` 从 0 开始，每次循环都要加 1，并在循环开始判断 `i<10`，对应的汇编代码就是用 cmpl 指令，判断 i 是否小于等于 9，如果是，则继续执行循环体中的内容，如果不是则跳出循环。

### 3.3.5 函数调用与返回

1. `main` 函数

   ​	在 C 语言中，`main` 函数是程序的入口点，是程序开始执行的地方。每个 C 语言程序必须有且只能有一个 `main` 函数。当程序运行时，操作系统会首先调用 `main` 函数，然后程序从 `main` 函数开始执行。

   `main` 函数有两种常见的形式：

   1. 基本形式：`int main()`
   2. 带参数的形式：`int main(int argc, char *argv[])`

   `hello`采用的是带参数的形式中，`main` 函数接受两个参数：`argc` 和 `argv`。这两个参数的作用是用来处理命令行参数。

   `hello`的调用是在`shell`中输入：

   ```bash
   ./hello ID Name PhoneNumbles Seconds
   ```

   - `argc`是一个整数，表示命令行参数的个数，包括程序名称本身。`hello`调用中`argc = 5`
   - `argv`是一个指向指针的指针，每个指针指向一个字符串，这些字符串是命令行参数的具体值，其中 `argv[0]` 存储的是程序的名称，`argv[1]`、`argv[2]` 等存储的是传递给程序的其他参数。`hello`调用中`argv[0] = "hello"`、`argv[1] = ID`…准确来说是字符串的首地址。函数运行过程中需要将参数进行合适的转换才能使用。

2. `printf` 函数

   ​	`printf` 函数的基本语法为：`int printf(const char *format, ...);`,`format` 参数是一个字符串，其中包含了要输出的格式化信息。这个字符串可以包含普通的字符和格式控制符（如 `%d`、`%f`、`%s` 等）。`...` 表示 `printf` 函数支持可变数量的参数。这些额外的参数会根据 `format` 字符串中的格式控制符进行替换

   ​	通过设置寄存器 `%rdi、%rsi、%rdx`和`%rcx` 的值来传入参数并调用,其中`%rdi`中存放`printf`的请求格式`.string	"Hello %s %s %s\n"`的地址即标签`.LC1(%rip)`，调用`printf`会依次用`argv[1]、argv[2]、argv[3]`来替换下`%s`，`argv[1]、argv[2]、argv[3]`分别存放在`%rsi、%rdx`和`%rcx`中。

3. `atoi` 和`sleep`函数

   ​	使用 `atoi` 函数的语法是 `int atoi(const char *str)`，其中 `str` 是要转换的字符串。函数会遍历字符串，跳过前导空格，并解析字符串中的数字字符，直到遇到非数字字符为止。函数会将解析得到的数字转换为整数，并返回结果。

   ​	`hello`中将`argv[4]`的首地址赋给 `%rdi` 调用，函数返回这个字符串转成的整数值，存放在字符串 `%eax`。用于做`sleep`调用的参数。

## 3.4 本章小结

​	本章介绍了从 hello.i 文件编译成 hello.s 文件的过程，以及原始的 .c 文件中各部分变量、常量、控制转移以及函数调用在汇编语言中是什么样子。

接下来，只需要将 hello.s 稍加改造（汇编），就能让操作系统、让机器读懂它

# 第4章 汇编🍤

## 4.1 汇编的概念与作用

​	所谓汇编，就是汇编器 (as) 将 hello.s 翻译成机器语言指令，把这些指令打包成可重定位目标程序的格式，并将结果保存在文件 hello.o 中，hello.o 是一个二进制文件。

## 4.2 在 Ubuntu 下汇编的命令

Linux 下使用 gcc 汇编的命令为：

```bash
gcc -C hello.s -o hello.o
```

-C 表示只激活到汇编过程

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/8ca1aea0e20a4c5faa6d304fc0939a49.png" width="100%" alt="window" /> </div>

## 4.3 可重定位目标elf格式

 hello.o 文件在 x86-64 Linux 和 Unix 系统中使用可执行可链接格式即 (ELF)，典型的 elf 可重定位目标文件格式如下：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/f694b5174562446b981e56eb3e275239.png" width="100%" alt="window" />

</div>

 </div>


### 4.3.1 ELF头

使用一下指令查看 ELF 头，并重定向到`elf.txt`：

```bash
 readelf -h hello.o > elf.txt
```

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/df6a9a16ea5e4a2db5e3ece753d91601.png" width="100%" alt="window" /> </div>


如图:

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/459d7523bfe7451cba95cd8c05a4cd7b.png" width="100%" alt="window" /> </div>


​	EFL 头以 16 字节的序列 Magic 开始，这个序列描述了生成该文件的系统的字的大小和字节顺序，ELF 头剩下的部分包含帮助链接器语法分析和解释目标文件的信息，其中包括 ELF 头的大小、目标文件的类型、机器类型、字节头部表（section header table）的文件偏移，以及节头部表中条目的大小和数量等信息。

根据提供的 ELF 头信息，我们可以得到以下分析：

1. Magic Number:
   - ELF 头的 `Magic`部分为 `7f 45 4c 46 02 01 01`，这是 ELF 文件的标识符，用于表示文件类型为 ELF 格式。
2. 类型和架构信息：
   - `Class` 指示 ELF 文件的位数，这里是 `ELF64`，表示文件为 64 位格式。
   - `Data` 字段指示数据存储的端序，这里是 `2's complement、little endian`，表示数据以补码形式存储，小端序排列。
   - `Type` 指示文件类型为 DYN，表示共享对象文件。
   - `Machine` 字段指示目标处理器架构为 `Advanced Micro Devices X86-64`，即 `x86-64` 架构。
4. 其他重要信息：
   - `Entry point address`：入口点地址为 `0x1100`，即程序执行的起始地址。
   - `Start of program headers`：程序头的起始位置相对于文件的偏移为 64 字节。
   - `Start of section headers`：段头表的起始位置相对于文件的偏移为 14928 字节。
   - Flags 为 0x0，标志位为 0。
   - `Size of this header`：当前头部的大小为 64 字节。
   - `Size of program headers`：程序头部的大小为 56 字节。
   - `Number of program headers`：程序头部的数量为 13。
   - `Size of section headers`：段头表的大小为 64 字节。
   - `Number of section headers`：段头表的数量为 31。
   - `Section header string table index`：段头字符串表索引为 30，表示段头表中字符串名称的索引。

​	从EFL头中获得程序的入口点 (entry point)信息，也就是程序运行时要执行的第一条指令的地址为 0x0，可以查看hello.o 的反汇编代码，程序运行时的第一条指令的地址确实为 `0x1100`

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/b7cc96fefe734ad1bd6ebc5783e007f5.png" width="100%" alt="window" /> </div>


反汇编指令：

```bash
objdump -d hello.o > hello_obj.txt
```

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/8a88a21f52084b9e9811e3257b18793c.png" width="100%" alt="window" /> </div>


​	在程序运行时，`_start` 程序是程序的入口点，也可以说是程序的启动代码。当操作系统加载可执行文件并执行时，操作系统会执行 `_start` 程序，这段代码负责初始化程序运行环境、设置栈、调用主函数 `main`，最终启动程序的执行。

`_start` 程序通常包括以下几个步骤：
1. 设置栈：`_start` 程序会设置程序运行时的栈，将栈顶指针初始化为合适的位置。
2. 初始化寄存器：`_start` 程序会初始化各个寄存器的值，包括传递参数、设置参数、设置返回地址等。
3. 调用 `main()`：`_start` 程序最终会调用程序的主函数 `main`，将控制权转移到主函数，程序的实际逻辑在主函数中执行。

### 4.3.2 节头部表

使用 以下命令查看节头部表：

```bash
readelf -S hello.o > SectionHeaders.txt
```

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/3961850432b545e1be2f4c03fcb3f986.png" width="100%" alt="window" /> </div>


如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/0adf2f5295314fd395885899ce7b5900.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/7d4334c0e3d04541acdfb4d4c67bb040.png" width="100%" alt="window" /> </div>


节头部表描述了 hello.o 中文件中各个节的语义，包括节的类型、位置和大小等信息。由于这是可重定位目标文件，所以每个节的地址都从 0 开始。

举例分析

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/72dd2e3b0dbf48eda5b20113d205ca0c.png" width="100%" alt="window" /> </div>


​	`[16]`：这表示这个节的索引号；`.text`：节的名称，这里表示这个节包含了代码段`PROGBITS`：表示这个节包含的是程序数据而非节头本身。`0000000000001100`：表示这个节在文件中的偏移地址，即节在文件中的起始位置相对于文件起始位置的偏移地址。这里可以看到代码节的偏移地址和前面的入口地址一致；`00001100`：表示这个节的虚拟地址；`0000000000000205`：表示这个节的大小，即这个节所占据的字节数。`0000000000000000`：表示这个节在文件中对齐的起始位置。`AX`：表示这个节的属性，`A` 表示可以分配空间，`X` 表示节包含可执行代码（参照`Key to Flags`可以看出）。

### 4.3.3 符号表

使用一下命令查看 `.symtab` 节中的 ELF 符号表

```bash
 readelf -s hello.o > symtab.txt
```

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/62db848e9cbd462e8edbad92677307a2.png" width="100%" alt="window" /> </div>


如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/5ffa11ec192745f8b52102513bdffa2b.png" width="100%" alt="window" /> </div>


<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/93a3560621804381856107361d6f6050.png" width="100%" alt="window" /> </div>


它存放在程序中定义和引用的函数和全局变量的信息。

举例分析：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/281a9f43f15e4b9993e953f02b74900b.png" width="100%" alt="window" /> </div>


1. `63`：这是符号的索引号，表示在符号表中的第 63 个符号。
2. `00000000000011e9`：这是符号的值，即符号在代码段中的地址或者符号的数值值。
3. `157`：这是符号的大小，表示符号占据的字节数。
4. `FUNC`：表示这个符号是一个函数。
5. `GLOBAL`：表示这个符号是全局符号，可以被其他文件访问。
6. `DEFAULT`：表示这个符号的可见性为默认，即在程序的其他部分可以访问到这个符号。
7. `16`：这是一个节的索引号，表示这个符号位于第 16 个节（`.text` 节）中。

综上所述：这个符号条目告诉我们关于 `main` 函数符号的信息：它是一个全局函数，在 `.text` 节中的地址为 `00000000000011e9`，大小为 `157` 字节，其他文件可以访问并调用这个函数。

### 4.3.4 重定位条目

使用一下命令查看 hello.o 的重定位条目：

```bash
 readelf -r hello.o > relocal
```

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/6163adc9b5f34649a93a85f01caa14e0.png" width="100%" alt="window" /> </div>


如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/7e24a07c9ac84bbfbf124e7be413638c.png" width="100%" alt="window" /> </div>


​	当汇编器生成 hello.o 后，它并不知道数据和代码最终将放在内存中的什么位置。它也不知道这个模块引用的任何外部定义的函数或者全局变量的位置。所以，无论何时汇编器遇到对最终位置未知的目标引用，它就会生成一个重定位条目，告诉链接器在将目标文件合并成可执行文件时如何修改这个引用。代码重定位条目放在 `.rela.plt` 中，已初始化数据的重定位条目放在 `.rela.dyn`中。

举例：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/382f800837414625962c9cb882ad1a1a.png" width="100%" alt="window" /> </div>


1. `000000003fb0`：（`Offset`）这是重定位的起始地址，即需要进行重定位的位置在文件中的偏移地址。

   <div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/2f510e988103432785a139eb82b0ed23.png" width="100%" alt="window" /> </div>


2. `000300000007`：这表示重定位条目的类型，`R_X86_64_JUMP_SLO` 是一个 X86_64 架构下的跳转槽重定位类型。

3. `0000000000000000`：这是 `printf` 函数的全局偏移地址（Global Offset Table）。

4. `printf@GLIBC_2.2.5`：这是需要进行重定位的符号，即 `printf` 函数，并指定了该函数在 GLIBC 2.2.5 版本的库中。

5. `+ 0`：这表示对 `printf` 函数进行重定位时的偏移量为 0。

综上所述，这个重定位条目告诉程序加载器，当程序被加载到内存中时，需要将位于 `0000000000000000` 处的 `printf@GLIBC_2.2.5` 符号引用的地址替换为正确的地址，以便程序正确调用 `printf` 函数。

## 4.4 Hello.o的结果解析

使用一下命令反汇编 hello.o，查看反汇编后的汇编代码与 hello.s 有何不同：

```bash
objdump -d -r hello.o
```

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/efa3bee284c4431bb5c3acb7990631d0.png" width="100%" alt="window" /> </div>


**不同点：**

分支跳转：在 hello.s 中，分支跳转的目标位置是通过 .L1、.L2 这样的助记符来实现的，而 hello.o中，跳转的目标位置是指令的地址。

函数调用：在 hello.s 中，call 后面的目标函数是它的函数名，而在 hello.o 中，call 的是目标函数的相对偏移地址。

## 4.5 本章小结

本章分析了汇编的过程，并分析了 ELF 头、节头部表、重定位节以及符号表。比较了 hello.s 和 hello.o 反汇编之后的代码的不同。

# 第5章 链接🍧

## 5.1 链接的概念与作用

​	链接是将各种代码和数据片段收集并组合成为一个单一文件的过程，这个文件可被加载到内存并执行。

​	链接器在软件开发中扮演着一个关键的角色，因为它使得分离编译成为可能。我们不用将一个大型应用程序组织为一个巨大的源文件，而是可以把它分解为更小、更好管理的模块，可以独立地修改和编译这些模块。当我们改变这些模块中地一个时，只需简单地重新编译它，并重新链接应用，而不必重新编译其他文件。即使对hello这样一个非常简单的小程序，链接的作用也是巨大的。

## 5.2 在Ubuntu下链接的命令

Linux下使用链接器 (ld" width="100%" alt="window" /> </div> 链接的命令为：

```bash
ld -o hello -dynamic-linker /lib64/ld-linux-x86-64.so.2 /usr/lib/x86_64-linux-gnu/crt1.o /usr/lib/x86_64-linux-gnu/crti.o hello.o /usr/lib/x86_64-linux-gnu/libc.so /usr/lib/x86_64-linux-gnu/crtn.o
```

## 5.3 可执行目标文件hello的格式

### 5.3.1 ELF头

查看 hello 的 ELF 头：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/3dcfc2ec3b2b468bb88034a1a5578d7d.png" width="100%" alt="window" />

</div>

 </div>


可以看到，程序的 `Type` 变成了 `EXEC (Executable file" width="100%" alt="window" /> </div>`，程序入口也分配了地址，为 0x401190

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/b33caab423364937b7d3a43402fcb60c.png" width="100%" alt="window" /> </div>


### 5.3.2 节头部表

链接器将各个文件对应的段都合并了，并且重新分配并计算了相应节的类型、位置和大小等信息

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/a5531d9195cd4b499d6ed31ec6b77b10.png" width="100%" alt="window" /> </div>

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/48279875ffe646ad9f4b71fed5663475.png" width="100%" alt="window" /> </div>


各个节的地址也从 0 开始进行了分配。可以看到 .text 节的起始地址为 0x4010f0，刚好和main函数的地址相同。
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/34720339af3f48f581c02e1c69af93cd.png" width="100%" alt="window" /> </div>


## 5.4 hello的虚拟地址空间

使用 edb 打开 hello，可以看到 hello 的虚拟地址起始为 0x401000  

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/f4709ffa3f414c9b93f5e1810c06c261.png" width="100%" alt="window" /> </div>


与 5.3 中的节头部表进行比对，比如 .data 起始于 0x404048，查看这个内存单元

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/8d6e2a13cfc44dca9ac68558c265be27.png" width="100%" alt="window" /> </div>


## 5.5 链接的重定位过程分析

使用 一下命令反汇编代码，查看两者之间的不同

```bash
objdump -d -r hello > hello_obj_ex.txt
```

### 5.5.1新增函数

如图，链接后，加入了很多需要用到的库函数，`puts, pintf, getchar, atoi, exit, sleep` 等

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/c95d97851bda4e96a2470950e6671514.png" width="100%" alt="window" /> </div>


### 5.5.2 新增节

如图，新增了 .init 节和 .plt 节

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/211edf5d046647cb97d99ea06c904547.png" width="100%" alt="window" /> </div>


### 5.5.3 新增代码 endbr64

可以观察到，由 hello 反汇编生成的代码中有一句出现的频率非常高，那就是 endbr64，几乎在每一个函数或者代码片段的开头都是这句代码，非常有意思。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/ddf66f02b15143f3bcc9b62928d3250b.png" width="100%" alt="window" /> </div>


其实这是 Intel 的 CET 技术，这个机制主要是用来对抗 ROP 攻击。我们在第 3 章学到，黑客可以利用缓冲区溢出来进行攻击，使程序执行黑客想要执行的程序，增加系统风险。而 CPU 和操作系统也采用了相应措施来避免这个风险：

- 栈随机化。这段程序分配的栈的位置在每次运行时都是随机的，这就使我们无法确定在哪里插入代码
- 限制可执行代码区域。它限制栈上存放的代码是不可执行的。

但是这些措施却无法阻挡 ROP 攻击。什么是 ROP 攻击呢？ROP：面向返回的程序设计，所谓 ROP 攻击就是黑客在已经存在的程序中找到特定的以 ret 结尾的指令序列为我们所用，称这样的代码段为 gadget，把要用到部分的地址压入栈中，每次 ret 后又会取出一个新的 gadget，于是这样就能形成一个程序链，从而实现黑客的目的。我喜欢将这种攻击方式称作“就地取材，拼凑代码”，如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/1a1e0d30ba1349168d1668f1a7f6a192.png" width="100%" alt="window" /> </div>


​	对于 ROP 攻击也能找到解决办法，就是每次在跳转后，检查这段代码是不是程序想要的代码，也就是 CET 技术。CET 通过编译器在合理的间接跳转 (call/jmp" width="100%" alt="window" /> </div> 中用新的指令做标记，新指令包含 endbr32 和 endbr64。程序每次执行跳转时，CPU 都会判断下一条指令是不是 endbr32/endbr64 指令，如果是则正常执行，如果不是，则会触发 #CP 异常。

这也就是每个代码段和函数开头都有一句 endbr64的原因了。

### 5.5.4 函数调用与跳转

由于hello文件已经是重定位后的可执行目标文件，所以每一个 call/jmp 语句的目标地址就是确切的虚拟地址。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/822107e010914333b9f5c5706cb1e5b8.png" width="100%" alt="window" /> </div>


## 5.6 hello的执行流程

当在 Shell 中运行 hello 时，Shell 会调用驻留在存储器中的加载器来运行它。当加载器运行时，它创建如图的内存映像

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/835392455d41454f8486c8e76fb9eafa.png" width="100%" alt="window" /> </div>


在 ELF 头部表的引导下，加载器将可执行文件的片复制到代码段和数据段。接下来加载器跳转到程序的入口点，也就是 _start 函数的地址。这个函数是在系统目标文件 ctrl.o 中定义的。_start 函数调用系统启动函数 __libc_start_main，该函数定义在 libc.so中。它初始化执行环境，调用用户层的 main 函数，处理 main 函数的返回值，并且在需要的时候把控制返回给内核。



## 5.7 Hello的动态链接分析

在进行动态链接前，首先进行静态链接，生成部分链接的可执行目标文件 hello。此时共享库中的代码和数据没有被合并到 hello 中。只有在加载 hello 时，动态链接器才对共享目标文件中的相应模块内的代码和数据进行重定位，加载共享库，生成完全链接的可执行目标文件。

比如查看 _GLOBAL_OFFSET_TABLE 的内容：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/b38756bc5bdc47eca8742b0aa2081370.png" width="100%" alt="window" /> </div>


在运行前：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/019f2889b4c94240979f295a373bd3e6.png" width="100%" alt="window" /> </div>


运行 dl_init 后：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/dd235d6a05c04217ab100c730dea614b.png" width="100%" alt="window" /> </div>


## 5.8 本章小结

本章详细介绍了 hello 的链接过程，比对链接后的 hello 与 hello.o 的不同，并拓展讲解了 endbr64 的作用，最后使用 gdb 工具逐行查看 hello 的运行过程。

至此，我们的 hello 就成为了一个具有完整躯体与精神的青年了，也是时候让他进入社会，成为操作系统中运行的进程！

# 第6章 hello进程管理🧉

## 6.1 进程的概念与作用

### 6.1.1 进程的概念

进程(process" width="100%" alt="window" /> </div>，是操作系统对一个正在运行的程序的一种抽象。进程是程序的基本执行实体；在面向线程设计的系统（如当代多数操作系统、Linux 2.6及更新的版本）中，进程本身不是基本执行单位，而是线程的容器。程序本身只是指令、数据及其组织形式的描述，相当于一个名词，进程才是程序（那些指令和数据）的真正执行实例，

### 6.1.2 进程的作用

hello 在运行时，操作系统会提供一种假象，就好像系统上只有这个程序在运行。程序看上去是独占地使用处理器、主存和 I/O 设备。处理器看上去就像在不间断地一条接一条地执行程序中的指令，即该程序的代码和数据是系统内存中唯一的对象。这些假象就是通过进程来实现的。

## 6.2 简述壳Shell-bash的作用与处理流程

Shell 是一种交互型的应用级程序，用户能够通过 Shell 与操作系统内核进行交互，如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/44abab68318341e69683587e5492c2e9.png" width="100%" alt="window" /> </div>


Shell 处理流程：

1. 在 Shell 中输入 hello 程序的路径
2. Shell 判断用户输入的是否为内置命令，如果不是，就认为它是一个可执行目标文件
3. Shell 构造 argv 和 envp
4. Shell 使用 fork(" width="100%" alt="window" /> </div> 创建子进程，调用 execve(" width="100%" alt="window" /> </div> 函数在新创建的子基础南横的上下文中加载并运行 hello 程序。将 hello 中的 .text 节、.data 节、.bss 节等内容加载到当前进程的虚拟地址空间
5. execve(" width="100%" alt="window" /> </div> 函数调用加载器，跳转到程序的入口点，开始执行 _start 函数，我们的 hello 程序便正式开始执行了

## 6.3 Hello的fork进程创建过程

Linux 通过 clone(" width="100%" alt="window" /> </div> 系统调用来实现 fork(" width="100%" alt="window" /> </div>，由于 clone(" width="100%" alt="window" /> </div> 可以自主选择需要复制的资源，所以这个系统调用需要传入很多的参数标志用于指明父子进程需要共享的资源。fork(" width="100%" alt="window" /> </div>，vfork(" width="100%" alt="window" /> </div>，__clone(" width="100%" alt="window" /> </div> 函数都需要根据各自传入的参数去底层调用 clone(" width="100%" alt="window" /> </div> 系统调用，然后再由 clone(" width="100%" alt="window" /> </div> 去调用 do_fork(" width="100%" alt="window" /> </div>。do_fork(" width="100%" alt="window" /> </div> 完成了创建的大部分工作，该函数调用 copy_process(" width="100%" alt="window" /> </div> 函数,然后让进程开始运行。

copy_process(" width="100%" alt="window" /> </div> 函数是核心，他的工作分为这几步：

1. 调用 dup_task_struct(" width="100%" alt="window" /> </div> 为新进程创建一个内核栈，thread_info 结构和 task_struct，这些值和当前进程的值相同。也就是说，当前子进程和父进程的进程描述符是一致的。
2. 检查一次，确保创建新进程后，拥有的进程数目没有超过给它分配的资源和限制。所有进程的 task_struct 结构中都有一个数组 rlim，这个数组中记载了该进程对占用各种资源的数目限制，所以如果该用户当前拥有的进程数目已经达到了峰值，则不允许继续 fork(" width="100%" alt="window" /> </div>。这个值为 PID_MAX，大小为 0x8000，也就是说进程号的最大值为 0x7fff，即短整型变量 short 的大小 32767，其中 0~299 是为系统进程（包括内核线程）保留的，主要用于各种“保护神进程”。
3. 子进程为了将自己与父进程区分开来，将进程描述符中的许多成员全部清零或者设为初始值。不过大多数数据都未修改。
4. 将子进程的状态设置为 TASK_UNINTERRUPTIBLE 深度睡眠，不可被信号唤醒，以保证子进程不会投入运行。
5. copy_process(" width="100%" alt="window" /> </div> 函数调用 copy_flags(" width="100%" alt="window" /> </div> 以更新 task_struct 中的 flags 成员。其中表示进程是否拥有超级用户管理权限的 PF_SUPERPRIV 标志被清零，表示进程还没有调用 exec(" width="100%" alt="window" /> </div> 函数的 PF_FORKNOEXEC 标志也被清零。
6. 调用 alloc_pid 为子进程分配一个有效的 PID
7. 根据传递给 clone(" width="100%" alt="window" /> </div> 的参数标志，调用 do_fork(" width="100%" alt="window" /> </div>->copy_process(" width="100%" alt="window" /> </div> 拷贝或共享父进程打开的文件，信号处理函数，进程地址空间和命名空间等。一般情况下，这些资源会给进程下的所有线程共享。
8. 最后，copy_process(" width="100%" alt="window" /> </div> 做扫尾工作并返回一个指向子进程的指针。

## 6.4 Hello的execve过程

execve(" width="100%" alt="window" /> </div> 函数加载并运行可执行目标文件，且带参数列表 argv 和环境变量列表 envp，execve(" width="100%" alt="window" /> </div> 函数调用一次从不返回。它的执行过程如下：

1. 删除已存在的用户区域
2. 映射私有区：为 hello 的代码、数据、.bss 和栈区域创建新的区域结构，所有这些区域都是私有的、写时才复制的
3. 映射共享区：比如 hello 程序与共享库 libc.so 链接
4. 设置 PC：exceve(" width="100%" alt="window" /> </div> 做的最后一件事就是设置当前进程的上下文中的程序计数器，使之指向代码区域的入口点
5. execve(" width="100%" alt="window" /> </div> 在调用成功的情况下不会返回，只有当出现错误时，例如找不到需要执行的程序时，execve(" width="100%" alt="window" /> </div> 才会返回到调用程序

## 6.5 Hello的进程执行

### 6.5.1 逻辑控制流

操作系统将一个 CPU 物理控制流，分成多个逻辑控制流，每个进程独占一个逻辑控制流。当一个逻辑控制流执行的时候，其他的逻辑控制流可能会临时暂停执行。一般来说，每个逻辑控制流都是独立的。当两个逻辑控制流在时间上发生重叠，我们说是并行的。如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/45d76e56a449455fa800c403fe859837.png" width="100%" alt="window" /> </div>


处理器在多个进程中来回切换称为多任务，每个时间当处理器执行一段控制流称为时间片。因此多任务也指时间分片。

### 6.5.2 用户模式和内核模式

为了限制一个应用可以执行的指令以及它可以访问的地址空间范围，处理器用一个控制寄存器中的一个模式位来描述进程当前的特权。如图是 x86 CPU 提供的环保护机制：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/389689bd77824481bea4cb43cec59a01.webp" width="100%" alt="window" /> </div>


内核工作在 0 环，用户工作在 3 环，中间环留给中间软件用。Linux 仅用第 0 和第 3 环，即用户模式和内核模式。

**用户模式：**用户模式中的进程不允许执行特权指令，比如停止处理器、改变模式位，或者发起一个 I/O 操作。也不允许用户模式的进程直接引用地址空间中内核区内的代码和数据。用户程序必须通过系统调用接口间接地访问内核代码和数据。

进程从用户模式变为内核模式的唯一方法是通过诸如中断、故障或者陷入系统调用这样的异常。当异常发生时，控制传递到异常处理程序，处理器将模式从用户模式变为内核模式。处理程序运行在内核模式中，当它返回到应用程序代码时，处理器就把模式从内核模式改回到用户模式。

### 6.5.3 上下文切换

操作系统内核为每个进程维护一个上下文。所谓上下文就是内核重新启动一个被抢占的进程所需的状态。它由一些对象的值组成，这些对象包括通用寄存器、浮点寄存器、程序计数器、用户栈、状态寄存器、内核栈和各种内核数据结构，比如描述地址空间的页表，包含有关当前进程信息的进程表，以及包含进程已打开文件的信息的文件表。

### 6.5.4 hello 的执行

从 Shell 中运行 hello 时，它运行在用户模式，运行过程中，内核不断切换上下文，使运行过程被切分成时间片，与其他进程交替占用执行，实现进程的调度。如果在运行过程中收到信号等，那么就会进入内核模式，运行信号处理程序，之后再返回用户模式。

## 6.6 hello的异常与信号处理

### 6.6.1 异常

异常可以分为四类：中断、陷阱、故障和终止。它们的性质如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/fff13e09632642cca5521352f3ea2af9.png" width="100%" alt="window" /> </div>


**中断：**比如在 hello 运行过程中，我们敲击键盘，那么就会触发中断，系统调用内核中的中断处理程序执行，然后返回，hello 继续执行，如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/44f1a01983df415b821add0e6bd99bc6.png" width="100%" alt="window" /> </div>


**陷阱：**陷阱就是系统调用，我们的 hello 运行在用户模式下，无法直接运行内核中的程序，比如像 fork，exit 这样的系统调用。于是就通过陷阱的方式，执行 systemcall 指令，内核调用陷阱处理程序来执行系统调用，如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/7f52bca765394816a00ec8ac9971d424.png" width="100%" alt="window" /> </div>


**故障：**当我们的 hello 运行时，当某一条指令引用一个虚拟地址，而地址相对应的物理页面不在内存中，就会发生故障。内核调用故障处理程序（这里是缺页处理程序），缺页处理程序从磁盘中加载适当的页面，然后将控制返回给引起故障的指令，该指令就能顺畅地执行了。

当然，也有一些故障会使程序直接终止。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/f0d3d083eb2d499c941a6c5405443c08.png" width="100%" alt="window" /> </div>


### 6.6.2 信号

使用 man 7 signal 查看 Linux 信号如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/95f2820592ba4a459d7d8bcb57e5d501.png" width="100%" alt="window" /> </div>


我在hello运行过程中，测试其中部分信号。
**按下Ctrl+Z**：进程收到 SIGSTP 信号， hello 进程挂起。用ps查看其进程PID，可以发现hello的PID是1904；再用jobs查看此时hello的后台 job号是1，调用 fg 1将其调回前台。
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/70af7c6297b648248a601ebf573705b3.png" width="100%" alt="window" /> </div>
**Ctrl+C**：进程收到 SIGINT 信号，结束 hello。在ps中查询不到其PID，在job中也没有显示，可以看出hello已经被彻底结束。
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/3bf4146180db45afaa7e6d88a4abb433.png" width="100%" alt="window" /> </div>
**中途乱按**：只是将屏幕的输入缓存到缓冲区。乱码被认为是命令
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/24a152a2cbd54f71826157ecaea612df.png" width="100%" alt="window" /> </div>
**Kill命令**：挂起的进程被终止，在ps中无法查到到其PID
<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/0b8c4080b7084c8b9c52650926329674.png" width="100%" alt="window" /> </div>
















## 6.7本章小结

这章讲解了 hello 如何运行在操作系统的上下文中，以及它如何受到信号的控制。



# 第7章 hello的存储管理🍫

## 7.1 hello的存储器地址空间

我们的 hello 进程是与其它进程共享 CPU 和主存资源的，为了更加有效地管理内存并且少出错，现代操作系统提供了一种对主存的抽象概念，叫做虚拟内存。虚拟内存时硬件异常、硬件地址翻译、主存、磁盘文件和内核软件的完美交互，它为每个进程提供了一个大的、一致的和私有的地址空间。首先确定一些概念

1. 逻辑地址：格式为“段地址:偏移地址”，是 CPU 生成的地址，在内部和编程使用，并不唯一。
2. 线性地址：逻逻辑地址到物理地址变换之间的中间层，逻辑地址经过段机制后转化为线性地址。
3. 虚拟地址：保护模式下，hello 运行在虚拟地址空间中，它访问存储器所用的逻辑地址。
4. 物理地址：加载到内存地址寄存器中的地址，内存单元的真正地址。CPU 通过地址总线的寻址，找到真实的物理内存对应地址。

## 7.2 Intel逻辑地址到线性地址的变换-段式管理

在 Intel 平台下的实模式中，逻辑地址为：CS：EA，CS 是段寄存器，将 CS 里的值左移四位，再加上 EA 就是线性地址。

而保护模式下，要用段描述符作为下标，到 GDT（全局描述符表）/LAT（局部描述符表）中查表获得段地址，段地址+偏移地址就是线性地址。

段描述符是一个 16 位字长的字段，如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/e045d1fc7adb4f3ea0525056f77e9901.png" width="100%" alt="window" /> </div>


TI 位指示选择 GDT 还是 LDT，前 13 位作为索引来确定段描述符在描述符表中的位置。从段描述符和偏移地址得到线性地址的过程如图

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/199ead83bf9c498aaabdbfb9dbfd63d0.png" width="100%" alt="window" /> </div>


## 7.3 Hello的线性地址到物理地址的变换-页式管理

VM 系统将虚拟内存分割为成为虚拟页的大小固定的快，物理内存也被分割为物理页，成为页帧。虚拟页面就可以作为缓存的工具，被分为三个部分：

- 未分配的：VM 系统还未分配的页
- 已缓存的：当前已缓存在物理内存中的已分配页
- 未缓存的：未缓存在物理内存的已分配页

如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/5df0cc88f01f440b98a916f704d3ddb0.png" width="100%" alt="window" /> </div>


## 7.4 TLB与四级页表支持下的VA到PA的变换

页表是 PTE（页表条目）的数组，它将虚拟页映射到物理页，每个 PTE 都有一个有效位和一个 n 位地址字段，有效位表明该虚拟页是否被缓存在 DRAM 中，地址字段表明 DRAM 中相应物理页的起始位置，它分为两个部分：VPO（虚拟页面偏移）和 VPN（虚拟页号），如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/034a64a91e144d249a3f3f1b02334a21.png" width="100%" alt="window" /> </div>


### 7.4.1 TLB加速地址翻译

为了优化 CPU 产生一个虚拟地址后，MMU 查阅 PTE的过程，在 MMU 中设置一个关于 PTE 的小缓存，称为 TLB（翻译后备缓冲器）。像普通的缓存一样，TLB 的索引和标记是从 PTE 中的 VPN 提取出来的，如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/da8160e4c03b46e796c8e885876ab96a.png" width="100%" alt="window" /> </div>


### 7.4.2 四级页表翻译

Core i7 采用四级页表层次结构，如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/243a8a793cf94f87b6b099e085c975ac.png" width="100%" alt="window" /> </div>


每次 CPU 产生一个虚拟地址后，通过它的 VPN 部分看 TLB 中是否缓存，如果命中，直接得到 PPN，将虚拟地址中的 VPO 作为物理页偏移，这样就能得到物理地址；如果 TLB 不命中，则经过四级页表的查找得到最终的PTE，从而得到 PPN，进而得到物理地址。

## 7.5 三级Cache支持下的物理内存访问

​	得到物理地址后，将物理地址分为 CT（标记位）、CI(组索引" width="100%" alt="window" /> </div> 和 CO（块偏移）。根据 CI 查找 L1 缓存中的组，依次与组中每一行的数据比较，有效位有效且标记位一致则命中。如果命中，直接返回想要的数据。如果不命中，就依次去 L2、L3 缓存判断是否命中，命中时将数据传给 CPU 同时更新各级缓存。

## 7.6 hello进程fork时的内存映射

​	在 Shell 输入命令行后，内核调用fork创建子进程，为 hello 程序的运行创建上下文，并分配一个与父进程不同的PID。通过 fork 创建的子进程拥有父进程相同的区域结构、页表等的一份副本，同时子进程也可以访问任何父进程已经打开的文件。当 fork 在新进程中返回时，新进程现在的虚拟内存刚好和调用 fork 时存在的虚拟内存相同，当这两个进程中的任一个后来进行写操作时，写时复制机制就会创建新页面，因此，也就为每个进程保持了私有地址空间

## 7.7 hello进程execve时的内存映射

execve(" width="100%" alt="window" /> </div> 函数调用驻留在内核区域的启动加载器代码，在当前进程中加载并运行包含在可执行目标文件 hello 中的程序，用 hello 程序有效地替代了当前程序。加载并运行 hello 需要以下几个步骤：

1. 删除已存在的用户区域，删除当前进程虚拟地址的用户部分中的已存在的区域结构。
2. 映射私有区域，为新程序的代码、数据、bss 和栈区域创建新的区域结构，所有这些新的区域都是私有的、写时复制的。代码和数据区域被映射为 hello 文件中的 .text 和 .data 区，bss 区域是请求二进制零的，映射到匿名文件，其大小包含在 hello 中，栈和堆地址也是请求二进制零的，初始长度为零。
3. 映射共享区域， hello 程序与共享对象 libc.so链接，libc.so是动态链接到这个程序中的，然后再映射到用户虚拟地址空间中的共享区域内。
4. 设置程序计数器（PC），execv(" width="100%" alt="window" /> </div> 做的最后一件事情就是设置当前进程上下文的程序计数器，使之指向代码区域的入口点。

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/0e257efdd24942ba9146590fb30de757.png" width="100%" alt="window" /> </div>


## 7.8 缺页故障与缺页中断处理

正如前面讲到的，hello 在运行时，很有可能会发生缺页故障，大致流程已经在 6.6.1 中做了阐述。当 CPU 产生的一个虚拟地址并不在 DRAM 缓存中时，缺页异常处理程序会选择一个牺牲页，用要读取的地址的内容替换它，然后内核重新启动导致缺页的指令。

## 7.9动态存储分配管理

hello 在运行时，它调用的 printf 函数会调用malloc函数，动态存储分配管理又是操作系统的一个伟大设计！

### 7.9.1 堆

动态内存分配器维护着一个进程的虚拟内存区域，称为堆。如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/be5d837f7d4e4ec0ac5df3e858b3de14.png" width="100%" alt="window" /> </div>


分配器将堆视为一组大小不同的块的集合来维护，且它们的地址是连续的。将块标记为两种，已分配的块供应用程序使用，空闲块用来分配

### 7.9.2 隐式空闲链表管理

想要设计好的数据结构维护空闲块需要考虑以下方面：

1. 空闲块组织：利用隐式空闲链表记录空闲块

2. 放置策略：如何选择合适的空闲块分配？

3. 1. 首次适配：从头开始搜索空闲链表，选择第一个合适的空闲块
   2. 下一次适配：从上一次查询结束的地方开始搜索选择第一个合适的空闲块
   3. 最佳适配：搜索能放下请求大小的最小空闲块

4. 分割：在将一个新分配的块放置到某个空闲块后，剩余的部分要进行处理

5. 合并：释放某个块后，要让它与相邻的空闲块合并

每个空闲块的结构如下：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/00222f19a3e84b8e89313808bf952132.png" width="100%" alt="window" /> </div>


- 脚部与头部是相同的，均为 4 个字节，用来存储块的大小，以及表明这个块是已分配还是空闲块
- 由于要求块双字对齐，所以块大小就总是 8 的倍数，低 3 位总是为 0，因而，我们只需要利用头部和脚部的高29 位存储块的大小，剩下 3 位的最低位来指明这个块是否空闲，000 为空闲，001 为已分配

为什么既设置头部又设置尾部呢？这是为了能够以常数时间来进行块的合并。无论是与下一块还是与上一块合并，都可以通过他们的头部或尾部得知块大小，从而定位整个块，避免了从头遍历链表。空闲块怎么组织呢？如图：

<div style="text-align: center;">   <img src="https://img-blog.csdnimg.cn/direct/36ebc621b68d46b0a7bfff30ce23ae2e.png" width="100%" alt="window" /> </div>


堆有两个特殊的标记：

- 序言块：8 个字节，由一个头部和一个脚部组成
- 结尾块：大小为 0 的头部

为了消除合并空闲块时边界的考虑，将序言块和结尾块的分配位均设置为已分配。为了保证双字对齐，在序言块的前面还设置了 4 个字节作为填充。

### 7.9.3 显式空闲链表管理

真实的操作系统实际上使用的是显示空闲链表管理。它的思路是维护多个空闲链表，每个链表中的块有大致相等的大小，分配器维护着一个空闲链表数组，每个大小类一个空闲链表，当需要分配块时只需要在对应的空闲链表中搜索就好了，有两种分离存储的方法

**简单分离存储：**从不合并与分离，每个块的大小就是大小类中最大元素的大小。例如大小类为 {17~32}，则需要分配块的大小在这个区间时均在此对应链表进行分配，并且都是分配大小为 32 的块。这样做，显然分配和释放都是常数级的，但是空间利用率较低

**分离适配：**每个大小类的空闲链表包含大小不同的块，分配完一个块后，将这个块进行分割，并根据剩下的块的大小将其插入到适当大小类的空闲链表中。这个做法平衡了搜索时间与空间利用率，C 标准库提供的 GNU malloc 包就是采用的这种方法。

## 7.10本章小结

本章介绍了现代操作系统的灵魂：存储器地址空间、段式管理、页式管理，VA 到 PA 的变换、物理内存访问， hello 进程 fork 时和 execve 时的内存映射、缺页故障与缺页中断处理、包括隐式空闲链表和显式空闲链表的动态存储分配管理。这些巧妙的设计使得我们的 hello 最终得以运行。

# 第8章 hello的IO管理🍭


## 8.1 Linux的IO设备管理方法

Linux将文件所有的I/O设备都模型化为文件，甚至内核也被映射为文件。这种将设备优雅地映射为文件的方式，允许Linux内核引出一个简单、低级的应用接口，称为Unix I/O。Linux就是基于Unix I/O实现对设备的管理。

- 设备的模型化：文件

- 设备管理：unix io接口

## 8.2 简述Unix IO接口及其函数

Unix IO接口可以实现4种基本操作：

1. 打开文件，应用程序要求内核打开相应的文件，来宣告它想要访问一个IO设备，内核返回这个文件的描述符以标识这个文件。Shell创建的每个进程开始时都有3个打开的文件：标准输入（stdin）、标准输出（stdout）和标准错误（stderr）。
2. 改变当前的文件位置，应用程序通过执行seek操作，显式地设置文件的当前位置为k。
3. 读写文件，读操作就是从当前位置k开始，从文件复制n个字节到内存，然后将k增加到k+n，当k超出文件长度时应用程序能够通过EOF检测到。而写操作则是从内存复制n个字节到一个文件，从当前文件位置k开始，然后更新k。
4. 关闭文件，当应用完成了对文件的访问之后，它就通知内核关闭这个文件，内核释放文件打开时创建的数据结构和内存资源

## 8.3 printf的实现分析

Printf函数实现如下：

```c
int printf(const char *fmt, ..." width="100%" alt="window" /> </div> 
 {     
     int i;
     char buf[256];
     va_list arg = (va_list" width="100%" alt="window" /> </div>((char*" width="100%" alt="window" /> </div>(&fmt" width="100%" alt="window" /> </div> + 4" width="100%" alt="window" /> </div>;
     i = vsprintf(buf, fmt, arg" width="100%" alt="window" /> </div>;
     write(buf, i" width="100%" alt="window" /> </div>;
	return i;  
}

```

​	从vsprintf生成显示信息，到write系统函数，到陷阱-系统调用 int 0x80或syscall等.

字符显示驱动子程序：从ASCII到字模库到显示vram（存储每一个点的RGB颜色信息）。

显示芯片按照刷新频率逐行读取vram，并通过信号线向液晶显示器传输每一个点（RGB分量）。

## 8.4 getchar的实现分析

​	当程序调用getchar时，程序等待用户按键，用户输入的字符被存放在键盘缓冲区中直到用户按回车(回车也在缓冲区中" width="100%" alt="window" /> </div>。当用户键入回车之后，getchar才开始从stdio流中每次读入一个字符。getchar函数的返回值是用户输入的第一个字符的ascii码,如出错返回-1,且将用户输入的字符回显到屏幕。如用户在按回车之前输入了不止一个字符,其他字符会保留在键盘缓存区中,等待后续getchar调用读取。也就是说，后续的getchar调用不会等待用户按键,而直接读取缓冲区中的字符,直到缓冲区中的字符读完为后,才等待用户按键。

​	异步异常-键盘中断的处理：键盘中断处理子程序。接受按键扫描码转成ascii码，保存到系统的键盘缓冲区。

getchar等调用read系统函数，通过系统调用读取按键ascii码，直到接受到回车键才返回。

## 8.5本章小结

本章介绍了 Linux 的 I/O 设备的基本概念和管理方法，以及Unix I/O 接口及其函数。最后分析了printf 函数和 getchar 函数的工作过程。



# 结论

至此，hello 终于走完了它的一生，让我们为它的一生做个小结：

- 程序设计者编写出它的基因——hello.c
- 预处理器完善它的基因——hello.i
- 编译器为它注入的灵魂——hello.s
- 汇编器为它的诞生做最后的准备——hello.o
- 链接器让它长出完整的躯体——hello
- Shell 为它创建子进程，让它真正成为系统中的个体
- 加载器映射虚拟内存，给予它成长的条件
- CPU 的逻辑控制流让它驰骋在硬件与操作系统之上
- 虚拟地址这一计算机系统最伟大的抽象为它的驰骋导航
- malloc 的高效管理让它的驰骋拥有更广阔的天地
- 信号与异常约束它的行为，让它总是走在康庄大道之上
- Unix I/O 打开它与程序使用者交流的窗口
- 当 hello 垂垂老矣，运行完最后一行代码，__libc_start_main 将控制转移给内核，Shell 回收子进程，内核删除与它相关的所有数据结构，它在这个世界的所有痕迹至此被抹去。

回首它的一生，惊心动魄，千难万险。其中的每个阶段无不凝结着人类最伟大的智慧

