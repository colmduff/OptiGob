"""
protein_crops_budget
====================

This module contains the ProteinCropsBudget class, which is used to calculate various protein crop-related metrics
such as area, emissions (CO2, CH4, N2O, CO2e), and protein yield for protein crops.

Class:
    ProteinCropsBudget: Calculates area, emissions, and protein yield for protein crops.

Methods in ProteinCropsBudget:
    __init__(self, optigob_data_manager): Initializes the ProteinCropsBudget with the given data manager.
    get_crop_area(self): Returns the area for the protein crop and abatement in hectares (multiplied by the crop area multiplier).
    get_crop_emission_ch4(self): Returns the CH4 emission for the protein crop and abatement in kilotons.
    get_crop_emission_n2o(self): Returns the N2O emission for the protein crop and abatement in kilotons.
    get_crop_emission_co2(self): Returns the CO2 emission for the protein crop and abatement in kilotons.
    get_crop_emission_co2e(self): Returns the CO2e emission for the protein crop and abatement in kilotons.
    get_crop_protein_yield(self): Returns the protein yield for the protein crop and abatement in kg (multiplied by the crop area multiplier).
"""

class ProteinCropsBudget:
    def __init__(self, optigob_data_manager):
        """
        Initializes the ProteinCropsBudget with the given data manager.
        Reads target year, scenario, abatement, and crop area multiplier from the data manager.
        """
        self.data_manager_class = optigob_data_manager
        self.target_year = self.data_manager_class.get_target_year()
        self.abatement = self.data_manager_class.get_abatement_type()
        self.protein_crop_included = self.data_manager_class.get_protein_crop_included()
        self.crop_area_multiplier = self.data_manager_class.get_protein_crop_multiplier()
        self.crop_protein = self.data_manager_class.get_protein_content_scaler('crops')


    def zero_if_not_included(method):
        def wrapper(self, *args, **kwargs):
            if not getattr(self, "protein_crop_included", False):
                return 0
            return method(self, *args, **kwargs)
        return wrapper

    @zero_if_not_included
    def get_crop_area(self):
        """
        Returns the area for the protein crop and abatement in hectares (multiplied by the crop area multiplier).
        """

        crop_area_df = self.data_manager_class.get_protein_crop_emission_scaler(
            year=self.target_year,
            abatement=self.abatement,
            ghg='CO2e'
        )
        return crop_area_df["area"].item() * self.crop_area_multiplier

    @zero_if_not_included
    def get_crop_emission_ch4(self):
        """
        Returns the CH4 emission for the protein crop and abatement in kilotons.
        """
        crop_emission_df = self.data_manager_class.get_protein_crop_emission_scaler(
            year=self.target_year,
            abatement=self.abatement,
            ghg='CH4'
        )
        return crop_emission_df["value"].item() * self.crop_area_multiplier
    
    @zero_if_not_included
    def get_crop_emission_n2o(self):
        """
        Returns the N2O emission for the protein crop and abatement in kilotons.
        """
        crop_emission_df = self.data_manager_class.get_protein_crop_emission_scaler(
            year=self.target_year,
            abatement=self.abatement,
            ghg='N2O'
        )
        return crop_emission_df["value"].item() * self.crop_area_multiplier
    
    @zero_if_not_included
    def get_crop_emission_co2(self):
        """
        Returns the CO2 emission for the protein crop and abatement in kilotons.
        """
        crop_emission_df = self.data_manager_class.get_protein_crop_emission_scaler(
            year=self.target_year,
            abatement=self.abatement,
            ghg='CO2'
        )
        return crop_emission_df["value"].item() * self.crop_area_multiplier
    
    @zero_if_not_included
    def get_crop_emission_co2e(self):
        """
        Returns the CO2e emission for the protein crop and abatement in kilotons.
        """
        crop_emission_df = self.data_manager_class.get_protein_crop_emission_scaler(
            year=self.target_year,
            abatement=self.abatement,
            ghg='CO2e'
        )
        return crop_emission_df["value"].item() * self.crop_area_multiplier
    
    @zero_if_not_included
    def get_crop_protein_yield(self):
        """
        Returns the protein yield for the protein crop and abatement in kg (multiplied by the crop area multiplier).
        """
        crop_protein_yield_df = self.data_manager_class.get_protein_crop_protein_scaler(
            year=self.target_year,
            abatement=self.abatement
        )

        return (crop_protein_yield_df["value"].item() * self.crop_protein)* self.crop_area_multiplier


