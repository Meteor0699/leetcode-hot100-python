# L11 · 速查手册（打印版）

这一章不教新东西，只把「临时想查一下」的内容压成表格。刷题时开着它，忘了就查，别硬回忆。

---

## 1. 一页纸语法

下面是并列的速查条目，不是一段可执行的程序：

```text
# 输出 / 调试
print(x)
print(f"l={l} r={r} mid={mid}")     f-string，调试首选
print(f"{x=}")                       3.8+，连变量名一起打

# 类型与转换
int(x)  float(x)  str(x)  list(x)  set(x)  tuple(x)  bool(x)
type(x)  len(x)  ord('a')  chr(97)

# 运算
+ - * / // % **          / 得小数，// 向下取整，** 是幂，^ 是异或
== != < > <= >=          可链式：0 <= i < n
and or not               返回操作数本身，不是一定返回 True/False
is / is not              只用于 None
in / not in              查存在：dict/set 快，list 要翻一遍

# 分支
if cond:
    ...
elif cond2:
    ...
else:
    ...
v = A if cond else B     三元表达式

# 循环
for x in a: ...                         遍历值
for i, x in enumerate(a, start=0): ...  下标 + 值
for i in range(n): ...                  0 .. n-1
for i in range(a, b, step): ...         左闭右开 [a, b)
for i in range(n-1, -1, -1): ...        倒序
for k, v in d.items(): ...              字典键值
for x, y in zip(a, b): ...              两个序列一起
while cond: ...
break / continue                        没有 ++（写 i += 1）

# 函数
def f(a, b=0):              默认值别用 [] / {} / set()，用 None 兜底
    return a + b, a - b     多返回值 = 元组拆包
lam = lambda x: x[0]        只用于 sorted(key=...)

# 类（LeetCode 外壳）
class Solution:
    def method(self, nums):
        self.ans = 0         入口第一行重置共享状态
        return ...

# 其他
float('inf')  float('-inf')
assert cond                  挂了会停在那一行
```

**四条最容易忘的**：

| # | 规则 |
|---|---|
| 1 | 块靠**冒号 + 4 空格缩进**，`IndentationError` 先查空格 |
| 2 | `/` 得小数，算下标一律 `//` |
| 3 | `a.sort()` 原地返回 `None`；`sorted(a)` 返回新列表 |
| 4 | 比值用 `==`，只有 `None` 用 `is` |

---

## 2. 容器与代价速查

| 操作 | 写法 | 代价 |
|---|---|---|
| 建空 | `[]` `{}` `set()` | — |
| 定长初始化 | `[0] * n` | `O(n)` |
| 二维初始化 | `[[0] * n for _ in range(m)]` | **绝不写 `[[0]*n]*m`** |
| 索引 / 负下标 | `a[i]` `a[-1]` | 一瞬间 |
| 切片 | `a[l:r]` `a[::-1]` `a[::2]` | 花一段长度的时间，返回新列表 |
| 原地整段替换 | `a[:] = ...` | 原地改必须用这个 |
| 尾插 / 尾弹 | `a.append(x)` / `a.pop()` | 一瞬间，`pop()` 返回元素 |
| 头插 / 头弹 | `a.insert(0,x)` / `a.pop(0)` | **要翻一遍，用 `deque`** |
| 查存在 | `x in a` | 列表要翻一遍；集合/字典一瞬间 |
| 排序 | `a.sort()` / `sorted(a, key=...)` | `O(n log n)`，稳定 |
| 字典存取 | `d[k]` `d[k]=v` `k in d` | 一瞬间 |
| 字典安全取 | `d.get(k, 默认)` `d.setdefault(k, 默认)` | 一瞬间 |
| 拷贝 | `a[:]` / `copy.deepcopy(a)` | 嵌套结构要深拷贝 |
| 交换 / 滚动 | `a[i], a[j] = a[j], a[i]` | 右边先整体求值 |

**字符串**：`s.split()`（按空白切、丢空串）、`s.split(',')`（严格切、留空字段）、`','.join(字符串列表)`、`s.strip()`、`s[::-1]`、`ord(c) - ord('a')`。**不可变**：改字符要 `t = list(s)` → 改 → `''.join(t)`。

**真值判定（算「假」）**：`False None 0 0.0 "" [] {} set()`。所以 `if not stack:` 判栈空；但要判断数值恰好为 0 必须写 `if x == 0:`。

**本机实测**（Python 3.13）：简单循环约 5×10⁷ 次/秒、字典查找约 1.2×10⁷、集合判断约 1.4×10⁷。**估算按 1 秒 ≈ 10⁷ 次 Python 操作**（经验估计）。`list.pop(0)` 排空 10 万个数 8.59 秒，`deque.popleft()` 0.003 秒。

---

## 3. 标准库速查

