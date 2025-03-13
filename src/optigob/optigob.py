from optigob.optimisation.livestock_optimisation import LivestockOptimisation


class Optigob:
    def __init__(self, optigob_data_manager):
        self.data_manager_class = optigob_data_manager
        self.livestock_optimisation = LivestockOptimisation(optigob_data_manager)

        self.baseline_year = self.data_manager_class.get_baseline_year()
        self.target_year = self.data_manager_class.get_target_year()
        self.abatement_scenario = self.data_manager_class.get_abatement_scenario()
        self.gas = self.data_manager_class.get_gas()
        self.emissions_budget = self.data_manager_class.get_emissions_budget()
        self.dairy_beef_ratio = self.data_manager_class.get_dairy_beef_ratio()


        # Internal cache to store the optimization result for the baseline population.
        self._baseline_year_dict = None
        self._target_year_dict = None

    def _get_baseline_year_dict(self):
        """
        Retrieves and caches the livestock population for the baseline year.
        
        If the population has already been calculated, the cached value is returned.
        Otherwise, the optimization is run and the result is stored in the cache.
        """
        if self._baseline_year_dict is None:
            # Run the optimization and cache the result.
            self._baseline_year_dict = self.livestock_optimisation.optimise_livestock_pop(
                self.gas,
                self.emissions_budget,
                self.dairy_beef_ratio,
                self.baseline_year,
                self.abatement_scenario
            )
        return self._baseline_year_dict
    
    def _get_target_year_dict(self):
        """
        Retrieves and caches the livestock population for the target year.
        
        If the population has already been calculated, the cached value is returned.
        Otherwise, the optimization is run and the result is stored in the cache.
        """
        if self._target_year_dict is None:
            # Run the optimization and cache the result.
            self._target_year_dict = self.livestock_optimisation.optimise_livestock_pop(
                self.gas,
                self.emissions_budget,
                self.dairy_beef_ratio,
                self.target_year,
                self.abatement_scenario
            )
        return self._target_year_dict

    def get_baseline_beef_population(self):
        """
        Retrieves the baseline beef population using the cached optimization result.
        
        Returns:
            The beef population (e.g., in actual animal numbers) from the optimization.
        """

        pop = self._get_baseline_year_dict()

        return pop["Beef_animals"]

    def get_baseline_dairy_population(self):
        """
        Retrieves the baseline dairy population using the cached optimization result.
        
        Returns:
            The dairy population (e.g., in actual animal numbers) from the optimization.
        """

        pop = self._get_baseline_year_dict()
        return pop["Dairy_animals"]
    
    
    def get_target_beef_population(self):
        """
        Retrieves the target beef population using the cached optimization result.
        
        Returns:
            The beef population (e.g., in actual animal numbers) from the optimization.
        """

        pop = self._get_target_year_dict()
        return pop["Beef_animals"]
    
    def get_target_dairy_population(self):
        """
        Retrieves the target dairy population using the cached optimization result.
        
        Returns:
            The dairy population (e.g., in actual animal numbers) from the optimization.
        """

        pop = self._get_target_year_dict()
        return pop["Dairy_animals"]
    

