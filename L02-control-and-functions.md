# L02 · 让代码会判断、会重复、能复用

上一章的代码都是「从上往下，一行执行一次」。这一章加三样东西：

- **判断**：根据情况走不同的路
- **循环**：把同一件事重复做很多次
- **函数**：把一段代码打包，起个名字反复用

这三样凑齐，你就能写出真正解决问题的程序了。

---

## 1. `if`：满足条件才做

```python
x = 5
if x > 0:
    print("正数")
```

输出 `正数`。如果 `x` 是 `-1`，什么都不会打印。

结构就三块：

```python
if 条件:
    ...               # 条件成立时执行
elif 另一个条件:
    ...               # 第一个不成立、这个成立时执行
else:
    ...               # 都不成立时执行
```

**每个条件后面都有冒号，被包住的行缩进 4 个空格**（[L01 §3](L01-first-steps.md) 那条规则在这里全面生效）。

`elif` 是 `else if` 的缩写，可以写任意多个，也可以不写。`else` 最多一个，也可以不写。

```python
score = 85
if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("要加油")
# 及格
```

**顺序很重要**：Python 从上往下找，命中第一个成立的分支就停下来，后面的都不看。所以上面如果把 `score >= 60` 放前面，85 分就会先命中「及格」，永远不会到「优秀」。写多个条件时，把**最严格**的放前面。

### 1.1 条件里可以放什么

```python
x = 5
print(x > 0)        # True
print(x == 5)       # True
print(x != 3)       # True
print(0 <= x < 10)  # True   链式比较，等价于 0 <= x and x < 10
```

组合多个条件用 `and`（并且）、`or`（或者）、`not`（取反）：

```python
age = 20
if age >= 18 and age < 60:
    print("成年人且未退休")

if age < 0 or age > 150:
    print("年龄不合理")
```

**短路**是个有用的特性：`A and B` 如果 A 已经不成立，B 根本不会被计算。于是这种写法是安全的：

```python
node = None
if node is not None and node.val > 0:
    print(node.val)
```

`node` 是 `None` 时第一个条件就挂了，`node.val` 不会被碰到，所以不会报错。反过来写成 `node.val > 0 and node is not None` 就会崩。这种「先判空再用」的顺序，做链表和树的题时天天见。

### 1.2 判断「空」的真值写法

[L01 §5.3](L01-first-steps.md) 说过，`0`、`""`、`[]`、`{}`、`None` 都算「假」。所以判断一个列表是不是空的，直接写：

```python
nums = [3, 1, 4]
if nums:
    print("列表里有东西")

if not nums:
    print("列表是空的")
```

`if nums:` 读作「如果 nums 非空」。刷题里到处都是这个写法，比 `len(nums) > 0` 更地道。

**但要注意**：`if not x` 是「x 是空 / 零 / None」，不是「x 等于 0」。如果 `x` 是一个可能有意义的数字 0，你得明确写 `if x == 0:`。

### 1.3 `is None`：一个必须记住的特例

```python
x = None
if x is None:
    print("x 什么都没有")
```

判断「是不是空值」用 `is None` / `is not None`。判断「两个值相不相等」用 `==`。

**为什么不能用 `== None`？** 能用，但 Python 社区约定用 `is`，而且 `==` 在某些情况下会被自定义对象改写，可能给出意料之外的结果。至于 `is` 判断的是「是不是同一个对象」，所以**除了 `None` 之外别拿它比数字和字符串**：

```python
a = 1000
b = 1000
print(a == b)   # True   值相等
# print(a is b) ← 别这么写，结果取决于解释器的内部优化，可能 True 可能 False
```

机械记住：**比大小比值一律 `==`，只有 `None` 用 `is`**，就不会错。

### 1.4 三元表达式：一行给变量选个值

```python
x = -5
sign = 1 if x > 0 else -1
print(sign)   # -1
```

读作「如果 x > 0 就取 1，否则取 -1」。适合简单的二选一，条件复杂时老老实实写 `if`。

---

## 2. `while`：条件成立就一直做

```python
i = 1
while i <= 3:
    print(i)
    i += 1
```

```text
1
2
3
```

执行过程：`i=1` → 条件成立 → 打印 1、i 变 2 → 回去再判断 → …… → `i=4` 时条件不成立，结束。

