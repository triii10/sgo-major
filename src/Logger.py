from inspect import getframeinfo, stack
from sys import stderr
def log(*msg):
    logging = False
    '''
    log function to display the logs on stderr
    '''
    if(logging):
        caller = getframeinfo(stack()[1][0])
        print("{} --> {}".format(caller.lineno, msg), file=stderr)
