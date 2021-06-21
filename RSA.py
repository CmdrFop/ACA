class RSA:
    def __init__(self, vocabulary, referents, lexicon, order):
        self.vocabulary = vocabulary
        self.R = referents
        self.lex = lexicon
        self.n = order

    def run_rsa_speaker(self, referent):
        speaker_signals = []
        for signals in self.vocabulary:
            signal_prob = self.speaker_from_speaker_perspective(signals, referent, self.n)
            speaker_signals.append(signal_prob)
        return speaker_signals

    def run_rsa_listener(self, signal):
        self.signal = signal
        listener_referents = []
        for referents in self.R:
            referent_prob = self.listener_from_listener_perspective(signal, referents, self.n)
            listener_referents.append(referent_prob)

        return listener_referents

    # Speaker
    ###########################################################################
    def speaker_from_speaker_perspective(self, signal, referent, n):
        if n == 0:
            return self.delta_speaker(signal, referent)

        LS = self.listener_from_speaker_perspective(referent, signal, n)

        sum = 0
        for signals in self.vocabulary:
            sum += self.listener_from_speaker_perspective(referent, signals, n)
        if sum == 0:
            sum = 1
        return LS / sum

    def listener_from_speaker_perspective(self, referent, signal, n):

        SS = self.speaker_from_speaker_perspective(signal, referent, n - 1)

        sum = 0
        for referents in self.R:
            sum += self.speaker_from_speaker_perspective(signal, referents, n - 1)
        if sum == 0:
            sum = 1
        return SS / sum

    def delta_speaker(self, signal, referent):
        L = self.lexicon(signal, referent)

        sum = 0
        for signals in self.vocabulary:
            sum += self.lexicon(signals, referent)
        if sum == 0:
            sum = 1
        return L / sum

    ###########################################################################

    def lexicon(self, signal, referent):
        return self.lex[referent][signal]

    # Listener
    ###########################################################################
    def listener_from_listener_perspective(self, signal, referent, n):
        if n == 0:
            return self.delta_listener(signal, referent)
        LS = self.speaker_from_listener_perspective(referent, signal, n)

        sum = 0
        for referents in self.R:
            sum += self.speaker_from_listener_perspective(referents, signal, n)
        if sum == 0:
            sum = 1
        return LS / sum

    def speaker_from_listener_perspective(self, referent, signal, n):
        SL = self.listener_from_listener_perspective(signal, referent, n - 1)

        sum = 0
        for signals in self.vocabulary:
            sum += self.listener_from_listener_perspective(signals, referent, n - 1)
        if sum == 0:
            sum = 1
        return SL / sum

    def delta_listener(self, signal, referent):
        L = self.lexicon(referent, signal)

        sum = 0
        for referents in self.R:
            sum += self.lexicon(referents, signal)
        if sum == 0:
            sum = 1
        return L / sum
    ###########################################################################