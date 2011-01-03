import re
from zendone.exceptions import InvalidRuleException, InvalidKoanException

class Rule:
    valid_rule = re.compile('(\W)(.{0,60})\\1', re.IGNORECASE)

    def __init__(self, rulestr):
        try:
            rule = Rule.valid_rule.match(rulestr)
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
    valid_koan = re.compile('^[abc]{3}$', re.IGNORECASE)

    def __init__(self, koanstr):
        if not Koan.valid_koan.match(koanstr):
            raise InvalidKoanException(koanstr)

    @classmethod
    def all():
        for first in 'abc':
            for second in 'abc':
                for third in 'abc':
                    yield Koan('%c%c%c' % (first, second, third))

