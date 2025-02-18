import math
import matplotlib.pyplot as plt
import networkx as nx


print('\nZADANIE 1\n')

class MT :

    def __init__(self):
        self.zb_stnw = set()
        self.alfbt_wej = set()
        self.alfbt_tsm = set()
        self.fun_prz = {}
        self.stn_p = ''
        self.stn_ak = ''
        self.stn_od = ''
    def start(self, zb_stnw, alfbt_wej , alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od) :
        self.zb_stnw = zb_stnw
        self.alfbt_wej = alfbt_wej
        self.alfbt_tsm = alfbt_tsm
        self.fun_prz = fun_prz
        self.stn_p = stn_p
        self.stn_ak = stn_ak
        self.stn_od = stn_od


    def simulate(self, word):
        tape = list(word)
        head = 0
        state = self.stn_p

        print("Wejście taśmy:", ''.join(tape))
        print("Stan początkowy:", state)

        while state != self.stn_ak and state != self.stn_od:
            current_symbol = tape[head]

            if (current_symbol, state) in self.fun_prz:
                new_symbol, move, new_state = self.fun_prz[(current_symbol, state)]
                tape[head] = new_symbol
                if move == 'R':
                    head += 1
                    if head == len(tape):
                        tape.append(' ')
                elif move == 'L':
                    head -= 1
                    if head < 0:
                        tape.insert(0, ' ')
                state = new_state

                print("Taśma:", ''.join(tape))
                print("Stan obecny:", state)
            else:
                state = self.stn_od

        return ''.join(tape), state



zb_stnw = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'qa', 'qr'}
alfbt_wej = {'a', 'blank'}
alfbt_tsm = {'a', 'blank', 'a.', '/a'}
fun_prz = {
    ('a', 'q0'): ('a.', 'R', 'q1'),
    ('blank', 'q0'): ('blank', 'L', 'qr'),  
    ('/a', 'q1'): ('/a', 'R', 'q1'),
    ('blank', 'q1'): ('blank', 'L', 'qa'),  
    ('a', 'q1'): ('a', 'L', 'q2'),
    ('/a', 'q2'): ('/a', 'L', 'q2'),
    ('a.', 'q2'): ('a.', 'L', 'q3'),
    ('/a', 'q3'): ('/a', 'R', 'q3'),
    ('a', 'q3'): ('a', 'R', 'q4'),
    ('a.', 'q3'): ('a.', 'R', 'q4'),
    ('a', 'q3'): ('/a', 'R', 'q5'),
    ('blank', 'q3'): ('blank', 'L', 'q6'),  
    ('/a', 'q4'): ('/a', 'R', 'q4'),
    ('blank', 'q4'): ('blank', 'L', 'qr'),  
    ('a', 'q4'): ('/a', 'R', 'q5'),
    ('/a', 'q5'): ('/a', 'R', 'q5'),
    ('a', 'q5'): ('/a', 'R', 'q3'),
    ('blank', 'q5'): ('blank', 'L', 'qr'),  
    ('a', 'q6'): ('a', 'L', 'q6'),
    ('/a', 'q6'): ('/a', 'L', 'q6'),
    ('a.', 'q6'): ('a.', 'R', 'q1')
}

stn_p = 'q0'
stn_ak = 'qa'
stn_od = 'qr'


mt = MT()
mt.start(zb_stnw, alfbt_wej, alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od)
word = "aaablank"
result, final_state = mt.simulate(word)
print("Taśma na wyjściu:", result)
print("Stan końcowy", final_state)


print('\nZADANIE 2\n')

