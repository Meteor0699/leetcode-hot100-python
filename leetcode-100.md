# LeetCode 热题 100 · 原题与 Python 题解

> 原题题面来自 LeetCode 官网（leetcode.cn），题解为本仓库整理的 Python 实现。

> 逐题讲解、思路、复杂度、易错点见 [leetcode-100.html](leetcode-100.html) 或 L06–L09 教程。


---


## 1. 两数之和（LeetCode 1 · 简单）

### 原题

给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target 的那 两个 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

你可以按任意顺序返回答案。

示例 1：

输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。

示例 2：

输入：nums = [3,2,4], target = 6
输出：[1,2]

示例 3：

输入：nums = [3,3], target = 6
输出：[0,1]

提示：

• 2 <= nums.length <= 10⁴

• -10⁹ <= nums[i] <= 10⁹

• -10⁹ <= target <= 10⁹

• 只会存在一个有效答案

进阶：你可以想出一个时间复杂度小于 O(n²) 的算法吗？

### Python 题解

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

---


## 2. 两数相加（LeetCode 2 · 中等）

### 原题

给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。

请你将两个数相加，并以相同形式返回一个表示和的链表。

你可以假设除了数字 0 之外，这两个数都不会以 0 开头。

示例 1：

输入：l1 = [2,4,3], l2 = [5,6,4]
输出：[7,0,8]
解释：342 + 465 = 807.

示例 2：

输入：l1 = [0], l2 = [0]
输出：[0]

示例 3：

输入：l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
输出：[8,9,9,9,0,0,0,1]

提示：

• 每个链表中的节点数在范围 [1, 100] 内

• 0 <= Node.val <= 9

• 题目数据保证列表表示的数字不含前导零

### Python 题解

```python
class Solution:
    def addTwoNumbers(self, l1, l2):
        dummy = cur = ListNode(0)
        carry = 0
        while l1 is not None or l2 is not None or carry:
            s = carry + (l1.val if l1 else 0) + (l2.val if l2 else 0)
            carry, v = divmod(s, 10)
            cur.next = ListNode(v)
            cur = cur.next
            if l1 is not None:
                l1 = l1.next
            if l2 is not None:
                l2 = l2.next
        return dummy.next
```

---


## 3. 无重复字符的最长子串（LeetCode 3 · 中等）

### 原题

给定一个字符串 s ，请你找出其中不含有重复字符的 最长 子串 的长度。

示例 1:

输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。注意 "bca" 和 "cab" 也是正确答案。

示例 2:

输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。

示例 3:

输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。

提示：

• 0 <= s.length <= 10⁵

• s 由英文字母、数字、符号和空格组成

### Python 题解

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

---


## 4. 寻找两个正序数组的中位数（LeetCode 4 · 困难）

### 原题

给定两个大小分别为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。请你找出并返回这两个正序数组的 中位数 。

算法的时间复杂度应该为 O(log (m+n)) 。

示例 1：

输入：nums1 = [1,3], nums2 = [2]
输出：2.00000
解释：合并数组 = [1,2,3] ，中位数 2

示例 2：

输入：nums1 = [1,2], nums2 = [3,4]
输出：2.50000
解释：合并数组 = [1,2,3,4] ，中位数 (2 + 3) / 2 = 2.5

提示：

• nums1.length == m

• nums2.length == n

• 0 <= m <= 1000

• 0 <= n <= 1000

• 1 <= m + n <= 2000

• -10⁶ <= nums1[i], nums2[i] <= 10⁶

### Python 题解

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

---


## 5. 最长回文子串（LeetCode 5 · 中等）

### 原题

给你一个字符串 s，找到 s 中最长的 回文 子串。

示例 1：

输入：s = "babad"
输出："bab"
解释："aba" 同样是符合题意的答案。

示例 2：

输入：s = "cbbd"
输出："bb"

提示：

• 1 <= s.length <= 1000

• s 仅由数字和英文字母组成

### Python 题解

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

---


## 6. 盛最多水的容器（LeetCode 11 · 中等）

### 原题

给定一个长度为 n 的整数数组 height 。有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i]) 。

找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

返回容器可以储存的最大水量。

说明：你不能倾斜容器。

示例 1：

输入：[1,8,6,2,5,4,8,3,7]
输出：49
解释：图中垂直线代表输入数组 [1,8,6,2,5,4,8,3,7]。在此情况下，容器能够容纳水（表示为蓝色部分）的最大值为 49。

示例 2：

输入：height = [1,1]
输出：1

提示：

• n == height.length

• 2 <= n <= 10⁵

• 0 <= height[i] <= 10⁴

### Python 题解

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

---


## 7. 三数之和（LeetCode 15 · 中等）

### 原题

给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。

注意：答案中不可以包含重复的三元组。

示例 1：

输入：nums = [-1,0,1,2,-1,-4]
输出：[[-1,-1,2],[-1,0,1]]
解释：
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0 。
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0 。
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0 。
不同的三元组是 [-1,0,1] 和 [-1,-1,2] 。
注意，输出的顺序和三元组的顺序并不重要。

示例 2：

输入：nums = [0,1,1]
输出：[]
解释：唯一可能的三元组和不为 0 。

示例 3：

输入：nums = [0,0,0]
输出：[[0,0,0]]
解释：唯一可能的三元组和为 0 。

提示：

• 3 <= nums.length <= 3000

• -10⁵ <= nums[i] <= 10⁵

### Python 题解

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

---


## 8. 电话号码的字母组合（LeetCode 17 · 中等）

### 原题

给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。答案可以按 任意顺序 返回。

给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。

示例 1：

输入：digits = "23"
输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]

示例 2：

输入：digits = "2"
输出：["a","b","c"]

提示：

• 1 <= digits.length <= 4

• digits[i] 是范围 ['2', '9'] 的一个数字。

### Python 题解

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

---


## 9. 删除倒数第 N 个结点（LeetCode 19 · 中等）

### 原题

给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。

示例 1：

输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]

示例 2：

输入：head = [1], n = 1
输出：[]

示例 3：

输入：head = [1,2], n = 1
输出：[1]

提示：

• 链表中结点的数目为 sz

• 1 <= sz <= 30

• 0 <= Node.val <= 100

• 1 <= n <= sz

进阶：你能尝试使用一趟扫描实现吗？

### Python 题解

```python
class Solution:
    def removeNthFromEnd(self, head, n):
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n):
            fast = fast.next
        while fast.next is not None:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return dummy.next
```

---


## 10. 有效的括号（LeetCode 20 · 简单）

### 原题

给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。

有效字符串需满足：

• 左括号必须用相同类型的右括号闭合。

• 左括号必须以正确的顺序闭合。

• 每个右括号都有一个对应的相同类型的左括号。

示例 1：

输入：s = "()"

输出：true

示例 2：

输入：s = "()[]{}"

输出：true

示例 3：

输入：s = "(]"

输出：false

示例 4：

输入：s = "([])"

输出：true

示例 5：

输入：s = "([)]"

输出：false

提示：

• 1 <= s.length <= 10⁴

• s 仅由括号 '()[]{}' 组成

### Python 题解

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

---


## 11. 合并两个有序链表（LeetCode 21 · 简单）

### 原题

将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。

示例 1：

输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]

示例 2：

输入：l1 = [], l2 = []
输出：[]

示例 3：

输入：l1 = [], l2 = [0]
输出：[0]

提示：

• 两个链表的节点数目范围是 [0, 50]

• -100

### Python 题解

```python
class Solution:
    def mergeTwoLists(self, list1, list2):
        dummy = cur = ListNode(0)
        while list1 is not None and list2 is not None:
            if list1.val <= list2.val:
                cur.next, list1 = list1, list1.next
            else:
                cur.next, list2 = list2, list2.next
            cur = cur.next
        cur.next = list1 if list1 is not None else list2
        return dummy.next
```

---


## 12. 括号生成（LeetCode 22 · 中等）

### 原题

数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。

示例 1：

输入：n = 3
输出：["((()))","(()())","(())()","()(())","()()()"]

示例 2：

输入：n = 1
输出：["()"]

提示：

• 1 <= n <= 8

### Python 题解

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

---


## 13. 合并 K 个升序链表（LeetCode 23 · 困难）

### 原题

给你一个链表数组，每个链表都已经按升序排列。

请你将所有链表合并到一个升序链表中，返回合并后的链表。

示例 1：

输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
解释：链表数组如下：
[
1->4->5,
1->3->4,
2->6
]
将它们合并到一个有序链表中得到。
1->1->2->3->4->4->5->6

示例 2：

输入：lists = []
输出：[]

示例 3：

输入：lists = [[]]
输出：[]

提示：

• k == lists.length

• 0 <= k <= 10^4

• 0 <= lists[i].length <= 500

• -10^4 <= lists[i][j] <= 10^4

• lists[i] 按 升序 排列

• lists[i].length 的总和不超过 10^4

### Python 题解

```python
import heapq

class Solution:
    def mergeKLists(self, lists):
        h = []
        seq = 0
        for node in lists:
            if node is not None:
                heapq.heappush(h, (node.val, seq, node))
                seq += 1
        dummy = cur = ListNode(0)
        while h:
            _, _, node = heapq.heappop(h)
            cur.next = node
            cur = cur.next
            if node.next is not None:
                heapq.heappush(h, (node.next.val, seq, node.next))
                seq += 1
        return dummy.next
```

---


## 14. 两两交换链表中的节点（LeetCode 24 · 中等）

### 原题

给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。你必须在不修改节点内部的值的情况下完成本题（即，只能进行节点交换）。

示例 1：

输入：head = [1,2,3,4]
输出：[2,1,4,3]

示例 2：

输入：head = []
输出：[]

示例 3：

输入：head = [1]
输出：[1]

提示：

• 链表中节点的数目在范围 [0, 100] 内

• 0 <= Node.val <= 100

### Python 题解

```python
class Solution:
    def swapPairs(self, head):
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next is not None and prev.next.next is not None:
            a, b = prev.next, prev.next.next
            prev.next, b.next, a.next = b, a, b.next
            prev = a
        return dummy.next
```

---


## 15. K 个一组翻转链表（LeetCode 25 · 困难）

### 原题

给你链表的头节点 head ，每 k 个节点一组进行翻转，请你返回修改后的链表。

k 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 k 的整数倍，那么请将最后剩余的节点保持原有顺序。

你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。

示例 1：

输入：head = [1,2,3,4,5], k = 2
输出：[2,1,4,3,5]

示例 2：

输入：head = [1,2,3,4,5], k = 3
输出：[3,2,1,4,5]

提示：

• 链表中的节点数目为 n

• 1 <= k <= n <= 5000

• 0 <= Node.val <= 1000

进阶：你可以设计一个只用 O(1) 额外内存空间的算法解决此问题吗？

### Python 题解

