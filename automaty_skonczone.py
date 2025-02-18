import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

Q = ['q0', 'q1', 'q2', 'q3'] # zbiór stanów, q0 - stan początkowy
F = ['q3'] # stan akceptujący
sigma = [0, 1] # alfabet

def automat(ciąg, stan='q0'):
    for wyraz in ciąg:

        if stan == 'q0':
            if wyraz == 0:
                stan = 'q1'; print(f"delta(q0, 0) -> {stan}")
            elif wyraz == 1:
                stan = 'q0'; print(f"delta(q0, 1) -> {stan}")

        elif stan == 'q1':
            if wyraz == 0:
                stan = 'q3'; print(f"delta(q1, 0) -> {stan}")
            elif wyraz == 1:
                stan = 'q2'; print(f"delta(q1, 1) -> {stan}")

        elif stan == 'q2':
            if wyraz == 0:
                stan = 'q2'; print(f"delta(q2, 0) -> {stan}")
            elif wyraz == 1:
                stan = 'q0'; print(f"delta(q2, 1) -> {stan}")

        elif stan == 'q3':
            if wyraz == 0:
                stan = 'q2'; print(f"delta(q3, 0) -> {stan}")
            elif wyraz == 1:
                stan = 'q2'; print(f"delta(q3, 1) -> {stan}")
    if stan == 'q3':
        print('Końcowy stan to q3 - Akceptuję')
    else:
        print(f'Końsowy stan to {stan} - Odrzucam')

automat([1, 1, 1, 1, 1, 1, 0, 0,])

#2
Q = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'] # zbiór stanów, q0 - stan początkowy
F = ['q0', 'q4', 'q5'] # stany akceptujący
sigma = ['a', 'b', 'c'] # alfabet

delta = {
    ('q0', 'a'): 'q2',
    ('q0', 'b'): 'q2',
    ('q0', 'c'): 'q2',
    ('q1', 'a'): 'q4',
    ('q1', 'b'): 'q0',
    ('q1', 'c'): 'q3',
    ('q2', 'c'): 'q6',
    ('q2', 'a'): 'q1',
    ('q2', 'b'): 'q1',
    ('q3', 'a'): 'q3',
    ('q3', 'b'): 'q3',
    ('q3', 'c'): 'q3',
    ('q4', 'a'): 'q0',
    ('q4', 'b'): 'q5',
    ('q4', 'c'): 'q5',
    ('q5', 'a'): 'q4',
    ('q5', 'b'): 'q4',
    ('q5', 'c'): 'q4',
    ('q6', 'a'): 'q3',
    ('q6', 'b'): 'q3',
    ('q6', 'c'): 'q3'
}

ciąg = ['a', 'b', 'a', 'a', 'b', 'c', 'c', 'a']

G = nx.DiGraph()
last = 'q0'
for wyraz in ciąg:
    G.add_nodes_from(Q)

    for (start, symbol), meta in delta.items():
        G.add_edge(start, meta)

    pos = nx.circular_layout(G)

    nx.draw_networkx_nodes(G, pos, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, arrows=True, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=12)


    new = delta[(last, wyraz)]
    if new == last:
        nx.draw_networkx_edges(G, pos, edgelist=[(new, last)], arrows=True, edge_color='red')
    plt.annotate(text='', xy=pos[new], xytext=pos[last], arrowprops=dict(arrowstyle='->', shrinkA=15, shrinkB=15, color='red'))
    last = new

    plt.title('Graf z połączeniami z ciągu')
    plt.waitforbuttonpress()
    plt.close()


ciąg = 'aa10101'

def test_języka(ciąg):
    if len(ciąg) == 0: return print('język nierozpoznany')
    if ciąg[0] == 'a':

        for i in range(1, len(ciąg)):
            if ciąg[i] in ['0', '1']:
                pass
            else:
                break

        if ciąg[i] == 'a':
            if i+1 == len(ciąg):
                print('język rozpoznany')
            else:
                for j in range(i+1, len(ciąg)):
                    if ciąg[j] in ['0', '1']:
                        if j == len(ciąg) - 1: print('język rozpoznany')
                    else:
                        print('język nierozpoznany'); break
        else:
            print('język nierozpoznany')
    else:
        print('język nierozpoznany')

test_języka(ciąg)


def maszyna(str):
    stan = 'q0'
    funkcja = {
        'q0': {'a': 'q0', 'b': 'q1', 'c': 'q3', 'd': 'q3'},
        'q1': {'a': 'q3', 'b': 'q3', 'c': 'q2', 'd': 'q3'},
        'q2': {'a': 'q3', 'b': 'q3', 'c': 'q3', 'd': 'q2'},
        'q3': {'a': 'q3', 'b': 'q3', 'c': 'q3', 'd': 'q3'}
    }

    for symbol in str:
        if symbol not in ['a', 'b', 'c', 'd']:
            return print("Nieznany znak \njęzyk nierozpoznany")

        z1 = stan
        stan = funkcja[stan][symbol]
        print(f"f({z1}, {symbol}) = {stan}")

    if stan == 'q2':
        print('Końcowy stan q2 akceptuje - język rozpoznany')
    else:
        print('Końcowy stan =/= q2 - język nierozpoznany')

maszyna('abcdddd')