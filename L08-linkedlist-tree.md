# L08 · 链表与二叉树（29 题）

这一册最多，也最容易卡人。卡住的原因通常不是算法难，而是**「节点」和「递归」这两个概念没建立起来**。所以先看第 0 节，别急着跳到题目。

| 部分 | 题号 · 题名 | 难度 |
|---|---|---|
| 链表基础 | 160 相交链表 · 206 反转链表 · 141 环形链表 · 142 环形链表 II · 21 合并两个有序链表 · 2 两数相加 | 易×4 中×2 |
| 链表进阶 | 19 删除倒数第 N 个 · 24 两两交换 · 25 K 个一组翻转 · 148 排序链表 · 23 合并 K 个升序链表 · 146 LRU 缓存 | 中×4 难×2 |
| 链表收尾 | 234 回文链表 · 138 随机链表的复制 | 易 中 |
| 树的遍历 | 94 中序遍历 · 104 最大深度 · 226 翻转二叉树 · 101 对称二叉树 · 543 二叉树的直径 · 102 层序遍历 | 易×5 中 |
| 树的进阶 | 98 验证 BST · 230 BST 第 K 小 · 199 右视图 · 105 前序中序构造 · 236 最近公共祖先 · 124 最大路径和 | 中×5 难 |
| 树的收尾 | 108 有序数组转 BST · 114 展开为链表 · 437 路径总和 III | 易 中 中 |

---

## 0. 先把三个概念讲透（别跳）

### 0.1 节点：一个装着「值」和「下一个在哪」的小盒子

LeetCode 里链表节点长这样（平台已经定义好，你直接用）：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val      # 这个节点存的值
        self.next = next    # 下一个节点在哪；没有就是 None
```

三个节点连起来：

```python
a = ListNode(1)
b = ListNode(2)
c = ListNode(3)
a.next = b
b.next = c
# 现在：1 -> 2 -> 3 -> None
```

用文字画出来：

```text
  a           b           c
┌───┬───┐   ┌───┬───┐   ┌───┬────┐
│ 1 │ ●─┼──>│ 2 │ ●─┼──>│ 3 │None│
└───┴───┘   └───┴───┘   └───┴────┘
```

**关键理解**：`a.next = b` 不是「把 b 复制进 a」，而是「a 身上记下了 b 在哪」。`a` 和 `b` 是两个独立的小盒子，中间靠一根线连着。

所以改 `cur.next = pre`，改的是**这根线指向谁**，节点本身没动。链表所有操作，本质都是改这些线。

二叉树节点多一根线：

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### 0.2 `None` 是什么

`None` 表示「这里没有节点」。判断必须写：

```python
def count_nodes(head):
    if head is None:
        return 0        # 空节点的答案是 0；具体返回什么由「状态定义」决定
    return 1 + count_nodes(head.next)
```

`node.next` 在 `node` 是 `None` 时会报错（`AttributeError`），所以「往后走」之前一定要判空，或者用短路：

```python
while cur is not None and cur.next is not None:
    ...
```

`and` 的短路保证前面不成立时不会去碰后面那个。

### 0.3 递归：让函数自己调用自己

树的题几乎都靠递归。刚开始觉得绕很正常，只要每次写代码前回答**三个问题**：

1. **这个函数的返回值代表什么？**（例：「以 node 为根的子树的最大深度」）
2. **这一层要做什么？**（例：「问左子树多深、问右子树多深，取较大 +1」）
3. **什么时候直接返回？**（例：「node 是 None 时深度是 0」）

看一个完整的：

```python
def maxDepth(root):
    if root is None:            # ③ 终止条件
        return 0
    left = maxDepth(root.left)  # ② 问左边
    right = maxDepth(root.right)# ② 问右边
    return max(left, right) + 1 # ② 合并，① 返回值是「深度」
