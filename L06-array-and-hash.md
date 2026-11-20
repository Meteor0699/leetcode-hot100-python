# L06 · 数组与哈希（26 题）

本册 26 道题，全部围绕「一串数据」。先把套路讲透，再看具体题。

## 本册题目

| 套路   | 题号 · 题名                                                                    | 难度        |
| ---- | -------------------------------------------------------------------------- | --------- |
| 哈希   | 1 两数之和 · 49 字母异位词分组 · 128 最长连续序列                                           | 易 中 中     |
| 双指针  | 283 移动零 · 11 盛最多水的容器 · 15 三数之和 · 42 接雨水                                    | 易 中 中 难   |
| 滑动窗口 | 3 无重复字符的最长子串 · 438 找到字符串中所有字母异位词 · 560 和为 K 的子数组 · 76 最小覆盖子串 · 239 滑动窗口最大值 | 中 中 中 难 难 |
| 普通数组 | 53 最大子数组和 · 56 合并区间 · 189 轮转数组 · 238 除自身以外数组的乘积 · 41 缺失的第一个正数              | 中 中 中 中 难 |
| 矩阵   | 73 矩阵置零 · 54 螺旋矩阵 · 48 旋转图像 · 240 搜索二维矩阵 II                                | 中×4       |
| 技巧   | 136 只出现一次的数字 · 169 多数元素 · 75 颜色分类 · 31 下一个排列 · 287 寻找重复数                   | 易 易 中 中 中 |

---

## 套路一 · 哈希表：把「翻一遍」变成「查一下」

**它在解决什么问题**：数组里找「某个数在不在」要从头翻到尾，很慢。字典能让你一瞬间查到。

**为什么能做到**：字典内部按名字直接算出存放位置，不用挨个比。代价是多用了一些内存——**用空间换时间**，这是算法里最划算的交易之一。

**三种用法**：查配对（1 题）、分组（49 题）、查存在（128 题）。

### 1 · 两数之和（简单）

给数组 `nums` 和 `target`，找出两个数使它们的和为 `target`，返回下标。

**怎么想**：笨办法是试遍每一对（`O(n²)`）。慢在「每来一个数，都要翻一遍前面找补数」。用字典把见过的值和下标记下来，查补数就变成一瞬间。注意**先查后存**，否则同一个元素会配自己。

```python
class Solution:
    def twoSum(self, nums, target):
        seen = {}                        # 值 -> 下标
        for i, x in enumerate(nums):
            need = target - x
            if need in seen:
                return [seen[need], i]
            seen[x] = i
        return []
```

时间 `O(n)`，空间 `O(n)`。**易错**：`[3]`, `target=6` 时不能返回 `[0,0]`，所以 `seen[x] = i` 必须在 `if` 之后。

### 49 · 字母异位词分组（中等）

把字母组成相同（顺序可以不同）的单词放到一组。

**怎么想**：关键是给每组找一个「共同的身份证」。把单词的字母排序后，`"eat"`、`"tea"`、`"ate"` 都变成 `"aet"`，用它当字典的键即可。

```python
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs):
        groups = defaultdict(list)
        for s in strs:
            key = "".join(sorted(s))
            groups[key].append(s)
        return list(groups.values())
```

时间 `O(n × k log k)`（k 是单词长度，花在排序上），空间 `O(nk)`。**易错**：`sorted(s)` 返回的是字符列表，必须 `join` 回字符串才能当键。

### 128 · 最长连续序列（中等）

找出数组里最长的一段连续数字的长度，如 `[100,4,200,1,3,2]` → `4`（1,2,3,4）。要求 `O(n)`。

**怎么想**：先全部放进集合（查存在一瞬间）。然后**只从「一段的起点」开始数**——如果 `x-1` 也在集合里，说明 x 不是起点，跳过它。这样每个数字最多被内层循环访问一次，整体仍是 `O(n)`。

```python
class Solution:
    def longestConsecutive(self, nums):
        s = set(nums)
        best = 0
        for x in s:
            if x - 1 not in s:          # 只从起点出发
                y = x
                while y + 1 in s:
                    y += 1
                best = max(best, y - x + 1)
        return best
```

