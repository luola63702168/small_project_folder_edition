#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Author  : rusi_
# coding:utf-8


class Node(object):
    '''节点'''

    def __init__(self, elem):
        # 数据区
        self.elem = elem
        # 连接区
        self.next = None


class SingleCycleLinkList(object):
    '''单向循环链表'''

    def __init__(self, node=None):
        self.__head = node
        if node:
            node.next = node

    def is_empty(self):
        '''链表是否为空'''
        return self.__head is None  # 这里是一个判断

    def length(self):
        """链表长度"""
        if self.is_empty():
            return 0
        else:
            # cur游标，用来移动遍历节点
            cur = self.__head
            count = 1  # cur=self.__head的那个节点(尾节点)也是需要被计数的。
            while cur.next != self.__head:
                count += 1
                cur = cur.next  # 游标运动的过程
            return count

    def travel(self):
        """遍历整个列表"""
        if self.is_empty():
            return
        else:
            cur = self.__head
            while cur.next != self.__head:
                print(cur.elem, end=' ')
                cur = cur.next
            # 退出循环的那个节点（尾节点）的那个值也得打印
            print(cur.elem)

    def add(self, item):
        """链表头部添加元素，头插法"""
        node = Node(item)
        if self.is_empty():
            self.__head = node
            node.next = node
            #  return
        else:
            cur = self.__head
            while cur.next != self.__head:
                cur = cur.next
            # 退出循环就代表游标已经处在尾节点了。
            node.next = self.__head
            self.__head = node
            # cur.next =
            cur.next = self.__head

    def append(self, item):
        """尾部添加元素,尾插法"""
        node = Node(item)  # 这个时候node已经实例化了,（也就具备节点所对应的两个属性了）
        if self.is_empty():
            self.__head = node
            node.next = node
        else:
            cur = self.__head
            while cur.next != self.__head:
                cur = cur.next  # 链接区一直指向下一个节点
            # cur.next=node
            # node.next=self.__head
            node.next = self.__head  # 等于 node.next = cur.next
            cur.next = node
        # node=Node(item)
        # if self.is_empty():
        #     self.__head=node
        #     node.next=self.__head
        # else:
        #     cur=self.__head
        #     while cur.next != self.__head:
        #         cur=cur.next
        #     node.next=self.__head
        #     cur.next=node

    def insert(self, pos, item):
        """
        指定位置插入元素
        :param pos:从零开始，在哪添加元素
        :param item: 添加的元素
        """
        if pos <= 0:
            self.add(item)
        elif pos > self.length() - 1:  # pos相当于索引，是要按照索引的级别进行比较的（而且不能相等--相等的时候意为在最后一个元素的前面添加一个元素，是插入，而不是追加）
            self.append(item)
        else:
            pre = self.__head
            count = 0
            while count < (pos - 1):  # 需要让添加的元素变为pos对应的索引，所以需要操作原本的该索引对应的前一个。
                count += 1
                pre = pre.next
            node = Node(item)
            # 当循环退出后 pre指向pos-1位置
            node.next = pre.next
            pre.next = node

    def remove_2(self, item):
        '''删除节点方法2'''
        if self.is_empty():
            return
        cur = self.__head
        pre = None
        while cur.next != self.__head:
            if cur.elem == item:
                if cur == self.__head:
                    # 头节点
                    # 找尾节点
                    rear = self.__head
                    while rear.next != self.__head:
                        rear = rear.next
                    self.__head = cur.next
                    rear.next = self.__head
                else:
                    # 中间节点
                    pre.next = cur.next
                # break
                return  # 为什么不用break？因为删完了就让该函数退出即可，break只能有终止此次循环的作用，有可能结束不了此程序
            else:
                pre = cur
                cur = cur.next
        # 退出循环代表尾节点
        if cur.elem == item:
            # 这个判断和上面的那个判断是否为头节点的语法不矛盾，因为只要退出循环了就说明cur.next==self.__head了，下面的这个判断，其实包含了两个判断语句。
            # 而上面的那个，也是在cur.next != self.__head的条件下，判断 cur == self.__head的。
            if cur == self.__head:  # 此时代表链表中只有一个节点（尾节点也是头节点） if self.length()==1
                self.__head = None
            else:
                pre.next = cur.next

    def search(self, item):
        """查找节点是否存在"""
        if self.is_empty():
            return False  # return 终止程序，所以不需要else
        cur = self.__head
        while cur.next != self.__head:
            if item == cur.elem:
                return True
            else:
                cur = cur.next
        if cur.elem == item:  # 判断尾节点
            return True
        else:
            return False


if __name__ == '__main__':
    ll = SingleCycleLinkList()
    print(ll.is_empty())
    print(ll.length())

    ll.append(1)
    print(ll.is_empty())
    print(ll.length())

    ll.append(2)
    ll.append(3)
    ll.append(4)
    ll.append(5)
    ll.append(6)
    ll.add(2)
    ll.insert(2, 7)
    print(ll.search(7))
    ll.remove_2(2)
    ll.remove_2(7)
    ll.travel()
    print(ll.search(7))
