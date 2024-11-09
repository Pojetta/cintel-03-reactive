from shiny import reactive
import plotly.express as px
from palmerpenguins import load_penguins
from shiny.express import input, ui, render
from shinywidgets import render_widget, render_plotly
import seaborn as sns

# Load the penguins dataset
penguins = load_penguins()

# Set up the UI options
ui.page_opts(title="Pojetta and the Penguin Plots", fillable=True)

# Add a sidebar with input components
with ui.sidebar(
    position="right", bg="#e6b6e8", open="open"
):

    # Sidebar header
    ui.h2("Sidebar")  
    
    # Checkbox to filter species plotly scatterplot
    ui.input_checkbox_group(
        "selected_species_list_scatterplot",
        "Select a Species (Scatterplot)",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )

    # Checkbox to filter plotly histogram species 
    ui.input_checkbox_group(
        "selected_species_list_histogram",
        "Select a Species (Histogram)",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )
    # Dropdown menu for histogram attribute
    ui.input_selectize(
        "selected_attribute",
        "Histogram Attribute",
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Slider input for plotly histogram bin count
    ui.input_slider(
        "plotly_bin_count", "Histogram Bin Count", 5, 100, 50
    )

    # Dividing line
    ui.hr()

    # Hyperlink to GitHub repo
    ui.h5("GitHub Repo")
    ui.a(
        "cintel-03-data",
        href="https://github.com/Pojetta/cintel-03-data",
        target="_blank",
    )

# Main content layout
with ui.nav_panel("Plots"):
    # Plotly Scatterplot (showing selected species)
    with ui.card():
        ui.card_header("Scatterplot")
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                data_frame=filtered_data_scatterplot(),  # Use scatterplot-specific filtered data
                title="Pojetta's Palmer Penguins",
                x="bill_length_mm",
                y="body_mass_g",
                color="species",
                labels={
                    "bill_length_mm": "Bill Length (mm)",
                    "body_mass_g": "Body Mass (g)",
                },
                color_discrete_sequence=["#C964CF", "#008C95", "#FFAA4D"],  # Custom colors for the scatterplot
            )

    # Plotly Histogram
    with ui.card():
        ui.card_header("Histogram")
        @render_plotly
        def plotly_histogram():
            return px.histogram(
                data_frame=filtered_data_histogram(),  # Use histogram-specific filtered data
                title="Pojetta's Palmer Penguins",
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
                color_discrete_sequence=["#C964CF", "#008C95", "#FFAA4D"],  # Custom colors for the histogram
            ) 

with ui.nav_panel("Tables"):    
    # Display Data Table (showing all data)   
    with ui.card(full_screen=True):
        ui.card_header("Data Table")
        @render.data_frame
        def data_table():
            return render.DataTable(penguins)

    # Display Data Grid (showing all data)
    with ui.card(full_screen=True):
        ui.card_header("Data Grid")
        @render.data_frame
        def data_grid():
            return render.DataGrid(penguins)
    
# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input function used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

# Filtered data for the scatterplot
@reactive.calc
def filtered_data_scatterplot():
    selected_species_scatterplot = input.selected_species_list_scatterplot()
    if selected_species_scatterplot:
        return penguins[penguins['species'].isin(selected_species_scatterplot)]
    return penguins

# Filtered data for the histogram
@reactive.calc
def filtered_data_histogram():
    selected_species_histogram = input.selected_species_list_histogram()
    if selected_species_histogram:
        return penguins[penguins['species'].isin(selected_species_histogram)]
    return penguins

