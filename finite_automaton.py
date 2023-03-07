class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            if (current_state, symbol) not in self.transitions:
                return False
            current_state = self.transitions[(current_state, symbol)]
        if current_state not in self.accept_states:
            return False
        return True

    def to_regular_grammar(self):
        # Initialize the production rules and start symbol of the grammar
        productions = []
        start_symbol = 'S'

        # Add a production rule for each final state
        for final_state in self.accept_states:
            productions.append(start_symbol + " -> " + final_state + "\n")

        # Add a production rule for each transition
        for state in self.states:
            for symbol in self.alphabet:
                transitions = self.transitions[state][symbol]
                for transition in transitions:
                    productions.append(state + " -> " + symbol + transition + "\n")

        # Remove duplicates and sort the production rules
        productions = list(set(productions))
        productions.sort()

        # Create the regular grammar as a string
        regular_grammar = start_symbol + " -> " + self.start_state + "\n"
        for production in productions:
            regular_grammar += production

        return regular_grammar

    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                # check if there is more than one transition for the same symbol
                if sum(1 for t in self.transitions[state] if t[0] == symbol) > 1:
                    return False
        return True

    def convert_to_dfa(self):
        # Step 1: Create new start state s0
        s0 = frozenset(self.epsilon_closure({self.start_state}))

        # Step 2: Create new set of states with s0
        new_states = {s0}

        # Step 3: Create transitions for each symbol in the alphabet to a new DFA state
        new_delta = {}
        for state in new_states:
            for symbol in self.alphabet:
                # Find all the states that can be reached from the current state using the symbol
                next_states = set()
                for s in state:
                    if (s, symbol) in self.transitions:
                        next_states |= set(self.transitions[(s, symbol)])
                next_states = self.epsilon_closure(next_states)

                if not next_states:
                    continue

                # Create the new state and add it to the set of new states
                new_state = frozenset(next_states)
                new_states.add(new_state)

                # Add the transition to the new delta
                if state not in new_delta:
                    new_delta[state] = {}
                new_delta[state][symbol] = new_state

        # Step 4: Repeat step 3 until there are no more new states to add
        dfa_states = {}
        for i, state in enumerate(new_states):
            dfa_states[state] = f"q{i}"

        dfa_delta = {}
        for state, transitions in new_delta.items():
            dfa_state = dfa_states[state]
            for symbol, next_state in transitions.items():
                dfa_next_state = dfa_states[next_state]
                dfa_delta[dfa_state, symbol] = dfa_next_state

        dfa_q0 = dfa_states[s0]

        dfa_F = set()
        for state in new_states:
            for final_state in self.accept_states:
                if final_state in state:
                    dfa_F.add(dfa_states[state])

        return FiniteAutomaton(new_states, self.alphabet, dfa_delta, dfa_q0, dfa_F)

    def epsilon_closure(self, states):
        closure = set(states)
        new_states = set(states)
        while new_states:
            state = new_states.pop()
            if (state, '') in self.transitions:
                for next_state in self.transitions[(state, '')]:
                    if next_state not in closure:
                        closure.add(next_state)
                        new_states.add(next_state)
        return closure

    def __str__(self):
        s = "Finite Automaton:\n"
        s += "States: " + str(self.states) + "\n"
        s += "Alphabet: " + str(self.alphabet) + "\n"
        s += "Transitions:\n"
        for transition in self.transitions:
            s += str(transition[0]) + " --" + str(transition[1]) + "--> " + str(self.transitions[transition]) + "\n"
        s += "Start state: " + str(self.start_state) + "\n"
        s += "Accept states: " + str(self.accept_states) + "\n"
        return s
