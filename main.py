# pylint: disable=C0301, R0911, R0912, R0913, R0914, R0915

# disable pylint :
# line too long : C0301
# Too many return statements R0911
# Too many branches : R0912
# Too many arguments : R0913
# Too many local variables : R0914
# Too many statements : R0915

"""
    Main application pour la datavision des accidents de la route
    de France et DOM
"""
import re
import math
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash.dash import no_update
import plotly.express as px

import process_module

class_map = process_module.ClassMap()


# multi drop down choice
multi_option_dict = {"Color": ["Department", "Commune"], "Point": 0}

app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])
app.layout = html.Div(
    [
        html.H1("Data visualisation accident de la route", style={"textAlign": "center"}),
        process_module.make_adaptatif_histo(
            "histo_main_graph",
            {
                "id": "histo_main_values_param_dropdown",
                "options": [
                    {"label": label[0], "value": label[1]} for label in process_module.observable_values_labels.items()
                ],
                "value": "jour",
            },
            {
                "id": "histo_main_color_param_dropdown",
                "options": [
                    {"label": "None", "value": ""},
                    {"label": "Sexe", "value": "sexe"},
                    {"label": "Gravité de blessure", "value": "grav"},
                ],
                "value": "",
            },
            {
                "id": "histo_main_histnorm_param_radio_btn",
                "options": [
                    {"label": "Nombre", "value": ""},
                    {"label": "Probabilité", "value": "probability"},
                    {"label": "Pourcentage", "value": "percent"},
                ],
                "value": "percent",
            },
            {
                "id": "histo_main_barmode_param_radio_btn",
                "options": [
                    {"label": "Stack", "value": "stack"},
                    {"label": "Group", "value": "group"},
                    {"label": "Overlay", "value": "overlay"},
                ],
                "value": "stack",
            },
        ),
        html.H1("Carte des accidents", style={"textAlign": "center", "marginTop": 80}),
        html.Div(
            [
                html.Label("Filtres carte", style={"marginRight": 5}),
                # dropdown choix d'affichage global map
                dcc.Dropdown(
                    id="multi_filter_choice",
                    options=[{"label": name, "value": name} for name in multi_option_dict],
                    style={"width": 250, "textAlign": "left"},
                    multi=True,
                ),
                # permet de lancer le choix
                html.Button("Visualiser", id="visual_button", n_clicks=0, style={"marginLeft": 5}),
            ],
            style={"display": "flex", "justifyContent": "center", "alignItems": "center"},
        ),
        # map
        dcc.Graph(figure=class_map.default_map, id="accident_map"),
        html.Div(
            [
                # dropdown du focus
                html.Div(
                    [
                        html.Label("Item sélectionné", htmlFor="info_dropdown", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="info_dropdown",
                            options=[
                                {
                                    "label": class_map.departments_map_info["mergeText"][i],
                                    "value": class_map.departments_map_info["mergeText"][i],
                                }
                                for i in range(class_map.departments_map_info["size"])
                            ],
                            style={"width": 250, "textAlign": "left"},
                        ),
                    ],
                    style={"textAlign": "center"},
                ),
                # dropwn choix
                html.Div(
                    [
                        html.Label("Choix à opérer", htmlFor="wtd_down", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="wtd_down",
                            options=[{"label": "Zoom", "value": "Zoom"}, {"label": "Focus", "value": "Focus"}],
                            style={"width": 250, "textAlign": "left", "marginLeft": 2},
                            multi=True,
                        ),
                    ],
                    style={"textAlign": "center"},
                ),
                html.Button("Go", id="go_request", n_clicks=0, style={"marginLeft": 6, "marginTop": 24}),
            ],
            style={"display": "flex", "justifyContent": "center", "alignItems": "center"},
        ),
        html.Div(
            [
                dcc.Graph(
                    id="map_focus_pie",
                    figure=px.pie(
                        values=class_map.all_merged.grav.value_counts().values,
                        names=class_map.all_merged.grav.value_counts().index,
                        title="Gravité des accidents",
                    ),
                    style={"flex": "1 1 0", "width": 0},
                ),
                dcc.Graph(
                    id="map_focus_line",
                    figure=px.line(
                        class_map.all_merged.mois.value_counts().sort_index(),
                        y="mois",
                        title="Nombre d'accident par mois",
                    ),
                    style={"flex": "1 1 0", "width": 0},
                ),
                dcc.Graph(
                    id="map_focus_pie_choc",
                    figure=px.pie(
                        values=class_map.all_merged.choc.value_counts(),
                        names=class_map.all_merged.choc.value_counts().index,
                        title="Endroit du choc",
                    ),
                    style={"flex": "1 1 0", "width": 0},
                ),
            ],
            style={
                "display": "flex",
            },
        ),
        process_module.make_adaptatif_histo(
            "histo_focus_graph",
            {
                "id": "histo_focus_value_param_dropdown",
                "options": [
                    {"label": label[0], "value": label[1]} for label in process_module.observable_values_labels.items()
                ],
                "value": "col",
            },
            {
                "id": "histo_focus_color_param_dropdown",
                "options": [
                    {"label": "None", "value": ""},
                    {"label": "Sexe", "value": "sexe"},
                    {"label": "Gravité de blessure", "value": "grav"},
                ],
                "value": "",
            },
            {
                "id": "histo_focus_histnorm_param_radio_btn",
                "options": [
                    {"label": "Nombre", "value": ""},
                    {"label": "Probabilité", "value": "probability"},
                    {"label": "Pourcentage", "value": "percent"},
                ],
                "value": "percent",
            },
            {
                "id": "histo_focus_barmode_param_radio_btn",
                "options": [
                    {"label": "Stack", "value": "stack"},
                    {"label": "Group", "value": "group"},
                    {"label": "Overlay", "value": "overlay"},
                ],
                "value": "group",
            },
        ),
    ],
    style={"width": "90%", "margin": "auto"},
)


