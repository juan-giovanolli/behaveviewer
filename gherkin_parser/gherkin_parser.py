from parser_constants import *


class Stack:
    """
    This is a stack of tuples (key, value) of strings
    """

    def __init__(self):
        self.items = []

    def push(self, key=None, value=None):
        assert key is not None, "Invalid values in the stack"
        self.items.append((key, value))

    def pop(self):
        return self.items.pop()

    def is_empty(self):
        return (self.items == [])

    def contains(self, key=None):
        assert key is not None, "contains method recieved a None key"
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
        self._EOF = False    # Needed to analize last scenario
        self._parsed_feature = Stack()
        self._feature_processed = False

    def parse_file(self, filename=None):
        """
        Parses one feature file. It returns a tuple with the list of scenarios
        parsed and the name of feature and background steps if it has.
        """
        if filename is None:
            print "No file to parse"
        else:
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
                list_of_scenarios.append(self._process_scenario())
            return list_of_scenarios, self._parsed_feature.to_list()

    def _analize_line(self, line=None):
        assert line is not None, "No line to analize. None value recieved in _analize_line"
        """
        Given a line, it delegates further action to its handler depending on the keyword
        """
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

    def _tokenize_line(self, line=None):
        assert line is not None, "No line to tokenize. None value recieved in _tokenize_line"
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

    def _is_feature(self, tokens=None):
        assert tokens is not None, "None tokens recieved at _is_feature"
        return tokens[0].lower() == FEATURE_MARK

    def _is_background(self, tokens=None):
        assert tokens is not None, "None tokens recieved at _is_background"
        return tokens[0].lower() == BACKGROUND_MARK

    def _is_tag(self, tokens=None):
        assert tokens is not None, "None tokens recieved at _is_tag"
        return tokens[0][0] == TAG_MARK

    def _is_scenario(self, tokens=None):
        assert tokens is not None, "None tokens recieved at _is_scenario"
        token = tokens[0].lower()
        if token == 'scenario':  # TODO change this for support to scenario outlines and tables
            token += ':'
        return token == SCENARIO_MARK

    def _is_step(self, tokens=None):
        assert tokens is not None, "None tokens recieved at _is_step"
        step = tokens[0].lower()
        return step == GIVEN or step == WHEN or step == THEN or step == AND

    def _handle_feature(self, tokens=None):
        assert tokens is not None, "None tokens recieved at _handle_feature"
        result = not self._parser_stack.contains(FEATURE_MARK)
        if result:
            self._parser_stack.push(FEATURE_MARK, tokens[1:])
        else:
            raise ValueError("Reusing parser object for a different feature is not supported")
        return result

    def _handle_background(self, tokens=None):
        assert tokens is not None, "None tokens recieved at _handle_background"
        result = not self._parser_stack.contains(BACKGROUND_MARK)
        if result:
            self._parser_stack.push(BACKGROUND_MARK, [])
        else:
            raise ValueError("There is more than one background in the feature.")
        return result

    def _handle_tag(self, tokens=None):
        assert tokens is not None, "None tokens recieved at _handle_tag"
        end_scenario = self._parser_stack.contains(SCENARIO_MARK) or self._EOF
        if end_scenario:
            self._scenario_ready = True
        list_of_tags = []
        for tk in tokens:
            if tk[0] == TAG_MARK:
                list_of_tags.append(tk[1:])
        self._parser_stack.push(TAG, list_of_tags)

    def _handle_scenario(self, tokens=None):
        assert tokens is not None, "None tokens recieved at _handle_scenario"
        end_scenario = self._parser_stack.contains(SCENARIO_MARK) or self._EOF
        if end_scenario:
            self._scenario_ready = True
        self._parser_stack.push(SCENARIO_MARK, tokens[1:])

    def _handle_step(self, tokens=None):
        assert tokens is not None, "None tokens recieved at _handle_step"
        self._parser_stack.push(tokens[0], tokens[1:])

    def _process_feature(self):
        if self._parser_stack.contains(FEATURE_MARK):
            background_steps = []
            while self._parser_stack.contains(BACKGROUND_MARK):
                last_token, text = self._parser_stack.pop()
                if last_token != BACKGROUND_MARK:
                    background_steps.append((last_token, text))
                else:
                    background_steps.reverse()
                    self._parsed_feature.push(last_token, background_steps)
            assert(self._parser_stack.contains(FEATURE_MARK))
            last_token, text = self._parser_stack.pop()
            self._parsed_feature.push(last_token, text)
            self._feature_processed = True

    def _process_scenario(self):
        """
        Returns a list with the scenario elements in this order: tags, scenario, steps
        """
        parsed_scenario = Stack()
        last_token, text = self._parser_stack.pop()
        if last_token.lower() == SCENARIO_MARK or last_token.lower() == TAG:
            temp = last_token, text
        assert(self._parser_stack.contains(SCENARIO_MARK))
        while self._parser_stack.contains(SCENARIO_MARK) or self._parser_stack.contains(TAG):
            last_token, text = self._parser_stack.pop()
            parsed_scenario.push(last_token, text)
        # parsed_scenario.push(last_token, text) # TODO: check why this is not needed
        self._process_feature()
        self._scenario_ready = False
        self._parser_stack.push(temp[0], temp[1])  # TODO: fix this: temp is for the tag or scenario that triggered the parse of scenario
        return parsed_scenario.to_list()
