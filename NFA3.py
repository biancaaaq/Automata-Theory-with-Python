class NFA:
    def __init__(self, filename):
        self.filename = filename
        self.sigma = set()  # Alfabetul
        self.states = {}  # Starile
        self.transitions = []  # Tranzitiile

    def validare(self):
        with open(self.filename, 'r') as file:
            section = None
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Setarea sectiunii
                if 'Sigma' in line:
                    section = 'Sigma'
                elif 'States' in line:
                    section = 'States'
                elif 'Transitions' in line:
                    section = 'Transitions'
                elif line == 'End':
                    section = None
                else:
                    # Pentru adaugarea alfabetului
                    if section == 'Sigma':
                        self.sigma.add(line)

                    # Pentru adaugarea starilor
                    elif section == 'States':
                        state_info = line.split(',')
                        state = state_info[0].strip()

                        if state not in self.states:
                            self.states[state] = {'F': False, 'S': False}

                        if len(state_info) == 2:
                            status_1 = state_info[1].strip()
                            if status_1 not in {'F', 'S'}:
                                print(f"Starea '{state_info}' este invalida.")
                                return False
                            self.states[state][status_1] = True

                        if len(state_info) == 3:
                            status_1 = state_info[1].strip()
                            status_2 = state_info[2].strip()
                            if status_1 not in {'F', 'S'} or status_2 not in {'F', 'S'}:
                                print(f"Starea '{state_info}' este invalida.")
                                return False
                            self.states[state][status_1] = True
                            self.states[state][status_2] = True

                    # Pentru adaugarea tranzitiilor
                    elif section == 'Transitions':
                        transition_info = line.split(',')
                        if len(transition_info) != 3:
                            print(f"Tranzitia {line} este invalida.")
                            return False
                        source_state = transition_info[0].strip()
                        letter = transition_info[1].strip()
                        target_state = transition_info[2].strip()
                        if letter not in self.sigma:
                            print(f"Tranzitia '{line}' este invalida.")
                            return False
                        self.transitions.append((source_state, letter, target_state))

        # Verificare daca avem exact o stare initiala
        initial_states = [state for state, props in self.states.items() if props['S']]
        if len(initial_states) != 1:
            print("NFA invalid: trebuie sa fie exact o stare initiala")
            return False

        return True

    def acceptare(self, input_string):
        current_state = set(self.states['S'])  # Stare initiala
        for letter in input_string:
            next_states = set()
            for state in current_state:
                for transition in self.transitions:
                    source_state, trans_letter, target_state = transition
                    if source_state == state and trans_letter == letter:
                        next_states.add(target_state)
            current_state = next_states
            if not current_state:
                return False  # Nicio stare nu este accesibila cu simbolul curent
        # Verifica daca cel putin una dintre starile curente este finala
        return any(state in current_state for state in self.states if self.states[state]['F'])

   #determina toate starile care pot fi atinse dintr-o stare initiala folosind tranzitii epsilon
    def epsilon_closure(self, states):
        closure = set(states)
        unprocessed_states = list(states)
        while unprocessed_states:
            current_state = unprocessed_states.pop()
            for transition in self.transitions:
                source_state, letter, target_state = transition
                if source_state == current_state and letter == '' and target_state not in closure:
                    closure.add(target_state)
                    unprocessed_states.append(target_state)
        return closure

#determina toate starile care pot fi atinse din starea initiala folosind un simbol specific din alfabet
    
    def move(self, states, symbol):
        target_states = set()
        for state in states:
            for transition in self.transitions:
                source_state, letter, target_state = transition
                if source_state == state and letter == symbol:
                    target_states.add(target_state)
        return target_states

class DFA:
    def __init__(self, sigma, states, transitions, start_state, accept_states):
        self.sigma = sigma
        self.states = states
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def convert_from_nfa(self, nfa):
        dfa_states = []  # Stările DFA-ului
        dfa_transitions = {}  # Tranzitiile DFA-ului
        dfa_start_state = frozenset(nfa.epsilon_closure([state for state in nfa.states if nfa.states[state]['S']]))  # Starea de start a DFA-ului

        # Colectăm toate stările posibile ale DFA-ului
        unmarked_states = [dfa_start_state]
        while unmarked_states:
            current_dfa_state = unmarked_states.pop(0)
            if current_dfa_state not in dfa_states:
                dfa_states.append(current_dfa_state)
                for symbol in self.sigma:
                    target_nfa_states = nfa.epsilon_closure(nfa.move(current_dfa_state, symbol))
                    if target_nfa_states:
                        dfa_transitions[(current_dfa_state, symbol)] = frozenset(target_nfa_states)
                        if frozenset(target_nfa_states) not in dfa_states:
                            unmarked_states.append(frozenset(target_nfa_states))

        # Identificăm stările finale ale DFA-ului
        dfa_accept_states = [state for state in dfa_states if any(nfa.states[nfa_state]['F'] for nfa_state in state)]

        self.states = dfa_states
        self.transitions = dfa_transitions
        self.start_state = dfa_start_state
        self.accept_states = dfa_accept_states

    def write_configuration(self, filename):
        with open(filename, 'w') as file:
            file.write(f"Sigma\n")
            for symbol in self.sigma:
                file.write(f"{symbol}\n")
            file.write(f"States\n")
            for state in self.states:
                state_list = list(state)
                if any(self.states[nfa_state]['F'] for nfa_state in state):
                    state_list.append('F')
                if any(self.states[nfa_state]['S'] for nfa_state in state):
                    state_list.append('S')
                file.write(f"{','.join(sorted(state_list))}\n")
            file.write(f"Transitions\n")
            for (source_state, symbol), target_state in self.transitions.items():
                file.write(f"{','.join(sorted(list(source_state)))},{symbol},{','.join(sorted(list(target_state)))}\n")
            file.write(f"End\n")

import sys

if len(sys.argv) != 4:
    print("Usage: python conv_nfa_2_dfa_engine.py nfa_config_file converted_dfa_config_file")
    sys.exit(1)

nfa_file = sys.argv[1]
dfa_file = sys.argv[2]

nfa = NFA(nfa_file)
if not nfa.validare():
    print("Invalid NFA configuration")
    sys.exit(1)

dfa = DFA(nfa.sigma, set(), {}, frozenset(), [])
dfa.convert_from_nfa(nfa)
dfa.write_configuration(dfa_file)
print("Conversion completed successfully.")
