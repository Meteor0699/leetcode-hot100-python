# L09 · 回溯、图论、动态规划（27 题）

最后一册，也是最难的一册。分三块：回溯（把所有可能试一遍）、图论（在网格和依赖关系里搜索）、动态规划（把大问题拆成会重复的小问题）。

| 部分 | 题号 · 题名 | 难度 |
|---|---|---|
| 回溯 | 46 全排列 · 78 子集 · 17 电话号码的字母组合 · 39 组合总和 · 22 括号生成 · 79 单词搜索 · 131 分割回文串 · 51 N 皇后 | 中×7 难 |
| 图论 | 200 岛屿数量 · 994 腐烂的橘子 · 207 课程表 · 208 实现 Trie | 中×4 |
| 动态规划 | 70 爬楼梯 · 118 杨辉三角 · 198 打家劫舍 · 279 完全平方数 · 322 零钱兑换 · 139 单词拆分 · 300 最长递增子序列 · 152 乘积最大子数组 · 416 分割等和子集 · 32 最长有效括号 | 易×2 中×7 难 |
| 多维 DP | 62 不同路径 · 64 最小路径和 · 5 最长回文子串 · 1143 最长公共子序列 · 72 编辑距离 | 中×5 |

---

# 第一部分 · 回溯

## 1. 回溯到底是什么

**一句话**：像走迷宫，每到一个岔路选一条走下去，走不通就**退回来换一条**，直到把所有可能都试完。

统一骨架（八道题全靠它）：

```python
res = []
def dfs(状态参数):
    if 走到终点:
        res.append(path[:])      # ← 必须是快照！
        return
    for 选择 in 当前可选集合:
        path.append(选择)         # 做选择
        dfs(更新后的参数)          # 往下走
        path.pop()                # 撤销选择，恢复现场
```

三行核心是「做选择 → 递归 → 撤销」。**撤销不能省**，否则上一条路的状态会污染下一条。

**`path[:]` 为什么必须是快照**：`path` 是一个列表，如果你直接 `res.append(path)`，存进去的是「同一个列表的标签」。后面 `path.pop()` 把它清空时，之前存的所有位置看到的都是同一个空列表。这是 Python 刷题最著名的 bug：

```python
# 错误结果示例：[[], [], [], []]
```

正确写法永远是 `res.append(path[:])`（或 `path.copy()`）。

**三家族只差「可选集合怎么定」**：

| 家族 | 每次能选谁 | 递归参数 |
|---|---|---|
| 全排列 46 | 所有**没用过**的元素 | 一个 `used` 数组 |
| 子集 78 | 每个元素选 / 不选 | `start = i + 1` |
| 组合 39 | 从 `start` 往后选，允许重复选自己 | `start = i`（不 +1） |

### 46 · 全排列（中等）

给不含重复数字的数组，返回所有排列。

```python
class Solution:
    def permute(self, nums):
        res, path = [], []
        used = [False] * len(nums)
        def dfs():
            if len(path) == len(nums):
                res.append(path[:])
                return
            for i, x in enumerate(nums):
                if used[i]:
                    continue
                used[i] = True
                path.append(x)
                dfs()
                path.pop()
                used[i] = False
        dfs()
        return res
```

时间 `O(n × n!)`，空间 `O(n)`（不含结果）。**易错**：`used` 也要在递归后恢复，否则下一条路会以为这个元素被占用了。

### 78 · 子集（中等）

返回数组的所有子集（包括空集）。

**怎么想**：对每个位置，决定「选它」还是「不选它」。用 `start` 保证只往後看，避免 `[1,2]` 和 `[2,1]` 重复。

```python
class Solution:
    def subsets(self, nums):
        res, path = [], []
        def dfs(start):
            res.append(path[:])          # 每个节点都是一个合法子集
            for i in range(start, len(nums)):
                path.append(nums[i])
                dfs(i + 1)
                path.pop()
        dfs(0)
        return res
```

时间 `O(n × 2ⁿ)`，空间 `O(n)`。**易错**：`res.append` 放在函数开头（不是只在叶子），因为每个节点都算一个子集。