时间 `O(n)`，空间 `O(n)`。**易错**：漏掉 `if x - 1 not in s`，每个数都会把整段重新数一遍，退化成 `O(n²)`。

---

## 套路二 · 双指针：让两个位置一起走

**它在解决什么问题**：两层循环慢在「内层每次都从头开始」。如果两个位置**只往一个方向走、不回头**，总步数就只有 `2n`，变成 `O(n)`。

**两种形状**：

- **对撞**：一个在最左、一个在最右，根据大小往中间靠（11、15、42）
- **读写**：一个读、一个写，写指针永远不越过读指针（283）

**为什么不会漏掉答案**：因为每次移动都能从逻辑上证明「被跳过的那些组合一定不可能更优」。比如 11 题里移动较矮的那块板，是因为宽度在变小、而高度上限被矮板卡死，换任何另一块矮板都不会更好。做题时把这句话能讲出来，才算真懂。

### 283 · 移动零（简单）

把数组里所有 0 移到末尾，其他数字保持相对顺序，要求原地改。

**怎么想**：设一个 `k` 表示「下一个非零数该放哪」。遍历时遇到非零就写到 `nums[k]`，`k` 前进。因为 `k` 永远不超过当前读到的位置，不会覆盖还没读的数据。最后把 `k` 之后全填 0。

```python
class Solution:
    def moveZeroes(self, nums):
        k = 0
        for x in nums:
            if x != 0:
                nums[k] = x
                k += 1
        for i in range(k, len(nums)):
            nums[i] = 0
```

时间 `O(n)`，空间 `O(1)`。**易错**：别在遍历时 `remove(0)`——边遍历边删会漏元素，而且 `remove` 本身是 `O(n)`。

### 11 · 盛最多水的容器（中等）

找两条竖线，使它们和 x 轴围成的面积最大。面积 = 两边距离 × 较矮的高度。

**怎么想**：笨办法试遍所有两两组合（`O(n²)`）。用对撞指针从最宽的开始，每次**移动较矮的那一边**：宽度已经变小了，只有换掉矮的那根、让高度有可能变大，面积才可能变大。

```python
class Solution:
    def maxArea(self, height):
        l, r = 0, len(height) - 1
        ans = 0
        while l < r:
            ans = max(ans, (r - l) * min(height[l], height[r]))
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return ans
```

时间 `O(n)`，空间 `O(1)`。**易错**：面积要用 `min(两边)` 的高度，不是随便挑一个；两边相等时移哪边都行。

### 15 · 三数之和（中等）

找出所有和为 0 且不重复的三元组。

**怎么想**：先排序，然后固定第一个数 `i`，剩下两个数用对撞指针找（有序数组才能根据和的大小决定移动哪边）。**去重**全靠「排序后相同值相邻」：跳过重复的 `i`，命中后也跳过重复的 `l`。

```python
class Solution:
    def threeSum(self, nums):
        nums.sort()
        res, n = [], len(nums)
        for i in range(n - 2):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            l, r = i + 1, n - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s < 0:
                    l += 1
                elif s > 0:
                    r -= 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
        return res
```

时间 `O(n²)`，空间 `O(1)`（不计结果）。**易错**：两处去重 `while` 都不能省；`nums.sort()` 返回 `None`，别写成 `nums = nums.sort()`。

### 42 · 接雨水（困难）

给一排柱子的高度，求能接多少雨水。

**怎么想**：每个位置能存多少水，取决于「它左边最高的」和「右边最高的」里较矮的那个，减去自己的高度。用对撞指针从两端往中间走，同时维护 `left_max` 和 `right_max`：哪边当前较矮，就处理哪边（因为它能存多少已经由这一侧的最大值决定了，另一侧肯定更高）。

```python
class Solution:
    def trap(self, height):
        l, r = 0, len(height) - 1
        left_max = right_max = 0
        ans = 0
        while l < r:
            if height[l] < height[r]:
                left_max = max(left_max, height[l])
                ans += left_max - height[l]
                l += 1
            else:
                right_max = max(right_max, height[r])
                ans += right_max - height[r]
                r -= 1
        return ans
```

