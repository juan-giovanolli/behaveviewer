from collections import OrderedDict
from parser_constants import *

class Stack:
    """
    This is a stack of tuples (key, value) of strings
    """

    def __init__(self):
        self.items = []


    def push(self, key, value):
        self.items.append((key, value))


    def pop(self):
        return self.items.pop()


    def is_empty(self):
        return (self.items == [])


    def contains(self, key):
        result = False
        for it in self.items:
            result = result or it[0] == key.lower()
        return result


    def to_list(self):
        result = []
        for item in reversed(self.items):
            result.append(item)
        return result


    def size(self):
        return len(self.items)


class Parser:

    def __init__(self):
        self._parser_stack = Stack()
        self._parsed_scenario = Stack()
        self._scenario_ready = False
        self._has_background = False
        self._EOF = False    #Needed to analize last scenario
        self._parsed_feature = Stack()
        self._feature_processed = False

    def parse_file(self, filename):
        """
        Parses one feature file. It returns a tuple with the list of scenarios
        parsed and the name of feature and background steps if it has.
        """
        list_of_scenarios = []
        line = 'initial value for string that should be overwritten'
        with open(filename) as file:
            while line:
                if self._scenario_ready:
                    list_of_scenarios.append(self._process_scenario())
                else:
                    line = file.readline()
                    self._analize_line(line)
            self._EOF = True
            self._analize_line(line)
        print list_of_scenarios, self._parsed_feature.to_list()
        return list_of_scenarios, self._parsed_feature.to_list()
            

    def _analize_line(self, line):
        tokens = self._tokenize_line(line)
        if tokens and self._is_feature(tokens):
            self._handle_feature(tokens)
        elif tokens and self._is_background(tokens):
            self._handle_background(tokens)
        elif self._EOF or tokens and self._is_tag(tokens):
            self._handle_tag(tokens)
        elif tokens and self._is_scenario(tokens):
            self._handle_scenario(tokens)
        elif tokens and self._is_step(tokens):
            self._handle_step(tokens)


    def _tokenize_line(self, line):
        new_line = []
        raw_line = line.split()
        if raw_line and '#' not in raw_line[0]:
            for a in raw_line:
                tokens = a.split(':')
                if len(tokens) > 1:
                    new_line.append(tokens[0] + ':')
                    new_line.append(tokens[1])
                else:
                    new_line.append(tokens[0])
        return new_line


    def _is_feature(self, tokens):
        return tokens[0].lower() == FEATURE


    def _is_background(self, tokens):
        return tokens[0].lower() == BACKGROUND


    def _is_tag(self, tokens):
        return tokens[0][0] == TAG_MARK


    def _is_scenario(self, tokens):
        return tokens[0].lower() == SCENARIO


    def _is_step(self, tokens):
        step = tokens[0].lower()
        return step == GIVEN or step == WHEN or step == THEN or step == AND


    def _handle_feature(self, tokens):
        result = not self._parser_stack.contains(FEATURE)
        if result:
            self._parser_stack.push(FEATURE, tokens[1:])
        else:
            raise ValueError("Reusing parser object for a different feature is not supported")
        return result


    def _handle_background(self, tokens):
        self._has_background = True
        result = not self._parser_stack.contains(BACKGROUND)
        if result:
            self._parser_stack.push(BACKGROUND, [])
        else:
            raise ValueError("There is more than one background in the feature.")
        return result


    def _handle_tag(self, tokens):
        end_scenario = self._parser_stack.contains(SCENARIO) or self._EOF
        if end_scenario:
            self._scenario_ready = True
        list_of_tags = []
        for tk in tokens:
            if tk[0] == TAG_MARK:
                list_of_tags.append(tk[1:])
        self._parser_stack.push(TAG, list_of_tags)


    def _handle_scenario(self, tokens):
        end_scenario = self._parser_stack.contains(SCENARIO) or self._EOF
        if end_scenario:
            self._scenario_ready = True
        self._parser_stack.push(SCENARIO, tokens[1:])


    def _handle_step(self, tokens):
        self._parser_stack.push(tokens[0], tokens[1:])


    def _process_feature(self):
        if self._parser_stack.contains(FEATURE):
            background_steps = []
            while self._parser_stack.contains(BACKGROUND):
                last_token, text = self._parser_stack.pop()
                if last_token != BACKGROUND:
                    background_steps.append((last_token, text))
                else:
                    background_steps.reverse()
                    self._parsed_feature.push(last_token, background_steps)
            assert(self._parser_stack.contains(FEATURE))
            last_token, text = self._parser_stack.pop()
            self._parsed_feature.push(last_token, text)
            self._feature_processed = True     


    def _process_scenario(self):
        parsed_scenario = Stack()
        last_token, text = self._parser_stack.pop()
        if last_token.lower() == SCENARIO or last_token.lower() == TAG:
            temp = last_token, text
        assert(self._parser_stack.contains(SCENARIO))
        while self._parser_stack.contains(SCENARIO) or self._parser_stack.contains(TAG):
            last_token, text = self._parser_stack.pop()
            parsed_scenario.push(last_token, text)
        #parsed_scenario.push(last_token, text) # TODO: check why this is not needed
        self._process_feature()
        self._scenario_ready = False
        #Returns a list with this order: tags, scenario, steps
        self._parser_stack.push(temp[0], temp[1]) #TODO: fix this: temp is for the tag or scenario that triggered the parse of scenario
        return parsed_scenario.to_list()