```python
class Solution:
    def reverseKGroup(self, head, k):
        def kth_after(node, k):
            for _ in range(k):
                if node is None:
                    return None
                node = node.next
            return node

        dummy = ListNode(0, head)
        group_prev = dummy
        while True:
            kth = kth_after(group_prev, k)
            if kth is None:
                break
            group_next = kth.next
            prev, cur = group_next, group_prev.next
            while cur is not group_next:
                nxt = cur.next
                cur.next = prev
                prev, cur = cur, nxt
            old_head = group_prev.next       # 翻转后它成了这组尾巴
            group_prev.next = kth
            group_prev = old_head
        return dummy.next
```

---


## 16. 下一个排列（LeetCode 31 · 中等）

### 原题

整数数组的一个 排列 就是将其所有成员以序列或线性顺序排列。

• 例如，arr = [1, 2, 3] ，以下这些都可以视作 arr 的排列：[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1] 。

整数数组的 下一个排列 是指其整数的下一个字典序更大的排列。更正式地，如果数组的所有排列根据其字典顺序从小到大排列在一个容器中，那么数组的 下一个排列 就是在这个有序容器中排在它后面的那个排列。如果不存在下一个更大的排列，那么这个数组必须重排为字典序最小的排列（即，其元素按升序排列）。

• arr = [1, 2, 3] 的下一个排列是 [1, 3, 2] 。

• arr = [2, 3, 1] 的下一个排列是 [3, 1, 2] 。

• arr = [3, 2, 1] 的下一个排列是 [1, 2, 3] ，因为 [3, 2, 1] 不存在一个字典序更大的排列。

给你一个整数数组 nums ，找出 nums 的下一个排列。

必须 原地 修改，只允许使用额外常数空间。

示例 1：

输入：nums = [1,2,3]
输出：[1,3,2]

示例 2：

输入：nums = [3,2,1]
输出：[1,2,3]

示例 3：

输入：nums = [1,1,5]
输出：[1,5,1]

提示：

• 1 <= nums.length <= 100

• 0 <= nums[i] <= 100

### Python 题解

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

---


## 17. 最长有效括号（LeetCode 32 · 困难）

### 原题

给你一个只包含 '(' 和 ')' 的字符串，找出最长有效（格式正确且连续）括号 子串 的长度。

左右括号匹配，即每个左括号都有对应的右括号将其闭合的字符串是格式正确的，比如 "(()())"。

示例 1：

输入：s = "(()"
输出：2
解释：最长有效括号子串是 "()"

示例 2：

输入：s = ")()())"
输出：4
解释：最长有效括号子串是 "()()"

示例 3：

输入：s = ""
输出：0

提示：

• 0 <= s.length <= 3 * 10⁴

• s[i] 为 '(' 或 ')'

### Python 题解

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

---


## 18. 搜索旋转排序数组（LeetCode 33 · 中等）

### 原题

整数数组 nums 按升序排列，数组中的值 互不相同 。

在传递给函数之前，nums 在预先未知的某个下标 k（0 <= k < nums.length）上进行了 向左旋转，使数组变为 [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]（下标 从 0 开始 计数）。例如， [0,1,2,4,5,6,7] 下标 3 上向左旋转后可能变为 [4,5,6,7,0,1,2] 。

给你 旋转后 的数组 nums 和一个整数 target ，如果 nums 中存在这个目标值 target ，则返回它的下标，否则返回 -1 。

你必须设计一个时间复杂度为 O(log n) 的算法解决此问题。

示例 1：

输入：nums = [4,5,6,7,0,1,2], target = 0
输出：4

示例 2：

输入：nums = [4,5,6,7,0,1,2], target = 3
输出：-1

示例 3：

输入：nums = [1], target = 0
输出：-1

提示：

• 1 <= nums.length <= 5000

• -10⁴ <= nums[i] <= 10⁴

• nums 中的每个值都 独一无二

• 题目数据保证 nums 在预先未知的某个下标上进行了旋转

• -10⁴ <= target <= 10⁴

### Python 题解

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

---


## 19. 找第一个和最后一个位置（LeetCode 34 · 中等）

### 原题

给你一个按照非递减顺序排列的整数数组 nums，和一个目标值 target。请你找出给定目标值在数组中的开始位置和结束位置。

如果数组中不存在目标值 target，返回 [-1, -1]。

你必须设计并实现时间复杂度为 O(log n) 的算法解决此问题。

示例 1：

输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]

示例 2：

输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]

示例 3：

输入：nums = [], target = 0
输出：[-1,-1]

提示：

• 0 <= nums.length <= 10⁵

• -10⁹ <= nums[i] <= 10⁹

• nums 是一个非递减数组

• -10⁹ <= target <= 10⁹

### Python 题解

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

---


## 20. 搜索插入位置（LeetCode 35 · 简单）

### 原题

给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。如果目标值不存在于数组中，返回它将会被按顺序插入的位置。

请必须使用时间复杂度为 O(log n) 的算法。

示例 1:

输入: nums = [1,3,5,6], target = 5
输出: 2

示例 2:

输入: nums = [1,3,5,6], target = 2
输出: 1

示例 3:

输入: nums = [1,3,5,6], target = 7
输出: 4

提示:

• 1 <= nums.length <= 10⁴

• -10⁴ <= nums[i] <= 10⁴

• nums 为 无重复元素 的 升序 排列数组

• -10⁴ <= target <= 10⁴

### Python 题解

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

---


## 21. 组合总和（LeetCode 39 · 中等）

### 原题

给你一个 无重复元素 的整数数组 candidates 和一个目标整数 target ，找出 candidates 中可以使数字和为目标数 target 的 所有 不同组合 ，并以列表形式返回。你可以按 任意顺序 返回这些组合。

candidates 中的 同一个 数字可以 无限制重复被选取 。如果至少一个数字的被选数量不同，则两种组合是不同的。

对于给定的输入，保证和为 target 的不同组合数少于 150 个。

示例 1：

输入：candidates = [2,3,6,7], target = 7
输出：[[2,2,3],[7]]
解释：
2 和 3 可以形成一组候选，2 + 2 + 3 = 7 。注意 2 可以使用多次。
7 也是一个候选， 7 = 7 。
仅有这两种组合。

示例 2：

输入: candidates = [2,3,5], target = 8
输出: [[2,2,2,2],[2,3,3],[3,5]]

示例 3：

输入: candidates = [2], target = 1
输出: []

提示：

• 1 <= candidates.length <= 30

• 2 <= candidates[i] <= 40

• candidates 的所有元素 互不相同

• 1 <= target <= 40

### Python 题解

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

---


## 22. 缺失的第一个正数（LeetCode 41 · 困难）

### 原题

给你一个未排序的整数数组 nums ，请你找出其中没有出现的最小的正整数。

请你实现时间复杂度为 O(n) 并且只使用常数级别额外空间的解决方案。

示例 1：

输入：nums = [1,2,0]
输出：3
解释：范围 [1,2] 中的数字都在数组中。

示例 2：

输入：nums = [3,4,-1,1]
输出：2
解释：1 在数组中，但 2 没有。

示例 3：

输入：nums = [7,8,9,11,12]
输出：1
解释：最小的正数 1 没有出现。

提示：

• 1 <= nums.length <= 10⁵

• -2³¹ <= nums[i] <= 2³¹ - 1

### Python 题解

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

---


## 23. 接雨水（LeetCode 42 · 困难）

### 原题

给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

示例 1：

输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。

示例 2：

输入：height = [4,2,0,3,2,5]
输出：9

提示：

• n == height.length

• 1 <= n <= 2 * 10⁴

• 0 <= height[i] <= 10⁵

### Python 题解

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

---


## 24. 跳跃游戏 II（LeetCode 45 · 中等）

### 原题

给定一个长度为 n 的 0 索引整数数组 nums。初始位置在下标 0。

每个元素 nums[i] 表示从索引 i 向后跳转的最大长度。换句话说，如果你在索引 i 处，你可以跳转到任意 (i + j) 处：

• 0 <= j <= nums[i] 且

• i + j < n

返回到达 n - 1 的最小跳跃次数。测试用例保证可以到达 n - 1。

示例 1:

输入: nums = [2,3,1,1,4]
输出: 2
解释: 跳到最后一个位置的最小跳跃数是 2。
从下标为 0 跳到下标为 1 的位置，跳 1 步，然后跳 3 步到达数组的最后一个位置。

示例 2:

输入: nums = [2,3,0,1,4]
输出: 2

提示:

• 1 <= nums.length <= 10⁴

• 0 <= nums[i] <= 1000

• 题目保证可以到达 n - 1

### Python 题解

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

---


## 25. 全排列（LeetCode 46 · 中等）

### 原题

给定一个不含重复数字的数组 nums ，返回其 所有可能的全排列 。你可以 按任意顺序 返回答案。

示例 1：

输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

示例 2：

输入：nums = [0,1]
输出：[[0,1],[1,0]]

示例 3：

输入：nums = [1]
输出：[[1]]

提示：

• 1 <= nums.length <= 6

• -10 <= nums[i] <= 10

• nums 中的所有整数 互不相同

### Python 题解

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

---


## 26. 旋转图像（LeetCode 48 · 中等）

### 原题

给定一个 n × n 的二维矩阵 matrix 表示一个图像。请你将图像顺时针旋转 90 度。

你必须在 原地 旋转图像，这意味着你需要直接修改输入的二维矩阵。请不要 使用另一个矩阵来旋转图像。

示例 1：

输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[[7,4,1],[8,5,2],[9,6,3]]

示例 2：

输入：matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
输出：[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]

提示：

• n == matrix.length == matrix[i].length

• 1 <= n <= 20

• -1000 <= matrix[i][j] <= 1000

### Python 题解

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

---


## 27. 字母异位词分组（LeetCode 49 · 中等）

### 原题

给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。

示例 1:

输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

输出: [["bat"],["nat","tan"],["ate","eat","tea"]]

解释：

• 在 strs 中没有字符串可以通过重新排列来形成 "bat"。

• 字符串 "nat" 和 "tan" 是字母异位词，因为它们可以重新排列以形成彼此。

• 字符串 "ate" ，"eat" 和 "tea" 是字母异位词，因为它们可以重新排列以形成彼此。

示例 2:

输入: strs = [""]

输出: [[""]]

示例 3:

输入: strs = ["a"]

输出: [["a"]]

提示：

• 1 <= strs.length <= 10⁴

• 0 <= strs[i].length <= 100

• strs[i] 仅包含小写字母

### Python 题解

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

---


## 28. N 皇后（LeetCode 51 · 困难）

### 原题

按照国际象棋的规则，皇后可以攻击与之处在同一行或同一列或同一斜线上的棋子。

n 皇后问题 研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。

给你一个整数 n ，返回所有不同的 n 皇后问题 的解决方案。

每一种解法包含一个不同的 n 皇后问题 的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。

示例 1：

