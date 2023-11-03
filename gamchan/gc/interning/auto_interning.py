a = "hello"  # 리터럴로 생성된 문자열
b = "hello"
c = "".join(["h", "e", "l", "l", "o"])  # 동적으로 생성된 문자열

print(a is b)  # True
print(a is c)  # False
print(a == c)  # True