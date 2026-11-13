# L03 · 四种盒子：一次装一堆数据

到目前为止，一个变量只能装一个数：

```python
a = 10
b = 20
c = 30
```

如果要处理 100 个成绩呢？定义 100 个变量显然不现实。这一章讲四种「能装一堆东西的盒子」，它们是刷题最核心的工具——**100 道题里大约九成代码都在操作它们**。

| 盒子 | 写法 | 特点 | 什么时候用 |
|---|---|---|---|
| 列表 `list` | `[1, 2, 3]` | 有顺序、能改、能装重复 | 数组、栈、结果列表 |
| 字符串 `str` | `"abc"` | 有顺序、**不能改** | 文字、字符序列 |
| 字典 `dict` | `{"a": 1}` | 按「名字」取值，查得快 | 计数、查配对、分组 |
| 集合 `set` | `{1, 2}` | 无序、自动去重、查得快 | 判重、查存在 |

---

## 1. 列表 `list`：最常用的盒子

### 1.1 创建和取东西

```python
a = [1, 2, 3]
b = []                    # 空列表
c = [0] * 5               # [0, 0, 0, 0, 0]
d = list(range(5))        # [0, 1, 2, 3, 4]
e = list("abc")           # ['a', 'b', 'c']

print(a[0])     # 1    下标从 0 开始
print(a[2])     # 3
print(a[-1])    # 3    负下标从末尾数
print(a[-2])    # 2
print(len(a))   # 3    长度
```

**负下标是刷题利器**：`a[-1]` 就是最后一个元素，比 `a[len(a)-1]` 干净得多。但空列表上写 `a[-1]` 会报 `IndexError`，所以判空要写在前面：

```python
if a and a[-1] > 0:
    ...
```

`and` 的短路保证 `a` 为空时不会去取 `a[-1]`。

### 1.2 切片：一次取一段

```python
a = [0, 1, 2, 3, 4, 5]
print(a[1:4])     # [1, 2, 3]     从第 1 个到第 3 个（不含第 4 个）
print(a[:3])      # [0, 1, 2]     从头开始
print(a[3:])      # [3, 4, 5]     到结尾
print(a[:])       # [0, 1, 2, 3, 4, 5]   整个复制一份
print(a[::2])     # [0, 2, 4]     每隔一个取一个
print(a[::-1])    # [5, 4, 3, 2, 1, 0]   反转
print(a[-3:])     # [3, 4, 5]     最后三个
```

通用形式是 `a[起点:终点:步长]`，三部分都可以省略。**终点取不到**（和 `range` 一样是左闭右开），所以 `a[0:3]` 是前 3 个元素。

切片的四条性质：

1. **越界不报错，自动截断**：`a[2:100]` 得到 `[2,3,4,5]`，`a[100:]` 得到 `[]`。写边界时省心，但也意味着写错不一定立刻发现。
2. **切片会造一个新列表**，改它不影响原来那个：
   ```python
   a = [1, 2, 3]
   b = a[:]
   b[0] = 99
   print(a)    # [1, 2, 3]   没变
   ```
3. **切片赋值可以原地替换一段**：
   ```python
   a = [1, 2, 3, 4, 5]
   a[1:4] = [20, 30]
   print(a)    # [1, 20, 30, 5]   长度都变了
   ```
4. `a[::-1]` 会造一个新列表；只是想倒着遍历、不想花内存，用 `reversed(a)`：
   ```python
   for x in reversed(a):
       print(x)
   ```

`a[::-1]` 也是判断回文的最短写法：`s == s[::-1]`。

### 1.3 增删改查

```python
a = [3, 1, 2]

a.append(4)          # [3, 1, 2, 4]        末尾加一个
a.insert(1, 9)       # [3, 9, 1, 2, 4]     在第 1 个位置插入
a.extend([7, 8])     # [3, 9, 1, 2, 4, 7, 8]   一次加好几个

last = a.pop()       # 删掉并返回最后一个（8）
first = a.pop(0)     # 删掉并返回第一个（3）
a.remove(9)          # 删掉第一个值是 9 的元素；找不到会报错
a[0] = 100           # 改某个位置
del a[0]             # 删某个位置

print(a.index(2))    # 2 第一次出现在哪个位置；找不到会报错
print(a.count(2))    # 2 出现几次
print(2 in a)        # True  判断在不在里面
a.sort()             # 原地排序
a.reverse()          # 原地反转
a.clear()            # 清空
```

