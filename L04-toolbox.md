# L04 · 常用工具、LeetCode 代码框、还有怎么调试

这一章补四件事：几个特别好用的标准库工具、LeetCode 给的代码框怎么读、链表和树的节点长什么样、代码写错了怎么查。

工具部分**不用背**。第一遍只记「遇到什么事该想到谁」，用到时回来抄代码，抄三次自然记住。

---

## 1. `collections`：四个天天见的帮手

用之前先写一行导入：

```python
from collections import defaultdict, Counter, deque, OrderedDict
```

### 1.1 `defaultdict`：键不存在时自动准备好

[L03 §3.1](L03-containers.md) 的分组写法要 `setdefault`，用 `defaultdict` 更省事：

```python
from collections import defaultdict

groups = defaultdict(list)          # 值默认是「空列表」
for word in ["eat", "tea", "tan", "ate", "nat"]:
    groups["".join(sorted(word))].append(word)
print(dict(groups))
# {'aet': ['eat', 'tea', 'ate'], 'ant': ['tan', 'nat']}
```

括号里传的是**「造默认值的工厂」**，不是造好的值：写 `defaultdict(list)`，不能写 `defaultdict([])`。

三种最常用的：

```python
defaultdict(list)   # 分组、邻接表；默认值是空列表
defaultdict(int)    # 计数；默认值是 0
defaultdict(set)    # 去重集合；默认值是空集合

cnt = defaultdict(int)
for ch in "abracadabra":
    cnt[ch] += 1                   # 不用先判断键在不在
print(dict(cnt))                   # {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}
```

**一个细节**：`k in d` 只查不取，**不会**触发默认值创建；只有 `d[k]` 会。所以「只看一眼在不在」不会污染字典。

### 1.2 `Counter`：专门数次数

```python
from collections import Counter

c = Counter("abracadabra")
print(c)                    # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
print(c["a"], c["z"])       # 5 0   ← 不存在的键给 0，不报错
print(c.most_common(2))     # [('a', 5), ('b', 2)]   出现最多的两个
```

还能做加减和交集，判断「两个字符串字母组成是否相同」「窗口里够不够」时很顺手：

```python
a = Counter("aab")
b = Counter("abb")
print(a - b)      # Counter({'a': 1})          只留正的
print(a & b)      # Counter({'a': 1, 'b': 1})  取较小值
print(a == Counter("baa"))   # True   组成相同
```

**坑**：`c[k]` 对不存在的键返回 0（普通字典会报错），这很方便；但 `c[k] -= 1` 会真的插进来一个负数键。做「窗口计数」时，减到 0 的键最好 `del` 掉，否则判断长度会出错。

### 1.3 `deque`：两头都能瞬间增删的队列

[L03 §1.4](L03-containers.md) 说过，`list.pop(0)` 要挪动后面所有元素，慢得离谱。`deque` 就是来解决这个的：

```python
from collections import deque

q = deque()
q.append(1)          # 右端进
q.append(2)
q.appendleft(0)      # 左端进
print(q)             # deque([0, 1, 2])
print(q.popleft())   # 0   左端出，一瞬间
print(q.pop())       # 2   右端出，一瞬间
```

两端增删都是一瞬间。它还有一个「固定长度」的用法，自动丢掉最左边：

```python
d = deque(maxlen=3)
for x in range(5):
    d.append(x)
    print(list(d))
# [0] / [0,1] / [0,1,2] / [1,2,3] / [2,3,4]
```

**什么时候必须用**：需要「先进先出」的队列（按层遍历树、网格一圈圈扩散、滑动窗口最大值）。这些场景用 `list.pop(0)` 会超时。

**它不擅长的**：按下标随机访问中间元素比较慢。不过刷题里队列只用两头，正好避开。

### 1.4 `OrderedDict`：按访问顺序淘汰

```python
from collections import OrderedDict

d = OrderedDict()
d["a"] = 1
d["b"] = 2
d.move_to_end("a")            # 把 a 挪到「最新」
print(list(d.keys()))          # ['b', 'a']
print(d.popitem(last=False))   # ('b', 2)   弹出「最旧」的
```

普通字典也有插入顺序，所以 `OrderedDict` 现在主要就靠这两个独门操作。做「LRU 缓存」那道题时能把代码压到十几行（见 [L08](L08-linkedlist-tree.md)）。

---

## 2. `heapq`：每次自动拿到最小的

「堆」是一种盒子：你往里随便丢数字，它永远能**一瞬间告诉你最小的是谁**，取走最小的也很快。