@app.callback(
    Output("histo_main_graph", "figure"),
    [
        Input("histo_main_values_param_dropdown", "value"),
        Input("histo_main_color_param_dropdown", "value"),
        Input("histo_main_histnorm_param_radio_btn", "value"),
        Input("histo_main_barmode_param_radio_btn", "value"),
    ],
)
def update_histo_main_figure(values_param, color_param, histnorm_param, barmode_param):
    """
    Update l'histogramme principal en fonction des changements de valeurs radio button et dropdown

    Parameters:
        values_param : valeurs principales à observer
        color_param : valeurs de comparaison
        histnorm_param : mode d'affichage (nombre/probabilité/pourcentage)
        barmode_param : mode d'affichage comparateur (stack/group/overlay)

    Returns:
        figure histo_main_graph
    """

    fig = process_module.update_histo(values_param, color_param, histnorm_param, barmode_param, class_map.all_merged)
    if not fig:
        raise PreventUpdate

    fig.update_layout(title_text=f"Histogramme des accidents de France")

    return fig


@app.callback(
    Output("multi_filter_choice", "options"),
    Input("multi_filter_choice", "value"),
    prevent_initial_call=True,
)
def update_filter_multi_options(values):
    """
    génère automatiquement les options disponibles du dropdown en fonction de celles déja séléctionnées

    Parameters:
        values : valeurs séléctionnées

    Returns:
        [options disponibles]
    """
    # si aucune valeur ne fait rien
    if not values:
        return [{"label": name, "value": name} for name in multi_option_dict]
    # si première valeur ne correspond pas à Color ou point efface les choix
    # et retourne les choix classiques
    if values[0] not in ["Color", "Point"]:
        return [{"label": name, "value": name} for name in multi_option_dict]
    # si valeurs choisies point ou 2 change les options pour seulement elles-même
    if len(values) >= 2 or values[0] == "Point":
        return [{"label": value, "value": value} for value in values]
    # crée les options liées au premier choix
    opts = multi_option_dict[values[0]]
    options = [{"label": value, "value": value} for value in opts]
    options.append({"label": values[0], "value": values[0]})
    return options