```

**为什么这样能行**：不要试图在脑子里一层层展开（会晕）。只要相信「`maxDepth(root.left)` 一定会正确返回左子树的深度」——因为对更小的树，这个函数干的正是同一件事。这叫**信任递归**。

**Python 的一个限制**：默认最多约 1000 层嵌套调用，一条 2000 个节点的链用递归会 `RecursionError`。做题时可以在文件顶部加：

```python
import sys
sys.setrecursionlimit(10 ** 6)
```

但能改成循环的题（尤其链表）优先改循环。

### 0.4 本地怎么造链表和树

平台会自动构造，但本地调试要自己写：

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
```

`dummy`（虚拟头节点）是链表题第一大技巧，下面第一题就会用到。

---

# 第一部分 · 链表

## 1. 链表基础

### 160 · 相交链表（简单）

给两条链表的头，找它们第一个公共节点，没有返回 `None`。

**怎么想**：两条链可能不一样长，同时从头走会错开。让两个指针各自走完自己那条后，**切换到另一条的头继续走**——这样两者走的总路程都是「A 长 + B 长」，必然在公共节点（或同时走到 `None`）相遇。

```python
class Solution:
    def getIntersectionNode(self, headA, headB):
        a, b = headA, headB
        while a != b:
            a = a.next if a is not None else headB
            b = b.next if b is not None else headA
        return a
```

时间 `O(m+n)`，空间 `O(1)`。**易错**：判断「走完了」用 `a is None`，切换后不能立刻又切回来；不相交时两者会同时变成 `None`，循环自然结束。

### 206 · 反转链表（简单）

**怎么想**：三个变量 `pre`（已经反转好的部分）、`cur`（当前处理的）、`nxt`（临时存住下一个）。每轮先把 `cur.next` 改指向 `pre`，然后三个一起往前挪。

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

手动模拟 `1 -> 2 -> 3`：

| 轮 | cur | nxt | 改完后 cur.next | pre | 新 cur |
|---|---|---|---|---|---|
| 1 | 1 | 2 | None | 1 | 2 |
| 2 | 2 | 3 | 1 | 2 | 3 |
| 3 | 3 | None | 2 | 3 | None |

时间 `O(n)`，空间 `O(1)`。**这个「三个变量一起挪」的形状是后面大部分链表题的骨架**，值得抄三遍。

### 141 · 环形链表（简单）

判断链表里有没有环。

**怎么想**：快慢指针，慢的每次走一步、快的每次走两步。有环的话快的迟早从后面追上慢的；没环的话快的会先走到 `None`。

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

时间 `O(n)`，空间 `O(1)`。**易错**：判「是不是同一个节点」用 `is`，不是 `==`；循环条件要同时保证 `fast` 和 `fast.next` 都不是 `None`。

### 142 · 环形链表 II（中等）

有环的话，返回环的入口节点。

**怎么想**：先用快慢指针找到相遇点，然后让一个指针回到链表头，两个指针**同速**前进，再次相遇处就是环入口。（背后的数学：设头到入口距离为 a、入口到相遇点为 b，快指针走的路是慢指针两倍，可推出「头到入口」等于「相遇点再走到入口」。）

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

时间 `O(n)`，空间 `O(1)`。**易错**：第二段循环两个指针都走一步，别再让其中一个走两步。

### 21 · 合并两个有序链表（简单）

**怎么想**：用虚拟头节点 `dummy`，每次挑两个链表头里较小的那个接上去，被挑中的往后走一步。最后把没走完的那条整段接上。

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

时间 `O(m+n)`，空间 `O(1)`。**易错**：`cur.next, list1 = list1, list1.next` 右侧先整体求值，所以 `list1.next` 是**原来的**下一个节点，不会被覆盖。`dummy` 本身不存有效数据，最后返回 `dummy.next`。

### 2 · 两数相加（中等）

两个链表各自表示一个数字（低位在前），返回它们和的链表。

**怎么想**：像手算加法一样逐位加，维护进位 `carry`。两条链表长度可能不同，短的那条没了就当 0。

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