```python
import heapq

h = []
heapq.heappush(h, 3)
heapq.heappush(h, 1)
heapq.heappush(h, 2)
print(h[0])                 # 1   最小的一直在堆顶
print(heapq.heappop(h))     # 1   弹出最小的
print(h)                    # [2, 3]
```

**Python 的堆只有「小根堆」**（堆顶最小）。想每次拿最大的，把数字**取负号**存进去，取出来再取负：

```python
h = []
for x in [3, 1, 5]:
    heapq.heappush(h, -x)
print(-heapq.heappop(h))    # 5
```

常用函数：

```python
heapq.heapify(a)                  # 把一个已有列表原地变成堆，一次搞定
heapq.heappush(h, x)              # 放进一个
heapq.heappop(h)                  # 弹出最小的
heapq.heappushpop(h, x)           # 放进 x，再弹出最小的
heapq.heapreplace(h, x)           # 先弹出最小的，再放进 x
heapq.nlargest(3, nums)           # 最大的 3 个
```

`heappushpop` 和 `heapreplace` 不一样：新元素比堆顶还小时，`heappushpop` 会把新元素自己弹出去、堆不变；`heapreplace` 则无条件换掉堆顶。没想清楚时用 `heappushpop` 更安全。

**求「第 K 大」的标准做法**：维护一个大小恰好为 K 的**小根堆**，堆顶就是第 K 大的那个。

```python
def kth_largest(nums, k):
    h = []
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heapreplace(h, x)   # 已经判断过 x 更大了
    return h[0]
```

**元组也能进堆**，按第一项比、第一项相同再比第二项：

```python
h = []
heapq.heappush(h, (2, "任务B"))
heapq.heappush(h, (1, "任务A"))
print(heapq.heappop(h))    # (1, '任务A')
```

如果第二项是无法比较的对象（比如自己定义的节点），前两项又可能相等，会报错。标准解法是插一个不会重复的序号：

```python
heapq.heappush(h, (值, 序号, 对象))   # 序号保证永远不会比到「对象」
```

---

## 3. 其他随手可用的

```python
import bisect
a = [1, 2, 2, 2, 4]
print(bisect.bisect_left(a, 2))    # 1   第一个 >= 2 的位置
print(bisect.bisect_right(a, 2))   # 4   第一个 > 2 的位置
# 2 出现的次数 = 4 - 1 = 3
```

`bisect` 要求列表**已经升序**，否则会静默给出错误答案（不报错）。二分查找那章会详讲。

```python
import math
print(math.inf, -math.inf)      # 无穷大 / 负无穷
print(math.isqrt(17))           # 4    整数平方根，大数也不丢精度
print(math.gcd(12, 18))         # 6
print(math.prod([2, 3, 4]))     # 24
print(math.comb(5, 2))          # 10   组合数
```

```python
from functools import cache

@cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(100))    # 354224848179261915075
```

`@cache` 是「算过的结果记下来，下次直接用」。不加它，`fib(40)` 就要跑很久；加了之后每个 `n` 只算一次。动态规划那章会重点用它。**限制**：参数必须是不可变的东西（数字、字符串、元组），列表要转成元组；函数必须是「同样输入永远给同样输出」。

```python
import itertools
print(list(itertools.combinations([1,2,3], 2)))   # [(1,2),(1,3),(2,3)]
print(list(itertools.permutations([1,2], 2)))     # [(1,2),(2,1)]
print(list(itertools.product([0,1], repeat=2)))   # [(0,0),(0,1),(1,0),(1,1)]
print(list(itertools.accumulate([1,2,3,4])))      # [1,3,6,10]   前缀和
```

`itertools` 能一行枚举出所有组合/排列。但**回溯题必须自己手写 DFS**（考点就是那个过程），这些工具主要用来造小数据验证你的答案对不对。

---

## 4. 读懂 LeetCode 给你的代码框

打开一道题，Python 那边给出的是：

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        ...
```

只需要知道四件事：

1. **`class Solution:` 是平台固定的外壳**，别改名字，别自己创建实例，别写 `main()`。平台在背后会做类似 `Solution().twoSum(...)` 的调用。
2. **第一个参数永远叫 `self`，但调用时不用传**。你写在 `class` 里的方法都要带它。
3. **`nums`、`target` 已经是给好的数据**，绝对不要写 `input()` 去读。
4. **用 `return` 交答案**，不要 `print`。`print` 的内容不算答案，还拖慢速度。

`: List[int]`、`-> List[int]` 这些叫**类型注解**，只是给人和编辑器看的注释，**Python 运行时完全不检查**。写题解时全删掉，平台也接受：

```python
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
        return []