**`pop()` 会返回被删掉的那个值**，所以「从栈顶拿一个」写 `x = stack.pop()` 一行就够。

**`in` 判断要小心**：`2 in a` 是把列表从头到尾找一遍。数据多的时候很慢。想快速判断「在不在」，用后面 §4 的集合。

### 1.4 每个操作要花多少力气（很重要）

这一节先建立直觉，[L05](L05-algorithm-thinking.md) 会正式讲怎么算。

| 操作 | 花多少力气 | 为什么 |
|---|---|---|
| `a[i]` 按下标取 | 一瞬间 | 直接算出位置 |
| `a.append(x)` 末尾加 | 一瞬间 | 后面没东西要挪 |
| `a.pop()` 末尾删 | 一瞬间 | 同上 |
| `a.insert(0, x)` 开头插 | **要挪动所有元素** | 后面的全得往后挪一格 |
| `a.pop(0)` 开头删 | **要挪动所有元素** | 后面的全得往前挪一格 |
| `x in a` 查存在 | **要从头翻到尾** | 只能一个一个比 |
| `a.sort()` 排序 | 比较多轮 | 比前面都慢 |

**「瞬间」和「要翻一遍」的差别，会直接决定你的代码是 0.1 秒还是超时。** 这不是理论警告，我在本机实测过（Python 3.13）：把 10 万个数用 `pop(0)` 一个个删光要 **8.59 秒**，换成下章会学的 `deque` 只要 **0.003 秒**，差了近 3000 倍。同一个思路，只换了个盒子。

所以：**需要频繁从开头删东西时，别用列表**，用 `collections.deque`（[L04](L04-toolbox.md) 讲）。

### 1.5 四个高频坑

**坑 1：`a.sort()` 返回 `None`。**

```python
a = [3, 1, 2]
print(a.sort())    # None   ← 不是排好序的列表！
print(a)           # [1, 2, 3]   它只是把 a 原地排好了
```

「不改动原列表、拿到一个新列表」要用 `sorted(a)`：

```python
a = [3, 1, 2]
b = sorted(a)
print(a, b)    # [3, 1, 2] [1, 2, 3]
```

于是 `for x in sorted(a):` 没问题，`for x in a.sort():` 会报「None 不能遍历」。新手写这行能卡十分钟。

**坑 2：`[[0] * n] * m` 造出来的每一行是同一行。**

```python
m = [[0] * 3] * 3
m[0][0] = 9
print(m)    # [[9, 0, 0], [9, 0, 0], [9, 0, 0]]   ← 三行全变了
```

因为 `* 3` 复制的是**同一个内层列表的标签**三份，不是三个新列表。做矩阵、棋盘、二维表格时，必须用推导式（§6）：

```python
m = [[0] * 3 for _ in range(3)]
m[0][0] = 9
print(m)    # [[9, 0, 0], [0, 0, 0], [0, 0, 0]]   ← 正确
```

一维的 `[0] * n` 没问题（0 是个数，不是盒子），**从二维开始就必须用推导式**。

**坑 3：边遍历边删会漏。**

```python
a = [1, 2, 2, 3, 2]
for x in a:
    if x == 2:
        a.remove(x)
print(a)    # [1, 3, 2]   ← 没删干净，还不报错
```

删除后后面的元素往前挪，而循环还在按原来的位置往后走，于是跳过了一个。正确做法是造个新列表：

```python
a = [x for x in a if x != 2]
```

或者从后往前删：

```python
for i in range(len(a) - 1, -1, -1):
    if a[i] == 2:
        del a[i]
```

**坑 4：`a = b` 不是复制，是同一份数据。**

```python
a = [1, 2, 3]
b = a
b[0] = 99
print(a)    # [99, 2, 3]   ← a 也变了
```

