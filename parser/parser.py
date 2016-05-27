from collections import OrderedDict

SCENARIO = 'scenario:'
BACKGROUND = 'background:'
FEATURE = 'feature:'
TAG = 'tag'
GIVEN = 'given'
WHEN = 'when'
THEN = 'then'
AND = 'and'


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


    def get_list(self):
        result = []
        while not self.is_empty():
            result.append(self.pop())
        return result


class Parser:

    def __init__(self):
        self.parser_stack = Stack()
        self.parsed_scenario = Stack()
        self.scenario_ready = False
        self.has_background = False
        self.EOF = False    #Needed to analize last scenario

    def parse_file(self, filename):
        list_of_scenarios = []
        line = 'initial value for string that should be overwritten'
        with open(filename) as file:
            while line:
                if self.scenario_ready:
                    list_of_scenarios.append(self._process_scenario())
                else:
                    line = file.readline()
                    self._analize_line(line)
            self.EOF = True
            self._analize_line(line)
        return list_of_scenarios
            

    def _analize_line(self, line):
        tokens = self._tokenize_line(line)
        if tokens and self._is_feature(tokens):
            self._handle_feature(tokens)
        elif tokens and self._is_background(tokens):
            self._handle_background(tokens)
        elif self.EOF or tokens and self._is_tag(tokens):
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
        return tokens[0][0] == '@'


    def _is_scenario(self, tokens):
        return tokens[0].lower() == SCENARIO


    def _is_step(self, tokens):
        step = tokens[0].lower()
        return step == GIVEN or step == WHEN or step == THEN or step == AND


    def _handle_feature(self, tokens):
        result = not self.parser_stack.contains(FEATURE)
        if result:
            self.parser_stack.push(FEATURE, tokens[1:])
        else:
            raise ValueError("Reusing parser object for a different feature is not supported")
        return result


    def _handle_background(self, tokens):
        self.has_background = True
        result = not self.parser_stack.contains(BACKGROUND)
        if result:
            self.parser_stack.push(BACKGROUND, '')
        else:
            raise ValueError("There is more than one background in the feature.")
        return result


    def _handle_tag(self, tokens):
        end_scenario = self.parser_stack.contains(TAG) or self.parser_stack.contains(SCENARIO) or self.EOF
        if end_scenario:
            self.scenario_ready = True
        else: #BUG: just works fine for hte first scenario
            self.parser_stack.push(TAG, [tk[1:] for tk in tokens ])


    def _handle_scenario(self, tokens):
        end_scenario = self.parser_stack.contains(SCENARIO) or self.EOF
        if end_scenario:
            self.scenario_ready = True
        self.parser_stack.push(SCENARIO, tokens[1:])


    def _handle_step(self, tokens):
        self.parser_stack.push(tokens[0], tokens[1:])


    def _process_scenario(self):
        parsed_scenario = Stack()
        while self.parser_stack.contains(TAG) or self.parser_stack.contains(SCENARIO): 
            last_token, text = self.parser_stack.pop()
            parsed_scenario.push(last_token, text)
        if self.parser_stack.contains(BACKGROUND):
            has_background = True
            last_token, text = self.parser_stack.pop()
            background_steps = []
            if last_token != BACKGROUND:
                #Parsing background steps
                background_steps.append((last_token, text))
            else:
                parsed_scenario.push(last_token, background_steps)
        if self.parser_stack.contains(FEATURE):
            last_token, text = self.parser_stack.pop()
            parsed_scenario.push(last_token, text)
        #clean up
        self._revert_stack(text)
        self.scenario_ready = False
        #Returns a list with this order: feature, tags, scenario, steps
        return parsed_scenario.get_list()


    def _revert_stack(self, text):
        self.parser_stack = Stack()
        self.parser_stack.push(FEATURE, text)
        if self.has_background:
            self.parser_stack.push(BACKGROUND, '')


if __name__ == '__main__':
    p = Parser()
    p.parse_file()

