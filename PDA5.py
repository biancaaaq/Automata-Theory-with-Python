import sys #am importat pentru a rula din terminal
import json  #am importat pentru a citi dintr-un fisier json


class PDA:
    def __init__(self, states, alphabet, stack_alphabet, transitions, start_state, start_stack_symbol, accept_states):   #initializez PDA-ul
        self.states = states                          #stari
        self.alphabet = alphabet                       #alfabet
        self.stack_alphabet = stack_alphabet           #stiva
        self.transitions = transitions                 #tranzitii
        self.start_state = start_state                 #starea de inceput
        self.start_stack_symbol = start_stack_symbol       #starea de inceput pentru stiva
        self.accept_states = accept_states               #starile acceptate

    def to_cfg(self):                   #converteste PDA-il intr-un CFG
        variables = set()            #multimea variabilelor, am ales multime ca sa ne asiguram ca fiecare variabila e unica
        productions = []             #lista de produse, va fi o pereche lhs, rhs adica partea stanga sau dreapta/
        start_symbol = f"S_{self.start_state}_{self.start_stack_symbol}" #simbolul de inceput contine starea initiala si simbolul initial al stivei

        for transition in self.transitions:
            (current_state, input_symbol, stack_top), (next_state, stack_push) = transition  #imparte fiecare tranzitie in componente
            if stack_push == '':   #verifica daca nu se pune nimic pe stiva
                stack_push = [stack_top]     #simpbolul din varful stivei ramane neschimbat si il transformam in stiva
            else:
                stack_push = list(stack_push)    
            for stack_symbol in self.stack_alphabet:   #pentru fiecare simbol din alfabetul stivei
                variables.add(f"A_{current_state}_{stack_symbol}")       #genereaza variabilele si produsele pentru fiecare combinatie posibila si o adauga
                rhs = f"{input_symbol}A_{next_state}_{stack_push[0]}"     #partea dreapta
                productions.append((f"A_{current_state}_{stack_top}", rhs))    #adauga produsul

        for state in self.accept_states:
            for stack_symbol in self.stack_alphabet:
                productions.append((f"A_{state}_{stack_symbol}", "")) #adauga produsul care permite eliminarea simbolului stivei cand se afla intr-o stare de acceptare
                #cand  partea dreapta a produsului este goală simbolul poate fi eliminat

        variables.add(start_symbol)
        return CFG(start_symbol, variables, productions)


class CFG:
    def __init__(self, start_symbol, variables, productions):
        self.start_symbol = start_symbol
        self.variables = variables
        self.productions = productions

    def save_to_file(self, file_path):    #functie pentru scrierea CFG-ului
        with open(file_path, 'w') as file:
            file.write("NonTerminals\n")
            for var in self.variables:
                file.write(f"{var}\n")
            file.write("End\n")

            file.write("Terminals\n")
            terminals = set()
            for lhs, rhs in self.productions:
                for symbol in rhs:
                    if symbol.islower():  # terminalele sunt scrise cu minuscule
                        terminals.add(symbol)
            for term in terminals:
                file.write(f"{term}\n")
            file.write("End\n")

            file.write("Productions\n")
            for lhs, rhs in self.productions:
                file.write(f"{lhs} -> {rhs}\n")
            file.write("End\n")

            file.write("StartSymbol\n")
            file.write(f"{self.start_symbol}\n")
            file.write("End\n")


def read_pda_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)         #citim dintr-un fisier json
        pda = PDA(
            states=config['states'],
            alphabet=config['alphabet'],
            stack_alphabet=config['stack_alphabet'],
            transitions=[(tuple(k), tuple(v)) for k, v in config['transitions']],
            start_state=config['start_state'],
            start_stack_symbol=config['start_stack_symbol'],
            accept_states=config['accept_states']
        )
        return pda


def main():
    if len(sys.argv) != 3:
        print("Usage: python conv_pda_to_cfg.py <pda_config_file> <cfg_config_file>")
        return

    pda_config_file = sys.argv[1]
    cfg_config_file = sys.argv[2]

    pda = read_pda_config(pda_config_file)
    cfg = pda.to_cfg()
    cfg.save_to_file(cfg_config_file)


if __name__ == "__main__":
    main()
