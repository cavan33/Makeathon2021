def accScore (ax, ay, az):
	"""
	Takes the 3 values of an instantaneous acceleration and 
	returns a health score from them
	"""
	score = 100-(ax+ay+az)
	return(score)