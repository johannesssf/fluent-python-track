import numpy as np

from typing import SupportsComplex


c64 = np.complex64(3+4j)  # 1
print(isinstance(c64, complex))  # 2
print(isinstance(c64, SupportsComplex))  # 3
c = complex(c64)  # 4
print(c)
print(isinstance(c, SupportsComplex))  # 5
print(complex(c))