| 需求 | 写法 | 代价 |
|---|---|---|
| 分组 / 计数 / 邻接表 | `defaultdict(list/int/set)` | 一瞬间 |
| 频次统计 | `Counter(a)`、`most_common(k)` | `O(n)` |
| 双端队列、BFS | `deque([x])`、`append/popleft` | 两端一瞬间 |
| LRU | `OrderedDict`、`move_to_end()`、`popitem(last=False)` | 一瞬间 |
| 最小堆 | `heapq.heappush/heappop/heapify` | `O(log n)` |
| 大根堆 | 存负数，取出再取负 | 同上 |
| 第 K 大 | 大小为 K 的小根堆 + `heapreplace` | `O(n log K)` |
| 二分插入位置 | `bisect_left / bisect_right` | `O(log n)` |
| 记忆化搜索 | `@cache`（3.9+） | 状态数 |
| 组合枚举（对拍用） | `itertools.combinations / permutations / product` | 惰性 |
| 前缀和 | `itertools.accumulate(a)` | `O(n)` |
| 数学 | `math.inf / isqrt / gcd / comb / prod` | — |
| 递归深度 | `sys.setrecursionlimit(10**6)` | 默认 1000 |

**用之前先问一句**：这个操作是不是在循环里？`set(a)`、`sorted(a)`、`a[:]`、`x in 列表` 放进循环就把复杂度乘一个 n。

---

## 4. 套路 → 题目总表

看到题目里的信号，先想到对应骨架，再回对应册读完整推理。

| 信号 | 先想到的骨架 | 册 |
|---|---|---|
| 找两个数、配对、补数 | 字典查配对，先查后存 | [L06](L06-array-and-hash.md) |
| 去重、分组、等价类 | 集合 / 字典 / `defaultdict(list)` | [L06](L06-array-and-hash.md) |
| 有序数组、找两个数 | 排序 + 对撞双指针 | [L06](L06-array-and-hash.md) |
| 连续子串、最长/最短 | 滑动窗口，`l` 只增不减 | [L06](L06-array-and-hash.md) |
| 子数组求和 + 含负数 | 前缀和 + 哈希，`cnt[0]=1` | [L06](L06-array-and-hash.md) |
| 每个窗口最大值 | 单调队列 `deque` 存下标 | [L06](L06-array-and-hash.md) |
| 矩阵、原地置换 | 四边界 / 转置 / 原地哈希 | [L06](L06-array-and-hash.md) |
| 出现次数、只出现一次 | 异或 / 摩尔投票 | [L06](L06-array-and-hash.md) |
| 有序、`O(log n)`、找边界 | 二分两个骨架 | [L07](L07-search-stack-heap.md) |
| 括号配对、嵌套展开 | 栈 | [L07](L07-search-stack-heap.md) |
| 下一个更大、最近比它矮 | 单调栈（存下标） | [L07](L07-search-stack-heap.md) |
| 第 K 大 / 前 K 个 | 大小为 K 的小根堆 | [L07](L07-search-stack-heap.md) |
| 动态维护中位数 | 双堆 | [L07](L07-search-stack-heap.md) |
| 每步选眼前最好 | 贪心（要能讲出理由） | [L07](L07-search-stack-heap.md) |
| 头节点可能被改 | 虚拟头 `dummy` | [L08](L08-linkedlist-tree.md) |
| 链表找中点 / 判环 | 快慢指针 | [L08](L08-linkedlist-tree.md) |
| 反转、K 组翻转 | `pre / cur / nxt` 三变量 | [L08](L08-linkedlist-tree.md) |
| 树深度、翻转、对称 | 递归三问 | [L08](L08-linkedlist-tree.md) |
| 按层、最短步数 | BFS + `for _ in range(len(q))` | [L08](L08-linkedlist-tree.md) |
| BST 相关 | 中序是升序 / 带上下界递归 | [L08](L08-linkedlist-tree.md) |
| 全局最优不能直接返回 | 递归返回单边值，`self.ans` 记全局 | [L08](L08-linkedlist-tree.md) |
| 所有排列 / 组合 / 子集 | 回溯三行骨架 + `path[:]` | [L09](L09-backtrack-graph-dp.md) |
| 网格连通、拓扑、前缀 | BFS / 入度队列 / Trie | [L09](L09-backtrack-graph-dp.md) |
| 最多/最少、能否凑出 | DP 五问，递归→记忆化→递推 | [L09](L09-backtrack-graph-dp.md) |
| 每个物品选一次 / 无限选 | 0-1 背包倒序 / 完全背包正序 | [L09](L09-backtrack-graph-dp.md) |
| 两个字符串比较、网格路径 | 二维 DP，可滚动成一维 | [L09](L09-backtrack-graph-dp.md) |

---

## 5. 报错速查

