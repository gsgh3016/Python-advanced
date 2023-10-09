import gc
import sys

gc.collect()

class Link:
    def __init__(self, next_link=None):
        self.next_link = next_link
        
        
link_3 = Link()
link_2 = Link(link_3)
link_1 = Link(link_2)

link_3.next_link = link_1

A = link_1
print(f"link_1: {sys.getrefcount(link_1)}, ", end="")
print(f"link_2: {sys.getrefcount(link_2)}, ", end="")
print(f"link_3: {sys.getrefcount(link_3)}")
del link_1, link_2, link_3

link_4 = Link()
link_4.next_link = link_4
print(f"link_4: {sys.getrefcount(link_4)}")
del link_4

print(f"unreachable: {gc.collect()}")