`a` 和 `b` 是贴在同一个盒子上的两张标签。要真复制：`b = a[:]` 或 `b = a.copy()`。

嵌套的盒子还要用深拷贝：

```python
import copy
a = [[1, 2], [3, 4]]
b = a[:]              # 只复制了外层，内层还是共享
b[0][0] = 9
print(a)              # [[9, 2], [3, 4]]
c = copy.deepcopy(a)  # 完全独立
```

**这条在后面「收集所有答案」的回溯题里是头号 bug**：如果你把 `path` 直接存进结果，后面一改，之前存的全跟着变。正确写法是存快照 `res.append(path[:])`。[L09](L09-backtrack-graph-dp.md) 会用实际错误输出演示。

### 1.6 列表排序的进阶用法

```python
nums = [3, 1, 2]
print(sorted(nums))                     # [1, 2, 3]
print(sorted(nums, reverse=True))       # [3, 2, 1]   降序

words = ["bb", "a", "ccc"]
print(sorted(words, key=len))           # ['a', 'bb', 'ccc']   按长度排

pairs = [(1, 3), (1, 2), (2, 1)]
print(sorted(pairs))                    # [(1, 2), (1, 3), (2, 1)]   默认按第一项、再按第二项
print(sorted(pairs, key=lambda p: (p[0], -p[1])))
# [(1, 3), (1, 2), (2, 1)]   第一项升序、第一项相同时第二项降序
```

`key` 是「给每个元素算一个用来比较的值」。默认排序是**稳定**的：大小一样的元素保持原来的先后顺序。

想「第一维升序、第二维降序」时，不能直接 `reverse=True`（那会把两维都反过来），要把需要降序的那一维取负号——上面那个 `(p[0], -p[1])` 就是干这个的。

---

## 2. 字符串 `str`：一串字符，不能改

```python
s = "abcdef"
print(s[0], s[-1], len(s))   # a f 6
print(s[1:4])                # bcd
print(s[::-1])               # fedcba
print("ab" in s)             # True
```

字符串能索引、能切片、能用 `in`，但**不能原地改**：

```python
s = "abc"
s[0] = "x"     # TypeError
```

想改就先转成列表，改完再拼回去：

```python
s = "abc"
t = list(s)       # ['a', 'b', 'c']
t[0] = "x"
s = "".join(t)    # "xbc"
```

常用方法：

```python
print("  LeetCode 2026  ".strip())     # "LeetCode 2026"   去两端空格
print("a,b,c".split(","))              # ['a', 'b', 'c']   按逗号切开
print("a b  c".split())                # ['a', 'b', 'c']   不写参数＝按任意空白切，连续空格当成一个
print(",".join(["a", "b", "c"]))       # "a,b,c"           拼回去
print("abc".replace("b", "X"))         # "aXc"
print("abc".upper(), "ABC".lower())    # ABC abc
print("abc".startswith("ab"))          # True
print("abc".find("c"))                 # 2   找不到返回 -1（不报错）
print("a1".isdigit(), "ab".isalpha())  # False True
```

**`split()` 和 `join()` 方向别搞反**：

- 字符串 → 列表：`s.split(分隔)`
- 列表 → 字符串：`分隔.join(字符串列表)`

`join` 要求列表里全是字符串。写 `"".join([1, 2, 3])` 会报错，要先转：`"".join(map(str, [1, 2, 3]))`。

字符与编号：

```python
print(ord('a'), ord('z'), ord('A'), ord('0'))   # 97 122 65 48
print(chr(97))                                  # a
print(ord('c') - ord('a'))                      # 2   'c' 是第 2 个字母（从 0 数）
```

做「统计 26 个字母出现次数」的题，会用 `ord(c) - ord('a')` 把字母变成 0～25 的下标。

---

## 3. 字典 `dict`：按名字查东西

列表靠「第几个」找数据，字典靠「名字」（叫**键**）找数据，就像通讯录按姓名查电话。

