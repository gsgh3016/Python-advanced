import sys

a = sys.intern("hello world")  # 명시적으로 intern
b = "hello world"
c = " ".join(["hello", "world"])  # 동적으로 생성

print(a is b)  # False
print(a is c)  # False

b = sys.intern(b)
c = sys.intern(c)

print(a is b)  # True
print(a is c)  # True