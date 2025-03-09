class AutomFinit:
    def __init__(self, filename):
        self.filename = filename
        self.sigma = set()  # alfabetul
        self.states = {}  # starile
        self.transitions = []  # tranzitiile
        self.start_state = None  # starea initiala
        self.accept_states = set()  # starile finale

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
                        if source_state not in self.states:
                            print(f"Tranzitia '{line}' este invalida.")
                            return False
                        if target_state not in self.states:
                            print(f"Tranzitia '{line}' este invalida.")
                            return False
                        if letter not in self.sigma:
                            print(f"Tranzitia '{line}' este invalida.")
                            return False
                        self.transitions.append((source_state, letter, target_state))

        # Verificare daca avem exact o stare initiala
        initial_states = [state for state, props in self.states.items() if props['S']]
        if len(initial_states) != 1:
            print("DFA invalid: trebuie sa fie exact o stare initiala")
            return False
        self.start_state = initial_states[0]

        # Adaugarea starilor finale
        self.accept_states = {state for state, props in self.states.items() if props['F']}

        return True

    def acceptare(self, input_string):
        current_state = self.start_state  # Starea initiala
        for letter in input_string:
            transition_found = False
            for transition in self.transitions:
                source_state, trans_letter, target_state = transition
                if source_state == current_state and trans_letter == letter:
                    current_state = target_state
                    transition_found = True
                    break
            if not transition_found:
                return False  # Tranzitie nu a fost gasita pentru starea curenta si litera de intrare
        # Verificam daca starea finala este in setul de stari de acceptare
        return current_state in self.accept_states


import sys

if len(sys.argv) != 3:
    print("Usage: python dfa_engine.py dfa_config_file input_string")
    sys.exit(1)

dfa_file = sys.argv[1]
input_string = sys.argv[2]

dfa = AutomFinit(dfa_file)
if not dfa.validare():
    print("Invalid DFA configuration")
    sys.exit(1)

if dfa.acceptare(input_string):
    print("accept")
else:
    print("reject")