```python
d = {"苹果": 5, "香蕉": 3}
print(d["苹果"])       # 5
d["橘子"] = 8          # 加一对
d["苹果"] = 6          # 改
print(len(d))          # 3
del d["香蕉"]          # 删
print("苹果" in d)     # True   ← 查的是「键」在不在，不是值
```

**查东西很快**：不管字典里有 10 个还是 10 万个键，按名字取都是一瞬间。这是它比列表厉害的地方——列表查「在不在」要一个个翻，字典直接算出位置。

### 3.1 键不存在时会报错，三种安全写法

```python
d = {"a": 1}
# print(d["x"])        # KeyError: 'x'   ← 直接报错
print(d.get("x"))      # None            取不到就给 None，不报错
print(d.get("x", 0))   # 0              取不到给指定的默认值
print(d.setdefault("x", 0))   # 0       取不到就先存一个默认值再返回
```

`d.get(键, 默认值)` 是刷题里最常用的写法，尤其是计数：

```python
cnt = {}
for ch in "abracadabra":
    cnt[ch] = cnt.get(ch, 0) + 1
print(cnt)    # {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}
```

`setdefault` 在「分组」时特别顺手：

```python
groups = {}
for word in ["eat", "tea", "tan", "ate"]:
    key = "".join(sorted(word))
    groups.setdefault(key, []).append(word)
print(groups)
# {'aet': ['eat', 'tea', 'ate'], 'ant': ['tan']}
```

一行就完成了「这个组还不存在就先建个空列表」。

### 3.2 遍历字典的三种方式

```python
d = {"a": 1, "b": 2, "c": 3}

for k in d:                  # 只要键
    print(k, d[k])

for v in d.values():         # 只要值
    print(v)

for k, v in d.items():       # 键和值都要 ← 最常用
    print(k, v)
```

`for k, v in d.items()` 会自动把每一对拆成两个变量。

**遍历时不能改变字典的大小**：

```python
for k in d:
    del d[k]      # RuntimeError: dictionary changed size during iteration
```

要删就先做一份快照：`for k in list(d.keys()): ...`。

### 3.3 什么能当键

键必须是「不可变」的东西。数字、字符串、元组都可以：

```python
d = {}
d[1] = "数字可以"
d["abc"] = "字符串可以"
d[(2, 3)] = "坐标 (行, 列) 也可以，网格题常用"
# d[[1, 2]] = "列表不行"     # TypeError: unhashable type: 'list'
```

Python 3.7 起字典**保证按插入顺序遍历**，调试时输出稳定，但刷题基本用不上这个性质。

### 3.4 字典的三种典型用途

| 用途 | 长什么样 | 例子 |
|---|---|---|
| **查配对** | 边走边查「要找的那个在不在」，不在就把自己记下来 | 两数之和 |
| **计数** | `d[x] = d.get(x, 0) + 1` | 统计频次 |
| **分组** | `d.setdefault(组名, []).append(x)` | 字母异位词分组 |

第一种的骨架值得现在就记住：

```python
def two_sum(nums, target):
    seen = {}                       # 值 -> 下标
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []
```

「**先查后存**」是这题的全部考点：如果先存再查，输入 `[3]`、`target=6` 会错误地让同一个元素配自己。

---

## 4. 集合 `set`：只关心「在不在」

```python
s = set()
s.add(1)
s.add(1)             # 重复加没效果
s.add(2)
print(s, len(s))     # {1, 2} 2
print(1 in s)        # True   ← 一瞬间，和字典一样快
s.discard(1)         # 删，不存在也不报错
s.remove(99)         # 删，不存在会报错
```

`a = {1, 2, 3}` 是集合字面量（注意 `{}` 是空字典，不是空集合，空集合要写 `set()`）。

```python
a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)    # {1, 2, 3, 4, 5}   并集
print(a & b)    # {3}                交集
print(a - b)    # {1, 2}             差集
print(a ^ b)    # {1, 2, 4, 5}      只在一边出现的
```

最常用的是**去重**和**快速判存在**：

```python
nums = [1, 2, 2, 3, 3, 3]
print(list(set(nums)))       # [1, 2, 3]（顺序不保证）
print(len(set(nums)))        # 3   有几不同的数
```

