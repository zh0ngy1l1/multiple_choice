from difflib import SequenceMatcher
from numpy import random
import os


class OneQuestion:
    
    def __init__(self, definition: str, term: str):
        self.definition: str = definition
        self.term: str = term
        self.options: dict = {"terms": [], "weights": []}
        
    def add_option(self, new_term: str, new_weight: float):
        '''
        adds option to self.options. preserves the options as sorted.
        '''
        for i in range(len(self.options["weights"])):
            if new_weight < self.options["weights"][i]:
                self.options["weights"].insert(i, new_weight)
                self.options["terms"].insert(i, new_term)
                return
        self.options["weights"].append(new_weight)
        self.options["terms"].append(new_term)
    
    def get_options(self) -> list:
        '''
        returns 3 incorrect options
        '''
        s = sum(self.options["weights"])
        p_distr = [i/s for i in self.options["weights"]]
        return random.choice(
            self.options["terms"], 
            size=3, replace=False ,p=p_distr
            ).tolist()
    
    def guess(self, correct: bool):
        self.tries = self.tries + 1
        if correct:
            self.successes = self.successes + 1
        else:
            pass
            #TODO add dynamic weights

def similar(a: str, b: str):
    return SequenceMatcher(None, a, b).ratio() + 0.1 # intuition tells me to add 0.1
    
class Questions:

    def __init__(self, dir: str):
        '''
        read questions from dir and initialize weights for questions
        '''
        
        self.questions = []
        self.length = self.__read_questions(dir)
        
        # Assume all has been asked twice and failed once. Don't ask why that's what my intuition says.
        self.nasked = [2] * self.length
        self.nfailed = [1] * self.length

        self.correct_choice: int = -1 # between 0 and 3 when running
        self.options: list = [""] * 4
        self.q_index: int = -1 # between 0 and self.length-1 when running
        
        self.__init_questions()
        
 
    def __read_questions(self, q_dir: str):
        '''
        reads q_dir/definitions.txt and dir/terms.txt as OneQuestion objects,
        to self.questions. returns number of questions.
        '''
        
        definitions = []
        terms = []        

        with open(
            os.path.join(q_dir, "definitions.txt"), 
            "r", encoding="utf-8"
            ) as file:
            
            for line in file:
                definitions.append(line.strip())
                
        with open(
            os.path.join(q_dir, "terms.txt"), 
            "r", encoding="utf-8"
            ) as file:
            
            for line in file:
                terms.append(line.strip())
        
        for i in range(len(terms)):
            self.questions.append(
                OneQuestion(
                    definition=definitions[i],
                    term=terms[i]
                )
            )
            
        return i + 1
        
    def __init_questions(self): 
        '''
        give initial weights to every OneQuestion
        '''
        for big_i in range(1, len(self.questions)):
            for small_i in range(big_i):
                bigq: OneQuestion = self.questions[big_i]
                smallq: OneQuestion = self.questions[small_i]
                weight = similar(bigq.term, smallq.term)
                bigq.add_option(smallq.term, weight)
                smallq.add_option(bigq.term, weight)
        return None
    
    def __choose_question(self) -> int:
        '''
        returns the index of the question that was picked by random.
        '''
        p_distr = [self.nfailed[i]/self.nasked[i] for i in range(self.length)]
        s = sum(p_distr)
        return random.choice(
            self.length, 
            p = [i/s for i in p_distr]
            )
    
    def generate_prompt(self):
        '''
        Chooses one question randomly and returns definition and all options 
        object Questions remembers the correct option
        '''
        self.q_index = self.__choose_question()
        question: OneQuestion = self.questions[self.q_index]
        definition: str = question.definition
        self.correct_choice = random.randint(4)
        self.options = question.get_options()
        self.options.insert(
            self.correct_choice, 
            question.term
            )
        
        return (definition, self.options)
    
    def check_choice(self, choice: int):
        '''
        1 if choice is correct. else 0 and update nfailed
        TODO update question weight as well.
        '''
        self.nasked[self.q_index] = self.nasked[self.q_index] + 1
        if choice == self.correct_choice:
            return 1
        self.nfailed[self.q_index] = self.nfailed[self.q_index] + 1
        return 0