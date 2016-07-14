title: Leetcode 题解
date: 2015-11-27 15:53:19
category: 算法
tags:
- leetcode
- c
---

### 1. Two Sum
#### 题目原文
[https://leetcode.com/problems/two-sum/](https://leetcode.com/problems/two-sum/)
#### 解题思路
给定一个整数数组nums[]和一个目标数target，从数组中找到两个数使它们相加的值为目标数，最后返回他们的坐标index1和index2。
1.   index1 < index2
2.   index1 != 0 && index2 != 0

首先我们知道目标数target，假设数组的第一个元素为要找的两个数之一num1，然后我们通过target和num1计算出num2，问题转化为在剩余数组是否存在num2。如果存在假设成立，返回num1和num2的坐标即可；如果不存在假设数组第二个元素为num1，依次类推。
但是，这样的解法为在数组中元素较多时效率非常低。我做了一个优化使用二分查找，二分查找要求数组是排好序的。这里我使用标准库函数`qsort`和`bsearch`。

<!-- more -->

```c
struct node {
    int pos;
    int val;
};

int cmp(const void *a, const void *b)
{
    return ((struct node *)a)->val - ((struct node *)b)->val;
}

int* twoSum(int *nums, int size, int target)
{
    struct node *arr = (struct node *) malloc(sizeof(struct node) * size);
    int i;
    int num = 0;
    struct node *tmp = NULL;
    struct node key;

    for (i = 0; i < size; i++) {
        arr[i].pos = i;
        arr[i].val = nums[i];
    }

    qsort(arr, size, sizeof(struct node), cmp);

    for (i = 0; i < size; i++) {
        key.val = target - arr[i].val;
        tmp = bsearch(&key, arr, size, sizeof(struct node), cmp);
        if (NULL != tmp) {
            int *res = (int*) malloc(sizeof(int) * 2);
            res[0] = arr[i].pos + 1;
            res[1] = tmp->pos + 1;
            // swap res[0] and res[1]
            if (res[0] > res[1]) {
                res[0] += res[1];
                res[1] = res[0] - res[1];
                res[0] -= res[1];
            }
            return res;
        }
    }

    return NULL;
}
```

### 2. Add Two Numbers
#### 题目原文
[https://leetcode.com/problems/add-two-numbers/](https://leetcode.com/problems/add-two-numbers/)
#### 解题思路
1. 链表长度可能不同
2. 处理进位

```c
struct ListNode* newlist()
{
    struct ListNode *list = malloc(sizeof(struct ListNode));
    list->val = 0;
    list->next = NULL;
    return list;
}

struct ListNode* addTwoNumbers(struct ListNode* l1, struct ListNode* l2)
{
    if (NULL == l1 || l2 == NULL) {
        return NULL;
    }

    int carry = 0;
    int num = 0;
    struct ListNode *res = newlist();
    struct ListNode *cur = res;
    struct ListNode *tmp = NULL;

    while (NULL != l1 || l2 != NULL || carry) {
        tmp = newlist();
        if (NULL != l1) {
            num += l1->val;
            l1 = l1->next;
        }
        if (NULL != l2) {
            num += l2->val;
            l2 = l2->next;
        }
        tmp->val = (num + carry) % 10;
        carry = (num + carry) / 10;
        cur = cur->next = tmp;
        num = 0;
    }
    return res->next;
}
```

### 7. Reverse Integer
#### 题目原文
[https://leetcode.com/problems/reverse-integer/](https://leetcode.com/problems/reverse-integer/)
#### 解题思路
1.   10 -> 1, 100 -> 1
2.   输入为一个32位整数比如1000000003，翻转后超出32位，输出应该为0
使用字符串模拟，先将数字转化为字符串，翻转字符串，字符串转化为整数，最后返回。注意2中要用到`INT_MAX`和`INT_MIN`这两个宏，它在`limits.h`中定义，表示最大的int型整数。

```c
char* int2str(int x, char *s)
{
    int i;
    for (i = 0; x != 0; i++) {
        s[i] = (x % 10) + '0';
        x /= 10;
    }
    s[i] = '\0';
    return s;
}

int str2int(char* s)
{
    long x = 0;
    int  i;
    int len = strlen(s);
    for (i = len - 1; i >= 0 ; i--) {
        x += ((long)(s[i] - '0') * pow(10, len - i - 1));
        if (x >= INT_MAX) {
            return 0;
        }
    }
    return (int)x;
}

int reverse(int x)
{
    if (INT_MIN == x || INT_MAX == x || x == 0) {
        return 0;
    }
    char s[128];
    if (x > 0) {
        return str2int(int2str(x, s));
    } else if (x < 0) {
        return -str2int(int2str(abs(x), s));
    }
    return 0;
}
```

### 8. String to Integer
#### 题目原文
[https://leetcode.com/problems/string-to-integer-atoi/](https://leetcode.com/problems/string-to-integer-atoi/)
#### 解题思路
题目非常简单，注意一下细节即可。
1. 字符串前边可能有空格或是空串
2. 字符串可能包含`+`、`-`和非数字字符

```c
int myAtoi(char *str)
{
    if (NULL == str) {
        return 0;
    }

    int i = 0;
    int symbol = 1;
    long res = 0;

    // 去掉前导空格
    while (isspace(str[i])) {
        i++;
    }

    // 确定正负数
    if ('-' == str[i]) {
        symbol = -1;
        i++;
    } else if ('+' == str[i]) {
        symbol = 1;
        i++;
    }

    while (str[i] >= '0' && str[i] <= '9') {
        res *= 10;
        res += str[i] - '0';
        if (res >= INT_MAX) {
            break;
        }
        i++;
    }
    res *= symbol;
    if (INT_MAX <= res) {
        return INT_MAX;
    } else if (INT_MIN >= res) {
        return INT_MIN;
    } else {
        return res;
    }
}
```

### 9. Palindrome Number

#### 题目原文
[https://leetcode.com/problems/palindrome-number/](https://leetcode.com/problems/palindrome-number/)
#### 解题思路
依次从最高位和最低位取整数的那一位的值做比较。
提示：计算一个正整数的位数 log10(num) + 1
注意：可能有负数

```c
bool isPalindrome(int x)
{
    if (x < 0) {
        return false;
    }

    int l = (int)pow(10, (int)(log10(x)));

    while (x) {
        if ((x / l) != (x % 10)) {
            return false;
        }
        x = (x % l) / 10;
        l /= 100;
    }

    return true;
}
```

### 19. Remove Nth Node From End of List
#### 题目原文
[https://leetcode.com/problems/remove-nth-node-from-end-of-list/](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)
#### 解题思路
如果链表长度大于n，题目要求删除链表倒数第n个元素，而链表只能顺序访问，我们需要连个指针p和q，让p和q直接的步长为n，同时向后移动，当p移到链表末尾时，q的位置正好是倒数第n＋1个元素，这时把q的next指针指向下下个元素且释放要删除的元素的内存即可;
如果链表长度等于n，返回head->next并且释放head指向的内存;
如果链表长度小于n，返回head。

```c
struct ListNode* removeNthFromEnd(struct ListNode* head, int n)
{
    struct ListNode *tmp = head;
    struct ListNode *p = tmp;
    struct ListNode *q = tmp;
    int i;

    for (i = 0; i < n; i++) {
        if (NULL == tmp->next && (i == n-1)) {
            tmp = head->next;
            free(head);
            return tmp;
        }
        p = tmp->next;
        tmp = tmp->next;
    }

    while (NULL != p->next) {
        p = p->next;
        q = q->next;
    }

    tmp = q->next->next;
    free(q->next);
    q->next = tmp;

    return head;
}
```

### 20. Valid Parentheses
#### 题目原文
[https://leetcode.com/problems/valid-parentheses/](https://leetcode.com/problems/valid-parentheses/)
#### 解题思路

```c
bool isValid(char *s)
{
    int length = strlen(s);
    int stack[length];
    int pos = 0;
    int i = 0;

    for (i = 0; i < length; i++) {
        if (s[i] == '(') {
            stack[pos++] = s[i];
            continue;
        } else if (s[i] == '{') {
            stack[pos++] = s[i];
            continue;
        } else if (s[i] == '[') {
            stack[pos++] = s[i];
            continue;
        }

        if (s[i] == ')' && 0 != pos && stack[pos-1] == '(') {
            stack[pos--] = 0;
            continue;
        } else if (s[i] == ')' && 0 != pos && stack[pos-1] != '(') {
            return false;
        } else if (s[i] == ')' && 0 == pos) {
            return false;
        }

        if (s[i] == '}' && 0 != pos && stack[pos-1] == '{') {
            stack[pos--] = 0;
            continue;
        } else if (s[i] == '}' && 0 != pos && stack[pos-1] != '{') {
            return false;
        } else if (s[i] == '}' && 0 == pos) {
            return false;
        }

        if (s[i] == ']' && 0 != pos && stack[pos-1] == '[') {
            stack[pos--] = 0;
            continue;
        } else if (s[i] == ']' && 0 != pos && stack[pos-1] != '[') {
            return false;
        } else if (s[i] == ']' && 0 == pos) {
            return false;
        }
    }
    if (0 != pos) {
        return false;
    } else {
        return true;
    }
}
```

### 21. Merge Two Sorted Lists
#### 题目原文
[https://leetcode.com/problems/merge-two-sorted-lists/](https://leetcode.com/problems/merge-two-sorted-lists/)
#### 解题思路

```c
struct ListNode* mergeTwoLists(struct ListNode *l1, struct ListNode *l2)
{
    if (NULL == l1) return l2;
    if (NULL == l2) return l1;
    if (l1->val < l2->val) {
        l1->next = mergeTwoLists(l1->next, l2);
        return l1;
    } else {
        l2->next = mergeTwoLists(l2->next, l1);
        return l2;
    }
}
```

### 26. Remove Duplicates from Sorted Array
#### 题目原文
[https://leetcode.com/problems/remove-duplicates-from-sorted-array/](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)
#### 解题思路

```c
int removeDuplicates(int *nums, int numsSize)
{
    if (NULL == nums || numsSize == 0) {
        return 0;
    }

    int size = 1;
    int i = 0;

    for (i = 1; i < numsSize; i++) {
        if (nums[i-1] != nums[i]) {
            nums[size++] = nums[i];
        }
    }

    return size;
}
```

### 27. Remove Element
#### 题目原文
[https://leetcode.com/problems/remove-element/](https://leetcode.com/problems/remove-element/)
#### 解题思路

```c
int cmp(const void *a, const void *b)
{
    return *(int *)a - *(int *)b;
}

int removeElement(int *nums, int numsSize, int val)
{
    if (NULL == nums || numsSize == 0) {
        return 0;
    }

    int i = 0;
    int begin = 0;
    int end = 0;
    int size = 0;

    qsort(nums, numsSize, sizeof(int), cmp);

    while (nums[i] != val && i < numsSize) {
        i++;
    }
    begin = i;

    while (nums[i] == val && i < numsSize) {
        i++;
    }
    end = i;

    size = numsSize - end + begin;

    for (i = end; i < numsSize; i++) {
        nums[begin++] = nums[i];
    }

    return size;
}
```

### 28. Implement strStr()
#### 题目原文
[https://leetcode.com/problems/implement-strstr/](https://leetcode.com/problems/implement-strstr/)
#### 解题思路
考虑haystack和needle为空串的情况，了解函数`strncmp`的用法。

```c
int strStr(char *haystack, char *needle)
{
    if (NULL == haystack || needle == NULL) {
        return -1;

    }

    int i = 0;
    int haystack_length = strlen(haystack);
    int needle_length = strlen(needle);

    if (!haystack_length && !needle_length) {
        return 0;

    }

    for (i = 0; i < haystack_length; i++) {
        if(!strncmp(haystack + i, needle, needle_length)) {
            return i;
        }

    }

    return -1;
}
```

### 58. Length of Last Word
#### 题目原文
[https://leetcode.com/problemset/algorithms/](https://leetcode.com/problemset/algorithms/)
#### 解题思路
这道题需要注意字符串最后可能有多余的空格，既从最后一个非空格字符开始计数直到遇到下一个空格字符结束。

```c
int lengthOfLastWord(char* s)
{
    if (NULL == s) {
        return 0;
    }
    int length = 0;
    char *p = s + strlen(s) - 1;

    while (p >= s && isspace(*p)) {
        p--;
    }

    while (p >= s && !isspace(*p)) {
        p--;
        length++;
    }

    return length;
}
```

### 83. Remove Duplicates from Sorted List
#### 题目原文
[https://leetcode.com/problemset/algorithms/](https://leetcode.com/problemset/algorithms/)
#### 解题思路

```c
struct ListNode* deleteDuplicates(struct ListNode* head)
{
    struct ListNode* cur = head;

    while (cur && cur->next) {
        struct ListNode* next = cur->next;
        while (next && cur->val == next->val) {
            cur->next = next->next;
            free(next);
            next = next->next;
        }
        cur = cur->next;
    }

    return head;
}
```

### 171. Excel Sheet Column Number
#### 题目原文
[https://leetcode.com/problems/excel-sheet-column-number/](https://leetcode.com/problems/excel-sheet-column-number/)
#### 解题思路
给定一个Excel表的列号如AB，计算它对应的整数28。
这个题可以参考10进制数的规律，每逢10进1；本题相当于26进制数([A-Z])，每逢26进1。

```c
int titleToNumber(char *s)
{
    int res = 0;
    int length = strlen(s);
    int i = 0;
    int tmp = 0;
    for (i = 0; i < length; i++) {
        tmp = (s[i] - 'A' + 1) * (int)pow(26, length - i - 1);
        res += tmp;
    }
    return res;
}
```

### 231. Power of Two
#### 题目原文
[https://leetcode.com/problems/power-of-two/](https://leetcode.com/problems/power-of-two/)
#### 解题思路

```c
bool isPowerOfTwo(int n)
{
    if (n > 0 && !(n & (n - 1))) {
        return true;
    } else {
        return false;
    }
}
```

### 237. Delete Node in a Linked List
#### 题目原文
[https://leetcode.com/problems/delete-node-in-a-linked-list/](https://leetcode.com/problems/delete-node-in-a-linked-list/)
#### 解题思路

```c
void deleteNode(struct ListNode* node)
{
    struct ListNode* tmp = node->next;
    node->val = node->next->val;
    node->next = node->next->next;
    free(tmp);
}
```

### 242. Valid Anagram
#### 题目原文
[https://leetcode.com/problems/valid-anagram/](https://leetcode.com/problems/valid-anagram/)
#### 解题思路

```c
bool isAnagram(char* s, char* t)
{
    if (NULL == s || t == NULL) {
        return false;
    }
    int len1 = strlen(s);
    int len2 = strlen(t);
    if (len1 != len2) {
        return false;
    }
    int cn1[26] = {0};
    int cn2[26] = {0};
    int i;
    for (i = 0; i < len1; i++){
        cn1[s[i] - 'a']++;
        cn2[t[i] - 'a']++;
    }
    for (i = 0; i < 26; i++) {
        if (cn1[i] != cn2[i]) {
            return false;
        }
    }
    return true;
}
```
