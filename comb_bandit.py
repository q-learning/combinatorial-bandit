import numpy as np
import pdb

np.random.seed(1337)

Trial_List = None
Score_List = None

# Sample Reward function which has a bias towards the latest items
def blackboxScore(trial):
	return np.sum(trial * np.arange(len(trial)).reshape(-1,1)).reshape(1,1)

# Checks the ratio of items at top 25% samples while also exploring
def getChance(worst_ratio = 0.75):
	half_len = int(Trial_List.shape[1]*0.75)
	half = np.sum(Trial_List[:,:half_len], axis=1)
	total = np.sum(Trial_List, axis=1) + 1
	chance = 1.0 - np.true_divide(half, total)

	half_len = int(Trial_List.shape[1]*0.9)
	best = np.mean(Trial_List[:,half_len:], axis=1).ravel() + 1.0

	novelty = 1.0 - np.mean(Trial_List, axis=1).ravel()
	return chance * novelty * best

# Samples item subsets based on chances computed at the previous step
def generateTrial(trial_len, k = 5):
	if Trial_List is None:
		Chances = np.ones(trial_len)
	else:
	    Chances = getChance()
	Chances /= np.sum(Chances)
	rand_vec = np.random.multinomial(k, Chances)
	rand_vec[rand_vec > 1] = 1
	return rand_vec.reshape(-1, 1)

# Total number of items to select from
No_Items = 100
No_Select = 5
accuracy = 0.0

while accuracy < 1.0:
	trial = generateTrial(No_Items, No_Select)

	if Trial_List is None:
		Trial_List = trial
	else:
		while not any(np.equal(Trial_List,trial).all(1)):
			print('skip duplicate')
			trial = generateTrial(No_Items, No_Select)
		Trial_List = np.concatenate((Trial_List, trial), axis = 1)

	#print(Trial_List[:, -1])
	score = blackboxScore(trial)

	if Score_List is None:
		Score_List = score
	else:
		Score_List = np.concatenate((Score_List, score), axis = 1)

	# Sorts Trial and Score lists simultaneously according to the Score list
	ind = np.unravel_index(np.argsort(Score_List, axis=None), Score_List.shape)

	Score_List = Score_List[:,ind[1]]
	Trial_List = Trial_List[:,ind[1]]
	best_trial = Trial_List[:, -1]
	print(best_trial)
	accuracy = np.mean(best_trial[-No_Select:])
	print(accuracy)
	print(Trial_List.shape[1])