时间 `O(n)`，空间 `O(1)`。**易错**：先更新最大值再算这一格的水，顺序反了会得到 0。

---

## 套路三 · 滑动窗口：只考虑「连续的一段」

**它在解决什么问题**：题目要「最长的连续子串」「和为 K 的连续子数组」「每个长度为 k 的窗口」。如果每个起点都重新扫一遍终点，是 `O(n²)`。

**核心骨架**（背下来）：

```python
# add / remove / valid 是按具体题意实现的占位函数
l = 0
ans = 0
for r, x in enumerate(data):
    add(x)                          # 1) 把 x 纳入窗口
    while l <= r and not valid():   # 2) 不满足条件就一直缩左端
        remove(data[l])
        l += 1
    ans = max(ans, r - l + 1)      # 3) 用 [l, r] 更新答案
```

三条纪律：`l` **只增不减**；`r` 用 `for` 走、`l` 用 `while` 缩；更新答案放在收缩之后。因为 `l`、`r` 各自最多走 n 步，总共 `O(n)`。

**什么时候不能用**：数组里有负数还要求「和 ≥ K」时，右端右移不再保证窗口和单调增大，缩左边反而可能让和变小——这类题要改用**前缀和 + 哈希**（560 题）。

### 3 · 无重复字符的最长子串（中等）

**怎么想**：用字典记每个字符最后一次出现的位置。右端 `r` 遇到重复字符时，把左端 `l` 直接跳到「上次出现位置 + 1」。**必须判断 `last[c] >= l`**：如果那个重复字符已经在窗口外了，就不能让 `l` 往回退。

```python
class Solution:
    def lengthOfLongestSubstring(self, s):
        last = {}
        l = ans = 0
        for r, c in enumerate(s):
            if c in last and last[c] >= l:
                l = last[c] + 1
            last[c] = r
            ans = max(ans, r - l + 1)
        return ans
```

时间 `O(n)`，空间 `O(字符集大小)`。**易错**：`s = "abba"` 是专门卡「漏掉 `>= l`」的用例，r=3 时 `a` 的上次位置 0 已在窗口外，若把 `l` 拉回 1，答案会错成 3。

### 438 · 找到字符串中所有字母异位词（中等）

在 `s` 里找出所有和 `p` 字母组成相同的连续子串，返回起始下标。

**怎么想**：维护一个长度恰好为 `len(p)` 的窗口，和一个 26 长度的计数数组。窗口里每个字母的「还差多少」凑齐后，就是一次命中。用 `diff` 表示「有多少个字母的数量还不匹配」，避免每轮都去比较整个数组。

```python
class Solution:
    def findAnagrams(self, s, p):
        if len(s) < len(p):
            return []
        need = [0] * 26
        for c in p:
            need[ord(c) - 97] += 1
        win = [0] * 26
        ans = []
        k = len(p)
        for i, c in enumerate(s):
            win[ord(c) - 97] += 1
            if i >= k:
                win[ord(s[i - k]) - 97] -= 1
            if i >= k - 1 and win == need:
                ans.append(i - k + 1)
        return ans
```

时间 `O(26n)` 即 `O(n)`，空间 `O(1)`。**易错**：`ord(c) - 97` 里的 97 是 `'a'` 的编号，更清楚的写法是 `ord(c) - ord('a')`；列表相等比较 `win == need` 是逐项比，长度只有 26 所以很便宜。

### 560 · 和为 K 的子数组（中等）

统计有多少个连续子数组的和恰好等于 K，**数组里可能有负数**。

**怎么想**：记 `pre[i]` 为「从开头到第 i 个的和」。那么「第 j+1 到 i 的和 = pre[i] - pre[j]」。要让这段等于 K，就得 `pre[j] = pre[i] - K`。于是边算前缀和，边用字典查「之前出现过多少个这样的 `pre[j]`」。

```python
from collections import defaultdict

class Solution:
    def subarraySum(self, nums, k):
        cnt = defaultdict(int)
        cnt[0] = 1                  # 前缀和恰好等于 k 的情况
        pre = ans = 0
        for x in nums:
            pre += x
            ans += cnt[pre - k]
            cnt[pre] += 1
        return ans
```

