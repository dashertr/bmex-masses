from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import utils.dash_reusable_components as drc
import utils.views_class as views
import numpy as np


class Sidebar:
    
    def __init__(self, views_dict={"dimension": 'landscape', "chain": 'isotopic', "quantity": 'BE', "dataset": ['EXP'], 
           "colorbar": 'linear', "wigner": [0], "proton": [None], "neutron": [None], "nucleon": [None], 
           "range": {"x": [None, None], "y": [None, None]}, "colorbar_range": [None, None], "uncertainty": False},
             series_tab=1, maintabs_length=1):
        for key in views_dict:
            setattr(self, key, views_dict[key])
        if series_tab == "new":
            self.series_n = len(views_dict["dataset"])
        else:
            self.series_n = series_tab
        self.maintabs_length = maintabs_length

    def proton_card(self, index):
        return drc.Card(
            id="protons-card",
            children=[
                html.P("Protons:", style={"padding-left": '.5rem'}),
                dcc.Input(
                    id={'type': 'input-protons','index': index+1},
                    type="number",
                    min=0,
                    max=200,
                    step=1,
                    placeholder="Proton #",
                    value=self.proton[index],
                    className="nucleon-input"
                ),
            ],
        )

    def neutron_card(self, index):
        return drc.Card(
            id="neutrons-card",
            children=[
                html.P("Neutrons:", style={"padding-left": '.5rem'}),
                dcc.Input(
                    id={'type': 'input-neutrons','index': index+1},
                    type="number",
                    min=0,
                    max=200,
                    step=1,
                    placeholder="Neutron #",
                    value=self.neutron[index],
                    className="nucleon-input"
                ),
            ],
        )

    def nucleon_card(self, index):
        if self.dimension == '1D':
            if self.chain == "isotopic":
                return self.proton_card(index)
            elif self.chain == "isotonic":
                return self.neutron_card(index)
            elif self.chain == "isobaric":
                return drc.Card(
                    id="nucleons-card",
                    children=[
                        html.P("Nucleons:", style={"padding-left": '.5rem'}),
                        dcc.Input(
                            id={'type': 'input-nucleons','index': index+1},
                            type="number",
                            min=0,
                            max=400,
                            step=1,
                            placeholder="Nucleon #",
                            value=self.nucleon[index],
                            className="nucleon-input"
                        ),
                    ],
                )
            else:
                return html.P("ERROR")

    def get_letter(self):
        if self.chain=='isotopic':
            return "Z"
        if self.chain=='isotonic':
            return "N"
        return "A"

    def get_nucleon_count(self, i):
        if self.chain=='isotopic':
            return self.proton[i]
        if self.chain=='isotonic':
            return self.neutron[i]
        return self.nucleon[i]

    def show(self):
        
        output = [
            drc.Card(id="dimension-card", title='Select a dimensionality of data to analyze', children=[
                drc.NamedDropdown(
                    name="Dimension",
                    id={'type': 'dropdown-dimension','index': 1},
                    options=[
                        {"label": "Single Nucleus", "value": "single"},
                        {"label": "1D Chains", "value": "1D"},
                        {"label": "Landscape", "value": "landscape"},
                    ],
                    clearable=False,
                    searchable=False,
                    value=self.dimension,
                )
            ])
        ]

        if self.dimension == '1D':
            output.append(
                drc.Card(id="oneD-card", title='Select the type of chain to plot', children=[
                    drc.NamedDropdown(
                        name='1D Chain',
                        id={'type': 'dropdown-1D','index': 1},
                        options=[
                            {"label": "Isotopic Chain", "value": "isotopic"},
                            {"label": "Isotonic Chain", "value": "isotonic"},
                            {"label": "Isobaric Chain", "value": "isobaric"},
                        ],
                        clearable=False,
                        searchable=False,
                        value=self.chain,
                    )
                ])
            )

        if self.dataset[self.series_n-1] in ['ME2', 'MEdelta', 'PC1', 'Nl3S']:
            quantity_options = [
                {"label": "Binding Energy", "value": "BE", "title": "Energy required to completely seperate the nucleus: \n B(N,Z)"},
                {"label": "One Neutron Separation Energy", "value": "OneNSE", "title": "Energy required to remove a neutron: \n S\u2099(N,Z) = B(N,Z) - B(N-1,Z)", "disabled": True},
                {"label": "One Proton Separation Energy", "value": "OnePSE", "title": "Energy required to remove a proton: \n S\u209A(N,Z) = B(N,Z) - B(N,Z-1)", "disabled": True},
                {"label": "Two Neutron Separation Energy", "value": "TwoNSE", "title": "Energy required to remove two neutrons: \n S\u2082\u2099(N,Z) = B(N,Z) - B(N-2,Z)"},
                {"label": "Two Proton Separation Energy", "value": "TwoPSE", "title": "Energy required to remove two protons: \n S\u2082\u209A(N,Z) = B(N,Z) - B(N,Z-2)"},
                {"label": "Alpha Separation Energy", "value": "AlphaSE", "title": "Energy required to remove an alpha particle: \n S\u2090 = B(N,Z) - B(N-2,Z-2) - 28.3 MeV"},
                {"label": "Two Neutron Shell Gap", "value": "TwoNSGap", "title": "\u03B4\u2082\u2099(N,Z) = S\u2082\u2099(N,Z) - S\u2082\u2099(N+2,Z)"},
                {"label": "Two Proton Shell Gap", "value": "TwoPSGap", "title": "\u03B4\u2082\u209A(N,Z) = S\u2082\u209A(N,Z) - S\u2082\u209A(N,Z+2)"},
                {"label": "Double Mass Difference", "value": "DoubleMDiff", "title": "\u03B4V\u209A\u2099(N,Z) = 1/4 S\u2082\u209A(N,Z) - S\u2082\u209A(N-2,Z)"},
                {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED", "title": "\u0394\u2099(N,Z) = 1/2 S\u2099(N,Z) -S\u2099(N+1,Z)", "disabled": True},
                {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED", "title": "\u0394\u209A(N,Z) = 1/2 S\u209A(N,Z) -S\u209A(N,Z+1)", "disabled": True},
                {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting", "title": "\u0394e\u2099(N,Z) = S\u2099(N,Z) - S\u2099(N+2,Z)", "disabled": True},
                {"label": "Single-Proton Energy Splitting", "value": "SPESplitting", "title": " \u0394e\u209A(N,Z) = S\u209A(N,Z) - S\u209A(N,Z+2)", "disabled": True},
                # {"label": "Wigner Energy Coefficient", "value": "WignerEC"},
                # {"label": "Quad Def Beta2", "value": "QDB2t"},
                {"label": "Binding Energy per Nucleon", "value": "BE/A", "title": "B/A(N,Z) = B(N,Z)/(N+Z)"},
            ]
        else:
            quantity_options = [
                {"label": "Binding Energy", "value": "BE", "title": "Energy required to completely seperate the nucleus: \n B(N,Z)"},
                {"label": "One Neutron Separation Energy", "value": "OneNSE", "title": "Energy required to remove a neutron: \n S\u2099(N,Z) = B(N,Z) - B(N-1,Z)"},
                {"label": "One Proton Separation Energy", "value": "OnePSE", "title": "Energy required to remove a proton: \n S\u209A(N,Z) = B(N,Z) - B(N,Z-1)"},
                {"label": "Two Neutron Separation Energy", "value": "TwoNSE", "title": "Energy required to remove two neutrons: \n S\u2082\u2099(N,Z) = B(N,Z) - B(N-2,Z)"},
                {"label": "Two Proton Separation Energy", "value": "TwoPSE", "title": "Energy required to remove two protons: \n S\u2082\u209A(N,Z) = B(N,Z) - B(N,Z-2)"},
                {"label": "Alpha Separation Energy", "value": "AlphaSE", "title": "Energy required to remove an alpha particle: \n S\u2090 = B(N,Z) - B(N-2,Z-2) - 28.3 MeV"},
                {"label": "Two Neutron Shell Gap", "value": "TwoNSGap", "title": "\u03B4\u2082\u2099(N,Z) = S\u2082\u2099(N,Z) - S\u2082\u2099(N+2,Z)"},
                {"label": "Two Proton Shell Gap", "value": "TwoPSGap", "title": "\u03B4\u2082\u209A(N,Z) = S\u2082\u209A(N,Z) - S\u2082\u209A(N,Z+2)"},
                {"label": "Double Mass Difference", "value": "DoubleMDiff", "title": "\u03B4V\u209A\u2099(N,Z) = 1/4 S\u2082\u209A(N,Z) - S\u2082\u209A(N-2,Z)"},
                {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED", "title": "\u0394\u2099(N,Z) = 1/2 S\u2099(N,Z) -S\u2099(N+1,Z)"},
                {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED", "title": "\u0394\u209A(N,Z) = 1/2 S\u209A(N,Z) -S\u209A(N,Z+1)"},
                {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting", "title": "\u0394e\u2099(N,Z) = S\u2099(N,Z) - S\u2099(N+2,Z)"},
                {"label": "Single-Proton Energy Splitting", "value": "SPESplitting", "title": " \u0394e\u209A(N,Z) = S\u209A(N,Z) - S\u209A(N,Z+2)"},
                # {"label": "Wigner Energy Coefficient", "value": "WignerEC"},
                # {"label": "Quad Def Beta2", "value": "QDB2t"},
                {"label": "Binding Energy per Nucleon", "value": "BE/A", "title": "B/A(N,Z) = B(N,Z)/(N+Z)"},
            ]
        if self.dimension=='single':
            quantity_options.append({"label": "All", "value": "All"})

        output.append(
            drc.Card(id="quantity-card", title='Select the quantity to be graphed on the selected figure', 
                children=[
                    drc.NamedDropdown(
                        name="Select Quantity",
                        id={'type': 'dropdown-quantity','index': 1},
                        options=quantity_options,
                        clearable=False,
                        searchable=False,
                        value=self.quantity,
                        maxHeight=160,
                        optionHeight=80,                           
                    )
                ]
            )
        )

        dataset_options = [
            {"label": "Experiment", "value": "EXP"},
            {"label": "ME2", "value": "ME2"},
            {"label": "MEdelta", "value": "MEdelta"},
            {"label": "PC1", "value": "PC1"},
            {"label": "NL3S", "value": "NL3S"},
            {"label": "SkMs", "value": "SKMS"},
            {"label": "SKP", "value": "SKP"},
            {"label": "SLY4", "value": "SLY4"},
            {"label": "SV", "value": "SV"},
            {"label": "UNEDF0", "value": "UNEDF0"},
            {"label": "UNEDF1", "value": "UNEDF1"},
        ]


        if self.quantity in ['OneNSE', 'OnePSE', 'N3PointOED', 'N3PointOED', 'SNESplitting', 'SPESplitting']:
            dataset_options = [
                {"label": "Experiment", "value": "EXP"},
                {"label": "ME2", "value": "ME2", "disabled": True},
                {"label": "MEdelta", "value": "MEdelta", "disabled": True},
                {"label": "PC1", "value": "PC1", "disabled": True},
                {"label": "NL3S", "value": "NL3S", "disabled": True},
                {"label": "SkMs", "value": "SKMS"},
                {"label": "SKP", "value": "SKP"},
                {"label": "SLY4", "value": "SLY4"},
                {"label": "SV", "value": "SV"},
                {"label": "UNEDF0", "value": "UNEDF0"},
                {"label": "UNEDF1", "value": "UNEDF1"},
            ]

        if self.quantity=="QDB2t":
            dataset_options = [
                {"label": "Experiment", "value": "EXP", "disabled": True},
                {"label": "ME2", "value": "ME2", "disabled": True},
                {"label": "MEdelta", "value": "MEdelta", "disabled": True},
                {"label": "PC1", "value": "PC1", "disabled": True},
                {"label": "NL3S", "value": "NL3S", "disabled": True},
                {"label": "SkMs", "value": "SKMS"},
                {"label": "SKP", "value": "SKP"},
                {"label": "SLY4", "value": "SLY4"},
                {"label": "SV", "value": "SV"},
                {"label": "UNEDF0", "value": "UNEDF0"},
                {"label": "UNEDF1", "value": "UNEDF1"},
            ] 

        tabs_component, series_button_card, uncertainty_card = None, None, [None]
        if self.dimension == '1D':
            tabs = []
            for i in range(len(self.dataset)):
                tabs.append(dcc.Tab(label=self.get_letter()+"="+str(self.get_nucleon_count(i))+" | "+str(self.dataset[i]), value='tab'+str(i+1), className='series-tab', selected_className='series-tab--selected'))
            if len(self.dataset) < 8:
                tabs.append(dcc.Tab(label="+", value='tab0', className='series-tab', selected_className='series-tab--selected'))  
            tabs_component = dcc.Tabs(id={'type': 'series_tabs','index': 1}, value='tab'+str(self.series_n), className='series-tabs', children=tabs)
            if len(self.dataset) > 1:
                series_button_card = drc.Card(id="delete-series-card", children=[
                    html.Button('Delete Series', id={'type': 'delete-series-button','index': 1}, value=None, className='delete-button')
                ])
            uncer_checklist = []
            if self.uncertainty[self.series_n-1]:
                uncer_checklist = ['Include Uncertainties']
            if self.dataset[self.series_n-1] == 'EXP':
                uncertainty_card = drc.Card(id="uncertainty-card", children=[
                    dcc.Checklist(options=['Include Uncertainties'], value=uncer_checklist, id={'type': 'uncertainty-checklist','index': 1}),
                ]),
            output.append(
                drc.Card(id='series-card', children=[
                    tabs_component,
                    self.nucleon_card(self.series_n-1),
                    drc.Card(id="dataset-card", children=[
                        drc.NamedDropdown(
                            name="Select Dataset",
                            id={'type': 'dropdown-dataset','index': self.series_n},
                            options=dataset_options,
                            clearable=False,
                            searchable=False,
                            value=self.dataset[self.series_n-1],
                        )
                    ]),
                    drc.Card(
                        id="Wigner-card", title='Allows for the adjustment from a Wigner term in the selected figure',
                        children=[
                            drc.NamedDropdown(
                                name="Wigner Adjustment",
                                id={'type': 'radio-wigner','index': 1},
                                options=[{"label": "None", "value": 0},{"label": "Wigner (1)", "value": 1},{"label": "Wigner (2)", "value": 2}],
                                clearable=False,
                                searchable=False,
                                value=self.wigner[self.series_n-1],
                            ),
                        ]
                    ),
                    uncertainty_card[0],
                    series_button_card
                ])
            )
        else:
            if self.dimension == 'single':
                output.append(self.proton_card(self.series_n-1))
                output.append(self.neutron_card(self.series_n-1))
            output.append(
                drc.Card(id="dataset-card", title='Select the experiment or model dataset to be used for the selected figure',
                    children=[
                        drc.NamedDropdown(
                            name="Select Dataset",
                            id={'type': 'dropdown-dataset','index': self.series_n},
                            options=dataset_options,
                            clearable=False,
                            searchable=False,
                            value=self.dataset[self.series_n-1],
                        )
                    ]
                ) 
            )
            output.append(
                drc.Card(
                    id="Wigner-card", title='Allows for the adjustment from a Wigner term in the selected figure',
                    children=[
                        drc.NamedDropdown(
                            name="Wigner Adjustment",
                            id={'type': 'radio-wigner','index': 1},
                            options=[
                                {"label": "None", "value": 0},
                                {"label": "Wigner (1)", "value": 1},
                                {"label": "Wigner (2)", "value": 2},
                            ],
                            clearable=False,
                            searchable=False,
                            value=self.wigner[self.series_n-1],
                        ),
                    ]
                ),
            )

        if self.dimension == 'landscape':
            output.append(
                drc.Card(
                    id="colorbar-card", title='Changes the color scheme of the selected figure',
                    children=[
                        drc.NamedDropdown(
                            name="Colorbar Style",
                            id={'type': 'dropdown-colorbar','index': 1},
                            options=[
                                {"label": "Linear", "value": "linear"},
                                {"label": "Equalized", "value": "equal"},
                                {"label": "Monochrome", "value": "monochrome"},
                                {"label": "Diverging", "value": "diverging"},
                            ],
                            clearable=False,
                            searchable=False,
                            value=self.colorbar,
                        )
                    ]
                )
            )
            output.append(
                drc.Card(id="colorbar-scale-card", children=[
                    html.Button("Rescale Colorbar", id={'type': 'rescale-colorbar-button','index': 1}, className='rescale-colorbar-button', 
                                title='Rescales the colorbar of the selected figure based on the min and max of its currently visable values'),
                ]),
            )
            # output.append(
            #     drc.Card(id="colorbar-slider-card", children=[
            #         dcc.RangeSlider(min=self.colorbar_range[0], max=self.colorbar_range[1], step=(self.colorbar_range[1]-self.colorbar_range[0])/10, id={'type': 'colorbar-slider','index': 1}, className='colorbar-slider'),
            #     ]),
            # )

        if self.maintabs_length > 2:
            output.append(
                drc.Card(id="delete-card", children=[
                    html.Button('Delete Plot', id={'type': 'delete-button','index': 1}, value=None, className='delete-button')
                ])
            )


        return output


