# L07 · 二分、栈、堆、贪心（18 题）

本册 18 道题，四个套路。它们看着不相关，其实都在做同一件事：**别把力气花在明显没希望的地方**。

| 套路 | 题号 · 题名 | 难度 |
|---|---|---|
| 二分 | 35 搜索插入位置 · 74 搜索二维矩阵 · 34 找第一个和最后一个位置 · 33 搜索旋转排序数组 · 153 旋转数组最小值 · 4 两个正序数组的中位数 | 易 中 中 中 中 难 |
| 栈 | 20 有效的括号 · 155 最小栈 · 394 字符串解码 · 739 每日温度 · 84 柱状图最大矩形 | 易 中 中 中 难 |
| 堆 | 215 第 K 个最大 · 347 前 K 个高频 · 295 数据流的中位数 | 中 中 难 |
| 贪心 | 121 买卖股票 · 55 跳跃游戏 · 45 跳跃游戏 II · 763 划分字母区间 | 易 中 中 中 |

---

## 套路一 · 二分查找：每次砍掉一半

**它在解决什么问题**：在有序数据里找一个数，从头翻是 `O(n)`；看一眼中间的数，就能确定目标在哪一半，一次砍掉一半 → `O(log n)`。10 亿个数据也只要约 30 步。

**一句话前提**：数据必须**有序**，或者「满足条件的边界」是单调的。

### 两个骨架，先背下来

**骨架 A：找某个确切的值，左闭右闭**

```python
def binary_search(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:                  # 等号不能少
        mid = (l + r) // 2         # 用 //，不是 /
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            l = mid + 1
        else:
            r = mid - 1
    return -1
```

**骨架 B：找「第一个 ≥ target 的位置」，左闭右开**

```python
def lower_bound(nums, target):
    l, r = 0, len(nums)            # 注意右端是 n
    while l < r:
        mid = (l + r) // 2
        if nums[mid] >= target:
            r = mid                # mid 可能就是答案，不能跳过
        else:
            l = mid + 1
    return l                       # 可能等于 n，表示全都小于 target
```

**为什么两个骨架长得不一样**：A 要找一个确切的值，区间里每个位置都可能是答案，所以 `l <= r` 且 `r = mid - 1`；B 要找「边界」，`nums[mid]` 本身可能就是答案，所以要把 `mid` 留在区间里（`r = mid`），并用 `l < r` 保证区间能收缩到一点。

三个高频错：漏 `l <= r` 的等号、用 `/` 算出小数下标、`r` 该减 1 时没减导致死循环。

Python 有个库函数能直接做骨架 B：

```python
import bisect
i = bisect.bisect_left(nums, target)        # 第一个 >= target 的位置
j = bisect.bisect_right(nums, target) - 1   # 最后一个 <= target 的位置
```

**面试时建议手写**（考的就是边界控制），但可以用它来给自己对拍。

### 35 · 搜索插入位置（简单）

有序数组里找 target，找到返回下标，没找到返回它该插入的位置。就是骨架 B。

```python
class Solution:
    def searchInsert(self, nums, target):
        l, r = 0, len(nums)
        while l < r:
            mid = (l + r) // 2
            if nums[mid] >= target:
                r = mid
            else:
                l = mid + 1
        return l
```

时间 `O(log n)`，空间 `O(1)`。**易错**：右端是 `len(nums)` 不是 `len(nums)-1`，因为插入位置可能是末尾。

### 74 · 搜索二维矩阵（中等）

矩阵每行升序，且下一行第一个数大于上一行最后一个数——整体其实就是一条拉直的有序数组。

**怎么想**：把「一维下标 mid」换算成「第 `mid // n` 行、第 `mid % n` 列」，然后照骨架 A 二分。

```python
class Solution:
    def searchMatrix(self, matrix, target):
        m, n = len(matrix), len(matrix[0])
        l, r = 0, m * n - 1
        while l <= r:
            mid = (l + r) // 2
            v = matrix[mid // n][mid % n]
            if v == target:
                return True
            elif v < target:
                l = mid + 1
            else:
                r = mid - 1
        return False
```

时间 `O(log(mn))`，空间 `O(1)`。**易错**：`m*n` 可能很大，但 Python 整数不溢出，直接算没问题。

### 34 · 找第一个和最后一个位置（中等）

