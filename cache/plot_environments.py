#
# Import packages
#

import numpy as np # For efficient array operations
import matplotlib.pyplot as plt # For plotting

try: # Seaborn makes prettier plots, but is not installed in a fresh Anaconda python
	import seaborn as sns 
	have_seaborn = True
except ImportError:
	have_seaborn = False

#
# Import other parts of the project
#

from constants import model_constants # Import model constants
from environment import * # Environment model

# Get model constants
constants = model_constants()

images = ["maritime.jpg","desert.jpg","nordic.jpg"]

if __name__ == '__main__':
	if have_seaborn: # initialize seaborn
		sns.set('poster',font_scale=1.5)
		sns.set_palette("bright", desat=.8)
		sns.set_context(rc={"figure.figsize": (10,7.5)})


	# plot environment
	t0 = np.arange(0,constants["L"]*constants["generations"])

	environments = []
	for (i,param) in enumerate(constants["environments"]):
		im = plt.imread(images[i])
		new_env = Environment(*param)
		environments.append(new_env)
		env_val = np.array(list(map(new_env.evaluate,t0)))

		plt.figure()
		plt.imshow(im,interpolation=None,extent=[0,t0[-1],-2,2],aspect="auto",alpha=.6)
		plt.plot(t0,env_val[:,0],label='E')
		plt.plot(t0,env_val[:,1],'.',label='C')
		plt.legend(loc='best')
		plt.ylim(-2,2)
		plt.xlim(0,t0[-1])
		plt.savefig('./environment_'+str(i+1)+'.pdf',bbox_inches='tight')