class MT:  
    def __init__(self):
        self.zb_stnw = set() 
        self.alfbt_wej = set()  
        self.alfbt_tsm = set()  
        self.fun_prz = {}  
        self.stn_p = ''
        self.stn_ak = ''  
        self.stn_od = '' 
        self.path_taken = []

    def initialize(self, zb_stnw, alfbt_wej, alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od):
        self.zb_stnw = zb_stnw
        self.alfbt_wej = alfbt_wej
        self.alfbt_tsm = alfbt_tsm
        self.fun_prz = fun_prz
        self.stn_p = stn_p
        self.stn_ak = stn_ak
        self.stn_od = stn_od

    def start(self, word):  
        tape = list(word)
        head = 0
        state = self.stn_p
        self.path_taken.append(state)

        print("Wejście taśmy:", ''.join(tape))
        print("Stan początkowy:", state)

        while state != self.stn_ak and state != self.stn_od:
            current_symbol = tape[head]

            if (current_symbol, state) in self.fun_prz:
                new_symbol, move, new_state = self.fun_prz[(current_symbol, state)]
                tape[head] = new_symbol
                if move == 'R':
                    head += 1
                    if head == len(tape):
                        tape.append(' ')
                elif move == 'L':
                    head -= 1
                    if head < 0:
                        tape.insert(0, ' ')
                state = new_state
                self.path_taken.append(state)

                print("Taśma:", ''.join(tape))
                print("Stan obecny:", state)
            else:
                state = self.stn_od

        return ''.join(tape), state

    def draw_graph(self, draw_transitions=False, draw_labels=False):
        G = nx.DiGraph()
        G.add_nodes_from(self.zb_stnw)

        for transition, effect in self.fun_prz.items():
            if draw_labels:
                G.add_edge(transition[1], effect[2], label=transition[0] + " -> " + effect[0] + ", " + effect[1])
            else:
                G.add_edge(transition[1], effect[2])

        pos = nx.kamada_kawai_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', font_size=10, arrows=True)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        path_edges = [(self.path_taken[i], self.path_taken[i+1]) for i in range(len(self.path_taken)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

        if self.stn_p == self.stn_od:
            nx.draw_networkx_edges(G, pos, edgelist=[(self.stn_p, self.stn_od)], arrows=True, edge_color='red')
            plt.annotate(text='', xy=pos[self.stn_p], xytext=pos[self.stn_od],
                         arrowprops=dict(arrowstyle='->', shrinkA=15, shrinkB=15, color='red'))

        plt.title('Graf działania MT')
        plt.show()


zb_stnw = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'qa', 'qr'}  
alfbt_wej = {'0', '1', 'b'}  
alfbt_tsm = {'0', '1', 'b', '/0', '/1', 'blank'}  
fun_prz = {  
    ('0', 'q0'): ('/0', 'R', 'q2'),
    ('1', 'q0'): ('/1', 'R', 'q3'),
    ('b', 'q0'): ('b', 'R', 'q1'),
    ('/0', 'q1'): ('/0', 'R', 'q1'),
    ('/1', 'q1'): ('/1', 'R', 'q1'),
    ('blank', 'q1'): ('blank', 'L', 'qa'),
    ('0', 'q1'): ('0', 'L', 'qr'),
    ('1', 'q1'): ('1', 'L', 'qr'),
    ('0', 'q2'): ('0', 'R', 'q2'),
    ('1', 'q2'): ('1', 'R', 'q2'),
    ('b', 'q2'): ('b', 'R', 'q4'),
    ('blank', 'q2'): ('blank', 'R', 'qr'),
    ('0', 'q3'): ('0', 'R', 'q3'),
    ('1', 'q3'): ('1', 'R', 'q3'),
    ('b', 'q3'): ('b', 'R', 'q5'),
    ('blank', 'q3'): ('blank', 'R', 'qr'),
    ('/0', 'q4'): ('/0', 'R', 'q4'),
    ('/1', 'q4'): ('/1', 'R', 'q4'),
    ('0', 'q4'): ('/0', 'L', 'q6'),
    ('1', 'q4'): ('1', 'R', 'qr'),
    ('blank', 'q4'): ('blank', 'R', 'qr'),
    ('/0', 'q5'): ('/0', 'R', 'q5'),
    ('/1', 'q5'): ('/1', 'R', 'q5'),
    ('1', 'q5'): ('/1', 'L', 'q6'),
    ('0', 'q5'): ('0', 'R', 'qr'),
    ('blank', 'q5'): ('blank', 'R', 'qr'),
    ('/0', 'q6'): ('/0', 'L', 'q6'),
    ('/1', 'q6'): ('/1', 'L', 'q6'),
    ('b', 'q6'): ('b', 'L', 'q7'),
    ('0', 'q7'): ('0', 'L', 'q7'),
    ('1', 'q7'): ('1', 'L', 'q7'),
    ('/0', 'q7'): ('/0', 'R', 'q0'),
    ('/1', 'q7'): ('/1', 'R', 'q0')
}

stn_p = 'q0'  
stn_ak = 'qa'  
stn_od = 'qr' 


tm = MT() 
tm.initialize(zb_stnw, alfbt_wej, alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od)
word = "1b1b0"
result, final_state = tm.start(word)  
print("Tape output:", result)
print("Final state:", final_state)