时间 `O(n)`，空间 `O(n)`。**易错**：`cnt[0] = 1` 不能漏，否则「从第一个元素开始、和正好是 K」的情况会被漏掉。另外**别用滑动窗口**，有负数时窗口不成立。

### 76 · 最小覆盖子串（困难）

在 `s` 里找最短的一段，包含 `t` 里所有字符（含重复次数）。

**怎么想**：`need` 记还缺什么，`window` 记窗口里有什么，`valid` 记「已经满足数量的字符种类数」。右端一直扩，一旦 `valid == len(need)` 说明覆盖了，就试着缩左端找更短的，并记录答案。

```python
from collections import Counter

class Solution:
    def minWindow(self, s, t):
        if not t or not s:
            return ""
        need = Counter(t)
        window = {}
        valid = 0
        l = 0
        best_len = float("inf")
        best = ""
        for r, c in enumerate(s):
            if c in need:
                window[c] = window.get(c, 0) + 1
                if window[c] == need[c]:
                    valid += 1
            while valid == len(need):
                if r - l + 1 < best_len:
                    best_len = r - l + 1
                    best = s[l:r + 1]
                out = s[l]
                if out in need:
                    if window[out] == need[out]:
                        valid -= 1
                    window[out] -= 1
                l += 1
        return best
```

时间 `O(n)`，空间 `O(字符集)`。**易错**：`valid` 只在「数量刚好达标」时 +1，超过不算；缩窗口时只在「刚好从达标掉下来」时 -1。切片 `s[l:r+1]` 每次花一段长度，数据大时能改成只记下标、最后切一次。

### 239 · 滑动窗口最大值（困难）

返回每个长度为 k 的窗口里的最大值。

**怎么想**：用一个**单调队列**（`deque`，里面存下标，对应的值从大到小）。新元素进来前，把队尾所有比它小的都弹掉——它们既比新元素小、又比新元素早出窗口，永远不可能成为最大值。队首就是当前窗口最大。

```python
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums, k):
        q = deque()
        ans = []
        for i, x in enumerate(nums):
            while q and nums[q[-1]] <= x:
                q.pop()
            q.append(i)
            if q[0] <= i - k:          # 队首已滑出窗口
                q.popleft()
            if i >= k - 1:
                ans.append(nums[q[0]])
        return ans
```

时间 `O(n)`（每个下标最多进队出队各一次），空间 `O(k)`。**易错**：队列里存**下标**而不是值，否则无法判断「队首是否已滑出窗口」；用 `list.pop(0)` 会超时，必须 `deque`。

---

## 套路四 · 普通数组：几个反复出现的手法

### 53 · 最大子数组和（中等）

找连续一段，使它的和最大（数组里可能有负数）。

**怎么想**：笨办法枚举所有起点终点（`O(n²)`）。扫的时候想：如果「以当前位置结尾的最大和」已经算出来是 `cur`，那下一个位置有两种选择——接在 `cur` 后面，或者干脆从自己重新开始。取较大的那个。**如果 `cur` 是负数，接上只会更差，必定重新开始**。

```python
class Solution:
    def maxSubArray(self, nums):
        cur = best = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)
            best = max(best, cur)
        return best
```

时间 `O(n)`，空间 `O(1)`。**易错**：初始值设成 0 会在全负数数组上错；要用第一个元素或 `float("-inf")`。


### 56 · 合并区间（中等）

把所有重叠的区间合并。

**怎么想**：先按左端点排序（Python 对列表默认按字典序，`sorted(intervals)` 正好先比左端点）。之后扫描：如果当前区间的左端点 ≤ 上一个区间的右端点，就延长上一个；否则新开一段。

```python
class Solution:
    def merge(self, intervals):
        intervals.sort()
        res = []
        for l, r in intervals:
            if res and l <= res[-1][1]:
                res[-1][1] = max(res[-1][1], r)
            else:
                res.append([l, r])
        return res
```

