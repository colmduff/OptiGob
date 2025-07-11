from optigob.input_helper import InputHelper

def test_input_helper():
    helper = InputHelper()
    print("\nAll input combinations (dict):")
    combos = helper.get_combos_dict()
    for input_type, combo_list in combos.items():
        print(f"\nInput type: {input_type}")
        for combo in combo_list:
            print(combo)
    print("\nAll input combinations (DataFrame):")
    df = helper.get_combos_df()
    print(df)
    print("\nFiltered combos (example: input_type='forest', broadleaf_frac=0.5):")
    filtered = helper.filter_combos(input_type='forest', broadleaf_frac=0.5)
    print(filtered)

    helper.print_readable_combos(12)

if __name__ == "__main__":
    test_input_helper()
