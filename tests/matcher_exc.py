
class MatcherException(Exception):
    def __str__(self):
        return repr('Difference greater than variance')
