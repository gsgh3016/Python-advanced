import sys

x = object()
print("ref count of x: ",  sys.getrefcount(x))
# return value is always 1 more

y = x
print("ref count of x: ", sys.getrefcount(x))

del y
print("ref count of x: ", sys.getrefcount(x))

# in cyclic GC

container = []
container.append(container)
print("\nref count of container: ", sys.getrefcount(container))

del container