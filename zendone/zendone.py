import re
import os
import sys
from random import shuffle

class Zendone:
    def __init__(self, game):
        self.gamecfg = __import__('zendone.games.%s' % game, 
                fromlist=['Rule','Koan'])
        self.gamename = game

    def load_library(self, filename):
        def line_to_triple(line):
            triple = line.strip().split(';')
            r = self.gamecfg.Rule(triple[0])
            t = self.gamecfg.Koan(triple[1])
            f = self.gamecfg.Koan(triple[2])
            assert r(t), "True koan %s doesn't match rule %s" % (t, r)
            assert not r(f), "False koan %s does match rule %s" % (f, r)
            return (r,t,f)
        self._library = map(line_to_triple, file(filename))

    def get_random_rule(self):
        from copy import copy
        library = copy(self._library)
        shuffle(library)
        return library[0]


class Rule:
    __valid_rule = re.compile('(\W)(.{0,60})\\1', re.IGNORECASE)

    def __init__(self, rulestr):
        try:
            rule = self.__valid_rule.match(rulestr)
            self.regex = re.compile(rule.group(2), re.IGNORECASE)
        except:
            raise InvalidRuleException(rulestr)

    def __call__(self, koan):
        return bool(self.regex.search(str(koan)))

    def __eq__(self, other):
        return self.regex.pattern == other.regex.pattern

    def __str__(self):
        return self.regex.pattern


class Koan(str):
    __valid_koan = re.compile('^[abc]{3}$', re.IGNORECASE)

    def __init__(self, koanstr):
        if not self.__valid_koan.match(koanstr):
            raise InvalidKoanException(koanstr)



def get_contradictions(rule, cache):
    return filter(lambda c: c[1] ^ rule(c[0]), cache)


def console_session(zendonecfg, rule, true_koan, false_koan):
    print "Zenregex -- A regex Zendo clone."
    print
    print "True koan:    ", true_koan
    print "False koan:   ", false_koan

    koan_cache = [(true_koan, True), (false_koan, False)]

    while True:
        s = raw_input(">>> ")
        
        # If a koan has been entered, evaluate it and write it to the cache.
        try:
            koan = Koan(s)
            is_cached = filter(lambda x: x[0] == s, koan_cache)
            if len(is_cached) > 0:
                print is_cached[0][1]
            else:
                print rule(s)
                koan_cache.append((s, rule(s)))
        except InvalidKoanException:
            pass
    
        # If a rule has been entered, print contradictions or compare it to
        # the actual rule.
        try:
            query = Rule(s)
            contra_cache = get_contradictions(query, koan_cache)
            if len(contra_cache) > 0:
                print "Nah, %s can not be the rule, because..." % query
                for koan, truth in contra_cache:
                    if truth:
                        print "\t...it does not match true koan '%s'" % koan
                    else:
                        print "\t...it does match false koan '%s'" % koan
            else:
                if query == rule:
                    print "Yeah, %s is the rule! You've reached enlightment." \
                            % query
                    break
                else:
                    print "Sorry, %s is not the rule."
        except InvalidRuleException:
            pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python %s <library.csv>" % sys.argv[0]
        exit(1)

    import readline
    histfile = os.path.join(os.environ["HOME"], ".zenregexhist")
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass

    import atexit
    atexit.register(readline.write_history_file, histfile)
    del os, histfile

    console_session(*Library(sys.argv[1]).get_random_rule())
    exit(0)