### 17 · 电话号码的字母组合（中等）

数字 `2~9` 各对应几个字母，给一串数字，返回所有可能的字母组合。

```python
class Solution:
    def letterCombinations(self, digits):
        if not digits:
            return []
        mp = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
              "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
        res, path = [], []
        def dfs(i):
            if i == len(digits):
                res.append("".join(path))
                return
            for c in mp[digits[i]]:
                path.append(c)
                dfs(i + 1)
                path.pop()
        dfs(0)
        return res
```

时间 `O(4ⁿ × n)`，空间 `O(n)`。**易错**：空字符串要返回 `[]` 而不是 `[[]]` 或 `[""]`；字符串用 `join` 收集，不能直接 `append` 到结果。

### 39 · 组合总和（中等）

给一组**无重复**的正数，找出所有和等于 target 的组合，每个数字可以**无限次**使用。

**怎么想**：`start` 表示「本层往下只能从下标 start 开始选」，避免顺序不同的重复组合；因为可以重复选自己，递归时传 `i` 而不是 `i + 1`。

```python
class Solution:
    def combinationSum(self, candidates, target):
        res, path = [], []
        def dfs(start, remain):
            if remain == 0:
                res.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remain:
                    continue
                path.append(candidates[i])
                dfs(i, remain - candidates[i])   # 仍是 i，允许重复选
                path.pop()
        dfs(0, target)
        return res
```

时间 `O(答案个数 × 答案长度)`，空间 `O(target)`。**易错**：`dfs(i, ...)` 里的 `i` 是关键，写成 `i+1` 就变成「每个数只能用一次」。

### 22 · 括号生成（中等）

生成 n 对括号的所有合法组合。

**怎么想**：两个剪枝条件就能保证任意前缀合法——左括号最多 n 个；右括号数量**不能超过**左括号数量。

```python
class Solution:
    def generateParenthesis(self, n):
        res, path = [], []
        def dfs(left, right):
            if len(path) == 2 * n:
                res.append("".join(path))
                return
            if left < n:
                path.append("(")
                dfs(left + 1, right)
                path.pop()
            if right < left:                 # 剪枝：保证前缀合法
                path.append(")")
                dfs(left, right + 1)
                path.pop()
        dfs(0, 0)
        return res
```

时间 `O(卡特兰数 × n)`，空间 `O(n)`。**易错**：`right < left` 这个条件是「合法括号串」的核心，漏掉会产生 `())(` 这类非法串。

### 79 · 单词搜索（中等）

在字符网格里，判断能否沿上下左右相邻的路径连出给定单词（同一格不能重复用）。

**怎么想**：对每个格子当起点做 DFS。用一个临时标记 `'#'` 原地表示「这个格子本条路径已用过」，递归返回前恢复。这就是回溯里的「做选择 / 撤销」。

```python
class Solution:
    def exist(self, board, word):
        m, n = len(board), len(board[0])
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        def dfs(r, c, k):
            if board[r][c] != word[k]:
                return False
            if k == len(word) - 1:
                return True
            tmp = board[r][c]
            board[r][c] = "#"                 # 标记已用
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != "#":
                    if dfs(nr, nc, k + 1):
                        board[r][c] = tmp
                        return True
            board[r][c] = tmp                 # 恢复现场
            return False
        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False
```

时间 `O(mn × 3^L)`（L 是单词长度），空间 `O(L)`。**易错**：无论成功还是失败，返回前都要把格子恢复；找到答案时也要恢复再 `return True`。

### 131 · 分割回文串（中等）

把字符串切成若干段，要求每段都是回文，返回所有切法。

**怎么想**：`start` 表示「从哪开始切下一段」，枚举这一段的所有可能终点 `end`，只有 `s[start:end]` 是回文才继续往下切。

```python
class Solution:
    def partition(self, s):
        res, path = [], []
        n = len(s)
        def dfs(start):
            if start == n:
                res.append(path[:])
                return
            for end in range(start + 1, n + 1):
                t = s[start:end]
                if t == t[::-1]:
                    path.append(t)
                    dfs(end)
                    path.pop()
        dfs(0)
        return res
```

