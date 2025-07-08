import plotly.graph_objects as go
from optigob.optigob import Optigob
from optigob.resource_manager.optigob_data_manager import OptiGobDataManager

# Load data as in example.py
data = './data/sip.yaml'
data_manager = OptiGobDataManager(data)
optigob = Optigob(data_manager)

# Get total area by sector (scenario)
area_by_sector = optigob.get_aggregated_total_land_area_by_sector()['scenario']
sectors = list(area_by_sector.keys())
areas = list(area_by_sector.values())

total_area = sum(areas)

# Prepare output nodes for each sector
def get_sector_outputs(sector):
    # Example: emissions, protein, bioenergy, CCS (if available)
    emissions = optigob.get_scenario_co2e_emissions_by_sector().get(sector, 0)
    protein = optigob.get_total_protein_by_sector()['scenario'].get(sector, 0)
    bioenergy = optigob.get_bioenergy_by_sector()['scenario'].get(sector, 0)
    # CCS/negative emissions could be added if available
    return emissions, protein, bioenergy

# Build node list
nodes = ['Total Area'] + sectors + []
output_types = ['Emissions', 'Protein', 'Bioenergy']
for out in output_types:
    for sector in sectors:
        nodes.append(f'{sector} {out}')

# Build links: Total Area -> Sectors
sources = []
targets = []
values = []
labels = []

# Total Area to Sectors
for i, (sector, area) in enumerate(zip(sectors, areas)):
    sources.append(0)  # 'Total Area' node
    targets.append(i+1)  # sector node
    values.append(area)
    labels.append(f'{area:.0f} ha')

# Sectors to Outputs
for i, sector in enumerate(sectors):
    emissions, protein, bioenergy = get_sector_outputs(sector)
    base_idx = 1 + len(sectors) + i*len(output_types)
    # Emissions
    sources.append(i+1)
    targets.append(len(sectors)+1 + i*len(output_types))
    values.append(emissions)
    labels.append(f'{emissions:.1f} kt CO2e')
    # Protein
    sources.append(i+1)
    targets.append(len(sectors)+2 + i*len(output_types))
    values.append(protein)
    labels.append(f'{protein:.1f} kg protein')
    # Bioenergy
    sources.append(i+1)
    targets.append(len(sectors)+3 + i*len(output_types))
    values.append(bioenergy)
    labels.append(f'{bioenergy:.1f} GJ bioenergy')

# Build Sankey diagram
data = go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes,
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        label=labels,
    )
)

fig = go.Figure(data)
fig.update_layout(title_text="Land Area Flow to Sectors and Outputs (Scenario)", font_size=10)

#save the figure
fig.write_html("./data/sankey_diagram.html")