一个非常常见的转换：

```python
nums = [1, 2, 3]
print(3 in nums)          # True，但要从头翻
print(3 in set(nums))     # True，一瞬间 —— 但 set(nums) 本身要花时间
```

**别在循环里反复 `set(nums)`**：建一次要翻一遍全部数据，放在 n 次循环里就变成翻 n 遍。要建就在循环外建一次。

---

## 5. 元组 `tuple`：不能改的列表

```python
t = (1, 2)
print(t[0], len(t))     # 1 2
# t[0] = 9              # TypeError，不能改
a, b = t                # 拆包
```

单个元素的元组要写逗号：`(1,)`，否则 `(1)` 只是个加了括号的数字。

它主要用在三个地方：

1. **当字典的键**（因为不可变）：坐标 `(行, 列)` 特别常用。
2. **函数返回多个值**（[L02 §5.2](L02-control-and-functions.md)：本质就是元组）。
3. **放进堆里比较**（[L07](L07-search-stack-heap.md) 会讲）。

比较规则是**字典序**：先比第一个，相同再比第二个。

```python
print((1, 5) < (1, 3))    # False
print(sorted([(2, "b"), (1, "c"), (1, "a")]))
# [(1, 'a'), (1, 'c'), (2, 'b')]
```

所以「先按第一项、再按第二项排」直接 `sorted(列表)` 就行，不用额外写 `key`。

---

## 6. 推导式：一行造出一个盒子

```python
[x * x for x in range(6)]                  # [0, 1, 4, 9, 16, 25]
[x for x in range(10) if x % 2 == 0]       # [0, 2, 4, 6, 8]   过滤
[x if x > 0 else 0 for x in [-1, 2, -3]]  # [0, 2, 0]          二选一
```

**两种 `if` 位置别搞混**：

- `[... for x in a if 条件]`：`if` 在后面 = **过滤**，不满足的不进结果，长度可能变短
- `[A if 条件 else B for x in a]`：`if` 在前面 = **对每个元素做选择**，长度不变

嵌套（二维展平、造矩阵）：

```python
mat = [[1, 2], [3, 4]]
print([x for row in mat for x in row])    # [1, 2, 3, 4]
print([[0] * 3 for _ in range(3)])        # 3×3 零矩阵，坑 2 的正确写法
```

嵌套的阅读顺序是「**从左到右，外循环在前**」，和手写双层 `for` 完全一致。

字典、集合也能用：

```python
nums = [1, 2, 3]
print({x: x * x for x in nums})             # {1: 1, 2: 4, 3: 9}
print({x for x in [1, 1, 2]})               # {1, 2}
print({i: c for i, c in enumerate("abc")})  # {0: 'a', 1: 'b', 2: 'c'}
```

**什么时候别用推导式**：循环里要维护好几个互相影响的状态、需要 `break`、有副作用、或者写完自己都要读两遍才懂——这些情况老实写循环。判断标准就一条：**能不能一眼看出它在干什么**。

---

## 7. 所有盒子通用的工具

```python
a = [3, 1, 4, 1, 5]

print(len(a))                      # 5    长度
print(sum(a), min(a), max(a))      # 14 1 5
print(any(x > 4 for x in a))       # True  有没有一个满足
print(all(x > 0 for x in a))       # True  是不是全满足
print(sorted(a))                   # [1, 1, 3, 4, 5]
print(list(reversed(a)))           # [5, 1, 4, 1, 3]
print(list(enumerate(a)))          # [(0,3), (1,1), (2,4), (3,1), (4,5)]
print(list(zip([1,2,3], "abc")))   # [(1,'a'), (2,'b'), (3,'c')]
print(3 in a)                      # True  查存在
```

`any` / `all` 里的东西没有方括号，这叫生成器表达式，它算到能满足就停，不会白白构造一整个列表。

`reversed(a)` 是「倒着走」的惰性对象，不复制数据；`a[::-1]` 会造一个新列表。只想遍历用前者。

---

## 8. 一张总表：哪个操作划算

