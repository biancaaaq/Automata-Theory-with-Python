class CFG:
    def __init__(self, filename):
        self.filename = filename
        self.non_terminals = set()
        self.terminals = set()
        self.productions = {}
        self.start_symbol = None

    def load_and_validate(self):
        with open(self.filename, 'r') as file:
            section = None
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if 'NonTerminals' in line:
                    section = 'NonTerminals'
                elif 'Terminals' in line:
                    section = 'Terminals'
                elif 'Productions' in line:
                    section = 'Productions'
                elif 'StartSymbol' in line:
                    section = 'StartSymbol'
                elif line == 'End':
                    section = None
                else:
                    if section == 'NonTerminals':
                        self.non_terminals.add(line)
                    elif section == 'Terminals':
                        self.terminals.add(line)
                    elif section == 'Productions':
                        lhs, rhs = line.split('->')
                        lhs = lhs.strip()
                        rhs = [prod.strip() for prod in rhs.split('|')]
                        if lhs in self.productions:
                            self.productions[lhs].extend(rhs)
                        else:
                            self.productions[lhs] = rhs
                    elif section == 'StartSymbol':
                        self.start_symbol = line

        # Validare CFG
        if not self.non_terminals:
            print("CFG invalid: Nu există neterminali.")
            return False
        if not self.terminals:
            print("CFG invalid: Nu există terminali.")
            return False
        if not self.productions:
            print("CFG invalid: Nu există producții.")
            return False
        if not self.start_symbol:
            print("CFG invalid: Nu există simbol de start.")
            return False
        if self.start_symbol not in self.non_terminals:
            print("CFG invalid: Simbolul de start nu este un neterminal valid.")
            return False

        for lhs in self.productions:
            if lhs not in self.non_terminals:
                print(f"CFG invalid: LHS-ul producției '{lhs}' nu este un neterminal valid.")
                return False
            for rhs in self.productions[lhs]:
                for symbol in rhs:
                    if symbol not in self.non_terminals and symbol not in self.terminals:
                        print(f"CFG invalid: Simbolul '{symbol}' din RHS-ul producției '{lhs} -> {rhs}' nu este valid.")
                        return False

        return True

# Utilizare
cfg = CFG('cfg_config.txt')
if cfg.load_and_validate():
    print("CFG valid")
else:
    print("CFG invalid")



