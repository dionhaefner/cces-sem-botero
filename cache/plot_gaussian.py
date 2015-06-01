import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set('poster',font_scale=1.5)

from animal import Animal

foo = Animal()
x = np.linspace(-4,4,400)
y = [foo._scale(X) for X in x]

plt.plot(x,y)
plt.xlabel("Gene")
plt.ylabel("Scale factor $f($Gene$)$")
plt.savefig("gaussian.pdf",bbox_inches='tight')