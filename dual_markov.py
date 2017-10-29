import pickle
import os

class DualMarkov():
    def __init__(self, ids):
        self.chains = dict()

        if not os.path.exists('markov'): os.makedirs('markov')
        for id in ids:
            fname = 'markov/{}'.format(id)
            try:
                fname = 'markov/{}'.format(id)
                print("Loading markov chains from {}".format(fname)) 
                with open(fname, 'r') as fp:
                    self.chains[id] = pickle.load(fp)
            except Exception:
                open(fname, 'a').close()
                self.chains[id] = dict()
                
    def register(self, id, text):
        pass
