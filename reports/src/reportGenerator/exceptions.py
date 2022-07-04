class CategoryException (Exception):
    def __init__(self, category):
        super().__init__(f"La catégorie '{category}' n'existe pas")

class IndicatorException (Exception):
    def __init__(self, indicator):
        super().__init__(f"L'indicateur '{indicator}' n'existe pas")

class ComparatorException (Exception):
    def __init__(self, comparator):
        super().__init__(f"L'opération de comparaison '{comparator}' n'existe pas")

class MissingComparison(KeyError):
    def __init__(self, indicator):
        super().__init__(f"L'indicateur '{indicator}' n'a pas d'assertion")