时间 `O(n × 2ⁿ)`，空间 `O(n)`。**易错**：`end` 要取到 `n`（`range(start+1, n+1)`），因为切片右端取不到；`t == t[::-1]` 每次切片花一段时间，数据大时可预先算好回文表。

### 51 · N 皇后（困难）

在 n×n 棋盘放 n 个皇后，互不攻击，返回所有摆法。

**怎么想**：一行一行放，每行只放一个。用三个集合记「已被占用的列」「已被占用的主对角线」「副对角线」。主对角线上的格子满足 `行 - 列` 相同，副对角线满足 `行 + 列` 相同。

```python
class Solution:
    def solveNQueens(self, n):
        res = []
        board = [["."] * n for _ in range(n)]
        cols, diag1, diag2 = set(), set(), set()
        def dfs(r):
            if r == n:
                res.append(["".join(row) for row in board])
                return
            for c in range(n):
                if c in cols or (r - c) in diag1 or (r + c) in diag2:
                    continue
                board[r][c] = "Q"
                cols.add(c); diag1.add(r - c); diag2.add(r + c)
                dfs(r + 1)
                cols.remove(c); diag1.remove(r - c); diag2.remove(r + c)
                board[r][c] = "."
        dfs(0)
        return res
```

时间 `O(n!)`，空间 `O(n²)`。**易错**：棋盘必须用推导式建（`[["."]*n for _ in range(n)]`），写成 `[["."]*n]*n` 会让所有行共享同一行；收集答案时要逐行 `join` 成字符串快照。

---

# 第二部分 · 图论

## 2. 图是什么

**把「一堆东西 + 它们之间的连接」叫图**。网格里相邻格子算连接，课程之间的先修关系也算连接。

两种基本走法：

- **BFS（广度优先）**：用队列，一圈一圈往外扩。适合「最短几步」「最少几层」。
- **DFS（深度优先）**：用递归或栈，一条路走到底再回头。适合「能不能到」「连通块」。

网格里四个方向固定写法：

```python
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
```

### 200 · 岛屿数量（中等）

给 `0/1` 网格，`1` 连成一块算一个岛，求岛的数量（上下左右相邻）。

**怎么想**：扫每个格子，遇到一个没访问过的 `1` 就答案 +1，然后用 BFS 把整块「淹掉」（改成 `0`），这样同一块不会被重复计数。

```python
from collections import deque

class Solution:
    def numIslands(self, grid):
        if not grid or not grid[0]:
            return 0
        m, n = len(grid), len(grid[0])
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        cnt = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] != "1":
                    continue
                cnt += 1
                q = deque([(r, c)])
                grid[r][c] = "0"           # 入队时就标记
                while q:
                    x, y = q.popleft()
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == "1":
                            grid[nx][ny] = "0"
                            q.append((nx, ny))
        return cnt
```

时间 `O(mn)`，空间 `O(mn)`。**易错**：**入队时就要标记**，等出队才标记会让同一个格子被多个邻居重复入队。

### 994 · 腐烂的橘子（中等）

网格里 `0` 空、`1` 好橘子、`2` 烂橘子。每分钟烂橘子会把上下左右的好橘子变烂，求全部变烂要几分钟，不可能返回 -1。

**怎么想**：**多源 BFS**——把所有初始烂橘子一起入队，按「层」扩散，每层就是一分钟。同时记好橘子数量，最后没减到 0 说明有孤岛。

```python
from collections import deque

class Solution:
    def orangesRotting(self, grid):
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    q.append((i, j))
                elif grid[i][j] == 1:
                    fresh += 1
        minutes = 0
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while q and fresh:
            for _ in range(len(q)):        # 这一层 = 一分钟
                r, c = q.popleft()
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        q.append((nr, nc))
            minutes += 1
        return minutes if fresh == 0 else -1
```

时间 `O(mn)`，空间 `O(mn)`。**易错**：`while q and fresh` 而不是 `while q`——好橘子为 0 时不用再计分钟；初始就没有好橘子要返回 0。

