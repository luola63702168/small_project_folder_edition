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


class SingleLinkList(object):
    '''单链表'''

    def __init__(self, node=None):  # node默认为none
        self.__head = node  # 私有属性,对象无法访问,可以导入
        # self._head = 1  # 禁止导入,可以访问

    def is_empty(self):
        '''链表是否为空'''
        # print(node.elem)
        return self.__head is None  # 这里是一个判断

    def length(self):
        """链表长度"""
        # cur游标，用来移动遍历节点
        cur = self.__head
        count = 0
        # cur.next == None不可作为判断条件，因为链接区为None的时候，数据区实际上是有数据的，如果使用这个条件，那么这个数据将不被计入，游标也不会加1。
        # 但是当节点为None时，意味着数据区已经没有数据，而且之前的那个cur.next == None时的数据区的数据也已经被计入了。
        while cur is not None:
            count += 1
            cur = cur.next  # 游标运动的过程
        return count

    def travel(self):
        """遍历整个列表"""
        cur = self.__head
        while cur is not None:
            print(cur.elem, end=' ')
            cur = cur.next
        print('')

    def add(self, item):
        """链表头部添加元素，头插法"""
        node = Node(item)
        node.next = self.__head
        self.__head = node

    def append(self, item):
        """尾部添加元素,尾插法"""
        node = Node(item)  # 这个时候node已经实例化了,（也就具备节点所对应的两个属性了）
        if self.is_empty():
            self.__head = node
        else:
            cur = self.__head
            while cur.next is not None:
                cur = cur.next  # 链接区一直指向下一个节点
            cur.next = node  # 将本为空的这个链接区，指向下个节点，使之不为空。

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

    def remove(self, item):
        """删除节点"""
        pre = self.__head
        if pre.elem == item:
            self.__head = pre.next  # 头节点换为头节点链接的下一个节点。
        else:
            while pre.next is not None:
                if pre.next.elem == item:
                    pre.next = pre.next.next
                else:
                    pre = pre.next

    def remove_2(self, item):
        '''删除节点方法2'''
        cur = self.__head
        pre = None
        while cur is not None:
            if cur.elem == item:
                if cur == self.__head:
                    self.__head = cur.next
                else:
                    pre.next = cur.next
                break
            else:
                pre = cur
                cur = cur.next

    def search(self, item):
        """查找节点是否存在"""
        cur = self.__head
        while cur is not None:
            if item == cur.elem:
                return True
            else:
                cur = cur.next
        return False

    def __call__(self, *args, **kwargs):
        '''打印该列表'''
        cur = self.__head
        if cur is None:
            return None
        else:
            s_tr = ''
            while cur is not None:
                if cur.next is not None:
                    s_tr += str(cur.elem) + '，'
                else:
                    s_tr += str(cur.elem)
                cur = cur.next
            s_tr = '<' + s_tr + '>'
            return s_tr


if __name__ == '__main__':
    ll = SingleLinkList()
    print(ll.is_empty())
    print(ll.length())

    print(ll())

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
    ll.remove(2)
    ll.remove_2(7)
    ll.travel()
    print(ll())
    