| 报错 | 八成是 |
|---|---|
| `IndentationError` | 空格 / Tab 混用、粘贴丢缩进 |
| `SyntaxError: invalid syntax` | 漏冒号、括号没配对；看报错行及上一行 |
| `NameError` | 拼写、大小写、变量没定义 |
| `TypeError: list indices ... not float` | 用 `/` 算了下标，改 `//` |
| `TypeError: 'NoneType' object is not iterable` | 把 `a.sort()` 的返回值拿去遍历了 |
| `TypeError: 'NoneType' object has no attribute 'val'` | 节点是 `None` 却去取 `.val` |
| `TypeError: unhashable type: 'list'` | 拿列表当字典键 / 集合元素，转元组 |
| `TypeError: '<' not supported` | 堆里对象不可比较，插序号 |
| `IndexError` | 下标越界、空列表取 `a[0]` / `a[-1]` |
| `KeyError` | 字典键不存在，用 `get` |
| `RecursionError` | 超过约 1000 层，或没写终止条件 |
| `UnboundLocalError` | 函数里改外层变量没声明，改用返回值 |
| `Time Limit Exceeded` | 查 [L05 §6.2](L05-algorithm-thinking.md) |
| **WA 但不报错** | 静默坑 → 边界用例 → 对拍 |

**读报错从最后一行往上**：最后一行是类型和原因，往上几行是文件和行号。

### 静默坑清单（不报错但答案错）

```
[ ] 默认参数里没有 [] / {} / set()
[ ] 收集答案是 path[:] 而不是 path
[ ] 二维容器用推导式创建
[ ] 没有在遍历中增删容器
[ ] 值比较用 ==，只有 None 用 is
[ ] 除法用 //（尤其算下标、算中点）
[ ] 计数用 .get(k,0) / defaultdict，没有裸 d[k] += 1
[ ] 所有 self.xxx 在入口第一行初始化
[ ] 含负数时确认过 // 和 % 的语义
[ ] 原地修改用 nums[:] = ... 且返回传入对象
[ ] 求最大值初始值是 -inf，求最小值是 inf
[ ] 0-1 背包倒序、完全背包正序
```

---

## 6. 100 题索引

题号即 LeetCode 题号，按本套教程的四册组织。

| 册 | 题号 | 题数 |
|---|---|---|
| [L06 数组与哈希](L06-array-and-hash.md) | 1、49、128、283、11、15、42、3、438、560、76、239、53、56、189、238、41、73、54、48、240、136、169、75、31、287 | 26 |
| [L07 二分栈堆贪心](L07-search-stack-heap.md) | 35、74、34、33、153、4、20、155、394、739、84、215、347、295、121、55、45、763 | 18 |
| [L08 链表与树](L08-linkedlist-tree.md) | 160、206、141、142、21、2、19、24、25、148、23、146、234、138、94、104、226、101、543、102、98、230、199、105、236、124、108、114、437 | 29 |
| [L09 回溯图论 DP](L09-backtrack-graph-dp.md) | 46、78、17、39、22、79、131、51、200、994、207、208、70、118、198、279、322、139、300、152、416、32、62、64、5、1143、72 | 27 |
| | **合计** | **100** |

分周安排见 [L10 §3](L10-training-plan.md)。

---

## 7. 提交前检查清单（打印贴在显示器旁）

```
语法 / 静默坑
[ ] 上面「静默坑清单」12 条过一遍
[ ] 删掉了调试 print
[ ] 没有 input() / 文件读写；答案用 return

算法 / 边界
[ ] 空输入、单元素、全重复、含负数、极值 都想过
[ ] 估算过复杂度，和 n 的上限对得上（L05 §2.2）
[ ] 循环里没有隐式 O(n)（L05 §3.2）
[ ] 队列用 deque；递归题设了 setrecursionlimit

工程
[ ] 本地 assert + 对拍通过
```

---

## 8. 暂时不用碰的清单

Hot 100 一道都用不到，别因为「没学全」而焦虑：

- 装饰器（自己写）、元类、描述符、上下文管理器、异步 `async/await`
- 正则表达式 `re`、文件读写、网络、数据库
- 异常处理 `try/except`（刷题里用 `if` 判空就够；报错反而应该让它崩）
- 多继承、运算符重载（除 `__repr__` / `__lt__` 这两个调试相关）
- 类型注解的进阶用法（泛型、静态检查）
- 第三方库（LeetCode 标准库够用，也不允许依赖）
- `functools.reduce`（用 `sum` / `math.prod` 更清楚）

等 100 题刷完、开始准备工程类笔试时再补，那时有具体场景，学得快得多。

---

## 索引

| 想要什么 | 去哪 |
|---|---|
| 完整路线与进度表 | [START-HERE.md](START-HERE.md) |
| 语法从零学 | [L01](L01-first-steps.md)、[L02](L02-control-and-functions.md)、[L03](L03-containers.md) |
| 工具与调试 | [L04](L04-toolbox.md) |
| 复杂度 / 算法思维 | [L05](L05-algorithm-thinking.md) |
| 100 题逐题讲解 | [L06](L06-array-and-hash.md) → [L09](L09-backtrack-graph-dp.md) |
| 训练计划 / 复盘表 | [L10](L10-training-plan.md) |
| 速查 / 报错 / 题号索引 | 本页 |
