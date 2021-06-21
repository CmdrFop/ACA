import numpy as np
import RSA
from ACA import CM
import copy


def run_model():
    order = 1
    intended_referent = 0
    Vocab = [0, 1, 2]
    Referets = [0, 1, 2]
    lexicon = [

        [1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0]
    ]
    lexicon_attitude = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]

    ])
    coherence_matrix_edges = [
        [0, -1, -1, 1, 0, 0, 0, 0, 0, 0],  # Albert
        [-1, 0, -1, -1, 1, 0, 0, 0, 0, 0],  # Jerry
        [-1, -1, 0, 0, 0, 1, 1, 0, 0, 0],  # Christine
        [1, -1, -1, 0, 0, 0, 0, 0, 1, 0],  # Crush On
        [0, 1, 0, 0, 0, -1, 0, 1, 0, 0],  # Friends
        [0, -1, 1, 0, -1, 0, 1, 0, 0, 0],  # Colleague
        [0, 0, 1, 0, 0, 1, 0, -1, 0, 1],  # Always Late
        [0, 0, 0, 0, 1, 0, -1, 0, -1, -1],  # Happy
        [0, 0, 0, 1, 0, 0, 0, -1, 0, -1],  # Awkward
        [0, 0, 0, 0, -1, 0, 1, -1, -1, 0]  # Sad
    ]
    nodes = ["Albert", "Jerry", "Christine", "Crush On", "Friends", "Colleague", "Always Late", "Happy", "Awkward",
             "Sad"]
    ####################################
    rsa_obj = RSA(Vocab, Referets, copy.deepcopy(lexicon), order)
    RSA_output = []
    for i in range(3):
        speaker_signal = rsa_obj.run_rsa_speaker(i)
        RSA_output.append(speaker_signal)

    #####################################
    set_node = "Happy"
    cm = CM(coherence_matrix_edges, copy.deepcopy(RSA_output), copy.deepcopy(nodes), set_node, Referets)
    output = cm.runCM()

    set_node = "Awkward"
    cm = CM(coherence_matrix_edges, copy.deepcopy(RSA_output), copy.deepcopy(nodes), set_node, Referets)
    output2 = cm.runCM()

    set_node = "Sad"
    cm = CM(coherence_matrix_edges, copy.deepcopy(RSA_output), copy.deepcopy(nodes), set_node, Referets)
    output3 = cm.runCM()
    ######################################
    values = []
    indeces = []
    outputs = [output, output2, output3]
    for i in outputs:
        signals = []
        for j in range(len(i)):
            signals.append(i[j][intended_referent] + i[j][intended_referent] - sum(i[j]))
        values.append((max(signals)))
        indeces.append(signals.index(max(signals)))

    attitude = values.index(max(values))
    speaker_signal = indeces[attitude]
    #########################################################
    rsa_ati = RSA(Vocab, Referets, copy.deepcopy(lexicon_attitude), 0)
    speaker_attitude_signal = rsa_ati.run_rsa_speaker(attitude)
    speaker_attitude_signal = speaker_attitude_signal.index(max(speaker_attitude_signal))
    infered_attitude = rsa_ati.run_rsa_listener(speaker_attitude_signal)
    infered_attitude = infered_attitude.index(max(infered_attitude))

    #################################################################
    rsa_obj2 = RSA(Vocab, Referets, lexicon, order)
    RSA_output = []
    for i in range(3):
        infered_referent = rsa_obj2.run_rsa_listener(i)
        RSA_output.append(infered_referent)

    Attitudes = ["Happy", "Awkward", "Sad"]
    cm2 = CM(coherence_matrix_edges, copy.deepcopy(RSA_output), copy.deepcopy(nodes), Attitudes[infered_attitude],
             Referets)
    output10 = cm2.runCM()

    indice = output10[speaker_signal].index(max(output10[speaker_signal]))
    infered_referent = indice
    print(infered_referent == intended_referent)
    return infered_referent == intended_referent


result_coh = run_model()