@app.callback(
    Output("accident_map", "figure"),
    Output("map_focus_pie", "figure"),
    Output("map_focus_line", "figure"),
    Output("map_focus_pie_choc", "figure"),
    Output("info_dropdown", "value"),
    Output("info_dropdown", "options"),
    Output("wtd_down", "options"),
    Output("histo_focus_graph", "figure"),
    Input("visual_button", "n_clicks"),
    Input("multi_filter_choice", "value"),
    Input("accident_map", "clickData"),
    Input("wtd_down", "value"),
    Input("go_request", "n_clicks"),
    Input("histo_focus_value_param_dropdown", "value"),
    Input("histo_focus_color_param_dropdown", "value"),
    Input("histo_focus_histnorm_param_radio_btn", "value"),
    Input("histo_focus_barmode_param_radio_btn", "value"),
    State("info_dropdown", "value"),
    prevent_initial_call=True,
)
def visual_multi_function(
    visual_button,
    multi_filter_choice,
    accident_map,
    wtd_down_value,
    go_request,
    histo_focus_value,
    histo_focus_color,
    histo_focus_histnorm_param,
    histo_focus_barmode_param,
    info_dropdown_value,
):
    """
    Update accident_map et figures liées en fonction des valeurs choisies dans wtd_down à l'appuie de go_request
    Change automatiquement les options wtd_down en fonction des valeurs sélectionnées
    Change automatiquement la valeur sélectionnée de info_dropdown au click sur la map
    Adapte les options de info_dropdown en fonction des éléments visibles sur la map

    Parameters:
        visual_button : nombre click
        multi_filter_choice : valeurs dropdown
        accident_map : clickData sur la map
        wtd_down_value : valeurs dropdown
        go_request : nombre click
        histo_focus_value : valeurs choisies d'afficher dans l'histogramme
        histo_focus_color : valeurs de comparaison dans l'histogramme
        histo_focus_histnorm_param : paramètre histnorm
        histo_focus_barmode_param : paramètre barmode
        info_dropdown_value : valeur dropdown

    Returns:
        figure accident_map
        figure map_focus_pie
        figure map_focus_line
        figure map_focus_pie_choc
        valeurs info_dropdown
        options info_dropdown : [{"label": label, "value": value},]
        options wtd_down : [{"label": label, "value": value},]
        figure histogramme
    """
    # récupère le contexte
    ctx = dash.callback_context
    # si aucun contexte ne fait rien
    if not ctx.triggered:
        raise PreventUpdate
    # récupère l'id de l'élément cliqué
    item_click_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # si clique sur wtd_down dropdown
    if item_click_id == "wtd_down":
        # si aucune valeur renvoie les valeurs par defaut
        if not wtd_down_value:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                [{"label": "Zoom", "value": "Zoom"}, {"label": "Focus", "value": "Focus"}],
                no_update,
            )
        # si la première valeur n'est pas zoom ou focus, return valeur par défaut
        if wtd_down_value[0] not in ["Zoom", "Focus"]:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                [{"label": "Zoom", "value": "Zoom"}, {"label": "Focus", "value": "Focus"}],
                no_update,
            )
        # si premiere valeur focus supprime les autres options
        if wtd_down_value[0] == "Focus":
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                [{"label": "Focus", "value": "Focus"}],
                no_update,
            )
        # si 2 valeurs, ne peut plus en choisir d'autres
        if len(wtd_down_value) >= 2:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                [{"label": value, "value": value} for value in wtd_down_value],
                no_update,
            )
        # return zoom et autres possibilités
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            [
                {"label": "Zoom", "value": "Zoom"},
                {"label": "Color", "value": "Color"},
                {"label": "Point", "value": "Point"},
            ],
            no_update,
        )

    # si l'évènement correspond au click sur le visual_button
    if item_click_id == "visual_button":
        # si il n'y a pas de value, ne fait rien
        if not multi_filter_choice:
            raise PreventUpdate
        # si choix point retourne map point
        if multi_filter_choice[0] == "Point":
            caracteristics = class_map.csv["characteristics"]
            caracteristics["type"] = ["_point" for string in range(len(caracteristics.index))]
            options_info_dropdown = [
                {"label": caracteristics["Num_Acc"][ind], "value": caracteristics["Num_Acc"][ind]}
                for ind in caracteristics.index
            ]

            if caracteristics.empty:
                raise PreventUpdate
            miny = min(caracteristics.lat)
            minx = min(caracteristics.long)
            maxy = max(caracteristics.lat)
            maxx = max(caracteristics.long)
            zoom = -math.sqrt((maxx - minx) * (maxy - miny)) * 2 + 11
            return (
                process_module.make_plot_map(caracteristics, zoom),
                no_update,
                no_update,
                no_update,
                [],
                options_info_dropdown,
                [{"label": "Focus", "value": "Focus"}],
                no_update,
            )
        # si color est multi_filter_choice inférieur à 2 ne fait rien
        if len(multi_filter_choice) < 2:
            raise PreventUpdate
        # si choix Département affiche color department
        if multi_filter_choice[1] == "Department":
            options_info_dropdown = [
                {
                    "label": class_map.departments_map_info["mergeText"][i],
                    "value": class_map.departments_map_info["mergeText"][i],
                }
                for i in range(class_map.departments_map_info["size"])
            ]
            options_wtd_down = [{"label": "Zoom", "value": "Zoom"}, {"label": "Focus", "value": "Focus"}]
            return (
                class_map.departments_map,
                no_update,
                no_update,
                no_update,
                [],
                options_info_dropdown,
                options_wtd_down,
                no_update,
            )
        # si choix Commune affiche color commune
        if multi_filter_choice[1] == "Commune":
            options_info_dropdown = [
                {
                    "label": class_map.communes_map_info["mergeText"][i],
                    "value": class_map.communes_map_info["mergeText"][i],
                }
                for i in range(class_map.communes_map_info["size"])
            ]
            options_wtd_down = [{"label": "Zoom", "value": "Zoom"}, {"label": "Focus", "value": "Focus"}]
            return (
                class_map.communes_map,
                no_update,
                no_update,
                no_update,
                [],
                options_info_dropdown,
                options_wtd_down,
                no_update,
            )

        raise PreventUpdate

    # si clique sur accident_map
    if item_click_id == "accident_map":
        # récupère type de l'élément cliqué
        click_type = accident_map["points"][0]["customdata"][0]
        # si clique sur un point ne fait rien
        if click_type.endswith("_point"):
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                accident_map["points"][0]["hovertext"],
                no_update,
                no_update,
                no_update,
            )
        # sélectionne automatiquement l'élément cliqué
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            "{} {}".format(accident_map["points"][0]["location"], accident_map["points"][0]["hovertext"]),
            no_update,
            no_update,
            no_update,
        )

    if item_click_id == "go_request":
        # si aucune valeur
        if not wtd_down_value or not info_dropdown_value:
            raise PreventUpdate

        # récupère le code INSEE et le nom
        try:
            location, name = info_dropdown_value.split(" ")
        except:
            location = info_dropdown_value
            name = ""

        # Si choisi focus adapte les graphiques
        if wtd_down_value[0] == "Focus":
            try:
                querry = info_dropdown_value.split()[0]
                if not re.search("[a-zA-Z]", querry):
                    querry = str(int(querry))

                if len(querry) < 4:
                    data_query = class_map.all_merged[class_map.all_merged.dep == querry]
                else:
                    data_query = class_map.all_merged[class_map.all_merged.com == querry]
            except:
                data_query = class_map.all_merged[class_map.all_merged.Num_Acc == info_dropdown_value]

            map_focus_pie = px.pie(
                values=data_query.grav.value_counts().values,
                names=data_query.grav.value_counts().index,
                title="Gravité des accidents",
            )
            map_focus_line = px.line(
                data_query.mois.value_counts().sort_index(), y="mois", title="Nombre d'accident par mois"
            )
            map_focus_line.update_layout(xaxis_title="Month", yaxis_title="Nombre d'accident")
            map_focus_pie_choc = px.pie(
                values=data_query.choc.value_counts(),
                names=data_query.choc.value_counts().index,
                title="Endroit du choc",
            )

            if not histo_focus_value:
                return (
                    no_update,
                    map_focus_pie,
                    map_focus_line,
                    map_focus_pie_choc,
                    no_update,
                    no_update,
                    no_update,
                    no_update,
                )

            fig = process_module.update_histo(
                histo_focus_value, histo_focus_color, histo_focus_histnorm_param, histo_focus_barmode_param, data_query
            )
            if not fig:
                raise PreventUpdate

            fig.update_layout(title_text=f"Histogramme du {location} {name}")

            return (
                no_update,
                map_focus_pie,
                map_focus_line,
                map_focus_pie_choc,
                no_update,
                no_update,
                no_update,
                fig,
            )

        elif len(wtd_down_value) < 2:
            raise PreventUpdate
        # Si Zoom point affiche la map point
        elif wtd_down_value[1] == "Point":
            caracteristics = class_map.csv["characteristics"]
            if len(str(location)) < 4:
                caracteristics["type"] = ["department_point" for string in range(len(caracteristics.index))]
            else:
                caracteristics["type"] = ["commune_point" for string in range(len(caracteristics.index))]
            datas = caracteristics.loc[caracteristics.com.astype(str).str.startswith(str(location))]
            options_info_dropdown = [
                {"label": datas["Num_Acc"][ind], "value": datas["Num_Acc"][ind]} for ind in datas.index
            ]
            if datas.empty:
                raise PreventUpdate
            miny = min(datas.lat)
            minx = min(datas.long)
            maxy = max(datas.lat)
            maxx = max(datas.long)
            zoom = -math.sqrt((maxx - minx) * (maxy - miny)) * 2 + 11
            return (
                process_module.make_plot_map(datas, zoom),
                no_update,
                no_update,
                no_update,
                [],
                options_info_dropdown,
                [{"label": "Focus", "value": "Focus"}],
                no_update,
            )

        # sinon color
        else:
            # si len < 4 : c'est un département donc zoom sur commune
            if len(str(location)) < 4:
                accident_com_location = class_map.accident_com.loc[
                    class_map.accident_com.insee_com.astype(str).str.startswith(str(location))
                ]
                communes_location = class_map.geojson["communes"].loc[
                    class_map.geojson["communes"].insee_com.astype(str).str.startswith(str(location))
                ]
                option_values = (
                    communes_location.loc[:, ["insee_com", "nom_comm"]]
                    .merge(accident_com_location["insee_com"], on="insee_com", how="inner")
                    .loc[:, ["insee_com", "nom_comm"]]
                )
                options_info_dropdown = [
                    {
                        "label": f"{option_values['insee_com'][ind]} {option_values['nom_comm'][ind]}",
                        "value": f"{option_values['insee_com'][ind]} {option_values['nom_comm'][ind]}",
                    }
                    for ind in option_values.index
                ]
                make_map = process_module.make_map(
                    accident_com_location,
                    communes_location,
                    "properties.insee_com",
                    "insee_com",
                    "nom_comm",
                    ["postal_code", "nb_accident"],
                    "nb_accident",
                    process_module.get_zoom(communes_location),
                    process_module.get_center_coords(process_module.get_antipodes(communes_location)),
                    1,
                    {"insee_com": "Code INSEE", "postal_code": "Code postal", "nb_accident": "Nombre d'accidents"},
                )

                return make_map, no_update, no_update, no_update, [], options_info_dropdown, no_update, no_update
            # c'est une commune zoom sur point
            else:
                caracteristics = class_map.csv["characteristics"]
                caracteristics["type"] = ["commune_point" for string in range(len(caracteristics.index))]
                datas = caracteristics.loc[caracteristics.com.astype(str).str.startswith(str(location))]
                options_info_dropdown = [
                    {"label": datas["Num_Acc"][ind], "value": datas["Num_Acc"][ind]} for ind in datas.index
                ]
                if datas.empty:
                    raise PreventUpdate
                miny = min(datas.lat)
                minx = min(datas.long)
                maxy = max(datas.lat)
                maxx = max(datas.long)
                zoom = -math.sqrt((maxx - minx) * (maxy - miny)) * 2 + 11
                return (
                    process_module.make_plot_map(datas, zoom),
                    no_update,
                    no_update,
                    no_update,
                    [],
                    options_info_dropdown,
                    [{"label": "Focus", "value": "Focus"}],
                    no_update,
                )
    if item_click_id in [
        "histo_focus_value_param_dropdown",
        "histo_focus_color_param_dropdown",
        "histo_focus_histnorm_param_radio_btn",
        "histo_focus_barmode_param_radio_btn",
    ]:
        # si aucune valeur
        if not wtd_down_value or not info_dropdown_value or not histo_focus_value:
            raise PreventUpdate

        try:
            querry = info_dropdown_value.split()[0]
            if not re.search("[a-zA-Z]", querry):
                querry = str(int(querry))

            if len(querry) < 4:
                data_query = class_map.all_merged[class_map.all_merged.dep == querry]
            else:
                data_query = class_map.all_merged[class_map.all_merged.com == querry]
        except:
            data_query = class_map.all_merged[class_map.all_merged.Num_Acc == info_dropdown_value]

        fig = process_module.update_histo(
            histo_focus_value, histo_focus_color, histo_focus_histnorm_param, histo_focus_barmode_param, data_query
        )
        if not fig:
            raise PreventUpdate

        # récupère le code INSEE et le nom
        try:
            location, name = info_dropdown_value.split(" ")
        except:
            location = info_dropdown_value
            name = ""
        fig.update_layout(title_text=f"Histogramme de {location} {name}")
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            fig,
        )
    raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
