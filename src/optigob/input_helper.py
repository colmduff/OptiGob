"""
input_helper.py
==============

This module provides the InputHelper class, which offers a user-friendly interface for querying and exploring valid input parameter combinations for scenario analysis in the OptiGob framework. It wraps the InputQuery class and provides additional convenience methods for users to inspect, filter, and display possible input combinations for use with the Optigob API.

Typical usage example:
    helper = InputHelper()
    helper.print_all_combos()
    df = helper.get_combos_df()
    combos = helper.get_combos_dict()
    filtered = helper.filter_combos(input_type="forest", broadleaf_frac=0.5)
"""

from optigob.resource_manager.input_query import InputQuery
import pandas as pd

class InputHelper:
    """
    InputHelper class for querying and displaying valid input parameter combinations for Optigob scenarios.
    Provides convenience methods to print, filter, and retrieve input combos as DataFrames or dicts.
    """
    def __init__(self):
        self.query = InputQuery()

    def get_combos_dict(self):
        """
        Returns all valid input combinations as a dictionary.
        Returns:
            dict: {input_type: [combo_dict, ...], ...}
        """
        return self.query.get_all_input_combos()

    def get_combos_df(self):
        """
        Returns all valid input combinations as a pandas DataFrame.
        Returns:
            pd.DataFrame: DataFrame with all input combinations and input_type column.
        """
        return self.query.get_all_input_combos_df()

    def print_all_combos(self):
        """
        Prints all valid input combinations to the screen, grouped by input type.
        """
        combos = self.get_combos_dict()
        for input_type, combo_list in combos.items():
            print(f"\nInput type: {input_type}")
            for combo in combo_list:
                print(combo)

    def filter_combos(self, input_type=None, **kwargs):
        """
        Filters input combinations by input_type and/or parameter values.
        Args:
            input_type (str, optional): Filter by input type (e.g., 'forest', 'organic_soil').
            **kwargs: Additional key-value pairs to filter on (e.g., broadleaf_frac=0.5).
        Returns:
            pd.DataFrame: Filtered DataFrame of input combinations.
        """
        df = self.get_combos_df()
        if input_type:
            df = df[df['input_type'] == input_type]
        for k, v in kwargs.items():
            if k in df.columns:
                df = df[df[k] == v]
        return df.reset_index(drop=True)

    def print_readable_combos(self, max_rows_per_type=10):
        """
        Prints a nicely formatted, readable summary of valid input combinations,
        grouped by input type. Limits rows per input type for readability.
        Args:
            max_rows_per_type (int): Maximum number of combos to show per input type.
        """
        combos = self.get_combos_dict()
        for input_type, combo_list in combos.items():
            print(f"\n\033[1mInput type: {input_type}\033[0m")  # Bold for input_type
            if not combo_list:
                print("  (No combos found)")
                continue
            # Get all keys for this input_type (preserves column order)
            keys = list(combo_list[0].keys())
            # Print header
            print("  " + " | ".join([f"{k}" for k in keys]))
            print("  " + "-" * (len(" | ".join(keys)) + 2))
            # Print each combo, up to max_rows_per_type
            for i, combo in enumerate(combo_list):
                if i == max_rows_per_type:
                    print(f"  ... ({len(combo_list) - max_rows_per_type} more combos not shown)")
                    break
                print("  " + " | ".join([str(combo[k]) for k in keys]))