**写 `while` 最容易犯的错是忘记改变条件变量**。如果上面漏了 `i += 1`，`i` 永远是 1，程序会无限打印直到你按 `Ctrl + C` 强行停止。看到程序「卡住不动」，先检查这个。

算法题里 `while` 比 `for` 更常用——双指针、滑动窗口、二分查找、队列弹出，全都是 `while`：

```python
l, r = 0, 5
while l < r:
    print(f"l={l} r={r}")
    l += 1
    r -= 1
```

```text
l=0 r=5
l=1 r=4
l=2 r=3
```

### 2.1 想「至少做一次」怎么办

Python 没有「先做再判断」的循环结构，标准写法是：

```python
while True:
    answer = input("输入 quit 退出：")
    if answer == "quit":
        break
    print("你输入了", answer)
```

`while True:` 表示「一直循环」，靠里面的 `break` 跳出来。

---

## 3. `for`：Python 的循环只有一种——「挨个取」

这是零基础最需要转换观念的一节。Python 的 `for` 不是「从几数到几」，而是「**从一个序列里，把每个元素依次取出来**」：

```python
nums = [10, 20, 30]
for x in nums:
    print(x)
```

```text
10
20
30
```

每轮循环，变量 `x` 自动变成列表里的下一个元素，直到取完。你不用管下标、不用管什么时候停。

要「循环 n 次」，用 `range()` 造一个数字序列：

```python
for i in range(5):
    print(i, end=" ")
# 0 1 2 3 4
```

`range` 的三种写法：

```python
print(list(range(5)))          # [0, 1, 2, 3, 4]          0 到 n-1
print(list(range(2, 6)))       # [2, 3, 4, 5]             从 2 到 5
print(list(range(1, 10, 2)))   # [1, 3, 5, 7, 9]          每次加 2
print(list(range(5, 0, -1)))   # [5, 4, 3, 2, 1]          倒着数
```

**`range(a, b)` 是左闭右开：包含 a，不包含 b。** 这句要形成条件反射。想循环 `n` 次就写 `range(n)`（得到 0～n-1，正好 n 个）；想包含右端点就写 `range(a, b + 1)`。数组下标越界有一半来自这里。

`range(10 ** 9)` 也不会占内存——它不是一个真的列表，而是「按需给出下一个数」的对象。想看内容才用 `list()` 转换，刷题时不要多此一举。

### 3.1 `enumerate`：又要编号又要值

新手常写 `for i in range(len(nums)): x = nums[i]`。Python 的标准写法是：

```python
nums = [10, 20, 30]
for i, x in enumerate(nums):
    print(i, x)
```

```text
0 10
1 20
2 30
```

一次拿到「第几个」和「是什么」。编号想从 1 开始：`enumerate(nums, start=1)`。

**为什么必须习惯它**：几乎所有数组题都要「边遍历边知道位置」。写 `range(len(...))` 不仅多打几个字，还容易把 `i` 和 `nums[i]` 搞混。

### 3.2 `zip`：同时遍历两个序列

```python
names = ["小明", "小红"]
scores = [95, 88]
for name, score in zip(names, scores):
    print(name, score)
```

```text
小明 95
小红 88
```

长度不一样时**以短的那个为准**，多出来的直接丢掉，而且不会报错。这个「静默截断」用之前要确认两个序列确实等长。

### 3.3 `break` 和 `continue`

```python
for i in range(6):
    if i == 2:
        continue      # 跳过这一轮剩下的部分，直接进下一轮
    if i == 5:
        break         # 整个循环结束
    print(i, end=" ")
# 0 1 3 4
```

- `break`：不玩了，跳出整个循环
- `continue`：这一轮剩下的跳过，下一轮继续

刷题里「找到就返回」通常用 `break` 或直接 `return`；「不符合条件就跳过本轮」用 `continue`。

---

## 4. 手动模拟：把刚学的拼起来

下面这段请**先在纸上写出输出**，再运行核对：

```python
nums = [4, 1, 7, 3]
best_i, best_v = -1, float("-inf")
for i, x in enumerate(nums):
    if x > best_v:
        best_v = x
        best_i = i
    print(f"i={i} x={x} best_i={best_i} best_v={best_v}")
print("最大值", best_v, "在下标", best_i)
```

输出：

```text
i=0 x=4 best_i=0 best_v=4
i=1 x=1 best_i=0 best_v=4
i=2 x=7 best_i=2 best_v=7
i=3 x=3 best_i=2 best_v=7
最大值 7 在下标 2
```

