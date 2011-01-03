import re
import os
import sys
from zendone import Zendone, InvalidRuleException, InvalidKoanException

def get_contradictions(rule, cache):
    return filter(lambda c: c[1] ^ rule(c[0]), cache)

def console_session(zendone, rule, true_koan, false_koan):
    print "Zendone -- A Zendo clone."
    print
    print "True koan:    ", true_koan
    print "False koan:   ", false_koan

    koan_cache = [(true_koan, True), (false_koan, False)]

    while True:
        s = raw_input(">>> ")
        
        # If a koan has been entered, evaluate it and write it to the cache.
        try:
            koan = zendone.gamecfg.Koan(s)
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
            query = zendone.gamecfg.Rule(s)
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

    zen = Zendone('regex')
    zen.load_library(sys.argv[1])
    console_session(zen, *zen.get_random_rule())
    exit(0)