```

但要能读懂题目给的注解，尤其：

| 注解 | 意思 | 你要留意的 |
|---|---|---|
| `Optional[X]` | 可能是 X，也可能是 `None` | 第一行先判空：`if head is None: return ...` |
| `List[List[int]]` | 二维列表 | 访问前先确认不是空的 |
| `ListNode` / `TreeNode` | 平台已经定义好的节点类型 | 用 `.val`、`.next`、`.left`、`.right` |
| `-> None` | 要求**原地修改**传入的对象 | 别返回新列表 |

### 4.1 需要跨方法记东西时

有些题要写好几个方法配合，想共享一个变量：

```python
class Solution:
    def dfs(self, node):
        if node is None:
            return 0
        return 1 + max(self.dfs(node.left), self.dfs(node.right))

    def countNodes(self, root):
        return self.dfs(root)
```

`self.xxx` 是挂在这个对象上的属性，所有方法都能用。比如要统计总数：

```python
class Solution:
    def dfs(self, node):
        if node is None:
            return
        self.ans += 1
        self.dfs(node.left)
        self.dfs(node.right)

    def countNodes(self, root):
        self.ans = 0            # 一定要在入口第一行重置
        self.dfs(root)
        return self.ans
```

**那个「重置」不能省**：平台可能用同一个对象连着跑好几组测试，不重置就会把上一组的答案带进下一组，表现为「样例能过、提交就错」。

---

## 5. 链表和树的节点长什么样

做链表/二叉树的题时，平台已经定义好了节点，你直接用就行。但**在本地调试必须自己写一份**：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

`__init__` 是「造一个新节点时怎么初始化」，`self` 指这个节点自己。`node.val` 是值，`node.next` 是「下一个节点」，空用 `None` 表示。

加一个 `__repr__` 能让打印变好看：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        vals, cur = [], self
        while cur:
            vals.append(str(cur.val))
            cur = cur.next
        return "->".join(vals) + "->None"

head = ListNode(1, ListNode(2, ListNode(3)))
print(head)     # 1->2->3->None
```

不加的话，打印出来是 `<__main__.ListNode object at 0x...>`，调试时什么也看不出来。

把列表变成链表、再变回来的工具（本地测试必备）：

```python
def build_list(vals):
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def dump_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out

print(dump_list(build_list([1, 2, 3])))   # [1, 2, 3]
```

那个 `dummy`（虚拟头节点）本身就是链表题最常用的技巧，[L08](L08-linkedlist-tree.md) 会正式讲。

---

## 6. 本地调试：比在网页上盲改快十倍

### 6.1 最小可运行模板

把题解复制到本地 `.py` 文件，加几行就能测：

```python
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
        return []

if __name__ == "__main__":
    s = Solution()
    assert s.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert s.twoSum([3, 2, 4], 6) == [1, 2]
    assert s.twoSum([3, 3], 6) == [0, 1]
    print("全部通过")
```

`assert 条件` 的意思是「我断言这个条件成立」，不成立就立刻停在那一行的 `AssertionError`。比 `print` 好在哪：**不用肉眼比对输出**，跑完没报错就是全对。

`if __name__ == "__main__":` 表示「这个文件被直接运行时才执行下面这段」，照抄就行，不用深究。

### 6.2 测试用例怎么造

三个样例不是随便挑的，分别覆盖「常规」「答案不在开头」「有重复元素」。做每道题提交前，至少过一遍这八类：

| # | 用例 | 会暴露什么 |
|---|---|---|
| 1 | 空输入 `[]` / `""` / `None` | 忘判空、取了第 0 个元素 |
| 2 | 只有一个元素 | 循环边界、初始下标 |
| 3 | 两个元素 | 交换、相邻比较 |
| 4 | 全都一样 `[2,2,2]` | 去重逻辑、`>` 写成 `>=` |
| 5 | 含负数、含 0 | 整除取模、初始值设成了 0 |
| 6 | 已经排好序 / 完全倒序 | 二分边界 |
| 7 | 很大的数、很长的串 | 会不会超时 |
| 8 | 答案在开头 / 结尾 / 根本不存在 | 提前返回、兜底返回值 |

第 5 条里「初始值设成 0」是新手最常犯的：求最大值写 `best = 0`，遇到全负数数组就错。一律用 `float("-inf")`。

### 6.3 打印中间过程

```python
l, r = 0, 5
while l < r:
    mid = (l + r) // 2
    print(f"l={l} r={r} mid={mid}")
    ...
```

递归时可以带个深度参数，输出自动形成缩进树，一眼看清调用顺序：

```python
def dfs(node, depth=0):
    if node is None:
        return 0
    print("  " * depth + f"访问 {node.val}")
    return 1 + max(dfs(node.left, depth + 1), dfs(node.right, depth + 1))
```