输入：n = 4
输出：[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
解释：如上图所示，4 皇后问题存在两个不同的解法。

示例 2：

输入：n = 1
输出：[["Q"]]

提示：

• 1 <= n <= 9

### Python 题解

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

---


## 29. 最大子数组和（LeetCode 53 · 中等）

### 原题

给你一个整数数组 nums ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

子数组 是数组中的一个连续部分。

示例 1：

输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。

示例 2：

输入：nums = [1]
输出：1

示例 3：

输入：nums = [5,4,-1,7,8]
输出：23

提示：

• 1 <= nums.length <= 10⁵

• -10⁴ <= nums[i] <= 10⁴

进阶：如果你已经实现复杂度为 O(n) 的解法，尝试使用更为精妙的 分治法 求解。

### Python 题解

```python
class Solution:
    def maxSubArray(self, nums):
        cur = best = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)
            best = max(best, cur)
        return best
```

---


## 30. 螺旋矩阵（LeetCode 54 · 中等）

### 原题

给你一个 m 行 n 列的矩阵 matrix ，请按照 顺时针螺旋顺序 ，返回矩阵中的所有元素。

示例 1：

输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,3,6,9,8,7,4,5]

示例 2：

输入：matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
输出：[1,2,3,4,8,12,11,10,9,5,6,7]

提示：

• m == matrix.length

• n == matrix[i].length

• 1

### Python 题解

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

---


## 31. 跳跃游戏（LeetCode 55 · 中等）

### 原题

给你一个非负整数数组 nums ，你最初位于数组的 第一个下标 。数组中的每个元素代表你在该位置可以跳跃的最大长度。

判断你是否能够到达最后一个下标，如果可以，返回 true ；否则，返回 false 。

示例 1：

输入：nums = [2,3,1,1,4]
输出：true
解释：可以先跳 1 步，从下标 0 到达下标 1, 然后再从下标 1 跳 3 步到达最后一个下标。

示例 2：

输入：nums = [3,2,1,0,4]
输出：false
解释：无论怎样，总会到达下标为 3 的位置。但该下标的最大跳跃长度是 0 ， 所以永远不可能到达最后一个下标。

提示：

• 1 <= nums.length <= 10⁴

• 0 <= nums[i] <= 10⁵

### Python 题解

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

---


## 32. 合并区间（LeetCode 56 · 中等）

### 原题

以数组 intervals 表示若干个区间的集合，其中单个区间为 intervals[i] = [starti, endi] 。请你合并所有重叠的区间，并返回 一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间 。

示例 1：

输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
解释：区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].

示例 2：

输入：intervals = [[1,4],[4,5]]
输出：[[1,5]]
解释：区间 [1,4] 和 [4,5] 可被视为重叠区间。

示例 3：

输入：intervals = [[4,7],[1,4]]
输出：[[1,7]]
解释：区间 [1,4] 和 [4,7] 可被视为重叠区间。

提示：

• 1 <= intervals.length <= 10⁴

• intervals[i].length == 2

• 0 <= starti <= endi <= 10⁴

### Python 题解

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

---


## 33. 不同路径（LeetCode 62 · 中等）

### 原题

一个机器人位于一个 m x n 网格的左上角 （起始点在下图中标记为 “Start” ）。

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）。

问总共有多少条不同的路径？

示例 1：

输入：m = 3, n = 7
输出：28

示例 2：

输入：m = 3, n = 2
输出：3
解释：
从左上角开始，总共有 3 条路径可以到达右下角。
1. 向右 -> 向下 -> 向下
2. 向下 -> 向下 -> 向右
3. 向下 -> 向右 -> 向下

示例 3：

输入：m = 7, n = 3
输出：28

示例 4：

输入：m = 3, n = 3
输出：6

提示：

• 1 <= m, n <= 100

• 题目数据保证答案小于等于 2 * 10⁹

### Python 题解

```python
class Solution:
    def uniquePaths(self, m, n):
        dp = [1] * n              # 滚动成一行
        for _ in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j - 1]
        return dp[n - 1]
```

---


## 34. 最小路径和（LeetCode 64 · 中等）

### 原题

给定一个包含非负整数的 m x n 网格 grid ，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。

说明：每次只能向下或者向右移动一步。

示例 1：

输入：grid = [[1,3,1],[1,5,1],[4,2,1]]
输出：7
解释：因为路径 1→3→1→1→1 的总和最小。

示例 2：

输入：grid = [[1,2,3],[4,5,6]]
输出：12

提示：

• m == grid.length

• n == grid[i].length

• 1 <= m, n <= 200

• 0 <= grid[i][j] <= 200

### Python 题解

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

---


## 35. 爬楼梯（LeetCode 70 · 简单）

### 原题

假设你正在爬楼梯。需要 n 阶你才能到达楼顶。

每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？

示例 1：

输入：n = 2
输出：2
解释：有两种方法可以爬到楼顶。
1. 1 阶 + 1 阶
2. 2 阶

示例 2：

输入：n = 3
输出：3
解释：有三种方法可以爬到楼顶。
1. 1 阶 + 1 阶 + 1 阶
2. 1 阶 + 2 阶
3. 2 阶 + 1 阶

提示：

• 1 <= n <= 45

### Python 题解

```python
class Solution:
    def climbStairs(self, n):
        a = b = 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
```

---


## 36. 编辑距离（LeetCode 72 · 中等）

### 原题

给你两个单词 word1 和 word2， 请返回将 word1 转换成 word2 所使用的最少操作数 。

你可以对一个单词进行如下三种操作：

• 插入一个字符

• 删除一个字符

• 替换一个字符

示例 1：

输入：word1 = "horse", word2 = "ros"
输出：3
解释：
horse -> rorse (将 'h' 替换为 'r')
rorse -> rose (删除 'r')
rose -> ros (删除 'e')

示例 2：

输入：word1 = "intention", word2 = "execution"
输出：5
解释：
intention -> inention (删除 't')
inention -> enention (将 'i' 替换为 'e')
enention -> exention (将 'n' 替换为 'x')
exention -> exection (将 'n' 替换为 'c')
exection -> execution (插入 'u')

提示：

• 0 <= word1.length, word2.length <= 500

• word1 和 word2 由小写英文字母组成

### Python 题解

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

---


## 37. 矩阵置零（LeetCode 73 · 中等）

### 原题

给定一个 m x n 的矩阵，如果一个元素为 0 ，则将其所在行和列的所有元素都设为 0 。请使用 原地 算法。

示例 1：

输入：matrix = [[1,1,1],[1,0,1],[1,1,1]]
输出：[[1,0,1],[0,0,0],[1,0,1]]

示例 2：

输入：matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
输出：[[0,0,0,0],[0,4,5,0],[0,3,1,0]]

提示：

• m == matrix.length

• n == matrix[0].length

• 1 <= m, n <= 200

• -2³¹ <= matrix[i][j] <= 2³¹ - 1

进阶：

• 一个直观的解决方案是使用 O(mn) 的额外空间，但这并不是一个好的解决方案。

• 一个简单的改进方案是使用 O(m + n) 的额外空间，但这仍然不是最好的解决方案。

• 你能想出一个仅使用常量空间的解决方案吗？

### Python 题解

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

---


## 38. 搜索二维矩阵（LeetCode 74 · 中等）

### 原题

给你一个满足下述两条属性的 m x n 整数矩阵：

• 每行中的整数从左到右按非严格递增顺序排列。

• 每行的第一个整数大于前一行的最后一个整数。

给你一个整数 target ，如果 target 在矩阵中，返回 true ；否则，返回 false 。

你必须编写一个时间复杂度为 O(log(m * n)) 的解决方案。

示例 1：

输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
输出：true

示例 2：

输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
输出：false

提示：

• m == matrix.length

• n == matrix[i].length

• 1 <= m, n <= 100

• -10⁴ <= matrix[i][j], target <= 10⁴

### Python 题解

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

---


## 39. 颜色分类（LeetCode 75 · 中等）

### 原题

给定一个包含红色、白色和蓝色、共 n 个元素的数组 nums ，原地 对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。

我们使用整数 0、 1 和 2 分别表示红色、白色和蓝色。

必须在不使用库内置的 sort 函数的情况下解决这个问题。

示例 1：

输入：nums = [2,0,2,1,1,0]

输出：[0,0,1,1,2,2]

解释：

该数组包含两个 0、两个 1 和两个 2。将它们原地排序后，所有 0 排在最前面，接着是所有 1，最后是所有 2。

示例 2：

输入：nums = [2,0,1]

输出：[0,1,2]

解释：

数组中有且仅有一个 0、一个 1 和一个 2，按 0、1、2 的顺序原地排列。

提示：

• n == nums.length

• 1 <= n <= 300

• nums[i] 为 0、1 或 2

进阶：

• 你能想出一个仅使用常数空间的一趟扫描算法吗？

### Python 题解

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

---


## 40. 最小覆盖子串（LeetCode 76 · 困难）

### 原题

给定两个字符串 s 和 t，长度分别是 m 和 n，返回 s 中的 最短窗口 子串，使得该子串包含 t 中的每一个字符（包括重复字符）。如果没有这样的子串，返回空字符串 ""。

测试用例保证答案唯一。

示例 1：

输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
解释：最小覆盖子串 "BANC" 包含来自字符串 t 的 'A'、'B' 和 'C'。

示例 2：

输入：s = "a", t = "a"
输出："a"
解释：整个字符串 s 是最小覆盖子串。

示例 3:

输入: s = "a", t = "aa"
输出: ""
解释: t 中两个字符 'a' 均应包含在 s 的子串中，
因此没有符合条件的子字符串，返回空字符串。

提示：

• m == s.length

• n == t.length

• 1 <= m, n <= 10⁵

• s 和 t 由英文字母组成

进阶：你能设计一个在 O(m + n) 时间内解决此问题的算法吗？

### Python 题解

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

---


## 41. 子集（LeetCode 78 · 中等）

### 原题

给你一个整数数组 nums ，数组中的元素 互不相同 。返回该数组所有可能的子集（幂集）。

解集 不能 包含重复的子集。你可以按 任意顺序 返回解集。

示例 1：

输入：nums = [1,2,3]
输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

示例 2：

输入：nums = [0]
输出：[[],[0]]

提示：

• 1 <= nums.length <= 10

• -10 <= nums[i] <= 10

• nums 中的所有元素 互不相同

### Python 题解

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

---


## 42. 单词搜索（LeetCode 79 · 中等）

### 原题

给定一个 m x n 二维字符网格 board 和一个字符串单词 word 。如果 word 存在于网格中，返回 true ；否则，返回 false 。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

示例 1：

输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "ABCCED"
输出：true

示例 2：

输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "SEE"
输出：true

示例 3：

输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "ABCB"
输出：false

提示：

• m == board.length

• n = board[i].length

• 1 <= m, n <= 6

• 1 <= word.length <= 15

• board 和 word 仅由大小写英文字母组成

进阶：你可以使用搜索剪枝的技术来优化解决方案，使其在 board 更大的情况下可以更快解决问题？

### Python 题解

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

---


## 43. 柱状图中最大的矩形（LeetCode 84 · 困难）

### 原题

给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。

求在该柱状图中，能够勾勒出来的矩形的最大面积。

示例 1:

输入：heights = [2,1,5,6,2,3]
输出：10
解释：最大的矩形为图中红色区域，面积为 10

示例 2：

输入： heights = [2,4]
输出： 4

提示：

• 1

### Python 题解

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

---


## 44. 二叉树的中序遍历（LeetCode 94 · 简单）

### 原题