### 207 · 课程表（中等）

有 n 门课，先修关系 `[a, b]` 表示「学 a 之前要学 b」，判断能否修完所有课。

**怎么想**：**拓扑排序**。把关系看成有向边 `b -> a`。维护每个节点的「入度」（还有几门先修课没学），把所有入度为 0 的课入队；每学完一门，就把依赖它的课的入度减一，减到 0 就入队。最后学完的门数等于 n 才说明没有环。

```python
from collections import defaultdict, deque

class Solution:
    def canFinish(self, numCourses, prerequisites):
        g = defaultdict(list)
        indeg = [0] * numCourses
        for a, b in prerequisites:
            g[b].append(a)
            indeg[a] += 1
        q = deque(i for i in range(numCourses) if indeg[i] == 0)
        learned = 0
        while q:
            u = q.popleft()
            learned += 1
            for v in g[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return learned == numCourses
```

时间 `O(n + e)`（e 是先修关系条数），空间 `O(n + e)`。**易错**：边方向别搞反（`b -> a`）；有环时环上节点入度永远降不到 0，`learned < n` 自然返回 False。

### 208 · 实现 Trie（中等）

实现前缀树，支持插入、查找完整单词、查找前缀。

**怎么想**：每个节点用字典存「字符 → 子节点」，再加一个 `is_end` 标记「是否有单词在这里结束」。插入就是顺着字符一路建节点。

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        cur = self.root
        for ch in word:
            if ch not in cur.children:
                cur.children[ch] = TrieNode()
            cur = cur.children[ch]
        cur.is_end = True

    def _walk(self, s):
        cur = self.root
        for ch in s:
            if ch not in cur.children:
                return None
            cur = cur.children[ch]
        return cur

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        return self._walk(prefix) is not None
```

`insert` / `search` / `startsWith` 都是 `O(长度)`，空间 `O(所有单词总字符数)`。**易错**：`search` 必须检查 `is_end`——插入过 `"apple"` 时 `search("app")` 应该是 False，但 `startsWith("app")` 是 True。

---

# 第三部分 · 动态规划

## 3. 先搞懂「状态」是什么

动态规划（DP）让很多人害怕，其实它的核心就一句话：**把大问题拆成会重复出现的小问题，把小问题的答案记下来，别反复算。**

### 3.1 从爬楼梯开始

题目：每次能爬 1 或 2 阶，爬到 n 阶有几种走法？

先按直觉写递归：

```python
def f(n):
    if n <= 2:
        return n
    return f(n - 1) + f(n - 2)
```

**为什么慢**：算 `f(5)` 要算 `f(4)` 和 `f(3)`，而 `f(4)` 又要算 `f(3)`……`f(3)` 被算了很多遍。

**第一招：记下来**（记忆化搜索）：

```python
from functools import cache

@cache
def f(n):
    if n <= 2:
        return n
    return f(n - 1) + f(n - 2)
```

`@cache` 让每个 `n` 只算一次，立刻从指数级变成 `O(n)`。

**第二招：倒过来算**（递推 / 填表）：

```python
def climb(n):
    a = b = 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

`a, b` 分别代表「到前一阶」「到当前阶」的走法数，每轮往前滚一格。这就是 **DP**：用几个变量记住「已经算好的小问题答案」，一步步推到大问题。

### 3.2 写 DP 前必须回答的五个问题

1. **`dp[i]` 的下标 i 代表什么？**（例：「只考虑前 i 个元素」）
2. **`dp[i]` 的值代表什么？**（例：「前 i 个元素能得到的最大和」）
3. **初始状态是什么？**（例：`dp[0] = 0`）
4. **转移：dp[i] 能从哪几个之前的状态推出来？**（这就是那句「状态转移方程」）
5. **最终答案在哪个格子？**（`dp[n]` 还是 `max(dp)`？）

**想不出解法时，先把这五句写在注释里**，往往写着写着就通了。这比盯着代码改有用得多。

### 3.3 滚动数组

