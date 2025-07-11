import marimo

__generated_with = "0.14.10"
app = marimo.App()


@app.cell
def _():
    import sys
    import os

    # Add the project root (parent of utils/) to the path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    import marimo as mo
    from optigob.optigob import Optigob
    from optigob.resource_manager.optigob_data_manager import OptiGobDataManager
    import matplotlib.pyplot as plt
    import numpy as np

    from utils.helpers import plot_stacked_bar
    from utils.config import DEFAULT_FIGSIZE, DEFAULT_CMAP, INPUT_DATA_PATH, FIGURES_PATH

    return (
        FIGURES_PATH,
        INPUT_DATA_PATH,
        OptiGobDataManager,
        Optigob,
        os,
        plot_stacked_bar,
    )


@app.cell
def _(INPUT_DATA_PATH, OptiGobDataManager, Optigob):
    # Initialize the data manager
    data_manager = OptiGobDataManager(INPUT_DATA_PATH)

    # Create an instance of Optigob
    optigob = Optigob(data_manager)
    return (optigob,)


@app.cell
def _(optigob):
    #Emisisons 
    co2e_df = optigob.get_total_emissions_co2e_by_sector_df()
    return (co2e_df,)


@app.cell
def _(co2e_df):
    print(co2e_df)
    return


@app.cell
def _(FIGURES_PATH, co2e_df, os, plot_stacked_bar):
    scenarios = ['baseline', 'scenario']
    scenario_labels=['Baseline', 'Scenario']

    fig, ax = plot_stacked_bar(
        co2e_df,
        scenarios=scenarios,
        y_label='CO2e Emissions (kt)',
        title='CO2e Emissions: Stacked by Category',
        scenario_labels=scenario_labels,
        ylim=(-15000, 30000)
    )

    fig.savefig(os.path.join(FIGURES_PATH,"co2e_stacked_bar.png"), dpi=400)
    return fig, scenario_labels, scenarios


@app.cell
def _(fig):
    fig
    return


@app.cell
def _(optigob):
    area_df= optigob.get_disaggregated_total_land_area_by_sector_df()
    return (area_df,)


@app.cell
def _(FIGURES_PATH, area_df, os, plot_stacked_bar, scenario_labels, scenarios):
    fig1, ax2 = plot_stacked_bar(
        area_df,
        scenarios=scenarios,
        y_label='Area (ha)',
        title='Area Footprint: Stacked by Category',
        scenario_labels=scenario_labels,
        ylim=(0, 7e6)
    )

    fig1.savefig(os.path.join(FIGURES_PATH,"area_stacked_bar.png"), dpi=400)
    return (fig1,)


@app.cell
def _(fig1):
    fig1
    return


@app.cell
def _(optigob):
    hnv_df =optigob.get_total_hnv_land_area_by_sector_df()
    return (hnv_df,)


@app.cell
def _(FIGURES_PATH, hnv_df, os, plot_stacked_bar, scenario_labels, scenarios):
    fig2, ax3 = plot_stacked_bar(
        hnv_df,
        scenarios=scenarios,
        y_label='Area (ha)',
        title='Area of High Nature Value: Stacked by Category',
        scenario_labels=scenario_labels,
        ylim=(0, 2.5e6)
    )

    fig2.savefig(os.path.join(FIGURES_PATH,"hnv_area_stacked_bar.png"), dpi=400)
    return (fig2,)


@app.cell
def _(fig2):
    fig2
    return


@app.cell
def _(optigob):
    protein_df = optigob.get_total_protein_by_sector_df()
    return (protein_df,)


@app.cell
def _(
    FIGURES_PATH,
    os,
    plot_stacked_bar,
    protein_df,
    scenario_labels,
    scenarios,
):
    fig3, ax4 = plot_stacked_bar(
        protein_df,
        scenarios=scenarios,
        y_label='Protein (kg)',
        title='Protein Output: Stacked by Category',
        scenario_labels=scenario_labels,
        ylim=(0, 1e9)
    )

    fig3.savefig(os.path.join(FIGURES_PATH,"protein_stacked_bar.png"), dpi=400)
    return (fig3,)


@app.cell
def _(fig3):
    fig3
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