调试完记得把 `print` 删掉再提交——大量打印会拖慢运行，甚至超时。

### 6.4 对拍：用笨办法验证巧办法

这是整套教程里最提速的一招。思路很简单：**写一个显然正确但很慢的笨办法，再写你的巧办法，用随机小数据跑几百组，一旦结果不一致就把那组数据打出来。**

```python
import random

def brute(nums):
    """笨办法：枚举所有子数组求和，取最大"""
    n = len(nums)
    best = float("-inf")
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            best = max(best, s)
    return best

def fast(nums):
    """巧办法：一遍扫描"""
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

random.seed(0)                       # 固定种子，失败才能复现
for t in range(300):
    a = [random.randint(-20, 20) for _ in range(random.randint(1, 12))]
    if brute(a) != fast(a):
        print(f"第 {t} 组不一致: {a} 笨={brute(a)} 巧={fast(a)}")
        break
else:
    print("300 组全部一致")
```

四条纪律：

1. 笨办法要**显然正确**，最好直接照题目定义枚举，别用任何技巧
2. 固定 `random.seed`，否则这次失败下次复现不了
3. 数据要小（笨办法才跑得动），但分布要刁：负数、重复、单元素都要有
4. 失败时打印完整输入，然后不断删元素直到它「刚好还出错」，得到最小反例

### 6.5 报错速查

| 报错 | 多半是 |
|---|---|
| `IndentationError` | 空格 / Tab 混用，粘贴丢了缩进 |
| `SyntaxError` | 漏冒号、括号没配对；看报错行**和上一行** |
| `NameError` | 拼写、大小写、变量没定义 |
| `TypeError: list indices ... not float` | 用 `/` 算了下标，改 `//` |
| `TypeError: 'NoneType' object is not iterable` | 把 `a.sort()` 的返回值拿去遍历了 |
| `TypeError: unhashable type: 'list'` | 拿列表当字典键，改成元组 |
| `IndexError` | 下标越界、空列表取了 `a[0]` |
| `KeyError` | 字典键不存在，用 `get` |
| `AttributeError: 'NoneType' object has no attribute 'val'` | 节点是 `None` 却去取 `.val`；检查判空和短路顺序 |
| `RecursionError` | 递归超过 1000 层，或没写终止条件 |
| `Time Limit Exceeded` | 见 [L05 §5](L05-algorithm-thinking.md) |

最后一行是错误类型和原因，往上几行是文件和行号。**从最后一行读起**。

---

## 7. 递归深度：一个 Python 特有的限制

```python
import sys
print(sys.getrecursionlimit())   # 1000
```

Python 默认最多允许约 1000 层嵌套调用（本机实测在第 999 层触发 `RecursionError`）。一条 2000 个节点的链表用递归遍历会直接炸。

刷题时可以在文件顶部加一行：

```python
import sys
sys.setrecursionlimit(10 ** 6)
```

但更稳的办法是**能改成循环就改**。树的遍历、链表操作都有迭代写法，[L08](L08-linkedlist-tree.md) 会讲到。

---

## 8. 动手练

1. 用 `defaultdict(list)` 把 `["eat","tea","tan","ate","nat","bat"]` 按字母组成分组。
2. 用 `Counter` 写 `top_k(nums, k)`：返回出现次数最多的 k 个值。
3. 用 `deque` 写 `sliding_max(nums, k)`：返回每个长度为 k 的窗口的最大值（先用 `max()` 实现即可）。
4. 用 `heapq` 写 `kth_largest(nums, k)`，并和 `sorted(nums)[-k]` 随机对拍 100 组。
5. 用 `bisect` 写 `count_in(sorted_a, x)`：返回 x 在有序列表里出现几次。
6. 用 `@cache` 写 `climb(n)`：每次爬 1 或 2 阶，到 n 阶有几种走法，打印 `climb(50)`。
7. 给 `ListNode` 加 `__repr__`，构造 `1->2->3` 并打印。
8. 用 `build_list` / `dump_list` 测「反转链表」在 `[]`、`[1]`、`[1,2,3]` 三种输入下的结果。
9. 写一段 `assert` 测试，覆盖两数之和的「常规」「答案在末尾」「有重复」三种情况。

<details>
<summary>参考答案</summary>

**1**

```python
from collections import defaultdict
d = defaultdict(list)
for w in ["eat", "tea", "tan", "ate", "nat", "bat"]:
    d["".join(sorted(w))].append(w)
print(dict(d))
```

**2**