如果 `dp[i]` 只依赖前一行/前一两个格子，就不用存整个数组，用几个变量滚动即可，空间从 `O(n)` 降到 `O(1)`。上面爬楼梯的 `a, b` 就是。

---

## 4. 动态规划 10 题

### 70 · 爬楼梯（简单）

就是 §3.1。

```python
class Solution:
    def climbStairs(self, n):
        a = b = 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
```

时间 `O(n)`，空间 `O(1)`。**易错**：`n = 1` 时循环不执行，返回 `b = 1`，正确。

### 118 · 杨辉三角（简单）

生成前 numRows 行，每个数等于上一行左右两数之和。

```python
class Solution:
    def generate(self, numRows):
        res = [[1]]
        for i in range(1, numRows):
            prev = res[-1]
            row = [1] * (i + 1)
            for j in range(1, i):
                row[j] = prev[j - 1] + prev[j]
            res.append(row)
        return res
```

时间 `O(n²)`，空间 `O(n²)`。**易错**：每行首尾都是 1，中间才用加法；`range(1, i)` 的右端取不到，正好不算最后一个。

### 198 · 打家劫舍（中等）

一排房子，不能偷相邻的，求最大金额。

**怎么想**：`dp[i]` = 偷到第 i 间为止的最大金额。对第 i 间只有两种选择：偷（那么 i-1 不能偷，拿 `dp[i-2] + nums[i]`）或不偷（拿 `dp[i-1]`）。只依赖前两格，用两个变量滚动。

```python
class Solution:
    def rob(self, nums):
        prev2 = prev1 = 0        # dp[i-2], dp[i-1]
        for x in nums:
            prev2, prev1 = prev1, max(prev1, prev2 + x)
        return prev1
```

时间 `O(n)`，空间 `O(1)`。**易错**：`prev2, prev1 = prev1, max(...)` 右边先整体求值，用的都是旧值，不需要临时变量。

### 279 · 完全平方数（中等）

求最少用几个完全平方数（1,4,9…）相加得到 n。

**怎么想**：`dp[i]` = 凑出 i 需要的最少个数。对每个 `i`，试所有 `j*j <= i`，取 `dp[i - j*j] + 1` 的最小值。

```python
class Solution:
    def numSquares(self, n):
        dp = [0] + [float("inf")] * n
        for i in range(1, n + 1):
            j = 1
            while j * j <= i:
                dp[i] = min(dp[i], dp[i - j * j] + 1)
                j += 1
        return dp[n]
```

时间 `O(n√n)`，空间 `O(n)`。**易错**：初始值是 `inf` 不是 0（除了 `dp[0] = 0`），否则 `min` 永远取不到正确值。

### 322 · 零钱兑换（中等）

给硬币面额（每种无限个），求凑出 amount 的最少硬币数，凑不出返回 -1。

**怎么想**：和 279 同构，`dp[i]` = 凑出 i 的最少硬币数。这是**完全背包**：每个面额可以无限用，所以金额要**正序**遍历（让同一个面额能被反复使用）。

```python
class Solution:
    def coinChange(self, coins, amount):
        dp = [0] + [float("inf")] * amount
        for c in range(1, amount + 1):
            for coin in coins:
                if coin <= c:
                    dp[c] = min(dp[c], dp[c - coin] + 1)
        return dp[amount] if dp[amount] != float("inf") else -1
```

时间 `O(amount × 硬币种类)`，空间 `O(amount)`。**易错**：返回前要判断「是不是 inf」，inf 表示凑不出。

### 139 · 单词拆分（中等）

判断字符串能否拆成字典里的单词（单词可重复使用）。

**怎么想**：`dp[i]` = 前 i 个字符能否被拆开。枚举最后一个单词的起点 `j`，若 `dp[j]` 为真且 `s[j:i]` 在字典里，则 `dp[i]` 为真。把字典转成集合，查找才快。

```python
class Solution:
    def wordBreak(self, s, wordDict):
        words = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[n]
```

时间 `O(n²)`（切片本身也花时间），空间 `O(n)`。**易错**：`dp[0] = True` 表示「空串可以被拆」，是递推的起点；`dp[i]` 对应前 i 个字符（不含 i）。