tm.draw_graph(draw_transitions=True, draw_labels=True)

print('\nZADANIE 3\n')

sigma = ['e', 'h', 'f'] 
x = 'x'  
w1 = ['x']
w2 = ['h', 'e', 'x', 'h', 'f']
w3 = ['h', 'e', 'x', 'h', 'f' ,'f']
def start(alfbt, word):
    def decyzja():
        if len(word) == 1:
            if word[0] == 'x':
                return 1
            else:
                return 0
        elif len(word) % 2 == 0:
            return 0

        hlf = math.floor(len(word) / 2)
        if word[hlf] == 'x':
            st = word[:hlf]
            nd = word[hlf + 1:]

            for elem in st + nd:
                if elem not in alfbt:
                    return 0

            if len(st) == len(nd):
                return 1
        else:
            return 0

    if decyzja() == 1:
        print('Język rozstrzygnięty')
    else:
        print('Język nierozstrzygnięty')

start(sigma, w1)
start(sigma, w2)
start(sigma, w3)


# 1. Jeśli pierwszy symbol to nie : a, blank : ODRZUĆ
# 2. Jeśli to : a lub blank, przejdź w PRAWO
# 3. Jeśli symbol to a, zamień go na b i przejdź w PRAWO
# 4.     Wpp. ODRZUĆ
# 5. Jeśli symbol to b, przejdź w LEWO i AKCEPTUJ
# 6. Jeśli symbol to c, przejdź w LEWO
# 7. Jeśli symbol to a lub blank, przejdź w PRAWO i ODRZUĆ
# 8. Jeśli symbol to b, zamień na a, i przejdź w PRAWO, oraz cofnij się do punku 2.

print('\nZADANIE 4\n')

class MT :

    def __init__(self):
        self.zb_stnw = set()
        self.alfbt_wej = set()
        self.alfbt_tsm = set()
        self.fun_prz = {}
        self.stn_p = ''
        self.stn_ak = ''
        self.stn_od = ''
    def start(self, zb_stnw, alfbt_wej , alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od) :
        self.zb_stnw = zb_stnw
        self.alfbt_wej = alfbt_wej
        self.alfbt_tsm = alfbt_tsm
        self.fun_prz = fun_prz
        self.stn_p = stn_p
        self.stn_ak = stn_ak
        self.stn_od = stn_od


    def simulate(self, word):
        tape = list(word)
        head = 0
        state = self.stn_p

        print("Wejście taśmy:", ''.join(tape))
        print("Stan początkowy:", state)

        while state != self.stn_ak and state != self.stn_od:
            current_symbol = tape[head]

            if (current_symbol, state) in self.fun_prz:
                new_symbol, move, new_state = self.fun_prz[(current_symbol, state)]
                tape[head] = new_symbol
                if move == 'R':
                    head += 1
                    if head == len(tape):
                        tape.append(' ')
                elif move == 'L':
                    head -= 1
                    if head < 0:
                        tape.insert(0, ' ')
                state = new_state

                print("Taśma:", ''.join(tape))
                print("Stan obecny:", state)
            else:
                state = self.stn_od

        return ''.join(tape), state



zb_stnw = {'q0', 'q1', 'q2', 'q3','qa', 'qr'}
alfbt_wej = {'a', 'blank'}
alfbt_tsm = {'a', 'blank', 'b.', 'c'}
fun_prz = {
    ('a', 'q0'): ('a', 'R', 'q1'),
    ('blank', 'q0'): ('blank', 'R', 'q1'),  
    ('a', 'q1'): ('b', 'R', 'q2'),
    ('b', 'q2'): ('b', 'L', 'qa'),
    ('c', 'q2'): ('c', 'L', 'q3'),
    ('b', 'q3'): ('a', 'L', 'q1'),
    ('blank', 'q3'): ('blank', 'L', 'q1'),
    ('a', 'q3'): ('a', 'R', 'qr'),
    ('blank', 'q3'): ('blank', 'R', 'qr'),
}

stn_p = 'q0'
stn_ak = 'qa'
stn_od = 'qr'


mt = MT()
mt.start(zb_stnw, alfbt_wej, alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od)
word = "aaablank"
result, final_state = mt.simulate(word)
print("Taśma na wyjściu:", result)
print("Stan końcowy", final_state)