有序数组里找 target 第一次和最后一次出现的下标，没有返回 `[-1, -1]`。

**怎么想**：两次「找边界」。第一次找「第一个 ≥ target」的位置；第二次找「第一个 ≥ target+1」的位置，减 1 就是最后一个 target。

```python
class Solution:
    def searchRange(self, nums, target):
        def lower(x):
            l, r = 0, len(nums)
            while l < r:
                mid = (l + r) // 2
                if nums[mid] >= x:
                    r = mid
                else:
                    l = mid + 1
            return l
        a = lower(target)
        b = lower(target + 1) - 1
        if a <= b:
            return [a, b]
        return [-1, -1]
```

时间 `O(log n)`，空间 `O(1)`。**易错**：`a == len(nums)`（target 比所有数都大）时 `a > b`，靠这个判断返回 `[-1,-1]`，不用额外判空。

### 33 · 搜索旋转排序数组（中等）

原本有序的数组被「旋转」过（如 `[4,5,6,7,0,1,2]`），找 target 的下标。

**怎么想**：数组不再是整体有序，但**从中间劈开，一定有一半是有序的**。判断哪半有序，再看 target 是否落在那一半里，就能决定砍掉哪边。

```python
class Solution:
    def search(self, nums, target):
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target:
                return mid
            if nums[l] <= nums[mid]:          # 左半有序
                if nums[l] <= target < nums[mid]:
                    r = mid - 1
                else:
                    l = mid + 1
            else:                             # 右半有序
                if nums[mid] < target <= nums[r]:
                    l = mid + 1
                else:
                    r = mid - 1
        return -1
```

时间 `O(log n)`，空间 `O(1)`。**易错**：判断「左半有序」用 `<=` 而不是 `<`，因为区间可能只剩两个元素。

### 153 · 寻找旋转排序数组中的最小值（中等）

**怎么想**：拿 `nums[mid]` 和 `nums[r]` 比。如果 `nums[mid] > nums[r]`，说明最小值一定在 mid 右边（因为左半是从大到小的跳变之前）；否则最小值在 mid 左边或就是 mid。

```python
class Solution:
    def findMin(self, nums):
        l, r = 0, len(nums) - 1
        while l < r:
            mid = (l + r) // 2
            if nums[mid] > nums[r]:
                l = mid + 1
            else:
                r = mid
        return nums[l]
```

时间 `O(log n)`，空间 `O(1)`。**易错**：和 `nums[r]` 比，不是 `nums[l]`；用 `r = mid` 保留 mid 本身。

### 4 · 寻找两个正序数组的中位数（困难）

两个有序数组，找合并后的中位数，要求 `O(log(m+n))`。

**怎么想**：中位数把数据分成左右两半，左边个数等于（或多一个）右边。只要在较短数组里二分一个「切分点 i」，另一个数组的切分点 `j` 就自动确定。当「左边最大值 ≤ 右边最小值」时，切分正确，中位数就在四个边界数里。边界之外用 `±inf` 兜底。

```python
class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        total = m + n
        half = (total + 1) // 2
        lo, hi = 0, m
        while lo <= hi:
            i = (lo + hi) // 2
            j = half - i
            l1 = float("-inf") if i == 0 else nums1[i - 1]
            r1 = float("inf") if i == m else nums1[i]
            l2 = float("-inf") if j == 0 else nums2[j - 1]
            r2 = float("inf") if j == n else nums2[j]
            if l1 <= r2 and l2 <= r1:
                if total % 2:
                    return float(max(l1, l2))
                return (max(l1, l2) + min(r1, r2)) / 2
            elif l1 > r2:
                hi = i - 1
            else:
                lo = i + 1
```

时间 `O(log(min(m,n)))`，空间 `O(1)`。**易错**：一定要在**较短**数组上二分，否则 `j` 可能超出范围；`half = (total+1)//2` 让奇数时左边多一个，中位数直接是 `max(l1,l2)`。

---

## 套路二 · 栈：只关心「最近放进去的」

**栈是什么**：像一摞盘子，只能从顶上放、从顶上拿。Python 里用普通列表就行：`append()` 放、`pop()` 拿、`stack[-1]` 看顶上都行。

**什么时候用**：题目里出现「配对」「嵌套」「上一个/下一个更大」「撤销回退」这类词。