时间 `O(n log n)`（花在排序），空间 `O(n)`。**易错**：合并时右端点要取 `max`，因为当前区间可能完全被上一个包住。

### 189 · 轮转数组（中等）

把数组向右轮转 k 位，要求原地改。

**怎么想**：三次反转——整体反转、前 k 个反转、剩下反转。也可以用切片赋值一行搞定：

```python
class Solution:
    def rotate(self, nums, k):
        n = len(nums)
        k %= n
        nums[:] = nums[-k:] + nums[:-k]
```

时间 `O(n)`，空间 `O(n)`（三次反转版是 `O(1)`）。**易错**：左边必须是 `nums[:]`。写 `nums = ...` 只是让函数里的变量指向新列表，外面看到的原数组根本没变。`k=0` 时 `nums[-0:]` 是整个列表、`nums[:-0]` 是空，结果碰巧正确。

### 238 · 除自身以外数组的乘积（中等）

返回数组，每个位置是「除了自己以外所有数的乘积」，不许用除法。

**怎么想**：每个位置的答案 = 它左边所有数的积 × 它右边所有数的积。两遍扫描分别把前缀积、后缀积累乘进去。

```python
class Solution:
    def productExceptSelf(self, nums):
        n = len(nums)
        ans = [1] * n
        p = 1
        for i in range(n):
            ans[i] = p
            p *= nums[i]
        p = 1
        for i in range(n - 1, -1, -1):
            ans[i] *= p
            p *= nums[i]
        return ans
```

时间 `O(n)`，空间 `O(1)`（不计结果）。**易错**：第二遍是 `ans[i] *= p`，别写成赋值把前缀积丢掉。

### 41 · 缺失的第一个正数（困难）

找出数组里没出现的最小正整数，要求 `O(n)` 时间、常数空间。

**怎么想**：答案是 1～n+1 中的某一个。利用「原地哈希」：把值 `x`（1 ≤ x ≤ n）交换到下标 `x-1` 的位置上。换完再扫一遍，第一个「位置 i 上不是 i+1」的就是答案。

```python
class Solution:
    def firstMissingPositive(self, nums):
        n = len(nums)
        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                j = nums[i] - 1
                nums[i], nums[j] = nums[j], nums[i]
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1
```

时间 `O(n)`（每个数最多被换到自己位置一次），空间 `O(1)`。**易错**：`while` 不能写成 `if`，换过来的新值可能还需要继续交换；`nums[nums[i]-1] != nums[i]` 这个判断防止两个相同值无限交换。

---

## 套路五 · 矩阵：把二维变成「走位」

### 73 · 矩阵置零（中等）

某个元素是 0，就把它所在的行和列全设为 0，要求原地、尽量省空间。

**怎么想**：用**第一行和第一列当标记本**，另外用两个变量记「第一行/第一列自己原本有没有 0」。先扫描打标记，再按标记置零，最后处理第一行第一列。

```python
class Solution:
    def setZeroes(self, matrix):
        m, n = len(matrix), len(matrix[0])
        first_row = any(matrix[0][j] == 0 for j in range(n))
        first_col = any(matrix[i][0] == 0 for i in range(m))
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0
        if first_row:
            for j in range(n):
                matrix[0][j] = 0
        if first_col:
            for i in range(m):
                matrix[i][0] = 0
```

时间 `O(mn)`，空间 `O(1)`。**易错**：`first_row` / `first_col` 必须**在打标记之前**算，否则标记会污染判断。

### 54 · 螺旋矩阵（中等）

按顺时针螺旋顺序输出矩阵所有元素。

**怎么想**：设四个边界 `top/bottom/left/right`，每走完一圈就往里缩一格。

```python
class Solution:
    def spiralOrder(self, matrix):
        m, n = len(matrix), len(matrix[0])
        top, bottom = 0, m - 1
        left, right = 0, n - 1
        res = []
        while top <= bottom and left <= right:
            for j in range(left, right + 1):
                res.append(matrix[top][j])
            top += 1
            for i in range(top, bottom + 1):
                res.append(matrix[i][right])
            right -= 1
            if top <= bottom:
                for j in range(right, left - 1, -1):
                    res.append(matrix[bottom][j])
                bottom -= 1
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    res.append(matrix[i][left])
                left += 1
        return res
```

