symbols = '$¢£¥€¤'

# if genexp is the single parameter, no need to duplicate enclosing parentheses
print(tuple(ord(symbol) for symbol in symbols))

import array
print(array.array('I', (ord(symbol) for symbol in symbols)))


# here the six-item list of T-shirts is never build in memory: the generator expression
# feeds the for loop producing one item at a time.
# If the two lists used in the Cartesian product had a thousand items each, using a generator
# expression wold save the cost of building a list whit a million items just to feed the for
# loop
colors = ['black', 'white']
sizes = ['S', 'M', 'L']

# the genexp yields items one by one, a list with all six T-shirt variations
# is never produced in this example
for tshirt in (f'{c} {s}' for c in colors for s in sizes):
    print(tshirt)