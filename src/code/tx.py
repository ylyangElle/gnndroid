import sys

from matplotlib.pyplot import flag
from pip import main

class ListNode:
    def __init__(self,x) -> None:
        self.val = x
        self.next = None
        
        
class Solution:
    
    def tolist(self,l):
        res = []
        while l is not None:
            res.append(l.val)
        return res
    

    
    def solve(self,a):
        arr = []
        arr_list = []
        for iter in a:
            arr.extend(self.tolist(iter))
        n = len(arr)
        arr_list = arr[0]
        for i in range(1,n):
           arr_list = list(set(arr_list).union(set(arr[i])))
        
        index = 0
        m_min = sys.maxsize
        for i in range(0,n):
            if arr_list[i] < m_min:
                m_min = arr_list[i]
                index = i
        
        left = i-1
        right = i+1
        flag = True
        while right < n and left >= 0:
            if(arr_list[right]<arr_list[left]):
                flag = False
                break
            elif arr_list[left] == arr_list[right]:
                continue
            
        res = ListNode(arr_list[index])
        temp_index = index
        if flag is True:
            temp_index+=1
        elif flag is False:
            temp_index-=1
        while temp_index != index:
            if flag is True:
                temp_index+=1
            elif flag is False:
                temp_index-=1
            temp = ListNode(arr_list[temp_index])
            res.next = temp
        return res
    

    