时间 `O(max(m,n))`，空间 `O(max(m,n))`。**易错**：循环条件里必须有 `or carry`，否则最后多出的一位（如 `5+5=10`）会丢。

---

## 2. 链表进阶

### 19 · 删除倒数第 N 个结点（中等）

**怎么想**：让 `fast` 先走 N 步，然后 `fast`、`slow` 一起走。`fast` 走到最后一个节点时，`slow` 正好停在要删节点的前一个。用虚拟头节点可以统一处理「删的是头节点」的情况。

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

时间 `O(n)`，空间 `O(1)`。**易错**：`while fast.next is not None` 而不是 `fast is not None`，这样 `slow` 才能停在待删节点的前一位。

### 24 · 两两交换链表中的节点（中等）

**怎么想**：每次处理一对 `(a, b)`，把 `prev -> a -> b -> next` 改成 `prev -> b -> a -> next`，然后 `prev` 挪到 `a`（它现在是这一对的尾）。

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

时间 `O(n)`，空间 `O(1)`。**易错**：那个三路赋值右边先整体求值，`b.next` 取的是**交换前** b 的下一个节点，正好是下一组的开头。写成三行分开的赋值反而容易错，因为 `b.next` 已经被改过了。

### 25 · K 个一组翻转链表（困难）

每 K 个节点翻转一组，不足 K 个的保持原样。

**怎么想**：先探路，从 `group_prev` 往前数 K 个找到 `kth`；数不够就结束。够的话记录 `group_next = kth.next`，用 206 题的反转手法把这一段翻转（注意反转的初始 `prev` 要设成 `group_next`，这样尾能自动接上后半段），最后把上一组的尾接到新头。

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

时间 `O(n)`，空间 `O(1)`。**易错**：`kth_after(group_prev, k)` 从虚拟头开始数 K 步才正好落在本组最后一个节点；反转时 `prev` 初值必须是 `group_next`。

### 148 · 排序链表（中等）

给链表排序，要求 `O(n log n)`。

**怎么想**：归并排序。用快慢指针找到中点、把链表断成两半，各自递归排序，再用 21 题的「合并两个有序链表」拼回去。

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

时间 `O(n log n)`，空间 `O(log n)`（递归栈）。**易错**：`prev.next = None` 不能漏，否则左半尾巴还连着右半，递归会无限循环。

### 23 · 合并 K 个升序链表（困难）

**怎么想**：把每条链表当前的头放进小根堆，每次弹出最小的接进答案，再把那条链表的下一个节点补进堆。因为节点对象不能直接比较，堆里放 `(值, 序号, 节点)`，序号保证永远不会比到节点本身。

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

时间 `O(N log k)`（N 总节点数、k 链表条数），空间 `O(k)`。**易错**：不插 `seq` 的话，两条链表头值相同时 Python 会去比较 `ListNode` 对象，直接 `TypeError`。

### 146 · LRU 缓存（中等）

设计缓存：`get` / `put` 都是 `O(1)`，容量满时淘汰最久没用过的。

**怎么想**：哈希表保证查找快，还要维护「谁最旧」。`OrderedDict` 正好提供了 `move_to_end()`（标记为最新）和 `popitem(last=False)`（弹出最旧）。

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

两个操作均 `O(1)`，空间 `O(capacity)`。**易错**：`get` 命中时也要 `move_to_end`，否则「最近使用」的信息就错了。面试有时会要求手写双向链表 + 哈希表，那时不能用这个偷懒版，但 LeetCode 上提交没问题。

---

## 3. 链表收尾

### 234 · 回文链表（简单）

判断链表是不是回文，要求 `O(1)` 额外空间。

**怎么想**：① 快慢指针找到中点；② 把后半段反转；③ 从头和从后半段头一起走，逐个比值。

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

时间 `O(n)`，空间 `O(1)`。**易错**：奇数长度时中点那个元素会被前半段包含，但后半段比完就停，不影响结果。