给定一个二叉树的根节点 root ，返回 它的 中序 遍历 。

示例 1：

输入：root = [1,null,2,3]
输出：[1,3,2]

示例 2：

输入：root = []
输出：[]

示例 3：

输入：root = [1]
输出：[1]

提示：

• 树中节点数目在范围 [0, 100] 内

• -100 <= Node.val <= 100

进阶: 递归算法很简单，你可以通过迭代算法完成吗？

### Python 题解

```python
class Solution:
    def inorderTraversal(self, root):
        res = []
        def dfs(node):
            if node is None:
                return
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)
        dfs(root)
        return res
```

---


## 45. 验证二叉搜索树（LeetCode 98 · 中等）

### 原题

给你一个二叉树的根节点 root ，判断其是否是一个有效的二叉搜索树。

有效 二叉搜索树定义如下：

• 节点的左子树只包含 严格小于 当前节点的数。

• 节点的右子树只包含 严格大于 当前节点的数。

• 所有左子树和右子树自身必须也是二叉搜索树。

示例 1：

输入：root = [2,1,3]
输出：true

示例 2：

输入：root = [5,1,4,null,null,3,6]
输出：false
解释：根节点的值是 5 ，但是右子节点的值是 4 。

提示：

• 树中节点数目范围在[1, 10⁴] 内

• -2³¹ <= Node.val <= 2³¹ - 1

### Python 题解

```python
class Solution:
    def isValidBST(self, root):
        def dfs(node, lo, hi):
            if node is None:
                return True
            if not (lo < node.val < hi):
                return False
            return dfs(node.left, lo, node.val) and dfs(node.right, node.val, hi)
        return dfs(root, float("-inf"), float("inf"))
```

---


## 46. 对称二叉树（LeetCode 101 · 简单）

### 原题

给你一个二叉树的根节点 root ， 检查它是否轴对称。

示例 1：

输入：root = [1,2,2,3,4,4,3]
输出：true

示例 2：

输入：root = [1,2,2,null,3,null,3]
输出：false

提示：

• 树中节点数目在范围 [1, 1000] 内

• -100 <= Node.val <= 100

进阶：你可以运用递归和迭代两种方法解决这个问题吗？

### Python 题解

```python
class Solution:
    def isSymmetric(self, root):
        def same(a, b):
            if a is None and b is None:
                return True
            if a is None or b is None:
                return False
            return a.val == b.val and same(a.left, b.right) and same(a.right, b.left)
        return root is None or same(root.left, root.right)
```

---


## 47. 二叉树的层序遍历（LeetCode 102 · 中等）

### 原题

给你二叉树的根节点 root ，返回其节点值的 层序遍历 。 （即逐层地，从左到右访问所有节点）。

示例 1：

输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]

示例 2：

输入：root = [1]
输出：[[1]]

示例 3：

输入：root = []
输出：[]

提示：

• 树中节点数目在范围 [0, 2000] 内

• -1000 <= Node.val <= 1000

### Python 题解

```python
from collections import deque

class Solution:
    def levelOrder(self, root):
        if root is None:
            return []
        q = deque([root])
        res = []
        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                if node.left is not None:
                    q.append(node.left)
                if node.right is not None:
                    q.append(node.right)
            res.append(level)
        return res
```

---


## 48. 二叉树的最大深度（LeetCode 104 · 简单）

### 原题

给定一个二叉树 root ，返回其最大深度。

二叉树的 最大深度 是指从根节点到最远叶子节点的最长路径上的节点数。

示例 1：

输入：root = [3,9,20,null,null,15,7]
输出：3

示例 2：

输入：root = [1,null,2]
输出：2

提示：

• 树中节点的数量在 [0, 10⁴] 区间内。

• -100 <= Node.val <= 100

### Python 题解

```python
class Solution:
    def maxDepth(self, root):
        if root is None:
            return 0
        return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1
```

---


## 49. 从前序与中序遍历序列构造二叉树（LeetCode 105 · 中等）

### 原题

给定两个整数数组 preorder 和 inorder ，其中 preorder 是二叉树的先序遍历， inorder 是同一棵树的中序遍历，请构造二叉树并返回其根节点。

示例 1:

输入: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
输出: [3,9,20,null,null,15,7]

示例 2:

输入: preorder = [-1], inorder = [-1]
输出: [-1]

提示:

• 1 <= preorder.length <= 3000

• inorder.length == preorder.length

• -3000 <= preorder[i], inorder[i] <= 3000

• preorder 和 inorder 均 无重复 元素

• inorder 均出现在 preorder

• preorder 保证 为二叉树的前序遍历序列

• inorder 保证 为二叉树的中序遍历序列

### Python 题解

```python
class Solution:
    def buildTree(self, preorder, inorder):
        idx = {v: i for i, v in enumerate(inorder)}
        def build(pl, pr, il, ir):
            if pl > pr:
                return None
            v = preorder[pl]
            k = idx[v]
            left_len = k - il
            root = TreeNode(v)
            root.left = build(pl + 1, pl + left_len, il, k - 1)
            root.right = build(pl + left_len + 1, pr, k + 1, ir)
            return root
        return build(0, len(preorder) - 1, 0, len(inorder) - 1)
```

---


## 50. 将有序数组转换为二叉搜索树（LeetCode 108 · 简单）

### 原题

给你一个整数数组 nums ，其中元素已经按 升序 排列，请你将其转换为一棵 平衡 二叉搜索树。

示例 1：

输入：nums = [-10,-3,0,5,9]
输出：[0,-3,9,-10,null,5]
解释：[0,-10,5,null,-3,null,9] 也将被视为正确答案：

示例 2：

输入：nums = [1,3]
输出：[3,1]
解释：[1,null,3] 和 [3,1] 都是高度平衡二叉搜索树。

提示：

• 1 <= nums.length <= 10⁴

• -10⁴ <= nums[i] <= 10⁴

• nums 按 严格递增 顺序排列

### Python 题解

```python
class Solution:
    def sortedArrayToBST(self, nums):
        def build(l, r):
            if l > r:
                return None
            mid = (l + r) // 2
            root = TreeNode(nums[mid])
            root.left = build(l, mid - 1)
            root.right = build(mid + 1, r)
            return root
        return build(0, len(nums) - 1)
```

---


## 51. 二叉树展开为链表（LeetCode 114 · 中等）

### 原题

给你二叉树的根结点 root ，请你将它展开为一个单链表：

• 展开后的单链表应该同样使用 TreeNode ，其中 right 子指针指向链表中下一个结点，而左子指针始终为 null 。

• 展开后的单链表应该与二叉树 先序遍历 顺序相同。

示例 1：

输入：root = [1,2,5,3,4,null,6]
输出：[1,null,2,null,3,null,4,null,5,null,6]

示例 2：

输入：root = []
输出：[]

示例 3：

输入：root = [0]
输出：[0]

提示：

• 树中结点数在范围 [0, 2000] 内

• -100

进阶：你可以使用原地算法（O(1) 额外空间）展开这棵树吗？

### Python 题解

```python
class Solution:
    def flatten(self, root):
        cur = root
        while cur is not None:
            if cur.left is not None:
                pre = cur.left
                while pre.right is not None:
                    pre = pre.right
                pre.right = cur.right
                cur.right = cur.left
                cur.left = None
            cur = cur.right
```

---


## 52. 杨辉三角（LeetCode 118 · 简单）

### 原题

给定一个非负整数 numRows。

返回「杨辉三角」的前 numRows 行。

在「杨辉三角」中，每个数是它左上方和右上方的数的和。

示例 1:

输入: numRows = 5
输出: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]

示例 2:

输入: numRows = 1
输出: [[1]]

提示:

• 1 <= numRows <= 30

### Python 题解

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

---


## 53. 买卖股票的最佳时机（LeetCode 121 · 简单）

### 原题

给定一个数组 prices ，它的第 i 个元素 prices[i] 表示一支给定股票第 i 天的价格。

你只能选择 某一天 买入这只股票，并选择在 未来的某一个不同的日子 卖出该股票。设计一个算法来计算你所能获取的最大利润。

返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 0 。

示例 1：

输入：[7,1,5,3,6,4]
输出：5
解释：在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格；同时，你不能在买入前卖出股票。

示例 2：

输入：prices = [7,6,4,3,1]
输出：0
解释：在这种情况下, 没有交易完成, 所以最大利润为 0。

提示：

• 1

### Python 题解

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

---


## 54. 二叉树中的最大路径和（LeetCode 124 · 困难）

### 原题

二叉树中的 路径 被定义为一条节点序列，序列中每对相邻节点之间都存在一条边。同一个节点在一条路径序列中 至多出现一次 。该路径 至少包含一个 节点，且不一定经过根节点。

路径和 是路径中各节点值的总和。

给你一个二叉树的根节点 root ，返回其 最大路径和 。

示例 1：

输入：root = [1,2,3]
输出：6
解释：最优路径是 2 -> 1 -> 3 ，路径和为 2 + 1 + 3 = 6

示例 2：

输入：root = [-10,9,20,null,null,15,7]
输出：42
解释：最优路径是 15 -> 20 -> 7 ，路径和为 15 + 20 + 7 = 42

提示：

• 树中节点数目范围是 [1, 3 * 10⁴]

• -1000 <= Node.val <= 1000

### Python 题解

```python
class Solution:
    def maxPathSum(self, root):
        self.ans = float("-inf")
        def dfs(node):
            if node is None:
                return 0
            l = max(0, dfs(node.left))
            r = max(0, dfs(node.right))
            self.ans = max(self.ans, node.val + l + r)
            return node.val + max(l, r)
        dfs(root)
        return self.ans
```

---


## 55. 最长连续序列（LeetCode 128 · 中等）

### 原题

给定一个未排序的整数数组 nums ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。

请你设计并实现时间复杂度为 O(n) 的算法解决此问题。

示例 1：

输入：nums = [100,4,200,1,3,2]
输出：4
解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。

示例 2：

输入：nums = [0,3,7,2,5,8,4,6,0,1]
输出：9

示例 3：

输入：nums = [1,0,1,2]
输出：3

提示：

• 0 <= nums.length <= 10⁵

• -10⁹ <= nums[i] <= 10⁹

### Python 题解

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

---


## 56. 分割回文串（LeetCode 131 · 中等）

### 原题

给你一个字符串 s，请你将 s 分割成一些 子串，使每个子串都是 回文串 。返回 s 所有可能的分割方案。

示例 1：

输入：s = "aab"
输出：[["a","a","b"],["aa","b"]]

示例 2：

输入：s = "a"
输出：[["a"]]

提示：

• 1 <= s.length <= 16

• s 仅由小写英文字母组成

### Python 题解

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

---


## 57. 只出现一次的数字（LeetCode 136 · 简单）

### 原题

给你一个 非空 整数数组 nums ，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。

你必须设计并实现线性时间复杂度的算法来解决此问题，且该算法只使用常量额外空间。

示例 1 ：

输入：nums = [2,2,1]

输出：1

示例 2 ：

输入：nums = [4,1,2,1,2]

输出：4

示例 3 ：

输入：nums = [1]

