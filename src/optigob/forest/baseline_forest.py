
class BaselineForest:
    def __init__(self, optigob_data_manager):
        self.data_manager_class = optigob_data_manager

        self.baseline_year = self.data_manager_class.get_baseline_year()
        self.harvest_rate = "low"


    def get_managed_forest_offset(self):
        """
        """
        managed_forest_df = self.data_manager_class.get_static_forest_scaler(
            target_year=self.baseline_year,
            harvest=self.harvest_rate
        )

        return managed_forest_df["emission_value"].item()
    

    def get_total_forest_offset(self):
        """
        """
        forest_val = self.get_managed_forest_offset()     
        return forest_val
    
    
    def get_managed_forest_area(self):
        """
        """
        managed_forest_df = self.data_manager_class.get_static_forest_scaler(
            target_year=self.baseline_year,
            harvest=self.harvest_rate
        )
        return managed_forest_df["area_ha"].item()