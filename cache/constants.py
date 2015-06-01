def model_constants():
	constants = {
		"population_size": 		5000, 
		"generations": 			5000, 
		"L": 					5, 
		"kd": 					0.02, 
		"ka": 					0.01, 
		"tau": 					0.25, 
		"q": 					2.2, 
		"mu":					0.001,
		"environments":			[(0.1,0.6,0.,0.),(.6,1.0,0.,0.5),(.5,1.0,0.,-0.7)],
		"environment_names":	["moderate","warm","cold"],
		"km":					0.2
		}
	return constants
