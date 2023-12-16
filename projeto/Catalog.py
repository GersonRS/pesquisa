events = [
    "GW150914",
    "GW151012",
    "GW151226",
    "GW170104",
    "GW170608",
    "GW170729",
    "GW170809",
    "GW170814",
    "GW170823",
]

data = {
    events[0]: {"mass1": 35.6, "mass2": 30.6, "f_band": [43.0, 300.0]},
    events[1]: {"mass1": 23.3, "mass2": 13.6, "f_band": [43.0, 400.0]},
    events[2]: {"mass1": 13.7, "mass2":  7.7, "f_band": [43.0, 800.0]},
    events[3]: {"mass1": 31.0, "mass2": 20.1, "f_band": [43.0, 800.0]},
    events[4]: {"mass1": 10.9, "mass2":  7.6, "f_band": [43.0, 600.0]},
    events[5]: {"mass1": 50.6, "mass2": 34.3, "f_band": [43.0, 300.0]},
    events[6]: {"mass1": 35.2, "mass2": 23.8, "f_band": [43.0, 300.0]},
    events[7]: {"mass1": 30.7, "mass2": 25.3, "f_band": [43.0, 380.0]},
    events[8]: {"mass1": 39.6, "mass2": 29.4, "f_band": [43.0, 300.0]},
}


def sliding_window(sequence, win_size, step=1):
    """Returns a generator that will iterate through
    the defined chunks of input sequence.  Input sequence
    must be iterable."""

    # Verify the inputs
    try:
        it = iter(sequence)
    except TypeError:
        raise Exception("**ERROR** sequence must be iterable.")
    if not ((type(0) == type(win_size)) and (type(step) == type(0))):
        raise Exception("**ERROR** type(winSize) and type(step) must be int.")
    if step > win_size:
        raise Exception("**ERROR** step must not be larger than winSize.")
    if win_size > len(sequence):
        raise Exception("**ERROR** winSize must not be larger than sequence length.")

    # Pre-compute number of chunks to emit
    num_of_chunks = ((len(sequence) - win_size) / step) + 1

    # Do the work
    for i in range(0, num_of_chunks * step, step):
        yield sequence[i:i + win_size]