输出：1

提示：

• 1 <= nums.length <= 3 * 10⁴

• -3 * 10⁴ <= nums[i] <= 3 * 10⁴

• 除了某个元素只出现一次以外，其余每个元素均出现两次。

### Python 题解

```python
class Solution:
    def singleNumber(self, nums):
        ans = 0
        for x in nums:
            ans ^= x
        return ans
```

---


## 58. 随机链表的复制（LeetCode 138 · 中等）

### 原题

给你一个长度为 n 的链表，每个节点包含一个额外增加的随机指针 random ，该指针可以指向链表中的任何节点或空节点。

构造这个链表的 深拷贝。 深拷贝应该正好由 n 个 全新 节点组成，其中每个新节点的值都设为其对应的原节点的值。新节点的 next 指针和 random 指针也都应指向复制链表中的新节点，并使原链表和复制链表中的这些指针能够表示相同的链表状态。复制链表中的指针都不应指向原链表中的节点 。

例如，如果原链表中有 X 和 Y 两个节点，其中 X.random --> Y 。那么在复制链表中对应的两个节点 x 和 y ，同样有 x.random --> y 。

返回复制链表的头节点。

用一个由 n 个节点组成的链表来表示输入/输出中的链表。每个节点用一个 [val, random_index] 表示：

• val：一个表示 Node.val 的整数。

• random_index：随机指针指向的节点索引（范围从 0 到 n-1）；如果不指向任何节点，则为 null 。

你的代码 只 接受原链表的头节点 head 作为传入参数。

示例 1：

输入：head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
输出：[[7,null],[13,0],[11,4],[10,2],[1,0]]

示例 2：

输入：head = [[1,1],[2,1]]
输出：[[1,1],[2,1]]

示例 3：

输入：head = [[3,null],[3,0],[3,null]]
输出：[[3,null],[3,0],[3,null]]

提示：

• 0 <= n <= 1000

• -10⁴ <= Node.val <= 10⁴

• Node.random 为 null 或指向链表中的节点。

### Python 题解

```python
class Solution:
    def copyRandomList(self, head):
        if head is None:
            return None
        d = {None: None}
        cur = head
        while cur is not None:
            d[cur] = Node(cur.val)      # Node 是平台定义的类型
            cur = cur.next
        cur = head
        while cur is not None:
            d[cur].next = d[cur.next]
            d[cur].random = d[cur.random]
            cur = cur.next
        return d[head]
```

---


## 59. 单词拆分（LeetCode 139 · 中等）

### 原题

给你一个字符串 s 和一个字符串列表 wordDict 作为字典。如果可以利用字典中出现的一个或多个单词拼接出 s 则返回 true。

注意：不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用。

示例 1：

输入: s = "leetcode", wordDict = ["leet", "code"]
输出: true
解释: 返回 true 因为 "leetcode" 可以由 "leet" 和 "code" 拼接成。

示例 2：

输入: s = "applepenapple", wordDict = ["apple", "pen"]
输出: true
解释: 返回 true 因为 "applepenapple" 可以由 "apple" "pen" "apple" 拼接成。
注意，你可以重复使用字典中的单词。

示例 3：

输入: s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
输出: false

提示：

• 1 <= s.length <= 300

• 1 <= wordDict.length <= 1000

• 1 <= wordDict[i].length <= 20

• s 和 wordDict[i] 仅由小写英文字母组成

• wordDict 中的所有字符串 互不相同

### Python 题解

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

---


## 60. 环形链表（LeetCode 141 · 简单）

### 原题

给你一个链表的头节点 head ，判断链表中是否有环。

如果链表中有某个节点，可以通过连续跟踪 next 指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。注意：pos 不作为参数进行传递 。仅仅是为了标识链表的实际情况。

如果链表中存在环 ，则返回 true 。 否则，返回 false 。

示例 1：

输入：head = [3,2,0,-4], pos = 1
输出：true
解释：链表中有一个环，其尾部连接到第二个节点。

示例 2：

输入：head = [1,2], pos = 0
输出：true
解释：链表中有一个环，其尾部连接到第一个节点。

示例 3：

输入：head = [1], pos = -1
输出：false
解释：链表中没有环。

提示：

• 链表中节点的数目范围是 [0, 10⁴]

• -10⁵ <= Node.val <= 10⁵

• pos 为 -1 或者链表中的一个 有效索引 。

进阶：你能用 O(1)（即，常量）内存解决此问题吗？

### Python 题解

```python
class Solution:
    def hasCycle(self, head):
        slow = fast = head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False
```

---


## 61. 环形链表 II（LeetCode 142 · 中等）

### 原题

给定一个链表的头节点 head ，返回链表开始入环的第一个节点。 如果链表无环，则返回 null。

如果链表中有某个节点，可以通过连续跟踪 next 指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。如果 pos 是 -1，则在该链表中没有环。注意：pos 不作为参数进行传递，仅仅是为了标识链表的实际情况。

不允许修改 链表。

示例 1：

输入：head = [3,2,0,-4], pos = 1
输出：返回索引为 1 的链表节点
解释：链表中有一个环，其尾部连接到第二个节点。

示例 2：

输入：head = [1,2], pos = 0
输出：返回索引为 0 的链表节点
解释：链表中有一个环，其尾部连接到第一个节点。

示例 3：

输入：head = [1], pos = -1
输出：返回 null
解释：链表中没有环。

提示：

• 链表中节点的数目范围在范围 [0, 10⁴] 内

• -10⁵ <= Node.val <= 10⁵

• pos 的值为 -1 或者链表中的一个有效索引

进阶：你是否可以使用 O(1) 空间解决此题？

### Python 题解

```python
class Solution:
    def detectCycle(self, head):
        slow = fast = head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                p = head
                while p is not slow:
                    p = p.next
                    slow = slow.next
                return p
        return None
```

---


## 62. LRU 缓存（LeetCode 146 · 中等）

### 原题

请你设计并实现一个满足 LRU (最近最少使用) 缓存 约束的数据结构。

实现 LRUCache 类：

• LRUCache(int capacity) 以 正整数 作为容量 capacity 初始化 LRU 缓存

• int get(int key) 如果关键字 key 存在于缓存中，则返回关键字的值，否则返回 -1 。

• void put(int key, int value) 如果关键字 key 已经存在，则变更其数据值 value ；如果不存在，则向缓存中插入该组 key-value 。如果插入操作导致关键字数量超过 capacity ，则应该 逐出 最久未使用的关键字。

函数 get 和 put 必须以 O(1) 的平均时间复杂度运行。

示例：

输入
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
输出
[null, null, null, 1, null, -1, null, -1, 3, 4]

解释
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // 缓存是 {1=1}
lRUCache.put(2, 2); // 缓存是 {1=1, 2=2}
lRUCache.get(1); // 返回 1
lRUCache.put(3, 3); // 该操作会使得关键字 2 作废，缓存是 {1=1, 3=3}
lRUCache.get(2); // 返回 -1 (未找到)
lRUCache.put(4, 4); // 该操作会使得关键字 1 作废，缓存是 {4=4, 3=3}
lRUCache.get(1); // 返回 -1 (未找到)
lRUCache.get(3); // 返回 3
lRUCache.get(4); // 返回 4

提示：

• 1 <= capacity <= 3000

• 0 <= key <= 10000

• 0 <= value <= 10⁵

• 最多调用 2 * 10⁵ 次 get 和 put

### Python 题解

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.d = OrderedDict()
        self.cap = capacity

    def get(self, key):
        if key not in self.d:
            return -1
        self.d.move_to_end(key)
        return self.d[key]

    def put(self, key, value):
        if key in self.d:
            self.d.move_to_end(key)
        self.d[key] = value
        if len(self.d) > self.cap:
            self.d.popitem(last=False)
```

---


## 63. 排序链表（LeetCode 148 · 中等）

### 原题

给你链表的头结点 head ，请将其按 升序 排列并返回 排序后的链表 。

示例 1：

输入：head = [4,2,1,3]
输出：[1,2,3,4]

示例 2：

输入：head = [-1,5,3,4,0]
输出：[-1,0,3,4,5]

示例 3：

输入：head = []
输出：[]

提示：

• 链表中节点的数目在范围 [0, 5 * 10⁴] 内

• -10⁵ <= Node.val <= 10⁵

进阶：你可以在 O(n log n) 时间复杂度和常数级空间复杂度下，对链表进行排序吗？

### Python 题解

```python
class Solution:
    def sortList(self, head):
        if head is None or head.next is None:
            return head
        slow = fast = head
        prev = None
        while fast is not None and fast.next is not None:
            prev = slow
            slow = slow.next
            fast = fast.next.next
        prev.next = None                # 断成两半
        left = self.sortList(head)
        right = self.sortList(slow)
        return self.merge(left, right)

    def merge(self, l1, l2):
        dummy = cur = ListNode(0)
        while l1 is not None and l2 is not None:
            if l1.val <= l2.val:
                cur.next, l1 = l1, l1.next
            else:
                cur.next, l2 = l2, l2.next
            cur = cur.next
        cur.next = l1 if l1 is not None else l2
        return dummy.next
