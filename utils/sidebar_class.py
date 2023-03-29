from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import utils.dash_reusable_components as drc
import utils.views_class as views
import numpy as np



class Sidebar:
    
    def __init__(self, views_dict={"dimension": 'landscape', "chain": 'isotopic', "quantity": 'BE', "dataset": ['EXP'], 
           "colorbar": 'linear', "wigner": 0, "proton": [None], "neutron": [None], "nucleon": [None]}, series_tab=1):
        for key in views_dict:
            setattr(self, key, views_dict[key])
        if series_tab == "new":
            self.series_n = len(views_dict["dataset"])
        else:
            self.series_n = series_tab

    def nucleon_card(self, index):
        if self.dimension == '1D':
            if self.chain == "isotopic":
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
            elif self.chain == "isotonic":
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

    def show(self):
        
        output = [
            drc.Card(id="dimension-card", children=[
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
                drc.Card(id="oneD-card", children=[
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

        output.append(
            drc.Card(id="quantity-card", children=[
                drc.NamedDropdown(
                    name="Select Quantity",
                    id={'type': 'dropdown-quantity','index': 1},
                    options=[
                        {"label": "All", "value": "All"},
                        {"label": "Binding Energy", "value": "BE"},
                        {"label": "One Neutron Separation Energy", "value": "OneNSE",},
                        {"label": "One Proton Separation Energy", "value": "OnePSE",},
                        {"label": "Two Neutron Separation Energy", "value": "TwoNSE",},
                        {"label": "Two Proton Separation Energy", "value": "TwoPSE",},
                        {"label": "Alpha Separation Energy", "value": "AlphaSE",},
                        {"label": "Two Proton Shell Gap", "value": "TwoNSGap",},
                        {"label": "Two Neutron Shell Gap", "value": "TwoPSGap",},
                        {"label": "Double Mass Difference", "value": "DoubleMDiff",},
                        {"label": "Neutron 3-Point Odd-Even Binding Energy Difference", "value": "N3PointOED",},
                        {"label": "Proton 3-Point Odd-Even Binding Energy Difference", "value": "P3PointOED",},
                        {"label": "Single-Neutron Energy Splitting", "value": "SNESplitting",},
                        {"label": "Single-Proton Energy Splitting", "value": "SPESplitting",},
                        {"label": "Wigner Energy Coefficient", "value": "WignerEC",},
                        {"label": "Quad Def Beta2", "value": "QDB2t",},
                    ],
                    clearable=False,
                    searchable=False,
                    value=self.quantity,
                    maxHeight=160,
                    optionHeight=80,                                   
                )
            ])
        )

        if self.dimension == '1D':
            print(self.series_n)
            tabs = []
            for i in range(len(self.dataset)):
                tabs.append(dcc.Tab(label=str(i+1), value='tab'+str(i+1), className='custom-tab', selected_className='custom-tab--selected'))
            if len(self.dataset) < 4:
                tabs.append(dcc.Tab(label="+", value='tab0', className='custom-tab', selected_className='custom-tab--selected'))
            output.append(
                dcc.Tabs(id={'type': 'series_tabs','index': 1}, value='tab'+str(self.series_n), parent_className='custom-tabs', className='custom-tabs-container', children=tabs)
            )
        output.append(
            drc.Card(id='series-card', children=[
                self.nucleon_card(self.series_n-1),
                drc.Card(id="dataset-card", children=[
                    drc.NamedDropdown(
                        name="Select Dataset",
                        id={'type': 'dropdown-dataset','index': self.series_n},
                        options=[
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
                        ],
                        clearable=False,
                        searchable=False,
                        value=self.dataset[self.series_n-1],
                    )
                ])
            ])
        )

        if self.dimension == 'landscape':
            output.append(
                drc.Card(
                    id="colorbar-card",
                    children=[
                        drc.NamedDropdown(
                            name="Colorbar Style",
                            id={'type': 'dropdown-colorbar','index': 1},
                            options=[
                                {"label": "Linear", "value": "linear"},
                                {"label": "Equalized", "value": "equal"},
                                {"label": "Monochrome", "value": "monochrome"},
                            ],
                            clearable=False,
                            searchable=False,
                            value="linear",
                        )
                    ]
                )
            )
        # elif self.dimension == '1D':
        #     output.append(
        #         drc.Card(id="series-card", children=[
        #             html.Button('+', id={'type': 'series-button','index': 1}, value=None, className='series-button')
        #         ])
        #     )

        output.append(
            drc.Card(id="delete-card", children=[
                html.Button('Delete Plot', id={'type': 'delete-button','index': 1}, value=None, className='delete-button')
            ])
        )

        return output
        # drc.Card(
        #     id="Wigner-card",
        #     children=[
        #         drc.NamedDropdown(
        #             name="Wigner Adjustment",
        #             id="radio-wigner",
        #             options=[
        #                 {"label": "None", "value": 0},
        #                 {"label": "Wigner (1)", "value": 1},
        #                 {"label": "Wigner (2)", "value": 2},
        #                 #{"label": "Wigner Coefficient", "value": 3},
        #             ],
        #             clearable=False,
        #             searchable=False,
        #             value=0,
        #         ),
        #     ]
        # ),


