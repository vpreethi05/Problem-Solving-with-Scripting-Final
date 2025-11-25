RULE_SETS = {}

def register_rule_set(name):
    """
    A decorator to register a rule set function.
    """
    def decorator(func):
        RULE_SETS[name] = func
        return func
    return decorator