import numpy as np
from typing import List, Tuple
from person_class import Person

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    # collaborated with Sky Jung! :)


    n = len(scores)
    proposers = []
    receivers = []
    proposals_tracker = {}
    receivers_tracker = []
    matches = []

    # initialize proposers and their scores with all receivers
    # and the proposals_tracker values as empty arrays
    for i in range(int(n/2)):
        proposer = Person()
        proposer.index = i
        proposer.gender_id = gender_id[i]
        proposer.gender_pref = gender_pref[i]
        proposals_tracker[i] = []
        for j in range(int(n/2), n):
            proposer.scores[j] = scores[i][j]
        proposers.append(proposer)

    # initialize receivers and their scores with all proposers
    # and the receivers_tracker values as -1
    for i in range(int(n/2), n):
        receiver = Person()
        receiver.index = i
        receiver.gender_id = gender_id[i]
        receiver.gender_pref = gender_pref[i]
        receivers_tracker[i] = -1
        for j in range(int(n/2)):
            receiver.scores[j] = scores[i][j]
        receivers.append(receiver)

    # sets compatibility score to 0 for matrix entries where the preference doesn't match with id
    for proposer in proposers:
        for receiver in receivers:
            if (proposer.gender_pref == Men and receiver.gender_id != Male) or (receiver.gender_pref == Men and proposer.gender_id != Male):
                proposer.scores[receiver.index] = 0
                receiver.scores[proposer.index] = 0
            elif (proposer.gender_pref == Woman and receiver.gender_id != Female) or (receiver.gender_pref == Woman and proposer.gender_id != Female):
                proposer.scores[receiver.index] = 0
                receiver.scores[proposer.index] = 0
            elif (proposers[i].gender_pref != Bisexual and receivers[i].gender_id == Nonbinary) or (proposer[i].gender_id == Nonbinary and receivers[i].gender_pref != Bisexual):
                proposer.scores[receiver.index] = 0
                receiver.scores[proposer.index] = 0

    # implement GS algorithm
    # check in there is a proposer who has no match
    while(False in proposers.matched):
        # check for all proposers if each proposer has proposed to all receivers
        for proposer in proposers:
            for i in range(int(n/2), n):
                if receivers[i].index not in proposers_tracker[proposer.index]:
                    if receivers_tracker[i] = -1:
                        receivers_tracker[i] = proposer.index
                        proposal_tracker[proposer.index].append(i)
                        proposer.matched = True
                    elif receiver.scores[proposer.index] > receiver.scores(receivers_tracker[i]):
                        proposers[receivers_tracker[i]].matched = False
                        receivers_tracker[i] = proposer.index
                        proposal_tracker[proposer.index].append(i)
                        proposer.matched = True
                    else:
                        proposal_tracker[proposer.index].append(i)

    # add matches to the matches list
    for receiver in receivers:
        matches.append(receivers_tracker[receiver], receiver)

    return matches


if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