### 300 · 最长递增子序列（中等）

找出最长的**严格递增**子序列长度（子序列不要求连续）。

**怎么想**：`dp[i]` = 以第 i 个元素**结尾**的最长递增子序列长度。对每个 i，往前找所有比它小的 j，取 `dp[j] + 1` 的最大值。答案是整个 `dp` 里的最大值（不一定以最后一个元素结尾）。

```python
class Solution:
    def lengthOfLIS(self, nums):
        n = len(nums)
        dp = [1] * n
        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
```

时间 `O(n²)`，空间 `O(n)`。**易错**：`dp` 初值全是 1（每个元素自己就是一个长度 1 的子序列）；`n = 0` 时 `max(dp)` 会报错，题目保证非空，自己写测试时要留意。这题还有 `O(n log n)` 的 `bisect` 解法，[L04 §3](L04-toolbox.md) 提过思路，学有余力可以再查。

### 152 · 乘积最大子数组（中等）

找连续一段，使乘积最大（可能有负数和 0）。

**怎么想**：和 53 题类似，但乘法有个陷阱——**一个很小的负数乘上另一个负数会变成很大的正数**。所以要同时维护「以当前结尾的最大值」和「最小值」，遇到负数时两者交换。

```python
class Solution:
    def maxProduct(self, nums):
        hi = lo = ans = nums[0]       # 以当前位置结尾的最大/最小乘积
        for x in nums[1:]:
            old_hi, old_lo = hi, lo
            hi = max(x, old_hi * x, old_lo * x)
            lo = min(x, old_hi * x, old_lo * x)
            ans = max(ans, hi)
        return ans
```

时间 `O(n)`，空间 `O(1)`。**易错**：算 `hi` 和 `lo` 必须都用**同一组旧值**（所以先存 `old_hi, old_lo`）。如果先更新 `hi` 再用新 `hi` 去算 `lo`，结果就串了。另一种写法是 `hi, lo = max(x, hi*x, lo*x), min(x, hi*x, lo*x)`，利用 Python「右边先整体求值」一次赋值，效果相同。

### 416 · 分割等和子集（中等）

判断数组能否分成两个子集，使两边和相等。

**怎么想**：总和必须是偶数，问题变成「能不能挑出一些数，和恰好等于总和的一半」。这是 **0-1 背包**：每个数只能选一次，所以金额必须**倒序**遍历（正序会让同一个数被重复使用）。

```python
class Solution:
    def canPartition(self, nums):
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True
        for x in nums:
            for c in range(target, x - 1, -1):   # 倒序！
                dp[c] = dp[c] or dp[c - x]
        return dp[target]
```

时间 `O(n × target)`，空间 `O(target)`。**易错**：倒序是本题的命根子，写成正序就变成「每个数无限用」，答案会错但样例常常还能过——务必用对拍验证。

### 32 · 最长有效括号（困难）

找最长的**连续合法括号子串**的长度。

**怎么想**：用栈存下标，栈底始终放「上一个无法匹配的位置」。遇到 `(` 压下标；遇到 `)` 先弹一个，若栈空了说明这个 `)` 无法匹配，把它自己当新的栈底；否则当前合法长度 = 当前下标 − 栈顶。

```python
class Solution:
    def longestValidParentheses(self, s):
        stack = [-1]
        ans = 0
        for i, c in enumerate(s):
            if c == "(":
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)
                else:
                    ans = max(ans, i - stack[-1])
        return ans
```

时间 `O(n)`，空间 `O(n)`。**易错**：栈初始放 `-1`（不是空），这样第一个合法段能算出完整长度；每遇到一个多余的 `)` 就把它的位置设为新基准。

---

## 5. 多维 DP（5 题）

**什么时候需要二维表**：状态要同时由两个东西决定时（比如「前 i 个字符」和「前 j 个字符」，或者网格的「行」和「列」）。

### 62 · 不同路径（中等）

机器人从左上走到右下，只能向右或向下，有多少条路。