逐步推演：

| 轮 | i | x | `x > best_v`？ | 动作 | best_v | best_i |
|---|---|---|---|---|---|---|
| 初始 | — | — | — | — | `-inf` | -1 |
| 1 | 0 | 4 | 4 > -inf ✓ | 更新 | 4 | 0 |
| 2 | 1 | 1 | 1 > 4 ✗ | 不动 | 4 | 0 |
| 3 | 2 | 7 | 7 > 4 ✓ | 更新 | 7 | 2 |
| 4 | 3 | 3 | 3 > 7 ✗ | 不动 | 7 | 2 |

**这个「先设一个极端初始值，然后遍历，满足条件就更新」的形状，是后面几十道题的骨架。** 请把它记在手里：求最大值用 `float("-inf")`，求最小值用 `float("inf")`，要同时记下标就多设一个变量。

顺便留意 `>` 和 `>=` 的差别：这里用 `>`，所以遇到并列最大值时保留**最先出现**的那个；改成 `>=` 就会保留最后一个。

---

## 5. 函数：把代码打包，起个名字

### 5.1 最简单的函数

```python
def add(a, b):
    return a + b

print(add(2, 3))    # 5
```

- `def` 后面跟函数名、括号里的参数、**冒号**
- 函数体缩进 4 空格
- `return` 后面是「算完的结果」，交回给调用它的地方
- 不写 `return`，函数默认返回 `None`

调用时 `add(2, 3)`，2 传给 `a`，3 传给 `b`。函数里的 `a`、`b` 只在这个函数内部有效，外面用不了。

**为什么需要函数**：同一段逻辑要写好几遍时，不用复制粘贴；改的时候只改一处。做算法题时，递归、深度优先搜索全靠函数调用自己。

### 5.2 一次返回多个值

```python
def min_max(nums):
    return min(nums), max(nums)

lo, hi = min_max([3, 1, 9])
print(lo, hi)          # 1 9

one = min_max([3, 1, 9])
print(one)             # (1, 9)
```

所谓「返回多个值」，其实是打包成一个**元组**（[L03](L03-containers.md) 会讲），再自动拆开。写 `lo, hi = ...` 时自动拆，写 `one = ...` 时拿到完整的一包。

Python 独有的便利：交换两个值不用临时变量。

```python
a, b = 1, 2
a, b = b, a       # 右边先算好，再一起赋值
print(a, b)       # 2 1
```

同理 `nums[i], nums[j] = nums[j], nums[i]` 就是交换数组里两个元素，后面排序、双指针的题里到处都是。

### 5.3 参数：位置、默认值、关键字

```python
def greet(name, punctuation="!"):
    return f"你好 {name}{punctuation}"

print(greet("小明"))                        # 你好 小明!
print(greet("小明", "?"))                   # 你好 小明?
print(greet(punctuation="。", name="小明"))  # 你好 小明。
```

- 有默认值的参数**必须放在没默认值的后面**
- 可以按「名字=值」传，这时顺序无所谓

**一个现在就要见的坑**：默认值如果是个列表/字典，会被所有调用共享。

```python
def append_to(x, acc=[]):        # 危险
    acc.append(x)
    return acc

print(append_to(1))    # [1]
print(append_to(2))    # [1, 2]   ← 你以为会是 [2]
```

原因是默认值在函数**定义时**创建一次，不是每次调用重新造。正确写法：

```python
def append_to(x, acc=None):
    if acc is None:
        acc = []
    acc.append(x)
    return acc

print(append_to(1))    # [1]
print(append_to(2))    # [2]
```

现在只要机械记住：**默认参数一律不用 `[]`、`{}`、`set()`，用 `None` 兜底**。这个坑在后面的回溯题里会显得特别阴险（上一题的答案会污染下一题），[L09](L09-backtrack-graph-dp.md) 会再提醒一次。

### 5.4 变量的作用域：里面能读，不能随便改

```python
cnt = 0

def f():
    print(cnt)     # 读外面的变量，可以

f()                # 0
```

但想在函数里**改**外面的变量，直接写会报错：

```python
cnt = 0

def g():
    cnt += 1       # UnboundLocalError

g()
```

