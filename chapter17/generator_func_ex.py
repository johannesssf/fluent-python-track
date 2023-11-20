def gen_AB():
    print('start')
    yield 'A'  # 1
    print('continue')
    yield 'B'  # 2
    print('end.')  # 3

# for use
# for c in gen_AB():  # 4
#     print('-->', c)  # 5

res1 = [x*3 for x in gen_AB()]  # 2
print(type(res1))


for i in res1:  # 3
    print('-->', i)


# generator expression
res2 = (x*3 for x in gen_AB())  # 4
print(res2)
for i in res2:  # 5
    print('-->', i)