### 138 · 随机链表的复制（中等）

每个节点除了 `next` 还有一个 `random` 指向任意节点，要深拷贝整条链。

**怎么想**：两遍哈希表。第一遍给每个原节点造一个新节点，存映射；第二遍照映射把 `next` 和 `random` 接上。字典里预存 `{None: None}` 这个哨兵，能省掉每处判空。

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

时间 `O(n)`，空间 `O(n)`。**易错**：不能一遍做完——第二遍接 `random` 时，目标节点可能还没被创建，所以必须先全部造好。节点对象能当字典的键（自定义类默认可哈希）。

---

# 第二部分 · 二叉树

## 4. 树的遍历

### 94 · 二叉树的中序遍历（简单）

按「左 → 根 → 右」的顺序输出所有值。

**怎么想**：递归三问——返回值：无（把值加进结果列表）；单层：先遍历左、记录自己、再遍历右；终止：节点是 `None` 就返回。

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

时间 `O(n)`，空间 `O(h)`（h 是树高，递归栈）。**易错**：`dfs` 定义在方法内部时，`res` 是外层变量，读它没问题；若要修改计数变量得用 `nonlocal` 或改成返回值。

### 104 · 二叉树的最大深度（简单）

**怎么想**：一棵树的深度 = 左右子树里较深的那个 + 1。空树深度 0。

```python
class Solution:
    def maxDepth(self, root):
        if root is None:
            return 0
        return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1
```

时间 `O(n)`，空间 `O(h)`。**易错**：别漏 `+ 1`（算上自己这一层）。

### 226 · 翻转二叉树（简单）

**怎么想**：翻转一棵树 = 交换它的左右子树，再各自递归翻转。

```python
class Solution:
    def invertTree(self, root):
        if root is None:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
```

时间 `O(n)`，空间 `O(h)`。**易错**：右边整体先求值，所以 `self.invertTree(root.right)` 拿到的是交换前的右子树，正好。

### 101 · 对称二叉树（简单）

判断一棵树是否左右镜像对称。

**怎么想**：不是「判断左子树等于右子树」，而是「左子树的左 对 右子树的右、左子树的右 对 右子树的左」都相等。写一个比较两棵树的辅助函数。

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

时间 `O(n)`，空间 `O(h)`。**易错**：两个都为空是 `True`，只有一个为空是 `False`，顺序别反。

### 543 · 二叉树的直径（简单）

直径 = 任意两点间最长路径的**边数**。

**怎么想**：一条最长路径一定经过某个节点，长度 = 它左子树深度 + 右子树深度。递归函数返回「深度」给父节点用，同时用一个全局的 `self.ans` 记「目前见过的最长路径」。这是树题里非常常见的「返回值和全局答案分离」结构。

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

时间 `O(n)`，空间 `O(h)`。**易错**：`self.ans = 0` 必须在入口方法里写，不能放进递归函数（那样每轮都被清零）；而且平台可能复用同一个对象跑多组测试，入口处重置是必须的。

### 102 · 二叉树的层序遍历（中等）

按层从上到下、每层从左到右输出。

**怎么想**：用队列（`deque`）。关键是**先记下当前队列长度**，这个长度就是当前层的节点数，然后只处理这么多个——即使处理过程中往队列里加了下一层的节点，也不会混进本层。

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

时间 `O(n)`，空间 `O(n)`。**易错**：`for _ in range(len(q))` 里的 `len(q)` 在循环开始时求值一次；用 `list.pop(0)` 会超时，必须 `deque`。

---

## 5. 二叉搜索树与进阶

**先补一个概念：二叉搜索树（BST）**。它满足「左子树所有值 < 根 < 右子树所有值」。由此推出一个极重要的性质：**对 BST 做中序遍历，得到的一定是升序序列**。下面两道题都靠它。

### 98 · 验证二叉搜索树（中等）

