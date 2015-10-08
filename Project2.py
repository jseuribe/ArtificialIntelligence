import shell
import util
import wordsegUtil

############################################################
# Problem 1b: Solve the segmentation problem under a unigram model

class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected
        return 0
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return state == len(self.query) #State is the index of our query, and if the index == len of inp, we are at the end
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)
        results = []
        word_start = state
        for word_end in range(len(self.query) + 1):
            #print "found chunk: ", self.query[word_start:word_end]
            results.append((self.query[word_start:word_end], word_end, self.unigramCost(self.query[word_start:word_end])))
            #print results

        return results

        #return the next "correct" word, the next index to be attempted, and the cost of the word.
        #Ideally, this should return a word chunk, update the next word chunk to be attempted
        # END_YOUR_CODE


def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    return ' '.join(ucs.actions)
    #print query.actions

    # END_YOUR_CODE

############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        state_tuple = ('', 0)#a state is defined by the previous word, and the current word
        return state_tuple #our states will be monitored by the words currently decided.
        #This is a necessity, as we have to remember the last word of our past bigram
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        if len(self.queryWords) == 1:
            return state[1] == len(self.queryWords) #Once we have seen all bigrams, the array should be as long as input
        else:
            return state[1] == len(self.queryWords) - 1
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)

        results = []
        current_state = state

        previous_word = current_state[0]
        previous_word_index = current_state[1]

        if len(self.queryWords) == 1:
            first_word_fills = self.possibleFills(self.queryWords[0])

            if not first_word_fills:
                first_and_only_choice = list()
                first_and_only_choice.append(self.queryWords[previous_word_index])
                first_word_fills = first_and_only_choice

            for first_words in first_word_fills:
                results.append((first_words, (first_words, previous_word_index + 1), self.bigramCost("", first_words)))

            return results
        elif previous_word_index == 0:#the first bigram
            first_word_fills = self.possibleFills(self.queryWords[previous_word_index])

            if not first_word_fills:
                first_and_only_choice = list()
                first_and_only_choice.append(self.queryWords[previous_word_index])
                first_word_fills = first_and_only_choice

            second_word_fills = self.possibleFills(self.queryWords[previous_word_index + 1])

            if not second_word_fills:
                second_and_only_choice = list()
                second_and_only_choice.append(self.queryWords[previous_word_index+1])
                second_word_fills = second_and_only_choice

            for first_words in first_word_fills:
                for second_words in second_word_fills:
                    results.append((first_words + ' ' + second_words, (second_words, previous_word_index + 1),
                                    self.bigramCost(first_words, second_words)))
            return results

        else:#generic bigram
            second_word_fills = self.possibleFills(self.queryWords[previous_word_index + 1])

            if not second_word_fills: #For words with no insertions, we will treat it as the only option.
                second_and_only_choice = []
                second_and_only_choice.append(self.queryWords[previous_word_index+1])
                second_word_fills = second_and_only_choice

            for second_words in second_word_fills:
                results.append((second_words, (second_words, previous_word_index + 1), self.bigramCost(previous_word, second_words)))

            return results
        # END_YOUR_CODE

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    if len(queryWords) == 0:
        return ''

    potential_single_word_input = possibleFills(queryWords[0])

    if len(queryWords) == 1 and not potential_single_word_input:
        return queryWords[0]
    else:
        ucs = util.UniformCostSearch(verbose=0)
        ucs.solve(VowelInsertionProblem(queryWords, bigramCost, possibleFills))

        print "here are the results:"
        print ucs.actions
        return ' '.join(ucs.actions)

    # END_YOUR_CODE

############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        state_tuple = ('', 0)#a state is defined by the previous word, and where the next word is at.
        return state_tuple
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return len(self.query) == state[1]
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 15 lines of code expected)
        start_pos = state[1]
        previous_word = state[0]
        results = []

        end_pos = start_pos + 1

        while end_pos != len(self.query) + 1:
            new_word = self.query[start_pos:end_pos]

            fills = self.possibleFills(new_word)
            if not fills:
                #Figure out how to ignore words with no vowel insertions at all.
                print "No fills found for potential word: ", new_word, ",it will not be considered"
            else:

                for next_word in fills:

                    if start_pos == 0:#first bigram word.
                        results.append((next_word, (next_word, end_pos), self.bigramCost('', next_word)))
                    else:
                        results.append((next_word, (next_word, end_pos), self.bigramCost(previous_word, next_word)))

            end_pos += 1

        return results
        # END_YOUR_CODE

def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''

    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(JointSegmentationInsertionProblem(query, bigramCost, possibleFills))

    print "segmentandinsert"
    print "here are the results:"
    print ucs.actions
    return ' '.join(ucs.actions)
    # END_YOUR_CODE

############################################################

if __name__ == '__main__':
    shell.main()