```

---


## 64. 乘积最大子数组（LeetCode 152 · 中等）

### 原题

给你一个整数数组 nums ，请你找出数组中乘积最大的非空连续 子数组（该子数组中至少包含一个数字），并返回该子数组所对应的乘积。

测试用例的答案是一个 32-位 整数。

请注意，一个只包含一个元素的数组的乘积是这个元素的值。

示例 1:

输入: nums = [2,3,-2,4]
输出: 6
解释: 子数组 [2,3] 有最大乘积 6。

示例 2:

输入: nums = [-2,0,-1]
输出: 0
解释: 结果不能为 2, 因为 [-2,-1] 不是子数组。

提示:

• 1 <= nums.length <= 2 * 10⁴

• -10 <= nums[i] <= 10

• nums 的任何子数组的乘积都 保证 是一个 32-位 整数

### Python 题解

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

---


## 65. 寻找旋转排序数组中的最小值（LeetCode 153 · 中等）

### 原题

已知一个长度为 n 的数组，预先按照升序排列，经由 1 到 n 次 旋转 后，得到输入数组。例如，原数组 nums = [0,1,2,4,5,6,7] 在变化后可能得到：

• 若旋转 4 次，则可以得到 [4,5,6,7,0,1,2]

• 若旋转 7 次，则可以得到 [0,1,2,4,5,6,7]

注意，数组 [a[0], a[1], a[2], ..., a[n-1]] 旋转一次 的结果为数组 [a[n-1], a[0], a[1], a[2], ..., a[n-2]] 。

给你一个元素值 互不相同 的数组 nums ，它原来是一个升序排列的数组，并按上述情形进行了多次旋转。请你找出并返回数组中的 最小元素 。

你必须设计一个时间复杂度为 O(log n) 的算法解决此问题。

示例 1：

输入：nums = [3,4,5,1,2]
输出：1
解释：原数组为 [1,2,3,4,5] ，旋转 3 次得到输入数组。

示例 2：

输入：nums = [4,5,6,7,0,1,2]
输出：0
解释：原数组为 [0,1,2,4,5,6,7] ，旋转 4 次得到输入数组。

示例 3：

输入：nums = [11,13,15,17]
输出：11
解释：原数组为 [11,13,15,17] ，旋转 4 次得到输入数组。

提示：

• n == nums.length

• 1 <= n <= 5000

• -5000 <= nums[i] <= 5000

• nums 中的所有整数 互不相同

• nums 原来是一个升序排序的数组，并进行了 1 至 n 次旋转

### Python 题解

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

---


## 66. 最小栈（LeetCode 155 · 中等）

### 原题

设计一个支持 push ，pop ，top 操作，并能在常数时间内检索到最小元素的栈。

实现 MinStack 类:

• MinStack() 初始化堆栈对象。

• void push(int value) 将元素 value 推入堆栈。

• void pop() 删除堆栈顶部的元素。

• int top() 获取堆栈顶部的元素。

• int getMin() 获取堆栈中的最小元素。

示例 1:

输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

输出：
[null,null,null,null,-3,null,0,-2]

解释：
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); --> 返回 -3.
minStack.pop();
minStack.top(); --> 返回 0.
minStack.getMin(); --> 返回 -2.

提示：

• -2³¹ <= val <= 2³¹ - 1

• pop、top 和 getMin 操作总是在 非空栈 上调用

• push, pop, top, and getMin最多被调用 3 * 10⁴ 次

### Python 题解

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

---


## 67. 相交链表（LeetCode 160 · 简单）

### 原题

给你两个单链表的头节点 headA 和 headB ，请你找出并返回两个单链表相交的起始节点。如果两个链表不存在相交节点，返回 null 。

图示两个链表在节点 c1 开始相交：

题目数据 保证 整个链式结构中不存在环。

注意，函数返回结果后，链表必须 保持其原始结构 。

自定义评测：

评测系统 的输入如下（你设计的程序 不适用 此输入）：

• intersectVal - 相交的起始节点的值。如果不存在相交节点，这一值为 0

• listA - 第一个链表

• listB - 第二个链表

• skipA - 在 listA 中（从头节点开始）跳到交叉节点的节点数

• skipB - 在 listB 中（从头节点开始）跳到交叉节点的节点数

评测系统将根据这些输入创建链式数据结构，并将两个头节点 headA 和 headB 传递给你的程序。如果程序能够正确返回相交节点，那么你的解决方案将被 视作正确答案 。

示例 1：

输入：intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA = 2, skipB = 3
输出：Intersected at '8'
解释：相交节点的值为 8 （注意，如果两个链表相交则不能为 0）。
从各自的表头开始算起，链表 A 为 [4,1,8,4,5]，链表 B 为 [5,6,1,8,4,5]。
在 A 中，相交节点前有 2 个节点；在 B 中，相交节点前有 3 个节点。
— 请注意相交节点的值不为 1，因为在链表 A 和链表 B 之中值为 1 的节点 (A 中第二个节点和 B 中第三个节点) 是不同的节点。换句话说，它们在内存中指向两个不同的位置，而链表 A 和链表 B 中值为 8 的节点 (A 中第三个节点，B 中第四个节点) 在内存中指向相同的位置。

示例 2：

输入：intersectVal = 2, listA = [1,9,1,2,4], listB = [3,2,4], skipA = 3, skipB = 1
输出：Intersected at '2'
解释：相交节点的值为 2 （注意，如果两个链表相交则不能为 0）。
从各自的表头开始算起，链表 A 为 [1,9,1,2,4]，链表 B 为 [3,2,4]。
在 A 中，相交节点前有 3 个节点；在 B 中，相交节点前有 1 个节点。

示例 3：

输入：intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB = 2
输出：No intersection
解释：从各自的表头开始算起，链表 A 为 [2,6,4]，链表 B 为 [1,5]。
由于这两个链表不相交，所以 intersectVal 必须为 0，而 skipA 和 skipB 可以是任意值。
这两个链表不相交，因此返回 null 。

提示：

• listA 中节点数目为 m

• listB 中节点数目为 n

• 1 <= m, n <= 3 * 10⁴

• 1 <= Node.val <= 10⁵

• 0 <= skipA <= m

• 0 <= skipB <= n

• 如果 listA 和 listB 没有交点，intersectVal 为 0

• 如果 listA 和 listB 有交点，intersectVal == listA[skipA] == listB[skipB]

进阶：你能否设计一个时间复杂度 O(m + n) 、仅用 O(1) 内存的解决方案？

### Python 题解

```python
class Solution:
    def getIntersectionNode(self, headA, headB):
        a, b = headA, headB
        while a != b:
            a = a.next if a is not None else headB
            b = b.next if b is not None else headA
        return a
```

---


## 68. 多数元素（LeetCode 169 · 简单）

### 原题

给定一个大小为 n 的数组 nums ，返回其中的多数元素。多数元素是指在数组中出现次数 大于 ⌊ n/2 ⌋ 的元素。

你可以假设数组是非空的，并且给定的数组总是存在多数元素。

示例 1：

输入：nums = [3,2,3]
输出：3

示例 2：

输入：nums = [2,2,1,1,1,2,2]
输出：2

提示：

• n == nums.length

• 1 <= n <= 5 * 10⁴

• -10⁹ <= nums[i] <= 10⁹

• 输入保证数组中一定有一个多数元素。

进阶：尝试设计时间复杂度为 O(n)、空间复杂度为 O(1) 的算法解决此问题。

### Python 题解

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

---


## 69. 轮转数组（LeetCode 189 · 中等）

### 原题

给定一个整数数组 nums，将数组中的元素向右轮转 k 个位置，其中 k 是非负数。

示例 1:

输入: nums = [1,2,3,4,5,6,7], k = 3
输出: [5,6,7,1,2,3,4]
解释:
向右轮转 1 步: [7,1,2,3,4,5,6]
向右轮转 2 步: [6,7,1,2,3,4,5]
向右轮转 3 步: [5,6,7,1,2,3,4]

示例 2:

输入：nums = [-1,-100,3,99], k = 2
输出：[3,99,-1,-100]
解释:
向右轮转 1 步: [99,-1,-100,3]
向右轮转 2 步: [3,99,-1,-100]

提示：

• 1 <= nums.length <= 10⁵

• -2³¹ <= nums[i] <= 2³¹ - 1

• 0 <= k <= 10⁵

进阶：

• 尽可能想出更多的解决方案，至少有 三种 不同的方法可以解决这个问题。

• 你可以使用空间复杂度为 O(1) 的 原地 算法解决这个问题吗？

### Python 题解

```python
class Solution:
    def rotate(self, nums, k):
        n = len(nums)
        k %= n
        nums[:] = nums[-k:] + nums[:-k]
```

---


## 70. 打家劫舍（LeetCode 198 · 中等）

### 原题

你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。

给定一个代表每个房屋存放金额的非负整数数组，计算你 不触动警报装置的情况下 ，一夜之内能够偷窃到的最高金额。

示例 1：

输入：[1,2,3,1]
输出：4
解释：偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
偷窃到的最高金额 = 1 + 3 = 4 。

示例 2：

输入：[2,7,9,3,1]
输出：12
解释：偷窃 1 号房屋 (金额 = 2), 偷窃 3 号房屋 (金额 = 9)，接着偷窃 5 号房屋 (金额 = 1)。
偷窃到的最高金额 = 2 + 9 + 1 = 12 。

提示：

• 1

### Python 题解

```python
class Solution:
    def rob(self, nums):
        prev2 = prev1 = 0        # dp[i-2], dp[i-1]
        for x in nums:
            prev2, prev1 = prev1, max(prev1, prev2 + x)
        return prev1
```

---


## 71. 二叉树的右视图（LeetCode 199 · 中等）

### 原题

给定一个二叉树的 根节点 root，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。

示例 1：

输入：root = [1,2,3,null,5,null,4]

输出：[1,3,4]

解释：

示例 2：

输入：root = [1,2,3,4,null,null,null,5]

输出：[1,3,4,5]

解释：

示例 3：

输入：root = [1,null,3]

输出：[1,3]

示例 4：

输入：root = []

输出：[]

提示:

• 二叉树的节点个数的范围是 [0,100]

• -100 <= Node.val <= 100

### Python 题解

```python
from collections import deque

class Solution:
    def rightSideView(self, root):
        if root is None:
            return []
        q = deque([root])
        res = []
        while q:
            res.append(q[-1].val)
            for _ in range(len(q)):
                node = q.popleft()
                if node.left is not None:
                    q.append(node.left)
                if node.right is not None:
                    q.append(node.right)
        return res
```

---


## 72. 岛屿数量（LeetCode 200 · 中等）

### 原题

给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

此外，你可以假设该网格的四条边均被水包围。

示例 1：

输入：grid = [
['1','1','1','1','0'],
['1','1','0','1','0'],
['1','1','0','0','0'],
['0','0','0','0','0']
]
输出：1

示例 2：

输入：grid = [
['1','1','0','0','0'],
['1','1','0','0','0'],
['0','0','1','0','0'],
['0','0','0','1','1']
]
输出：3

提示：

• m == grid.length

• n == grid[i].length

• 1 <= m, n <= 300

• grid[i][j] 的值为 '0' 或 '1'

### Python 题解

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

---


## 73. 反转链表（LeetCode 206 · 简单）

### 原题

给你单链表的头节点 head ，请你反转链表，并返回反转后的链表。

示例 1：

输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]

示例 2：

输入：head = [1,2]
输出：[2,1]

示例 3：

输入：head = []
输出：[]

提示：

• 链表中节点的数目范围是 [0, 5000]

• -5000

进阶：链表可以选用迭代或递归方式完成反转。你能否用两种方法解决这道题？

### Python 题解

```python
class Solution:
    def reverseList(self, head):
        pre = None
        cur = head
        while cur is not None:
            nxt = cur.next      # 必须先存，改完就找不回来了
            cur.next = pre
            pre, cur = cur, nxt
        return pre              # 循环结束时 pre 是新头