```python
from collections import Counter
def top_k(nums, k):
    return [x for x, _ in Counter(nums).most_common(k)]
```

**3**

```python
from collections import deque
def sliding_max(nums, k):
    q, ans = deque(), []
    for i, x in enumerate(nums):
        q.append(x)
        if len(q) > k:
            q.popleft()
        if len(q) == k:
            ans.append(max(q))
    return ans
```

（这个版本每个窗口都扫一遍，数据大时慢；[L07](L07-search-stack-heap.md) 会讲真正快的单调队列写法。）

**4**

```python
import heapq, random
def kth_largest(nums, k):
    h = []
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heapreplace(h, x)
    return h[0]

random.seed(0)
for _ in range(100):
    a = [random.randint(-10, 10) for _ in range(random.randint(1, 20))]
    k = random.randint(1, len(a))
    assert kth_largest(a, k) == sorted(a)[-k]
print("对拍通过")
```

**5**

```python
import bisect
def count_in(a, x):
    return bisect.bisect_right(a, x) - bisect.bisect_left(a, x)
```

**6**

```python
from functools import cache
@cache
def climb(n):
    if n <= 2:
        return n
    return climb(n - 1) + climb(n - 2)
print(climb(50))    # 20365011074
```

**7 / 8**

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __repr__(self):
        vals, cur = [], self
        while cur:
            vals.append(str(cur.val)); cur = cur.next
        return "->".join(vals) + "->None"

def build_list(vals):
    dummy = ListNode(0); cur = dummy
    for v in vals:
        cur.next = ListNode(v); cur = cur.next
    return dummy.next

def dump_list(head):
    out = []
    while head is not None:
        out.append(head.val); head = head.next
    return out

def reverse(head):
    pre, cur = None, head
    while cur is not None:
        nxt = cur.next
        cur.next = pre
        pre, cur = cur, nxt
    return pre

for vals in ([], [1], [1, 2, 3]):
    print(vals, "->", dump_list(reverse(build_list(vals))))
# [] -> [] ; [1] -> [1] ; [1, 2, 3] -> [3, 2, 1]
```

**9**

```python
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
        return []

s = Solution()
assert s.twoSum([2, 7, 11, 15], 9) == [0, 1]
assert s.twoSum([3, 2, 4], 6) == [1, 2]
assert s.twoSum([3, 3], 6) == [0, 1]
print("全部通过")
```

</details>

---

## 9. 本章自测（闭卷）

1. `defaultdict(list)` 括号里为什么写 `list` 而不是 `[]`？
2. 为什么说队列不能用 `list.pop(0)`？
3. Python 的堆默认每次取最大还是最小？想取最大怎么办？
4. `bisect_left([1,2,2,2,4], 2)` 和 `bisect_right([1,2,2,2,4], 2)` 各返回什么？
5. `@cache` 对参数有什么要求？
6. `Optional[ListNode]` 是什么意思，看到它第一行该写什么？
7. 说出 `a.sort()` 和 `sorted(a)` 的两个区别。
8. **口述题**：本地对拍是哪四步？为什么它比盯着代码想更快？

<details>
<summary>自测答案</summary>

1. 需要传的是「能造出默认值的函数」，函数被调用时才造新列表；写 `[]` 是造好了一个具体的列表，语法上也不对。
2. `pop(0)` 要挪动后面所有元素，做 n 次总共是平方级，10 万个数实测要 8.59 秒；`deque.popleft()` 只要 0.003 秒。
3. 最小（小根堆）。把值取负存进去，取出来再取负。
4. `1` 和 `4`。
5. 参数必须不可变（数字、字符串、元组），列表要转元组；函数必须同样输入给同样输出。
6. 参数可能是 `None`。第一行写 `if head is None: return ...`。
7. `a.sort()` 原地改、返回 `None`；`sorted(a)` 造新列表、原列表不变，且能接任何可迭代对象。
8. 写一个显然正确的笨办法 → 固定随机种子造小数据 → 跑几百组比对 → 不一致时打印输入并缩小成最小反例。因为「想哪里错了」靠猜，而对拍会**直接把出错的输入送到你面前**。

</details>

---

## 10. 下章预告

工具齐了，接下来是本教程最关键的一章：**怎么想问题**。

[L05](L05-algorithm-thinking.md) 会讲清楚：为什么有的代码数据一多就卡死、「O(n)」到底在说什么、看到数据范围怎么反推该用什么办法、怎么从「两层循环的笨办法」一步步想到「一遍扫描的巧办法」、以及读一道题该问自己哪六个问题。

这一章不讲新语法，但它决定了后面 100 道题你是「看懂答案」还是「自己想出来」。