| 操作 | 列表 | 字典 | 集合 | 字符串 |
|---|---|---|---|---|
| 按下标/键取 | 一瞬间 | 一瞬间 | — | 一瞬间 |
| 末尾加 | 一瞬间 | — | — | — |
| 开头加/删 | **很慢** | — | — | — |
| 查「在不在」 | **要翻一遍** | 一瞬间（查键） | 一瞬间 | 要翻一遍 |
| 插入/删除 | 中间很慢 | 一瞬间 | 一瞬间 | 不能改 |
| 切片 | 花一段长度的时间 | — | — | 花一段长度的时间 |
| 排序 | 比较多轮 | — | — | — |

**整张表最要命的两格**：列表的「开头增删慢」和「查存在要翻一遍」。它们看起来人畜无害，却最容易让代码超时。

---

## 9. 动手练

**先写再对答案。**

1. `a = [1,2,3,4,5,6]`，用切片取出前三个、后三个、偶数位置的元素、反转。
2. 写 `rotate(nums, k)`：把列表**原地**向右轮转 k 位（用切片赋值，不许返回新列表）。
3. 写 `uniq_sorted(nums)`：去重后升序，一行搞定。
4. 造 4×4 零矩阵，把主对角线设成 1，打印验证只有对角线是 1。
5. 写 `word_count(s)`：统计每个单词出现次数，返回字典。
6. `"a,b,,c".split(",")` 和 `"a,b,,c".split()` 分别得到什么？
7. 写 `char_index(s)`：返回 `{字符: 第一次出现的下标}`。
8. 写 `anagram_key(s)`：让 `"eat"` 和 `"tea"` 得到同一个 key。
9. 用一个表达式判断 `nums = [1,2,3]` 里有没有重复元素。
10. 不运行，写出输出：
    ```python
    a = [1, 2, 3]
    b = a
    c = a[:]
    b.append(4)
    c[0] = 9
    print(a, b, c, len(a))
    ```
11. 用列表推导式得到 `[(i, i*i) for i in range(1, 6)]`，但只保留平方为偶数的项。
12. 写 `count_chars(s)` 返回字符计数字典，不许用任何现成计数工具。

<details>
<summary>参考答案</summary>

**1**

```python
a = [1, 2, 3, 4, 5, 6]
print(a[:3], a[-3:], a[::2], a[::-1])
# [1, 2, 3] [4, 5, 6] [1, 3, 5] [6, 5, 4, 3, 2, 1]
```

**2**

```python
def rotate(nums, k):
    n = len(nums)
    k %= n
    nums[:] = nums[-k:] + nums[:-k]

a = [1, 2, 3, 4, 5]
rotate(a, 2)
print(a)     # [4, 5, 1, 2, 3]
```

左边必须是 `nums[:]`。写成 `nums = ...` 只是让函数内部的变量指向了新列表，外面那个列表根本没变——这是「原地修改」题最经典的错法。

**3**

```python
def uniq_sorted(nums):
    return sorted(set(nums))
```

**4**

```python
n = 4
m = [[0] * n for _ in range(n)]
for i in range(n):
    m[i][i] = 1
for row in m:
    print(row)
```

**5**

```python
def word_count(s):
    d = {}
    for w in s.split():
        d[w] = d.get(w, 0) + 1
    return d
```

**6** `"a,b,,c".split(",")` → `['a', 'b', '', 'c']`，保留中间的空字段；`"a,b,,c".split()` → `['a,b,,c']`（没有空白字符可切）。

**7**

```python
def char_index(s):
    d = {}
    for i, c in enumerate(s):
        d.setdefault(c, i)      # 已存在就不覆盖
    return d
```

**8**

```python
def anagram_key(s):
    return "".join(sorted(s))
```

`sorted("eat")` 得到 `['a','e','t']`（字符列表），要 `join` 回字符串才能当字典的键。

**9**

```python
len(set(nums)) != len(nums)
```

**10** `[1, 2, 3, 4] [1, 2, 3, 4] [9, 2, 3] 4`。`b` 和 `a` 是同一个列表；`c` 是复制出来的新列表。

**11**

