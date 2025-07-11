from optigob.resource_manager.input_query import InputQuery

def test_get_organic_soil_input_combos():
    iq = InputQuery()
    combos = iq.get_organic_soil_input_combos()
    print("Organic soil input combinations:")
    for combo in combos:
        print(combo)
    assert isinstance(combos, list)
    assert all(isinstance(c, dict) for c in combos)

    forest_combos = iq.get_forest_input_combos()
    print("Forest input combinations:")
    for combo in forest_combos:
        print(combo)
    assert isinstance(forest_combos, list)
    assert all(isinstance(c, dict) for c in forest_combos)

    all_combos = iq.get_all_input_combos()
    print("All input combinations:")
    print(all_combos)
    print("#" * 50)

    all_combos_df = iq.get_all_input_combos_df()
    print("All input combinations DataFrame:")

    print(all_combos_df)

if __name__ == "__main__":
    test_get_organic_soil_input_combos()
