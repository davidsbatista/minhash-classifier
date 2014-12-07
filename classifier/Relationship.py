import re


class Relationship:

    def __init__(self, _id, _sentence=None,  _type=None):

        self.sentence = _sentence
        self.identifier = _id
        self.rel_type = _type
        self.before = None
        self.between = None
        self.after = None
        self.arg1type = None
        self.arg2type = None
        self.sigs = None

        if _sentence:
            regex = re.compile('<[A-Z]+>[^<]+</[A-Z]+>', re.U)
            matches = []
            for m in re.finditer(regex, self.sentence):
                matches.append(m)

            print matches

            for x in range(0, len(matches) - 1):
                if x == 0:
                    start = 0
                if x > 0:
                    start = matches[x - 1].end()
                try:
                    end = matches[x + 2].start()
                except:
                    end = len(self.sentence) - 1

                before = self.sentence[start:matches[x].start()]
                between = self.sentence[matches[x].end():matches[x + 1].start()]
                after = self.sentence[matches[x + 1].end(): end]
                ent1 = matches[x].group()
                ent2 = matches[x + 1].group()
                arg1match = re.match("<[A-Z]+>", ent1)
                arg2match = re.match("<[A-Z]+>", ent2)
                arg1type = arg1match.group()[1:-1]
                arg2type = arg2match.group()[1:-1]
                self.before = before
                self.between = between
                self.after = after
                self.arg1type = arg1type
                self.arg2type = arg2type