时间 `O(mn)`，空间 `O(1)`（不计结果）。**易错**：下面两个 `if` 是防止只有一行/一列时重复遍历，漏掉会在 `[[1,2,3]]` 上输出重复元素。

### 48 · 旋转图像（中等）

把 n×n 矩阵顺时针旋转 90 度，原地改。

**怎么想**：先沿主对角线转置，再把每一行左右翻转。两步合起来正好等于顺时针 90 度。

```python
class Solution:
    def rotate(self, matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for row in matrix:
            row.reverse()
```

时间 `O(n²)`，空间 `O(1)`。**易错**：转置时 `j` 从 `i+1` 开始，从 0 开始会把每个位置换两次、等于没换。

### 240 · 搜索二维矩阵 II（中等）

矩阵每行、每列都升序，判断目标值在不在。

**怎么想**：从**右上角**开始。当前值比目标大，说明这一列下面都更大，可以整列排除（左移）；比目标小，说明这一行左边都更小，整行排除（下移）。每步砍掉一行或一列。

```python
class Solution:
    def searchMatrix(self, matrix, target):
        m, n = len(matrix), len(matrix[0])
        r, c = 0, n - 1
        while r < m and c >= 0:
            if matrix[r][c] == target:
                return True
            elif matrix[r][c] > target:
                c -= 1
            else:
                r += 1
        return False
```

时间 `O(m + n)`，空间 `O(1)`。**易错**：只能从右上（或左下）开始；从左上角开始，两个方向都是「变大」，无法确定排除哪边。

---

## 套路六 · 位运算与技巧

### 136 · 只出现一次的数字（简单）

所有数都出现两次，只有一个出现一次，找出来。

**怎么想**：`a ^ a = 0`、`a ^ 0 = a`，而且异或满足交换律。把全部数异或起来，成对的全抵消，剩下的就是答案。`^` 是异或，不是乘方（乘方是 `**`）。

```python
class Solution:
    def singleNumber(self, nums):
        ans = 0
        for x in nums:
            ans ^= x
        return ans
```

时间 `O(n)`，空间 `O(1)`。

### 169 · 多数元素（简单）

找出出现次数超过一半的元素。

**怎么想**：**摩尔投票**。假设当前候选人是 `cand`，票数 `cnt`。遇到同样的就 +1，不同的就 -1，票归零就换候选人。因为真正的多数元素比「其他所有元素加起来」还多，两两抵消后它一定活到最后。

```python
class Solution:
    def majorityElement(self, nums):
        cand = None
        cnt = 0
        for x in nums:
            if cnt == 0:
                cand = x
            cnt += 1 if x == cand else -1
        return cand
```

时间 `O(n)`，空间 `O(1)`。**易错**：题目保证存在多数元素，所以不用再验一遍；不保证的话要补一次计数确认。

### 75 · 颜色分类（中等）

数组里只有 0、1、2，原地排成 0 在前、2 在后。

**怎么想**：三指针荷兰国旗。`l` 是「下一个 0 该放的位置」，`r` 是「下一个 2 该放的位置」，`i` 是当前检查的。遇到 0 和 `l` 交换并让 `i` 前进；遇到 2 和 `r` 交换，但 **`i` 不能前进**（换过来的还没检查过）。

```python
class Solution:
    def sortColors(self, nums):
        l = i = 0
        r = len(nums) - 1
        while i <= r:
            if nums[i] == 0:
                nums[l], nums[i] = nums[i], nums[l]
                l += 1
                i += 1
            elif nums[i] == 2:
                nums[r], nums[i] = nums[i], nums[r]
                r -= 1
            else:
                i += 1
```

时间 `O(n)`，空间 `O(1)`。**易错**：`i <= r` 不是 `i < len(nums)`；2 的分支里 `i` 不动。

### 31 · 下一个排列（中等）

把数组当成排列，原地改成字典序的下一个排列；若已是最大，改成最小。