**怎么想**：不能只比较「根和左右孩子」——某个深层节点可能违反和祖先的大小关系。给递归带上「允许的范围 `(lo, hi)`」，每往左走就把上界收紧到当前值，往右走就把下界收紧。

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

时间 `O(n)`，空间 `O(h)`。**易错**：用 `float("±inf")` 做初始界，别用 `-1`/`10**9` 这种具体数（节点值可能超出）；比较是严格的 `<`，BST 不允许相等。

### 230 · 二叉搜索树中第 K 小的元素（中等）

**怎么想**：中序遍历是升序，数到第 K 个就是答案。用一个计数变量，到 K 就记住答案并提前停。

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

时间 `O(h + k)`，空间 `O(h)`。**易错**：计数要放在「访问左子树之后、递归右子树之前」，那正是中序的位置；找到后靠 `self.ans is not None` 提前剪枝。

### 199 · 二叉树的右视图（中等）

从右边看这棵树，输出每层能看到的那个节点。

**怎么想**：层序遍历，每一层取**最后一个**节点。循环开始前队列里正好是当前层所有节点，所以 `q[-1]` 就是它。

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

时间 `O(n)`，空间 `O(n)`。**易错**：`q[-1]` 要在 `for` 循环**之前**取，那时队列还没混入下一层。

### 105 · 从前序与中序遍历序列构造二叉树（中等）

**怎么想**：前序第一个一定是根。在中序里找到根的位置，左边就是左子树的节点、右边是右子树的节点；由左子树长度可以切出前序里两段的范围，递归构造。用字典记「值 → 中序下标」，避免每次线性查找。

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

时间 `O(n)`，空间 `O(n)`。**易错**：`left_len = k - il`（中序里根左边的个数），前序里左段就是 `pl+1 ~ pl+left_len`，右段从 `pl+left_len+1` 开始。

### 236 · 二叉树的最近公共祖先（中等）

找两个节点最近的一个共同祖先。

**怎么想**：递归问左右子树。如果某一侧返回了 `None`，说明两个节点都在另一侧；如果**两侧都返回了非空**，说明当前节点就是分叉点，即答案。如果当前节点本身就是 p 或 q，直接返回它。

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

时间 `O(n)`，空间 `O(h)`。**易错**：判断「是不是同一个节点」用 `is`（这里比的是对象身份，是 `is` 少数正当用途之一）；返回值可能为空，用 `is not None` 判断。

### 124 · 二叉树中的最大路径和（困难）

任意一条路径（可以从任意节点到任意节点）的最大节点值之和，可能有负数。

**怎么想**：递归函数返回「从当前节点**往下走单边**能给父节点贡献的最大值」——负值贡献直接砍成 0（不要也罢）。同时在每层用「左贡献 + 右贡献 + 自己」更新全局答案，那条是穿过当前节点的完整路径，不能再往上延伸。

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

时间 `O(n)`，空间 `O(h)`。**易错**：返回值是**单边**（`node.val + max(l,r)`），全局更新用**双边**（`+ l + r`），两者别混；初始答案必须是 `-inf`，全负数树才对。

---

## 6. 树的收尾

### 108 · 将有序数组转换为二叉搜索树（简单）

把升序数组转成一棵高度平衡的 BST。

**怎么想**：取中间元素当根（两边节点数最接近，自然平衡），左半递归造左子树、右半递归造右子树。

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

时间 `O(n)`，空间 `O(log n)`。**易错**：`//` 不能写成 `/`，否则下标变小数会报错。

### 114 · 二叉树展开为链表（中等）

把树按前序顺序原地拉成一条「只有右孩子」的链。

**怎么想**：对每个节点，如果它有左子树，就把左子树接到「右子树之前」——具体做法：找到左子树最右边的节点（前序里左子树的最后一个），把原来的右子树挂到它的 `right` 上，然后把整棵左子树搬到 `right`，左孩子置空。一路往右走。

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

时间 `O(n)`，空间 `O(1)`。**易错**：`cur.left = None` 不能漏，否则不是「链表」；找 `pre` 时只沿 `right` 走。

