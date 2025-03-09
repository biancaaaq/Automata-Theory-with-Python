class AutomFinit:
    def __init__(self, filename):
        self.filename = filename
        self.sigma = set()  # alfabetul
        self.states = {}  # starile
        self.transitions = []  # tranzitiile

    def validare(self):
        file = open(self.filename, 'r')
        section = None
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # setarea sectiunii
            if 'Sigma' in line:
                section = 'Sigma'
            elif 'States' in line:
                section = 'States'
            elif 'Transitions' in line:
                section = 'Transitions'
            elif line == 'End':
                section = None
            else:
                # pentru adaugarea alfabetului
                if section == 'Sigma':
                    self.sigma.add(line.strip())  

                # pentru adaugarea starilor
                elif section == 'States':
                    state_info = line.split(',')
                    state = state_info[0].strip()

                    # initializam starea daca inca nu a fost adaugata
                    if state not in self.states:
                        self.states[state] = {'F': False, 'S': False}

                    # daca starea este insotita doar de 'S' sau 'F'
                    if len(state_info) == 2:
                        status_1 = state_info[1].strip()
                        if status_1 not in {'F', 'S'}:
                            print(f"Starea '{state_info}' este invalida.")
                            return False
                        self.states[state][status_1] = True

                    # daca starea este insotita atat de 'S', cat si de 'F'
                    if len(state_info) == 3:
                        status_1 = state_info[1].strip()
                        status_2 = state_info[2].strip()
                        if status_1 not in {'F', 'S'} or status_2 not in {'F', 'S'}:
                            print(f"Starea '{state_info}' este invalida.")
                            return False
                        self.states[state][status_1] = True
                        self.states[state][status_2] = True

                # pentru adaugarea tranzitiilor
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

        # verificare daca avem exact o stare initiala
        initial_states = [state for state, props in self.states.items() if props['S']]
        if len(initial_states) != 1:
            print("DFA invalid: trebuie sa fie exact o stare initiala")
            return False

        return True

automat = AutomFinit("5b.txt")
if automat.validare():
    print("Valid")
else:
    print("Invalid")
