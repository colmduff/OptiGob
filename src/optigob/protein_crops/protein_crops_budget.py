"""
protein_crops_budget
====================

This module contains the ProteinCropsBudget class, which is used to calculate various protein crop-related metrics
such as area, emissions, and protein yield for protein crop production.

Class:
    ProteinCropsBudget: Calculates area, emissions, and protein yield for protein crops.

Methods in ProteinCropsBudget:
    __init__(self, optigob_data_manager): Initializes the ProteinCropsBudget with the given data manager.
    get_crop_area(self): Returns the protein crop area in hectares.
    get_crop_emission_ch4(self): Returns the protein crop CH4 emissions in kilotons.
    get_crop_emission_n2o(self): Returns the protein crop N2O emissions in kilotons.
    get_crop_emission_co2(self): Returns the protein crop CO2 emissions in kilotons.
    get_crop_emission_co2e(self): Returns the protein crop CO2e emissions in kilotons.
    get_crop_protein_yield(self): Returns the protein crop protein yield in kilotons.
"""

class ProteinCropsBudget:
    def __init__(self, optigob_data_manager):
        """
        Initializes the ProteinCropsBudget with the given data manager.
        
        Args:
            optigob_data_manager: Data manager instance providing access to all model data and configuration.
        """
        self.data_manager_class = optigob_data_manager
        self.target_year = self.data_manager_class.get_target_year()
        self.abatement_type = self.data_manager_class.get_abatement_type()
        self.protein_crop_multiplier = self.data_manager_class.get_protein_crop_multiplier()
        
        # Check if protein crops are included in the scenario
        self.protein_crop_included = getattr(self.data_manager_class, 'get_protein_crop_included', lambda: True)()

    def zero_if_protein_crop_not_included(method):
        """Decorator to return 0 if protein crops are not included."""
        def wrapper(self, *args, **kwargs):
            if not self.protein_crop_included:
                return 0.0
            return method(self, *args, **kwargs)
        return wrapper

    @zero_if_protein_crop_not_included
    def get_crop_area(self):
        """
        Returns the protein crop area in hectares.
        
        Returns:
            float: Protein crop area in hectares.
        """
        area_data = self.data_manager_class.get_protein_crop_emission_scaler(
            year=self.target_year,
            gas="CO2e",
            abatement=self.abatement_type
        )
        return float(area_data["area"].item() * self.protein_crop_multiplier)

    @zero_if_protein_crop_not_included
    def get_crop_emission_ch4(self):
        """
        Returns the protein crop CH4 emissions in kilotons.
        
        Returns:
            float: CH4 emissions in kilotons.
        """
        emission_data = self.data_manager_class.get_protein_crop_emission_scaler(
            year=self.target_year,
            gas="CH4",
            abatement=self.abatement_type
        )
        return float(emission_data["emission_value"].item() * self.protein_crop_multiplier)

    @zero_if_protein_crop_not_included
    def get_crop_emission_n2o(self):
        """
        Returns the protein crop N2O emissions in kilotons.
        
        Returns:
            float: N2O emissions in kilotons.
        """
        emission_data = self.data_manager_class.get_protein_crop_emission_scaler(
            year=self.target_year,
            gas="N2O",
            abatement=self.abatement_type
        )
        return float(emission_data["emission_value"].item() * self.protein_crop_multiplier)

    @zero_if_protein_crop_not_included
    def get_crop_emission_co2(self):
        """
        Returns the protein crop CO2 emissions in kilotons.
        
        Returns:
            float: CO2 emissions in kilotons.
        """
        emission_data = self.data_manager_class.get_protein_crop_emission_scaler(
            year=self.target_year,
            gas="CO2",
            abatement=self.abatement_type
        )
        return float(emission_data["emission_value"].item() * self.protein_crop_multiplier)

    @zero_if_protein_crop_not_included
    def get_crop_emission_co2e(self):
        """
        Returns the protein crop CO2e emissions in kilotons.
        
        Returns:
            float: CO2e emissions in kilotons.
        """
        emission_data = self.data_manager_class.get_protein_crop_emission_scaler(
            year=self.target_year,
            gas="CO2e",
            abatement=self.abatement_type
        )
        return float(emission_data["emission_value"].item() * self.protein_crop_multiplier)

    @zero_if_protein_crop_not_included
    def get_crop_protein_yield(self):
        """
        Returns the protein crop protein yield in kilotons.
        
        Returns:
            float: Protein yield in kilotons.
        """
        protein_data = self.data_manager_class.get_protein_crop_protein_scaler(
            year=self.target_year,
            gas="CO2e",
            abatement=self.abatement_type
        )
        return float(protein_data["protein_yield"].item() * self.protein_crop_multiplier)