**怎么想**：`dp[i][j]` = 走到第 i 行第 j 列的路径数。只能从上方或左方来，所以 `dp[i][j] = dp[i-1][j] + dp[i][j-1]`。第一行和第一列都只有 1 条路。

```python
class Solution:
    def uniquePaths(self, m, n):
        dp = [1] * n              # 滚动成一行
        for _ in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j - 1]
        return dp[n - 1]
```

时间 `O(mn)`，空间 `O(n)`。**易错**：`dp[j] += dp[j-1]` 里，更新前的 `dp[j]` 就是「上方来的」，`dp[j-1]` 是刚更新的「左方来的」，正好。

### 64 · 最小路径和（中等）

网格每格有代价，找从左上到右下路径的最小总代价。

```python
class Solution:
    def minPathSum(self, grid):
        m, n = len(grid), len(grid[0])
        dp = [float("inf")] * n
        dp[0] = 0
        for i in range(m):
            for j in range(n):
                if j == 0:
                    dp[j] = dp[j] + grid[i][j]
                else:
                    dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]
        return dp[n - 1]
```

时间 `O(mn)`，空间 `O(n)`。**易错**：`dp[0] = 0` 让起点只加上自己的代价；第一行没有「上方」，靠 `j == 0` 分支处理。

### 5 · 最长回文子串（中等）

**怎么想**：回文可以从中心往两边扩。每个位置都可能是中心：奇数长度中心是 1 个字符，偶数长度中心是 2 个字符之间的缝。枚举 n 个位置 × 2 种中心。

```python
class Solution:
    def longestPalindrome(self, s):
        def expand(l, r):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return s[l + 1:r]
        ans = ""
        for i in range(len(s)):
            for a, b in ((i, i), (i, i + 1)):
                cand = expand(a, b)
                if len(cand) > len(ans):
                    ans = cand
        return ans
```

时间 `O(n²)`，空间 `O(1)`（不计返回的字符串）。**易错**：退出 `while` 时 `l, r` 已经越界或不匹配，所以切片要回退一格 `s[l+1:r]`。这题也能用二维区间 DP 做（状态是 `dp[i][j]` = s[i:j+1] 是否回文），但中心扩展更省空间。

### 1143 · 最长公共子序列（中等）

两个字符串的最长公共子序列长度（不要求连续）。

**怎么想**：`dp[i][j]` = `a` 的前 i 个字符和 `b` 的前 j 个字符的 LCS 长度。若 `a[i-1] == b[j-1]`，可以一起用上：`dp[i-1][j-1] + 1`；否则取「去掉 a 最后一个」和「去掉 b 最后一个」里较大的。

```python
class Solution:
    def longestCommonSubsequence(self, text1, text2):
        m, n = len(text1), len(text2)
        prev = [0] * (n + 1)
        for i in range(1, m + 1):
            cur = [0] * (n + 1)
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    cur[j] = prev[j - 1] + 1
                else:
                    cur[j] = max(prev[j], cur[j - 1])
            prev = cur
        return prev[n]
```

时间 `O(mn)`，空间 `O(n)`。**易错**：字符相等时用的是**左上角** `prev[j-1]`，不是 `prev[j]`；二维表第 0 行第 0 列全是 0，用滚动数组时 `cur = [0]*(n+1)` 正好承担这个角色。

### 72 · 编辑距离（中等）

把 word1 变成 word2，可以插入、删除、替换一个字符，求最少操作数。

**怎么想**：`dp[i][j]` = 把 `a` 的前 i 个字符变成 `b` 的前 j 个字符的最少操作数。字符相同则不用操作，直接继承 `dp[i-1][j-1]`；否则取「删」「插」「替换」三种里最小的 +1。

```python
class Solution:
    def minDistance(self, word1, word2):
        m, n = len(word1), len(word2)
        prev = list(range(n + 1))          # a 为空时，只能一直插入
        for i in range(1, m + 1):
            cur = [i] + [0] * n            # b 为空时，只能一直删除
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    cur[j] = prev[j - 1]
                else:
                    cur[j] = min(prev[j],      # 删
                                 cur[j - 1],   # 插
                                 prev[j - 1]   # 替换
                                 ) + 1
            prev = cur
        return prev[n]
```