### 20 · 有效的括号（简单）

判断括号串是否合法（`()[]{}`，要正确嵌套）。

**怎么想**：遇到左括号先把「期待的右括号」压栈；遇到右括号就看它是不是栈顶期待的那个。最后栈必须是空的。

```python
class Solution:
    def isValid(self, s):
        pairs = {')': '(', ']': '[', '}': '{'}
        st = []
        for c in s:
            if c in pairs:
                if not st or st[-1] != pairs[c]:
                    return False
                st.pop()
            else:
                st.append(c)
        return not st
```

时间 `O(n)`，空间 `O(n)`。**易错**：`"]"` 这种一上来就是右括号的，要先判 `not st`，否则 `st[-1]` 越界。

### 155 · 最小栈（中等）

设计一个栈，除了常规操作，还要能 `O(1)` 返回当前最小值。

**怎么想**：再用一个「最小值栈」，只在**新值 ≤ 当前最小值**时压入。弹出时如果弹的正好是当前最小值，就从最小值栈也弹一个。这样两个栈顶永远对得上。

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []

    def push(self, val):
        self.stack.append(val)
        if not self.mins or val <= self.mins[-1]:
            self.mins.append(val)

    def pop(self):
        x = self.stack.pop()
        if x == self.mins[-1]:
            self.mins.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.mins[-1]
```

每个操作 `O(1)`，空间 `O(n)`。**易错**：`push` 里用 `<=` 而不是 `<`，否则重复的最小值弹出时会出错。

### 394 · 字符串解码（中等）

`3[a2[c]]` 展开成 `accaccacc`。

**怎么想**：遇到 `[` 时，把「之前的字符串」和「重复次数」一起压栈，然后清空重新攒；遇到 `]` 时弹出来拼接。`num` 可能是多位数，要逐位累加。

```python
class Solution:
    def decodeString(self, s):
        stack = []
        cur = ""
        num = 0
        for c in s:
            if c.isdigit():
                num = num * 10 + int(c)
            elif c == "[":
                stack.append((cur, num))
                cur = ""
                num = 0
            elif c == "]":
                prev, k = stack.pop()
                cur = prev + cur * k
            else:
                cur += c
        return cur