```

---


## 74. 课程表（LeetCode 207 · 中等）

### 原题

你这个学期必须选修 numCourses 门课程，记为 0 到 numCourses - 1 。

在选修某些课程之前需要一些先修课程。 先修课程按数组 prerequisites 给出，其中 prerequisites[i] = [ai, bi] ，表示如果要学习课程 ai 则 必须 先学习课程 bi 。

• 例如，先修课程对 [0, 1] 表示：想要学习课程 0 ，你需要先完成课程 1 。

请你判断是否可能完成所有课程的学习？如果可以，返回 true ；否则，返回 false 。

示例 1：

输入：numCourses = 2, prerequisites = [[1,0]]
输出：true
解释：总共有 2 门课程。学习课程 1 之前，你需要完成课程 0 。这是可能的。

示例 2：

输入：numCourses = 2, prerequisites = [[1,0],[0,1]]
输出：false
解释：总共有 2 门课程。学习课程 1 之前，你需要先完成​课程 0 ；并且学习课程 0 之前，你还应先完成课程 1 。这是不可能的。

提示：

• 1 <= numCourses <= 2000

• 0 <= prerequisites.length <= 5000

• prerequisites[i].length == 2

• 0 <= ai, bi < numCourses

• prerequisites[i] 中的所有课程对 互不相同

### Python 题解

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

---


## 75. 实现 Trie（LeetCode 208 · 中等）

### 原题

Trie（发音类似 "try"）或者说 前缀树 是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。这一数据结构有相当多的应用情景，例如自动补全和拼写检查。

请你实现 Trie 类：

• Trie() 初始化前缀树对象。

• void insert(String word) 向前缀树中插入字符串 word 。

• boolean search(String word) 如果字符串 word 在前缀树中，返回 true（即，在检索之前已经插入）；否则，返回 false 。

• boolean startsWith(String prefix) 如果之前已经插入的字符串 word 的前缀之一为 prefix ，返回 true ；否则，返回 false 。

示例：

输入
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
输出
[null, null, true, false, true, null, true]

解释
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple"); // 返回 True
trie.search("app"); // 返回 False
trie.startsWith("app"); // 返回 True
trie.insert("app");
trie.search("app"); // 返回 True

提示：

• 1 <= word.length, prefix.length <= 2000

• word 和 prefix 仅由小写英文字母组成

• insert、search 和 startsWith 调用次数 总计 不超过 3 * 10⁴ 次

### Python 题解

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

---


## 76. 数组中的第 K 个最大元素（LeetCode 215 · 中等）

### 原题

给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。

请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。

你必须设计并实现时间复杂度为 O(n) 的算法解决此问题。

示例 1:

输入: [3,2,1,5,6,4], k = 2
输出: 5

示例 2:

输入: [3,2,3,1,2,4,5,5,6], k = 4
输出: 4

提示：

• 1 <= k <= nums.length <= 10⁵

• -10⁴ <= nums[i] <= 10⁴

### Python 题解

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

---


## 77. 翻转二叉树（LeetCode 226 · 简单）

### 原题

给你一棵二叉树的根节点 root ，翻转这棵二叉树，并返回其根节点。

示例 1：

输入：root = [4,2,7,1,3,6,9]
输出：[4,7,2,9,6,3,1]

示例 2：

输入：root = [2,1,3]
输出：[2,3,1]

示例 3：

输入：root = []
输出：[]

提示：

• 树中节点数目范围在 [0, 100] 内

• -100 <= Node.val <= 100

### Python 题解

```python
class Solution:
    def invertTree(self, root):
        if root is None:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
```

---


## 78. 二叉搜索树中第 K 小的元素（LeetCode 230 · 中等）

### 原题

给定一个二叉搜索树的根节点 root ，和一个整数 k ，请你设计一个算法查找其中第 k 小的元素（k 从 1 开始计数）。

示例 1：

输入：root = [3,1,4,null,2], k = 1
输出：1

示例 2：

输入：root = [5,3,6,2,4,null,null,1], k = 3
输出：3

提示：

• 树中的节点数为 n 。

• 1 <= k <= n <= 10⁴

• 0 <= Node.val <= 10⁴

进阶：如果二叉搜索树经常被修改（插入/删除操作）并且你需要频繁地查找第 k 小的值，你将如何优化算法？

### Python 题解

```python
class Solution:
    def kthSmallest(self, root, k):
        self.k = k
        self.ans = None
        def dfs(node):
            if node is None or self.ans is not None:
                return
            dfs(node.left)
            self.k -= 1
            if self.k == 0:
                self.ans = node.val
                return
            dfs(node.right)
        dfs(root)
        return self.ans
```

---


## 79. 回文链表（LeetCode 234 · 简单）

### 原题

给你一个单链表的头节点 head ，请你判断该链表是否为回文链表。如果是，返回 true ；否则，返回 false 。

示例 1：

输入：head = [1,2,2,1]
输出：true

示例 2：

输入：head = [1,2]
输出：false

提示：

• 链表中节点数目在范围[1, 10⁵] 内

• 0 <= Node.val <= 9

进阶：你能否用 O(n) 时间复杂度和 O(1) 空间复杂度解决此题？

### Python 题解

```python
class Solution:
    def isPalindrome(self, head):
        slow = fast = head
        while fast is not None and fast.next is not None:
            slow, fast = slow.next, fast.next.next
        pre, cur = None, slow
        while cur is not None:
            nxt = cur.next
            cur.next = pre
            pre, cur = cur, nxt
        while pre is not None:
            if pre.val != head.val:
                return False
            pre, head = pre.next, head.next
        return True
```

---


## 80. 二叉树的最近公共祖先（LeetCode 236 · 中等）

### 原题

给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

示例 1：

输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出：3
解释：节点 5 和节点 1 的最近公共祖先是节点 3 。

示例 2：

输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
输出：5
解释：节点 5 和节点 4 的最近公共祖先是节点 5 。因为根据定义最近公共祖先节点可以为节点本身。

示例 3：

输入：root = [1,2], p = 1, q = 2
输出：1

提示：

• 树中节点数目在范围 [2, 10⁵] 内。

• -10⁹

### Python 题解

```python
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if root is None or root is p or root is q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left is not None and right is not None:
            return root
        return left if left is not None else right
```

---


## 81. 除自身以外数组的乘积（LeetCode 238 · 中等）

### 原题

给你一个整数数组 nums，返回 数组 answer ，其中 answer[i] 等于 nums 中除了 nums[i] 之外其余各元素的乘积 。

题目数据 保证 数组 nums之中任意元素的全部前缀元素和后缀的乘积都在 32 位 整数范围内。

请 不要使用除法，且在 O(n) 时间复杂度内完成此题。

示例 1:

输入: nums = [1,2,3,4]
输出: [24,12,8,6]

示例 2:

输入: nums = [-1,1,0,-3,3]
输出: [0,0,9,0,0]

提示：

• 2 <= nums.length <= 10⁵

• -30 <= nums[i] <= 30

• 输入 保证 数组 answer[i] 在 32 位 整数范围内

进阶：你可以在 O(1) 的额外空间复杂度内完成这个题目吗？（ 出于对空间复杂度分析的目的，输出数组 不被视为 额外空间。）

### Python 题解

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

---


## 82. 滑动窗口最大值（LeetCode 239 · 困难）

### 原题

给你一个整数数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。

返回 滑动窗口中的最大值 。

示例 1：

输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
解释：
滑动窗口的位置 最大值
--------------- -----
[1 3 -1] -3 5 3 6 7 3
1 [3 -1 -3] 5 3 6 7 3
1 3 [-1 -3 5] 3 6 7 5
1 3 -1 [-3 5 3] 6 7 5
1 3 -1 -3 [5 3 6] 7 6
1 3 -1 -3 5 [3 6 7] 7

示例 2：

输入：nums = [1], k = 1
输出：[1]

提示：

• 1 <= nums.length <= 10⁵

• -10⁴ <= nums[i] <= 10⁴

• 1 <= k <= nums.length

### Python 题解

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

---


## 83. 搜索二维矩阵 II（LeetCode 240 · 中等）

### 原题

编写一个高效的算法来搜索 m x n 矩阵 matrix 中的一个目标值 target 。该矩阵具有以下特性：

• 每行的元素从左到右升序排列。

• 每列的元素从上到下升序排列。

示例 1：

输入：matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
输出：true

示例 2：

输入：matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 20
输出：false

提示：

• m == matrix.length

• n == matrix[i].length

• 1 <= n, m <= 300

• -10⁹ <= matrix[i][j] <= 10⁹

• 每行的所有元素从左到右升序排列

• 每列的所有元素从上到下升序排列

• -10⁹ <= target <= 10⁹

### Python 题解

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

---


## 84. 完全平方数（LeetCode 279 · 中等）

### 原题

给你一个整数 n ，返回 和为 n 的完全平方数的最少数量 。

完全平方数 是一个整数，其值等于另一个整数的平方；换句话说，其值等于一个整数自乘的积。例如，1、4、9 和 16 都是完全平方数，而 3 和 11 不是。

示例 1：

输入：n = 12
输出：3
解释：12 = 4 + 4 + 4

示例 2：

输入：n = 13
输出：2
解释：13 = 4 + 9

提示：

• 1 <= n <= 10⁴

### Python 题解

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

---


## 85. 移动零（LeetCode 283 · 简单）

### 原题

给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。

请注意 ，必须在不复制数组的情况下原地对数组进行操作。

示例 1:

输入: nums = [0,1,0,3,12]
输出: [1,3,12,0,0]

示例 2:

输入: nums = [0]
输出: [0]

提示:

• 1 <= nums.length <= 10⁴

• -2³¹ <= nums[i] <= 2³¹ - 1

进阶：你能尽量减少完成的操作次数吗？

### Python 题解

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

---


## 86. 寻找重复数（LeetCode 287 · 中等）

### 原题

给定一个包含 n + 1 个整数的数组 nums ，其数字都在 [1, n] 范围内（包括 1 和 n），可知至少存在一个重复的整数。

假设 nums 只有 一个重复的整数 ，返回 这个重复的数 。

你设计的解决方案必须 不修改 数组 nums 且只用常量级 O(1) 的额外空间。

示例 1：

输入：nums = [1,3,4,2,2]
输出：2

示例 2：

输入：nums = [3,1,3,4,2]
输出：3

示例 3 :

输入：nums = [3,3,3,3,3]
输出：3

提示：

• 1 <= n <= 10⁵

• nums.length == n + 1

• 1 <= nums[i] <= n

• nums 中 只有一个整数 出现 两次或多次 ，其余整数均只出现 一次

进阶：

• 如何证明 nums 中至少存在一个重复的数字?

• 你可以设计一个线性级时间复杂度 O(n) 的解决方案吗？

### Python 题解

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

---


## 87. 数据流的中位数（LeetCode 295 · 困难）

### 原题

中位数是有序整数列表中的中间值。如果列表的大小是偶数，则没有中间值，中位数是两个中间值的平均值。

• 例如 arr = [2,3,4] 的中位数是 3 。

• 例如 arr = [2,3] 的中位数是 (2 + 3) / 2 = 2.5 。

实现 MedianFinder 类:

•
MedianFinder() 初始化 MedianFinder 对象。

•
void addNum(int num) 将数据流中的整数 num 添加到数据结构中。

•
double findMedian() 返回到目前为止所有元素的中位数。与实际答案相差 10⁻⁵ 以内的答案将被接受。

示例 1：

输入
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
输出
[null, null, null, 1.5, null, 2.0]

解释
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1); // arr = [1]
medianFinder.addNum(2); // arr = [1, 2]
medianFinder.findMedian(); // 返回 1.5 ((1 + 2) / 2)
medianFinder.addNum(3); // arr[1, 2, 3]
medianFinder.findMedian(); // return 2.0

提示:

• -10⁵ <= num <= 10⁵

• 在调用 findMedian 之前，数据结构中至少有一个元素

• 最多 5 * 10⁴ 次调用 addNum 和 findMedian

### Python 题解

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

---


## 88. 最长递增子序列（LeetCode 300 · 中等）

### 原题

给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。

子序列 是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，[3,6,2,7] 是数组 [0,3,1,6,2,2,7] 的子序列。

示例 1：

输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。

示例 2：

输入：nums = [0,1,0,3,2,3]
输出：4

示例 3：

输入：nums = [7,7,7,7,7,7,7]
输出：1

提示：

• 1 <= nums.length <= 2500

• -10⁴ <= nums[i] <= 10⁴

进阶：

• 你能将算法的时间复杂度降低到 O(n log(n)) 吗?

### Python 题解

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

---


## 89. 零钱兑换（LeetCode 322 · 中等）

### 原题

给你一个整数数组 coins ，表示不同面额的硬币；以及一个整数 amount，表示总金额。

计算并返回可以凑成总金额所需的 最少 的硬币个数。如果没有任何一种硬币组合能组成总金额，返回 -1 。

你可以认为每种硬币的数量是无限的。

示例 1：

输入：coins = [1, 2, 5], amount = 11
输出：3
解释：11 = 5 + 5 + 1

示例 2：

输入：coins = [2], amount = 3
输出：-1

示例 3：

输入：coins = [1], amount = 0
输出：0

提示：

• 1 <= coins.length <= 12

• 1 <= coins[i] <= 2³¹ - 1

• 0 <= amount <= 10⁴

### Python 题解

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

---


## 90. 前 K 个高频元素（LeetCode 347 · 中等）

### 原题

给你一个整数数组 nums 和一个整数 k ，请你返回其中出现频率前 k 高的元素。你可以按 任意顺序 返回答案。

示例 1：

输入：nums = [1,1,1,2,2,3], k = 2

输出：[1,2]

示例 2：

输入：nums = [1], k = 1

输出：[1]

示例 3：

输入：nums = [1,2,1,2,1,2,3,1,3,2], k = 2

输出：[1,2]

提示：

• 1 <= nums.length <= 10⁵

• -10⁴ <= nums[i] <= 10⁴

• k 的取值范围是 [1, 数组中不相同的元素的个数]

• 题目数据保证答案唯一，换句话说，数组中前 k 个高频元素的集合是唯一的

进阶：你所设计算法的时间复杂度 必须 优于 O(n log n) ，其中 n 是数组大小。

### Python 题解

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

---


## 91. 字符串解码（LeetCode 394 · 中等）

### 原题

给定一个经过编码的字符串，返回它解码后的字符串。

编码规则为: k[encoded_string]，表示其中方括号内部的 encoded_string 正好重复 k 次。注意 k 保证为正整数。

你可以认为输入字符串总是有效的；输入字符串中没有额外的空格，且输入的方括号总是符合格式要求的。

此外，你可以认为原始数据不包含数字，所有的数字只表示重复的次数 k ，例如不会出现像 3a 或 2[4] 的输入。

测试用例保证输出的长度不会超过 10⁵。

示例 1：

输入：s = "3[a]2[bc]"
输出："aaabcbc"

示例 2：

输入：s = "3[a2[c]]"
输出："accaccacc"

示例 3：

输入：s = "2[abc]3[cd]ef"
输出："abcabccdcdcdef"

示例 4：

输入：s = "abc3[cd]xyz"
输出："abccdcdcdxyz"

提示：

• 1 <= s.length <= 30

• s 由小写英文字母、数字和方括号 '[]' 组成

• s 保证是一个 有效 的输入。

• s 中所有整数的取值范围为 [1, 300]

### Python 题解

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

---


## 92. 分割等和子集（LeetCode 416 · 中等）

### 原题

给你一个 只包含正整数 的 非空 数组 nums 。请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等。

示例 1：

输入：nums = [1,5,11,5]
输出：true
解释：数组可以分割成 [1, 5, 5] 和 [11] 。

示例 2：

输入：nums = [1,2,3,5]
输出：false
解释：数组不能分割成两个元素和相等的子集。

提示：

• 1

### Python 题解

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

---


## 93. 路径总和 III（LeetCode 437 · 中等）

### 原题

给定一个二叉树的根节点 root ，和一个整数 targetSum ，求该二叉树里节点值之和等于 targetSum 的 路径 的数目。

路径 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）。

示例 1：

输入：root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
输出：3
解释：和等于 8 的路径有 3 条，如图所示。

示例 2：

输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
输出：3

提示:

• 二叉树的节点个数的范围是 [0,1000]

• -10⁹

### Python 题解

```python
from collections import defaultdict