时间 `O(mn)`，空间 `O(n)`。**易错**：第 0 行是 `0,1,2,...,n`（空串变成长度 j 的串要插 j 次），第 0 列是 `0,1,2,...,i`，初始化错整张表都错。

---

## 6. 背包遍历方向（最容易背混的一条）

| 类型 | 每个物品 | 金额/容量遍历方向 | 例子 |
|---|---|---|---|
| 0-1 背包 | 只能用一次 | **倒序** `range(target, w-1, -1)` | 416 分割等和子集 |
| 完全背包 | 可以无限用 | **正序** `range(w, target+1)` | 322 零钱兑换、279 |

**为什么**：倒序时 `dp[c-w]` 还是「没考虑过当前物品」的旧值，保证每个物品只用一次；正序时 `dp[c-w]` 已经被当前物品更新过，等于允许重复使用。方向写反是最隐蔽的 Wrong Answer——样例常常还能过，务必用对拍验证。

---

## 本册小结

| 遇到什么 | 先想到 |
|---|---|
| 「所有排列 / 组合 / 子集」 | 回溯三行骨架 + `path[:]` |
| 棋盘、网格里找路径 | 回溯 + 原地标记 + 恢复 |
| 网格连通块、最少几步 | BFS + `deque`，入队即标记 |
| 依赖关系、能否全部完成 | 拓扑排序（入度 + 队列） |
| 字符串前缀查询 | Trie（字典 + `is_end`） |
| 大问题拆成重复小问题 | DP 五问 + 填表 |
| 每个数选一次 / 无限选 | 0-1 背包倒序 / 完全背包正序 |
| 两个字符串比较、网格路径 | 二维 DP，可滚动成一维 |

---

## 本册自测（闭卷）

1. 默写回溯三行骨架，说明为什么 `res.append(path[:])` 不能写成 `res.append(path)`。
2. 「每个数字只能选一次」和「可以无限选」，递归参数分别怎么写？
3. BFS 里为什么要「入队时就标记」？
4. DP 五问是哪五问？用打家劫舍举一遍。
5. 0-1 背包和完全背包的遍历方向分别是什么？为什么？
6. `72` 编辑距离里，第 0 行和第 0 列为什么不是全 0？
7. **口述题**：`152` 乘积最大子数组里为什么要同时维护最大值和最小值？

<details>
<summary>答案要点</summary>

1. 做选择 → 递归 → 撤销。存 `path` 存的是同一个列表对象的标签，后面 `pop()` 会把它清空，导致所有已存答案变成同一个空列表；`path[:]` 是当场复制的快照。
2. 只能选一次：递归传 `i + 1`；可重复选：传 `i`。
3. 否则同一个格子会被多个相邻格子重复入队，复杂度膨胀甚至出错。
4. 下标含义、值含义、初始状态、从哪几个状态转移、答案在哪个格子。打家劫舍：`i` 是偷到第 i 间；值是最大金额；`dp[0]=dp[1]=0` 起步；`dp[i] = max(dp[i-1], dp[i-2]+nums[i])`；答案在最后一格。
5. 0-1 倒序、完全正序。倒序保证 `dp[c-w]` 是没考虑当前物品的旧值；正序让它已被当前物品更新过，从而允许重复。
6. 第 0 行表示「空串变成 b 的前 j 个字符」，需要 j 次插入；第 0 列表示「a 的前 i 个字符变成空串」，需要 i 次删除。
7. 因为负数乘负数会变成大正数：当前最小的负值，下一步遇到负数可能变成最大的正值。只维护最大值会在这种翻转时丢掉最优解。

</details>

---

## 恭喜，100 道题讲完了

四册合计 `26 + 18 + 29 + 27 = 100` 道。接下来看 [L10](L10-training-plan.md) 的 12 周复刷计划和复盘表，以及 [L11](L11-cheatsheet.md) 的速查手册。

第一遍做不出来太正常了。**「看懂讲解」和「闭卷写出来」之间隔着一次复刷**，L10 整章就是为这个准备的。
