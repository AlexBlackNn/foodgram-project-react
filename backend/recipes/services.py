START_COUNT_WITH = 1


def get_ingredient_for_shopping(ingredient_and_amount):
    """Составить список покупок."""
    shopping_list = []
    for i, item in enumerate(ingredient_and_amount, START_COUNT_WITH):
        name = item.get('ingredient__name')
        amount = str(item.get('ingredient_amount'))
        measurement_unit = item.get('ingredient__measurement_unit')
        ingredient_row = f'{i}) {name} {amount} {measurement_unit}\n'
        shopping_list.append(ingredient_row)
    return shopping_list