### 437 · 路径总和 III（中等）

统计有多少条**向下**的路径，节点值之和等于 `targetSum`（路径不必从根开始、不必到叶子结束）。

**怎么想**：和 [L06 · 560 题](L06-array-and-hash.md) 是同一个套路。记从根到当前节点的前缀和 `pre`，若之前某处的前缀和是 `pre - targetSum`，那中间这一段就符合。用字典数前缀和出现次数；**离开当前节点时要撤销它的贡献**（回溯），否则会把别的分支的前缀和算进来。

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

时间 `O(n)`，空间 `O(h)`。**易错**：`cnt[0] = 1` 和最后的 `cnt[pre] -= 1` 都不能少；`self.ans` 要在入口处重置。

---

## 本册小结

| 遇到什么 | 先想到 |
|---|---|
| 头节点可能被改、要删第一个节点 | 虚拟头 `dummy` |
| 反转、两两交换、K 组翻转 | `pre / cur / nxt` 三变量 |
| 找中点、判环、倒数第 N 个 | 快慢指针 |
| 多条链表合并 | 堆（记得插序号避免比较节点） |
| 树的深度、翻转、对称 | 递归三问 |
| 按层处理 | `deque` + `for _ in range(len(q))` |
| BST 相关 | 中序是升序 / 带上下界递归 |
| 「全局最优」不能直接当返回值 | 递归返回单边值，`self.ans` 记全局 |
| 树的路径求和 | 前缀和 + 哈希 + 回溯撤销 |

**最该记住的三句话**：链表操作改的是「线」不是节点；递归前先回答三问；凡是 `self.xxx` 都要在入口方法第一行重置。

---

## 本册自测（闭卷）

1. 默写反转链表的迭代版，说明为什么必须先存 `nxt`。
2. 虚拟头节点解决了什么问题？举一道题。
3. 递归三问是哪三问？用「最大深度」举一遍。
4. `102` 层序遍历里 `for _ in range(len(q))` 为什么不能写成 `while q:`？
5. `543` 直径题里，为什么递归函数返回的是「深度」而答案却用 `l + r` 更新？
6. `437` 里最后的 `cnt[pre] -= 1` 漏了会怎样？
7. **口述题**：为什么 `23` 题入堆要放 `(值, 序号, 节点)` 而不是 `(值, 节点)`？

<details>
<summary>答案要点</summary>

1. `cur.next = pre` 会覆盖原来的后继，不先存就再也找不到下一个节点。三变量同时赋值 `pre, cur = cur, nxt` 右边先整体求值。
2. 让「头节点也要被改/删」的情况和中间节点走同一套逻辑，不用单独写 `if`。如 19 题删倒数第 N 个、21 题合并。
3. 返回值代表什么、单层做什么、终止条件。以最大深度为例：返回「以 node 为根的子树深度」；单层问左右深度取较大 +1；`node is None` 时返回 0。
4. 那样会把本轮新加入的下一层节点也当成当前层处理，分层结果就乱了；先固定 `len(q)` 才能精确处理一层。
5. 返回给父节点的只能是「从当前节点往下走一条单边链」的最大值（因为路径不能分叉）；而经过当前节点、连接左右两边的完整路径是全局候选，用 `l + r + node.val` 更新 `self.ans`。
6. 会把其他分支里的前缀和也算进当前路径，导致答案偏大（兄弟子树互相污染）。
7. 元组比较在第一项相等时会去比第二项；`ListNode` 之间没有定义「小于」，会抛 `TypeError`。插入唯一的 `seq` 保证前两项一定能分出胜负，永远比不到节点。

</details>

---

## 下一册

[L09](L09-backtrack-graph-dp.md) 是最后一册，27 道题：回溯、图论、动态规划。动态规划是全书最难的一章，会从「状态到底是什么」讲起，不假设你懂任何术语。允许在那儿多花一周。