原因：Python 只要在函数里看到给某个名字赋值，就把它当成本函数内的局部变量，于是 `cnt += 1` 里的「读」也去读那个还没赋值的局部 `cnt`。要改外面的，得先声明：

```python
cnt = 0

def g():
    global cnt
    cnt += 1

g()
print(cnt)    # 1
```

**刷题时有个更好的办法：别用全局变量，把状态放在函数参数里传，或者用返回值带出来。** 遇到需要「统计总数」的递归，常见写法是让递归函数自己返回结果，而不是偷偷改外面的计数器。这个思路在 [L08](L08-linkedlist-tree.md) 讲树递归时会反复用到。

初学阶段看到自己想写 `global`，先停一下，想想能不能改成 `return`。

### 5.5 `lambda`：一行的小函数

```python
square = lambda x: x * x
print(square(5))    # 25
```

等价于 `def square(x): return x * x`。它最大的用途是给排序当「按什么排」的说明：

```python
pairs = [(1, "b"), (3, "a"), (2, "c")]
print(sorted(pairs, key=lambda p: p[0]))
# [(1, 'b'), (2, 'c'), (3, 'a')]
```

`key=lambda p: p[0]` 的意思是「按每个元素的第 0 项排序」。别把复杂逻辑塞进 `lambda`，超过一行就老实写 `def`。

---

## 6. 综合练习：三个能跑的小程序

### 6.1 判断素数

```python
def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True

for n in [1, 2, 9, 17, 25]:
    print(n, is_prime(n))
```

```text
1 False
2 True
9 False
17 True
25 False
```

两处要留意：

- `int(n ** 0.5) + 1` 里的 `+1`：因为 `range` 右端取不到，不加会漏掉平方根本身（判断 9 时会误判成素数）。
- 一旦找到能整除的数就 `return False`，不用再往下试；全部试完都没找到才 `return True`。这种「提前返回 + 兜底返回」的结构非常常见。

### 6.2 FizzBuzz

```python
for i in range(1, 16):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

**顺序不能反**：15 同时是 3 和 5 的倍数，如果先判断 `% 3`，15 会被前面的分支抢走，永远打不出 `FizzBuzz`。这呼应了 §1 说的「最严格的条件放前面」。

### 6.3 统计一串数字里正数、负数、零各有几个

```python
nums = [3, -1, 0, 0, 5, -2]
pos = neg = zero = 0
for x in nums:
    if x > 0:
        pos += 1
    elif x < 0:
        neg += 1
    else:
        zero += 1
print(f"正数 {pos} 个，负数 {neg} 个，零 {zero} 个")
# 正数 2 个，负数 2 个，零 2 个
```

---

## 7. 本章常见报错

| 报错 | 八成是 |
|---|---|
| `IndentationError` | `if` / `for` / `def` 后面漏缩进，或空格数不一致 |
| `SyntaxError: invalid syntax` | 条件后漏了冒号；看报错行**和上一行** |
| `NameError` | 变量在函数外用不了，或拼写/大小写错 |
| `UnboundLocalError` | 函数里改外面的变量没写 `global`；改用返回值更好 |
| `TypeError: 'NoneType' object is not iterable` | 把没返回值的函数结果拿去遍历了 |
| `IndexError` | `range` 右开导致多算/少算，或下标越界 |
| 程序卡住不结束 | `while` 里忘了改变条件变量，按 `Ctrl + C` 停止 |

---

## 8. 动手练

**先写再对答案。**

1. 写函数 `sign(x)`：正数返回 1，负数返回 -1，零返回 0。
2. 写函数 `sum_to(n)`：用循环返回 `1 + 2 + ... + n`（不许用公式，不许用 `sum()`）。
3. `nums = [5, 2, 9, 2, 9]`，用 `enumerate` 打印所有值为 9 的下标。
4. 写函数 `clip(x, lo, hi)`：把 x 限制在 `[lo, hi]` 内，小于 lo 返回 lo，大于 hi 返回 hi，否则返回 x。不许嵌套超过两层 `if`。
5. 不运行，写出输出：
   ```python
   i = 0
   while i < 5:
       i += 1
       if i % 2 == 0:
           continue
       if i == 5:
           break
       print(i, end=" ")
   ```
6. 用 `zip` 把 `["a","b","c"]` 和 `[1,2,3]` 打印成 `a=1`、`b=2`、`c=3` 三行。
7. 写函数 `count_digits(s)`：返回字符串里数字字符的个数（提示：`ch.isdigit()`）。
8. 写函数 `argmax(nums)`：返回最大值的下标；并列时返回最靠左的；空列表返回 `-1`。用 `enumerate`，不许用 `max()`。
9. 写函数 `is_palindrome(s)`：判断字符串正着读反着读是否一样（提示：`s[::-1]`）。
10. 用 `while` 写「猜数字」：答案设成 7，变量 `guess` 从 1 开始每次加 1，猜到就 `break` 并打印猜了几次。

<details>
<summary>参考答案</summary>

**1**

```python
def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0
```

**2**

```python
def sum_to(n):
    s = 0
    for i in range(1, n + 1):     # 右端要 +1
        s += i
    return s