```python
[(i, i * i) for i in range(1, 6) if (i * i) % 2 == 0]
# [(2, 4), (4, 16)]
```

**12**

```python
def count_chars(s):
    d = {}
    for c in s:
        d[c] = d.get(c, 0) + 1
    return d
```

</details>

---

## 10. 本章坑清单（建议抄下来）

| # | 坑 | 正确做法 |
|---|---|---|
| 1 | `a.sort()` 返回 `None` | 要新列表用 `sorted(a)` |
| 2 | `[[0]*n]*m` 行共享 | `[[0]*n for _ in range(m)]` |
| 3 | 边遍历边删 | 推导式生成新列表，或倒着删 |
| 4 | `a = b` 以为是复制 | `b = a[:]`，嵌套用 `copy.deepcopy` |
| 5 | 循环里 `pop(0)` | 用 `collections.deque`（下章） |
| 6 | 循环里反复 `x in list` | 建一次 `set` |
| 7 | `d[k]` 键不存在 | `d.get(k, 默认值)` |
| 8 | 遍历字典时增删键 | 先 `list(d.keys())` 做快照 |
| 9 | 直接改字符串里的字符 | `list(s)` → 改 → `"".join(...)` |
| 10 | 想要字母序号写成 `c - 'a'` | `ord(c) - ord('a')` |
| 11 | 把 `path` 直接存进结果 | `res.append(path[:])` |
| 12 | 原地修改写成 `nums = ...` | `nums[:] = ...` |

---

## 11. 本章自测（闭卷）

1. `a = [0,1,2,3,4]`，写出 `a[1:4]`、`a[::-2]`、`a[-2:]`、`a[10:]`。
2. 说出 `a[i]`、`a.append(x)`、`a.pop(0)`、`x in a` 各自「花多少力气」。
3. 写一行代码创建 3×4 零矩阵，且改 `m[0][0]` 不影响其他行。
4. 写 `first_duplicate(nums)`：返回第一个重复出现的元素，没有返回 `None`。
5. 说明 `d.get(k, 0)`、`d[k]`、`d.setdefault(k, 0)` 在键不存在时的区别。
6. `"".join([1, 2, 3])` 为什么报错？怎么修？
7. **口述题**：为什么把 `path` 直接存进结果列表，最后会得到一堆空列表？怎么修？

<details>
<summary>自测答案</summary>

1. `[1, 2, 3]`；`[4, 2, 0]`；`[3, 4]`；`[]`。
2. 按下标取、末尾加都是一瞬间；开头删要挪动所有元素；查存在要从头翻一遍。
3. `m = [[0] * 4 for _ in range(3)]`。
4.
   ```python
   def first_duplicate(nums):
       seen = set()
       for x in nums:
           if x in seen:
               return x
           seen.add(x)
       return None
   ```
5. `d[k]` 直接报错；`get(k, 0)` 返回 0 且不插入；`setdefault(k, 0)` 会插入 `k: 0` 再返回 0。
6. `join` 要求列表里全是字符串，整数要先转换：`"".join(map(str, [1, 2, 3]))` 或 `"".join(str(x) for x in [1,2,3])`。
7. 因为存进去的是同一个列表对象的标签，后面 `path.pop()` 把它清空时，之前存的所有位置看到的都是同一个被清空的列表。存快照即可：`res.append(path[:])`。

</details>

---

## 12. 下章预告

四个盒子已经够你动手写第一道真题了。但还有些场景它们应付不来：

- 需要频繁从**开头**删元素（列表很慢）
- 需要「每次自动取最小/最大那个」（堆）
- 需要「这个键不存在时自动给个空列表」（更省事的字典）
- LeetCode 给的代码框里那个 `class Solution:` 和 `self` 到底是什么意思
- 代码跑错了怎么看中间变量

[L04](L04-toolbox.md) 把这些补齐，然后 [L05](L05-algorithm-thinking.md) 正式开始讲「算法思维」——怎么读题、怎么从笨办法想到好办法、怎么判断代码会不会超时。学完那两章，就可以进 [L06](L06-array-and-hash.md) 开刷了。
