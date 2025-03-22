import json
import yaml  # PyYAML package
import os
import pandas as pd

class ImportFactory:
    @staticmethod
    def load_config(config_path):
        """
        Loads a configuration file (JSON, YAML) based on the file extension.
        
        Parameters:
            config_path (str): Path to the configuration file.
        
        Returns:
            dict: The loaded configuration as a dictionary.
        """
        _, ext = os.path.splitext(config_path)
        
        with open(config_path, 'r') as file:
            if ext.lower() == '.json':
                return json.load(file)
            elif ext.lower() in ['.yaml', '.yml']:
                return yaml.safe_load(file)
            else:
                raise ValueError(f"Unsupported file extension: {ext}")
