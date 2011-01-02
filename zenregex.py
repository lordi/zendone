import re
import os
import readline
import sys

class RegexRule:
    """wadwadwad.

    >>> rule = RegexRule("^a", "abc", "bca")
    >>> rule("bda")
    False
    >>> rule("acd")
    True
    """

    def __init__(self, regex, true_koan=None, false_koan=None):
        self.regex = re.compile(regex, re.IGNORECASE)
        if true_koan:
            assert self(true_koan), "True example %s does not match %s" % \
                    (true_koan, self)
            self.true_koan = true_koan
        if false_koan:
            assert not self(false_koan), "False example %s does match %s" % \
                    (false_koan, self)
            self.false_koan = false_koan

    def __call__(self, koan):
        return bool(self.regex.search(koan))

    def __str__(self):
        return "<RegexRule /%s/>" % self.regex.pattern

    def __eq__(self, rule):
        return self.regex.pattern == rule.regex.pattern

def read_library(filename):
    return map(lambda x: RegexRule(*x.strip().split(';')), file(filename))

def select_random(rules):
    return rules[0]

def session(rule):
    print "Guess the regex!"
    print
    print "True koan:    ", rule.true_koan
    print "False koan:   ", rule.false_koan

    valid_koan = re.compile('^[a-z]+$', re.IGNORECASE)
    solution = re.compile('(\W)(.{0,40})\\1', re.IGNORECASE)
    koan_cache = [(rule.true_koan, True), (rule.false_koan, False)]

    for i in range(10):
        s = raw_input(">>> ")
        if valid_koan.search(s) != None:
            print rule(s)
            koan_cache.append((s, rule(s)))
        x = solution.match(s)
        if x:
            q = RegexRule(x.group(2))
            contradict = filter(lambda c: c[1] ^ q(c[0]), koan_cache)
            if len(contradict) > 0:
                print "Nah, %s can not the rule, because" % q
                for koan, s in contradict[:3]:
                    if s:
                        print "  * it does not match true koan '%s'" % koan
                    else:
                        print "  * it does match false koan '%s'" % koan
            else:
                if q == rule:
                    print "Yea, %s is the rule! You've reached enlightment.", q
                    return
                else:
                    print "Sorry, %s is not the rule."



if __name__ == "__main__":
    histfile = os.path.join(os.environ["HOME"], ".zenregexhist")
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    import atexit
    atexit.register(readline.write_history_file, histfile)
    del os, histfile

    rule = select_random(read_library(sys.argv[1]));
    session(rule)

