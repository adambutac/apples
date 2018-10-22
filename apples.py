import sys
import random
import time

class Apple:
    inp = {} 
    out = {}
    key = None
    sum = None

    def __init__(self, prt, val):
        if not (prt == None):
            self.inp = {}

        if not (val == None):
            self.out = {}
            self.key = val
            self.sum = 0

        if not(prt == None):
            self.inp[prt] = 1
            prt.out[self] = 1
            prt.sum += 1
            
    def append(self, vtx):
        ##vertex has an outgoing edge
        if vtx in self.out:
            ##inc weight on edge
            self.out[vtx] += 1
            if not (vtx.inp == None):
                vtx.inp[self] += 1
        else:
            ##new edge
            self.out[vtx] = 1
            if not (vtx.inp == None):
                vtx.inp[self] = 1

        self.sum += 1

    def bite(self):
        rng = random.randint(0, self.sum)
        idx = 0
        
        for i in self.out:
            idx += self.out[i]
            if(rng <= idx):
                return i

        return None

    def gex(self):
        chain = []
        apple = self
        while(apple.key):
            chain.append(apple)
            apple = apple.bite()
        return chain

    def toString(self, V):
        if(self.key == None):
            return "[None]"
        if(self.key in V):
            return str(self.key)

        V.append(self.key)
        return  str(self.key) + "".join(["\n\t" + i.toString(V) for i in self.out])

def learn(s):
    root = Apple(None, "root")
    null = Apple(None, None)

    G = {}
    for w in s:
        apple = root
        for l in w:
            if l in G:
                apple.append(G[l])
                apple = G[l]
            else:
                apple = Apple(apple, l)
                G[l] = apple

        apple.append(null)

    return root

def words(FILE):
    return [w.strip(' \t\n\r') for w in FILE]

def sentences(FILE, delim):
    # turn s into a list of sentences 
    s = []
    s.append([])
    w = ""
    for li in FILE:
        for ch in li:
            w += ch
            if(ch in delim):
                s[-1].append(w)
                s.append([])
                w = ""
            elif(ch == ' '):
                s[-1].append(w)
                w = ""
    return s

def sentences2(FILE, prelim, delim):
    s = []
    s.append([])
    plm = " " * len(prelim)
    dlm = " " * len(delim)

    # turn s into a list of sentences 
    w = None 
    for li in FILE:
        for ch in li:
            plm = plm[1:] + ch
            dlm = dlm[1:] + ch

            if not (w == None):
                w += ch
                if(ch == ' '):
                    s[len(s) - 1].append(w)
                    w = ""           # start a new sentence
            if(plm == prelim):
                w = ""
                s.append([])
            # end the sentence
            if(dlm == delim):
                w = w[:-len(delim)]
                s[len(s) - 1].append(w)
                w = None
            # start a new word

    return s

def binary(FILE):
    b = []
    byte = FILE.read(1)
    while byte != "":
        b.append(byte)
        byte = FILE.read(1)
    return b

def run(root, s):
    avg = [len(i) for i in s]
    avg = sum(avg) / float(len(s))
    total = 0
    n = 0

    while(True):
        print("".join([i.key for i in root.bite().gex()]))

def main():
    if len(sys.argv) < 2 :
        return

    FILE=open(sys.argv[1])

    seed = random.getrandbits(8)
    random.seed(seed)
    # populate graph
    #s = sentences2(FILE, "<p>", "</p>")
    s = sentences(FILE, ".")
    #s = words(FILE)
    #s = binary(FILE)
    root = learn(s)
    #print(root.toString([]))
    #print("seed: ", seed)
    run(root, s)

main()
