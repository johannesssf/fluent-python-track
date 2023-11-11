from decimal import Decimal, getcontext

ctx = getcontext()
print(ctx.prec)
ctx.prec = 40
print(ctx.prec)

result = 1 / 3
print(result)

print(result == result)
ctx.prec = 28
print(result == +result)
