"""
This module provides the BaselineForest class for managing forest data and calculating offsets.

Classes:
    BaselineForest: Manages forest data and calculates forest offsets.

Methods in BaselineForest:
    __init__(self, optigob_data_manager): Initializes the BaselineForest with a data manager.
    get_managed_forest_offset(self): Returns the managed forest emission offset in kt.
    get_total_forest_offset(self): Returns the total forest emission offset in kt.
    get_managed_forest_area(self): Returns the managed forest area in hectares.
    get_managed_forest_hnv_area(self): Returns the HNV managed forest area in hectares.
    get_hwp_volume(self): Returns the harvested wood product volume in cubic meters.
"""

class BaselineForest:
    def __init__(self, optigob_data_manager):
        """
        Initializes the BaselineForest with a data manager.

        Args:
            optigob_data_manager: An instance of the data manager class.
        """
        self.data_manager_class = optigob_data_manager

        self.baseline_year = self.data_manager_class.get_baseline_year()
        self.harvest_rate = "low"


    def get_managed_forest_offset(self):
        """
        Returns the managed forest emission offset in kt.

        Returns:
            float: The managed forest emission offset in kilotons.
        """
        managed_forest_df = self.data_manager_class.get_static_forest_scaler(
            target_year=self.baseline_year,
            harvest=self.harvest_rate
        )

        return managed_forest_df["emission_value"].item()

    def get_total_forest_offset(self):
        """
        Returns the total forest emission offset in kt.

        Returns:
            float: The total forest emission offset in kilotons.
        """
        forest_val = self.get_managed_forest_offset()     
        return forest_val

    def get_managed_forest_area(self):
        """
        Returns the managed forest area in hectares.

        Returns:
            float: The managed forest area in hectares.
        """
        managed_forest_df = self.data_manager_class.get_static_forest_scaler(
            target_year=self.baseline_year,
            harvest=self.harvest_rate
        )
        return managed_forest_df["area"].item()
    
    def get_managed_forest_hnv_area(self):
        """
        Returns the managed forest high nature value area in hectares.

        Returns:
            float: The managed forest high nature value area in hectares.
        """
        managed_forest_df = self.data_manager_class.get_static_forest_scaler(
            target_year=self.baseline_year,
            harvest=self.harvest_rate
        )
        return managed_forest_df["hnv_area"].item()
    
    def get_hwp_volume(self):
        """
        Retrieves the volume of harvested wood products (in cubic meters).

        NOTE: This method currently returns 0 as a placeholder.
        """

        return 0