```

时间 `O(展开后长度)`，空间 `O(嵌套深度)`。**易错**：`num` 在 `[` 之后必须清零，否则下一层数字会接在旧数字后面。

### 739 · 每日温度（中等）

对每个位置，求还要等几天才出现更高的温度，没有就 0。

**怎么想**：用**单调栈**存「还没找到更高温度的日子」的下标，对应温度从栈底到栈顶递减。新温度比栈顶高时，栈顶这些日子终于等到了，弹出来算天数。**每个下标最多进栈、出栈各一次**，所以整体 `O(n)`。

```python
class Solution:
    def dailyTemperatures(self, temperatures):
        st = []
        ans = [0] * len(temperatures)
        for i, x in enumerate(temperatures):
            while st and temperatures[st[-1]] < x:
                j = st.pop()
                ans[j] = i - j
            st.append(i)
        return ans
```

时间 `O(n)`，空间 `O(n)`。**易错**：栈里存**下标**，不是温度值——答案要的是天数差。

### 84 · 柱状图中最大的矩形（困难）

找相邻柱子能框出的最大矩形面积。

**怎么想**：对每根柱子，需要知道「左边第一个比它矮的」和「右边第一个比它矮的」，两者之间就是以它的高度为高的最大宽度。单调栈（高度递增）能一次找出来：遇到比栈顶矮的柱子时，栈顶的右边界就确定了，弹出来算面积。末尾加一个高度 0 的**哨兵**，保证最后所有柱子都能被弹出。

```python
class Solution:
    def largestRectangleArea(self, heights):
        h = heights + [0]           # 哨兵
        st = []
        ans = 0
        for i, x in enumerate(h):
            while st and h[st[-1]] > x:
                height = h[st.pop()]
                left = st[-1] if st else -1
                width = i - left - 1
                ans = max(ans, height * width)
            st.append(i)
        return ans
```

时间 `O(n)`，空间 `O(n)`。**易错**：`width = i - left - 1` 里的 `left` 是弹出后新的栈顶；没有哨兵时最后一段递增的柱子永远不会被结算。

---

## 套路三 · 堆：每次自动拿到最值

**它是什么**：往里随便丢数据，它永远能一瞬间告诉你最小的是谁，取走也很快（`O(log n)`）。Python 的 `heapq` 是**小根堆**（堆顶最小）。

**想要最大怎么办**：把值取负存进去，取出来再取负。

### 215 · 数组中的第 K 个最大元素（中等）

**怎么想**：维护一个大小恰好为 K 的**小根堆**。遍历时堆没满就放，满了且新数比堆顶大就替换堆顶。最后堆里就是最大的 K 个数，堆顶是这 K 个里最小的，正好是全体第 K 大。

```python
import heapq

class Solution:
    def findKthLargest(self, nums, k):
        h = []
        for x in nums:
            if len(h) < k:
                heapq.heappush(h, x)
            elif x > h[0]:
                heapq.heapreplace(h, x)
        return h[0]
```

时间 `O(n log k)`，空间 `O(k)`。**易错**：别把整个数组堆化再弹 n-k 次（`O(n log n)`）；`heapreplace` 前一定要先判断 `x > h[0]`。

### 347 · 前 K 个高频元素（中等）

**怎么想**：先用 `Counter` 数频次，再维护大小为 K 的小根堆，元素放 `(频次, 值)`，按频次比。

```python
import heapq
from collections import Counter

class Solution:
    def topKFrequent(self, nums, k):
        h = []
        for val, freq in Counter(nums).items():
            if len(h) < k:
                heapq.heappush(h, (freq, val))
            elif freq > h[0][0]:
                heapq.heapreplace(h, (freq, val))
        return [val for freq, val in h]
```

时间 `O(n log k)`，空间 `O(n)`。**易错**：元组入堆按第一项比较，所以频次必须放前面；如果第二项是无法比较的对象且频次可能相同，要插一个序号（见 [L04 §2](L04-toolbox.md)）。

### 295 · 数据流的中位数（困难）

不断来新数，随时要能返回当前所有数的中位数。

**怎么想**：**双堆**。`small` 存较小的一半（用负数模拟大根堆），`large` 存较大的一半（小根堆）。始终保持两边数量差不超过 1，那么中位数就是两边堆顶的平均（或 `small` 堆顶）。

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []      # 存负数 → 堆顶是较小半里最大的
        self.large = []      # 小根堆 → 堆顶是较大半里最小的

    def addNum(self, num):
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2
```

`addNum` 是 `O(log n)`，`findMedian` 是 `O(1)`，空间 `O(n)`。**易错**：每次从 `small` 顶移到 `large` 时记得取负号还原；平衡条件是 `large` 不能比 `small` 多。

---

## 套路四 · 贪心：每一步都选眼前最好的

**它在解决什么问题**：有些题不用「把所有可能都试一遍」，每一步选局部最优，最后就是全局最优。

**但贪心是最容易骗人的套路**：不是所有题都能这么干。能用的前提是能讲清「为什么这一步选了不会让后面变差」。做题时至少要能对自己说出一句话的理由，说不出就可能是错的。

### 121 · 买卖股票的最佳时机（简单）

只能买卖一次，求最大利润。

**怎么想**：扫一遍，始终记住「到今天为止最低的买入价」，然后算「今天卖出能赚多少」，取最大。

```python
class Solution:
    def maxProfit(self, prices):
        low = float("inf")
        ans = 0
        for p in prices:
            low = min(low, p)
            ans = max(ans, p - low)
        return ans
```

时间 `O(n)`，空间 `O(1)`。**易错**：`low` 必须初始化成正无穷，不能是 0（价格可能是任意正数）；先更新 `low` 再算利润，同一天买卖利润为 0，不影响结果。

### 55 · 跳跃游戏（中等）

数组每个位置表示最多能往后跳几步，判断能不能到最后一个位置。

**怎么想**：不需要真的模拟「跳到哪」，只要维护「目前能到达的最远位置 `far`」。扫到位置 `i` 时如果 `i > far`，说明连这里都到不了，后面更到不了。

```python
class Solution:
    def canJump(self, nums):
        far = 0
        for i, step in enumerate(nums):
            if i > far:
                return False
            far = max(far, i + step)
        return True
```

时间 `O(n)`，空间 `O(1)`。**易错**：判断 `i > far` 要在更新 `far` **之前**。

### 45 · 跳跃游戏 II（中等）

保证能到达终点，求最少跳几次。

**怎么想**：把「跳 k 次能到的范围」看成一个区间。当前这一跳的范围内，记录下一步最远能到哪；走到当前范围边界时，就必须再跳一次，同时把边界推到刚记录的最远处。像一层一层往外扩。

```python
class Solution:
    def jump(self, nums):
        ans = 0
        cur_end = 0        # 当前这一跳能到的最远位置
        farthest = 0       # 下一跳能到的最远位置
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == cur_end:
                ans += 1
                cur_end = farthest
        return ans
```

时间 `O(n)`，空间 `O(1)`。**易错**：循环到 `len(nums)-2` 就停（站在最后一个位置不用再跳）；只有一个元素时循环不执行，返回 0，正确。

### 763 · 划分字母区间（中等）

把字符串切成尽可能多的片段，要求同一个字母只出现在一个片段里。

**怎么想**：先记录每个字母**最后出现的位置**。扫描时不断把当前片段的右端点 `end` 推到「片段内所有字母的最远位置」；一旦扫到 `i == end`，说明这个片段里所有字母都不会再出现在后面，可以在这里切一刀。

```python
class Solution:
    def partitionLabels(self, s):
        last = {c: i for i, c in enumerate(s)}
        start = end = 0
        res = []
        for i, c in enumerate(s):
            end = max(end, last[c])
            if i == end:
                res.append(i - start + 1)
                start = i + 1
        return res
```

时间 `O(n)`，空间 `O(字符集)`。**易错**：`start` 要在切完后更新；字典推导式 `{c: i for ...}` 天然保留每个字母最后一次的下标。

---

## 本册小结

| 遇到什么 | 先想到 |
|---|---|
| 有序、找数或找边界、要求 `O(log n)` | 二分两个骨架 |
| 括号配对、嵌套展开、回退 | 栈 |
| 「下一个更大」「最近比它矮」 | 单调栈（存下标） |
| 第 K 大 / 前 K 个 | 大小为 K 的小根堆 |
| 动态维护中位数 | 双堆 |
| 每步选眼前最好、能讲出理由 | 贪心 |

**最容易错的三处**：二分的边界（`/` 要写成 `//`、`r = mid` 还是 `mid - 1`）、单调栈里存的是下标不是值、堆的大小和方向（要第 K 大却用了大根堆）。

---

## 本册自测（闭卷）

1. 默写二分查找的两个骨架，说明它们为什么不一样。
2. `34` 题里 `lower(target + 1) - 1` 为什么能得到最后一个位置？
3. 单调栈为什么整体是 `O(n)` 而不是 `O(n²)`？
4. 求第 K 大为什么用**小根堆**、大小恰好 K？
5. 贪心算法为什么不能「看着对就上」？
6. **口述题**：`45` 题里 `cur_end` 和 `farthest` 分别在表达什么？

<details>
<summary>答案要点</summary>

1. A 找确切值，区间每个位置都可能是答案，用 `l <= r` + `r = mid - 1`；B 找边界，`mid` 本身可能是答案，用 `l < r` + `r = mid` 把它留在区间里。
2. 「第一个 ≥ target+1 的位置」前面那个，就是最后一个 ≤ target（即等于 target）的位置；若 target 不存在，会得到 `a > b`，据此返回 `[-1,-1]`。
3. 每个下标最多进栈一次、出栈一次，虽然有 `while`，但总弹出次数不超过 n。
4. 大小为 K 的小根堆里装的正是全数组最大的 K 个数，堆顶是这 K 个里最小的，恰好就是全体第 K 大。用大根堆得弹 K 次才找得到，复杂度更高。
5. 局部最优未必能推出全局最优；必须能讲出「为什么这一步的选择不会让后续变差」的交换论证，否则很容易在特定数据上错。
6. `cur_end` 是「用当前跳跃次数能到达的最远边界」，`farthest` 是「在这个边界内所有位置出发，再跳一次能到达的最远处」。走到 `cur_end` 时不得不增加一跳，并把边界推进到 `farthest`。

</details>

---

## 下一册

[L08](L08-linkedlist-tree.md) 是 29 道题：链表和二叉树。会先花一整节讲清楚「节点」「引用」「递归」这三个让小白最卡的概念，再逐题展开。别跳那一节。