class Solution:
    def pathSum(self, root, targetSum):
        cnt = defaultdict(int)
        cnt[0] = 1
        self.ans = 0
        def dfs(node, pre):
            if node is None:
                return
            pre += node.val
            self.ans += cnt[pre - targetSum]
            cnt[pre] += 1
            dfs(node.left, pre)
            dfs(node.right, pre)
            cnt[pre] -= 1          # 离开这棵子树，撤销
        dfs(root, 0)
        return self.ans
```

---


## 94. 找到字符串中所有字母异位词（LeetCode 438 · 中等）

### 原题

给定两个字符串 s 和 p，找到 s 中所有 p 的 异位词 的子串，返回这些子串的起始索引。不考虑答案输出的顺序。

示例 1:

输入: s = "cbaebabacd", p = "abc"
输出: [0,6]
解释:
起始索引等于 0 的子串是 "cba", 它是 "abc" 的异位词。
起始索引等于 6 的子串是 "bac", 它是 "abc" 的异位词。

示例 2:

输入: s = "abab", p = "ab"
输出: [0,1,2]
解释:
起始索引等于 0 的子串是 "ab", 它是 "ab" 的异位词。
起始索引等于 1 的子串是 "ba", 它是 "ab" 的异位词。
起始索引等于 2 的子串是 "ab", 它是 "ab" 的异位词。

提示:

• 1 <= s.length, p.length <= 3 * 10⁴

• s 和 p 仅包含小写字母

### Python 题解

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

---


## 95. 二叉树的直径（LeetCode 543 · 简单）

### 原题

给你一棵二叉树的根节点，返回该树的 直径 。

二叉树的 直径 是指树中任意两个节点之间最长路径的 长度 。这条路径可能经过也可能不经过根节点 root 。

两节点之间路径的 长度 由它们之间边数表示。

示例 1：

输入：root = [1,2,3,4,5]
输出：3
解释：3 ，取路径 [4,2,1,3] 或 [5,2,1,3] 的长度。

示例 2：

输入：root = [1,2]
输出：1

提示：

• 树中节点数目在范围 [1, 10⁴] 内

• -100 <= Node.val <= 100

### Python 题解

```python
class Solution:
    def diameterOfBinaryTree(self, root):
        self.ans = 0
        def depth(node):
            if node is None:
                return 0
            l, r = depth(node.left), depth(node.right)
            self.ans = max(self.ans, l + r)
            return max(l, r) + 1
        depth(root)
        return self.ans
```

---


## 96. 和为 K 的子数组（LeetCode 560 · 中等）

### 原题

给你一个整数数组 nums 和一个整数 k ，请你统计并返回 该数组中和为 k 的子数组的个数 。

子数组是数组中元素的连续非空序列。

示例 1：

输入：nums = [1,1,1], k = 2
输出：2

示例 2：

输入：nums = [1,2,3], k = 3
输出：2

提示：

• 1 <= nums.length <= 2 * 10⁴

• -1000 <= nums[i] <= 1000

• -10⁷ <= k <= 10⁷

### Python 题解

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

---


## 97. 每日温度（LeetCode 739 · 中等）

### 原题

给定一个整数数组 temperatures ，表示每天的温度，返回一个数组 answer ，其中 answer[i] 是指对于第 i 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 0 来代替。

示例 1:

输入: temperatures = [73,74,75,71,69,72,76,73]
输出: [1,1,4,2,1,1,0,0]

示例 2:

输入: temperatures = [30,40,50,60]
输出: [1,1,1,0]

示例 3:

输入: temperatures = [30,60,90]
输出: [1,1,0]

提示：

• 1 <= temperatures.length <= 10⁵

• 30 <= temperatures[i] <= 100

### Python 题解

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

---


## 98. 划分字母区间（LeetCode 763 · 中等）

### 原题

给你一个字符串 s 。我们要把这个字符串划分为尽可能多的片段，同一字母最多出现在一个片段中。例如，字符串 "ababcc" 能够被分为 ["abab", "cc"]，但类似 ["aba", "bcc"] 或 ["ab", "ab", "cc"] 的划分是非法的。

注意，划分结果需要满足：将所有划分结果按顺序连接，得到的字符串仍然是 s 。

返回一个表示每个字符串片段的长度的列表。

示例 1：

输入：s = "ababcbacadefegdehijhklij"
输出：[9,7,8]
解释：
划分结果为 "ababcbaca"、"defegde"、"hijhklij" 。
每个字母最多出现在一个片段中。
像 "ababcbacadefegde", "hijhklij" 这样的划分是错误的，因为划分的片段数较少。

示例 2：

输入：s = "eccbbbbdec"
输出：[10]

提示：

• 1 <= s.length <= 500

• s 仅由小写英文字母组成

### Python 题解

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

---


## 99. 腐烂的橘子（LeetCode 994 · 中等）

### 原题

在给定的 m x n 网格 grid 中，每个单元格可以有以下三个值之一：

• 值 0 代表空单元格；

• 值 1 代表新鲜橘子；

• 值 2 代表腐烂的橘子。

每分钟，腐烂的橘子 周围 4 个方向上相邻 的新鲜橘子都会腐烂。

返回 直到单元格中没有新鲜橘子为止所必须经过的最小分钟数。如果不可能，返回 -1 。

示例 1：

输入：grid = [[2,1,1],[1,1,0],[0,1,1]]
输出：4

示例 2：

输入：grid = [[2,1,1],[0,1,1],[1,0,1]]
输出：-1
解释：左下角的橘子（第 2 行， 第 0 列）永远不会腐烂，因为腐烂只会发生在 4 个方向上。

示例 3：

输入：grid = [[0,2]]
输出：0
解释：因为 0 分钟时已经没有新鲜橘子了，所以答案就是 0 。

提示：

• m == grid.length

• n == grid[i].length

• 1 <= m, n <= 10

• grid[i][j] 仅为 0、1 或 2

### Python 题解

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

---


## 100. 最长公共子序列（LeetCode 1143 · 中等）

### 原题

给定两个字符串 text1 和 text2，返回这两个字符串的最长 公共子序列 的长度。如果不存在 公共子序列 ，返回 0 。

一个字符串的 子序列 是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。

• 例如，"ace" 是 "abcde" 的子序列，但 "aec" 不是 "abcde" 的子序列。

两个字符串的 公共子序列 是这两个字符串所共同拥有的子序列。

示例 1：

输入：text1 = "abcde", text2 = "ace"
输出：3
解释：最长公共子序列是 "ace" ，它的长度为 3 。

示例 2：

输入：text1 = "abc", text2 = "abc"
输出：3
解释：最长公共子序列是 "abc" ，它的长度为 3 。

示例 3：

输入：text1 = "abc", text2 = "def"
输出：0
解释：两个字符串没有公共子序列，返回 0 。

提示：

• 1

### Python 题解

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
