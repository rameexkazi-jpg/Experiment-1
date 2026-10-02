def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

result = fib(10)
print(f"Fibonacci(10) = {result}")
