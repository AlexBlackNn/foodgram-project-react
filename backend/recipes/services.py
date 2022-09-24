START_COUNT_WITH = 1


def form_shopping_list(ingredient_and_amount):
    """Составить список покупок."""
    shopping_list = []
    for i, item in enumerate(ingredient_and_amount, START_COUNT_WITH):
        name = item.get('ingredient__name')
        amount = str(item.get('ingredient_amount'))
        ingredient_row = str(i) + ') ' + name + ' ' + amount + '\n'
        shopping_list.append(ingredient_row)
    return shopping_list
