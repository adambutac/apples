import sys
import random

class Apple:
    def __init__(self, prt, val, ctx=None):
        self.inp = {}
        self.out = {}
        self.key = val
        self.sum = 0
        ##the last n tokens this node stands for (for toString)
        self.ctx = ctx if not (ctx == None) else val

        if not(prt == None):
            self.inp[prt] = 1
            prt.out[self] = 1
            prt.sum += 1
            
    def append(self, vtx):
        ##vertex has an outgoing edge
        if vtx in self.out:
            ##inc weight on edge
            self.out[vtx] += 1
            vtx.inp[self] += 1
        else:
            ##new edge
            self.out[vtx] = 1
            vtx.inp[self] = 1

        self.sum += 1

    def bite(self):
        rng = random.randint(1, self.sum)
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

    def name(self):
        if(self.key == None):
            return "[END]"
        ##escape whitespace so spaces/newlines in a context stay visible
        return repr("".join(self.ctx))[1:-1].replace(" ", "_")

    def toString(self):
        ##one line per node: context -> next contexts with edge weights
        lines = []
        V = {self}
        queue = [self]
        for apple in queue:
            if(apple.key == None):
                continue
            edges = sorted(apple.out.items(), key=lambda e: -e[1])
            lines.append(apple.name() + " -> " + ", ".join([i.name() + " x" + str(c) for i, c in edges]))
            for i, c in edges:
                if not (i in V):
                    V.add(i)
                    queue.append(i)
        return "\n".join(lines)

def learn(s, n):
    root = Apple(None, "root")
    null = Apple(None, None)

    G = {}
    for w in s:
        ##skip blank lines / empty sentences
        if not w:
            continue

        apple = root
        for i in range(len(w)):
            ##state is the last n tokens (fewer at the start of w)
            ctx = tuple(w[max(0, i - n + 1):i + 1])
            if ctx in G:
                apple.append(G[ctx])
                apple = G[ctx]
            else:
                apple = Apple(apple, w[i], ctx)
                G[ctx] = apple

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
            if(dlm == delim and not (w == None)):
                w = w[:-len(delim)]
                s[len(s) - 1].append(w)
                w = None
            # start a new word

    return s

def binary(FILE):
    # the whole file is one long sequence of characters
    return [FILE.read()]

def run(root, s):
    ##nothing was learned (empty input)
    if root.sum == 0:
        return

    while(True):
        print("".join([i.key for i in root.bite().gex()]))

def main():
    if len(sys.argv) < 2 :
        return

    FILE=open(sys.argv[1])
    # how many previous tokens each state remembers
    order = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    seed = random.getrandbits(8)
    random.seed(seed)
    # populate graph
    #s = sentences2(FILE, "<p>", "</p>")
    #s = sentences(FILE, ".")
    s = words(FILE)
    #s = binary(FILE)
    root = learn(s, order)
    #print(root.toString())
    #print("seed: ", seed)
    run(root, s)

main()