```

**3**

```python
nums = [5, 2, 9, 2, 9]
for i, x in enumerate(nums):
    if x == 9:
        print(i, end=" ")
# 2 4
```

**4**

```python
def clip(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x
```

**5** `1 3`。i 依次是 1～5；2 和 4 被 `continue` 跳过；5 时先 `break` 所以不打印。

**6**

```python
keys = ["a", "b", "c"]
vals = [1, 2, 3]
for k, v in zip(keys, vals):
    print(f"{k}={v}")
```

**7**

```python
def count_digits(s):
    cnt = 0
    for ch in s:
        if ch.isdigit():
            cnt += 1
    return cnt
```

**8**

```python
def argmax(nums):
    best_i, best_v = -1, float("-inf")
    for i, x in enumerate(nums):
        if x > best_v:          # 严格大于 → 并列时保留最左
            best_v = x
            best_i = i
    return best_i
```

`float("-inf")` 保证第一个元素一定能更新（数组里可能有负数）；`>` 而不是 `>=` 保证并列取最左。这就是 §4 那个骨架。

**9**

```python
def is_palindrome(s):
    return s == s[::-1]
```

**10**

```python
answer = 7
guess = 1
times = 0
while True:
    times += 1
    if guess == answer:
        break
    guess += 1
print("猜了", times, "次")   # 猜了 7 次
```

</details>

---

## 9. 本章自测（闭卷）

1. 写出 `list(range(3, 10, 2))` 和 `list(range(4, 0, -1))`。
2. `for x in nums` 和 `for i, x in enumerate(nums)` 分别在什么时候用？
3. `break` 和 `continue` 的区别是什么？
4. 不运行，写出输出：
   ```python
   for i in range(3):
       for j in range(2):
           print(i, j, end=" | ")
   ```
5. 写函数 `max_gap(nums)`：返回相邻两个元素差值的最大值；长度小于 2 时返回 0。
6. 说明 `==` 和 `is` 该怎么选，以及 `if node is not None and node.val > 0` 为什么不能把两个条件调换。
7. **口述题**：为什么 `def f(x, acc=[]):` 是危险的？正确写法是什么？

<details>
<summary>自测答案</summary>

1. `[3, 5, 7, 9]` 和 `[4, 3, 2, 1]`。
2. 只要值、不关心位置用前者；同时要下标和值用后者。
3. `break` 结束整个循环，`continue` 只跳过本轮剩下的语句。
4. `0 0 | 0 1 | 1 0 | 1 1 | 2 0 | 2 1 | `
5.
   ```python
   def max_gap(nums):
       if len(nums) < 2:
           return 0
       best = 0
       for i in range(1, len(nums)):
           best = max(best, abs(nums[i] - nums[i - 1]))
       return best
   ```
6. 比值用 `==`，只有判断 `None` 用 `is`。两个条件不能调换，因为 `and` 有短路：先判空才能安全地访问 `node.val`；调换后当 `node` 是 `None` 时会直接报错。
7. 默认值在函数定义时创建一次，之后所有调用共享同一个列表，上一次的残留会带进下一次。改成 `acc=None`，函数里写 `if acc is None: acc = []`。

</details>

---

## 10. 下章预告

现在你会让代码判断、循环、复用了。但有个大问题：目前一个变量只能装**一个**数。想处理「一个班的成绩」「一行输入里的所有数字」，总不能定义 100 个变量。

[L03](L03-containers.md) 讲四种「能装一堆东西的盒子」：列表、字符串、字典、集合。这是刷题用得最多的东西——**100 道题里九成的代码都在操作它们**。学完那一章，你就有能力做第一道真题了。
