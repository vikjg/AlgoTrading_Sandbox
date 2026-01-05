def check_last_signal(symbol, state):
    return state.get(symbol, None)

def update_position(symbol, signal, state):
    state[symbol] = signal
