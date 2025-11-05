# Model Limitations

`OptiGob` is designed as an exploratory decision-support tool for Ireland’s AFOLU (Agriculture, Forestry and Other Land Use) sector. While it provides a flexible platform for testing climate and land-use transition pathways, several limitations should be noted.

## Climate Neutrality Verification

`OptiGob` does **not** guarantee that user-defined configurations achieve climate neutrality.  
Users must verify whether selected pathways meet chosen targets.

## Scenario and Data Constraints

- The default SQLite database includes a limited set of **predefined combinations** for certain parameters (e.g., wetland restoration levels, forestry on organic soils).  
- Target years are currently **capped at 2050**, reflecting the availability of agricultural and animal productivity data.  
- Users can extend these limits by supplying a customised database.

## Assumptions and Uncertainty

Default emissions factors and productivity assumptions are based on nationally representative datasets and technical mitigation pathways.  
They do **not** capture uncertainty in adoption rates, behavioural responses, or emerging technologies.

## Model Scope

- The model operates at the **national scale** only; spatial differentiation (e.g., catchment-level or regional variation) is not yet implemented.  
- **Economic feedbacks** (e.g., price, trade, or demand effects) are not currently represented.
