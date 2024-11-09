import plotly.express as px
from palmerpenguins import load_penguins
from shiny.express import input, ui, render
from shinywidgets import render_widget, render_plotly
import seaborn as sns

# Load the penguins dataset
penguins = load_penguins()

# Set up the UI options
ui.page_opts(title="Pojetta and the Penguin Plots", fillable=True)

# ADD A SIDEBAR
with ui.sidebar(
    position="right", bg="#E5E1E6", open="open"
): 
    ui.h2("Sidebar")  # Sidebar header

    # Dropdown menu 
    ui.input_selectize(
        "selected_attribute",
        "Histogram Attributes",
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Numeric input for Plotly histogram
    ui.input_numeric("plotly_bin_count", "Bin Count (Plotly Histogram)", 50, min=1, max=100)

    # Slider input for Seaborn
    ui.input_slider(
        "seaborn_bin_count", "Bin Count (Seaborn Histogram)", 5, 50, 25
    )

    # Checkbox to filter species
    ui.input_checkbox_group(
        "selected_species_list",
        "Select a Species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )

    # Dividing line
    ui.hr()

    # Hyperlink to GitHub repo
    ui.h5("GitHub Repo")
    ui.a(
        "cintel-02-data",
        href="https://github.com/Pojetta/cintel-02-data",
        target="_blank",
    )

# Main content layout

with ui.layout_columns(): 
    # Display the Plotly Histogram
    with ui.card():
        ui.card_header("Plotly Histogram")

        @render_plotly
        def plotly_histogram():
            return px.histogram(
                penguins,
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
                color_discrete_sequence=["#C964CF", "#008C95", "#FFAA4D"],  # Custom colors for the histogram
            )

    # Display Data Table (showing all data)
    with ui.card():
        ui.card_header("Data Table")

        @render.data_frame
        def data_table():
            return render.DataTable(penguins)

    # Display Data Grid (showing all data)
    with ui.card():
        ui.card_header("Data Grid")

        @render.data_frame
        def data_grid():
            return render.DataGrid(penguins)

with ui.layout_columns():
    # Plotly Scatterplot (showing selected species)
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            # Filter the dataset based on selected species
            filtered_data = penguins[penguins['species'].isin(input.selected_species_list())]
            return px.scatter(
                data_frame=filtered_data,  # Use the filtered dataset
                x="body_mass_g",
                y="bill_length_mm",
                color="species",
                labels={
                    "bill_length_mm": "Bill Length (mm)",
                    "body_mass_g": "Body Mass (g)",
                },
                color_discrete_sequence=["#C964CF", "#008C95", "#FFAA4D"],  # Custom colors for the scatterplot
            )

    # Seaborn Histogram (showing all species)
    with ui.card():
        ui.card_header("Seaborn Histogram")

        @render.plot
        def seaborn_histogram():
            ax = sns.histplot(
                data=penguins,
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
            )
            ax.set_title("Palmer Penguins")
            ax.set_xlabel(input.selected_attribute())
            ax.set_ylabel("Count")
            return ax
