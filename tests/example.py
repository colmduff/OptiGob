from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

def main():
    data = './data/sip.json'
    # Initialize the data manager
    data_manager = OptiGobDataManager(data)

    # Create an instance of Optigob
    optigob = Optigob(data_manager)

    # Get baseline and target populations
    baseline_beef_population = optigob.get_baseline_beef_population()
    baseline_dairy_population = optigob.get_baseline_dairy_population()
    target_beef_population = optigob.get_target_beef_population()
    target_dairy_population = optigob.get_target_dairy_population()

    print(f"Baseline Beef Population: {baseline_beef_population}")
    print(f"Baseline Dairy Population: {baseline_dairy_population}")
    print(f"Target Beef Population: {target_beef_population}")
    print(f"Target Dairy Population: {target_dairy_population}")

if __name__ == '__main__':
    main()