**怎么想**：三步。① 从右往左找第一个「比右边小」的位置 `i`（这是还能变大的最靠右位置）。② 再从右往左找第一个比 `nums[i]` 大的数，和它交换。③ 把 `i` 之后的部分反转（原来是降序，反转后变成最小升序）。

```python
class Solution:
    def nextPermutation(self, nums):
        n = len(nums)
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        if i >= 0:
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        l, r = i + 1, n - 1
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
```

时间 `O(n)`，空间 `O(1)`。**易错**：`i = -1` 表示整个数组是降序（最大排列），此时跳过交换、直接整体反转。

### 287 · 寻找重复数（中等）

n+1 个数，值都在 1～n 之间，只有一个数重复，不改数组、空间 `O(1)` 找出它。

**怎么想**：把数组看成「链表」——下标 `i` 的下一个位置是 `nums[i]`。因为有重复值，必然有环，环的入口就是重复的数。用快慢指针找环入口：先让快慢相遇，再让一个指针回到起点，两者同速前进，再次相遇处即入口。

```python
class Solution:
    def findDuplicate(self, nums):
        slow = fast = 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        p = 0
        while p != slow:
            p = nums[p]
            slow = nums[slow]
        return p
```

时间 `O(n)`，空间 `O(1)`。**易错**：初始都从 0 出发；第二段循环是「先走再比」还是「先比再走」要一致，这里用 `while p != slow` 保证相遇时返回入口。

---

## 本册小结

| 遇到什么 | 先想到 |
|---|---|
| 找两个数、查补数 | 字典查配对，先查后存 |
| 去重、分组、判存在 | 集合 / 字典 |
| 有序、找两个数 | 对撞双指针 |
| 连续子串、最长/最短 | 滑动窗口（`l` 只增不减） |
| 子数组求和、含负数 | 前缀和 + 哈希，`cnt[0]=1` |
| 每个窗口最大值 | 单调队列（`deque` 存下标） |
| 网格里找路径/顺序 | 四个边界或右上角起步 |
| 出现次数、只出现一次 | 异或 / 摩尔投票 |

**共性**：绝大多数优化都是「把一遍遍翻找，变成查表或者不回头的指针」。想不出解法时，先问自己「哪一步在重复劳动」。

---

## 本册自测（闭卷）

1. 不查资料，默写两数之和、最长连续序列、滑动窗口通用骨架。
2. 说出「滑动窗口」和「前缀和」分别在什么时候用，为什么有负数时窗口会失效。
3. `3` 题里的 `last[c] >= l` 为什么不能省？举一个出错输入。
4. `560` 题里 `cnt[0] = 1` 漏了会怎样？
5. `239` 题为什么队列里存下标而不是值？
6. **口述题**：`11` 题里为什么每次移动较矮的那一边，不会漏掉最优解？

<details>
<summary>答案要点</summary>

1. 见各题代码。骨架是「`r` 用 for 扩、`l` 用 while 缩、缩完再更新答案」。
2. 窗口适用于「右端右移时窗口性质单调变化」；有负数时窗口和不再单调，缩左边可能让和变小甚至方向不定，改用前缀和 + 哈希统计 `pre[i] - K` 出现次数。
3. 输入 `"abba"`：r=3 时 `a` 的上次位置 0 已在左边界 2 之外，漏掉判断会把 `l` 拉回 1，答案错成 3。`l` 必须只增不减。
4. 会漏掉「从下标 0 开始、前缀和恰好等于 K」的子数组。
5. 存值无法判断队首元素是否已经滑出窗口；存下标后可以用 `q[0] <= i - k` 精确淘汰。
6. 面积 = 宽度 × 较矮高度。从最宽处开始，宽度只会变小。若移动较高的那边，较矮的板仍是高度上限，任何新位置面积都更小；只有换掉矮板才可能让高度变大，所以移动矮板不会漏掉更优解。

</details>

---

## 下一册

[L07](L07-search-stack-heap.md) 讲 18 道题：二分查找、栈与单调栈、堆、贪心。会用到本册的 `deque` 和双指针思路，按顺序读即可。
