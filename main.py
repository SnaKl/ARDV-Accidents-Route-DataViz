# disable pylint :
# line too long : C0301
# Too many return statements R0911
# Too many branches : R0912
# Too many arguments : R0913
# Too many local variables : R0914
# Too many statements : R0915
# pylint: disable=C0301, R0911, R0912, R0913, R0914, R0915
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


# mulit drop down choice
multi_option_dict = {"Color": ["Department", "Commune"], "Point": 0}

app = dash.Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])
app.layout = html.Div(
    [
        html.H1("Data visualisation accident de la route", style={"textAlign": "center"}),
        dcc.Graph(id="histo_main_graph"),
        html.Div(
            [
                # dropdown choix des valeurs
                html.Div(
                    [
                        html.Label(
                            "Valeurs à observer", htmlFor="histo_values_param_dropdown", style={"fontWeight": "bold"}
                        ),
                        dcc.Dropdown(
                            id="histo_values_param_dropdown",
                            options=[
                                {"label": label[0], "value": label[1]}
                                for label in process_module.observable_values_labels.items()
                            ],
                            value="jour",
                            style={"width": 250, "textAlign": "left"},
                        ),
                    ],
                    style={"textAlign": "center"},
                ),
                # dropdown choix comparaison
                html.Div(
                    [
                        html.Label("Comparateur", htmlFor="histo_color_param_dropdown", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="histo_color_param_dropdown",
                            options=[
                                {"label": "None", "value": ""},
                                {"label": "Sexe", "value": "sexe"},
                                {"label": "Gravité de blessure", "value": "grav"},
                            ],
                            value="",
                            style={"width": 250, "textAlign": "left"},
                        ),
                    ],
                    style={"display": "block", "marginLeft": 10, "textAlign": "center"},
                ),
                # radio button paramètre d'affichage
                html.Div(
                    [
                        html.Label(
                            "Paramètre d'affichage",
                            htmlFor="histo_histnorm_param_radio_btn",
                            style={"fontWeight": "bold"},
                        ),
                        dcc.RadioItems(
                            id="histo_histnorm_param_radio_btn",
                            options=[
                                {"label": "Nombre", "value": ""},
                                {"label": "Probalité", "value": "probability"},
                                {"label": "Pourcentage", "value": "percent"},
                            ],
                            value="percent",
                            style={"textAlign": "left", "margin": "auto"},
                        ),
                    ],
                    style={"display": "flex", "flexDirection": "column", "marginLeft": 10, "textAlign": "center"},
                ),
                # radio button paramètre d'affiche multiple
                html.Div(
                    [
                        html.Label(
                            "Paramètre comparateur",
                            htmlFor="histo_barmode_param_radio_btn",
                            style={"fontWeight": "bold"},
                        ),
                        dcc.RadioItems(
                            id="histo_barmode_param_radio_btn",
                            options=[
                                {"label": "Stack", "value": "stack"},
                                {"label": "Group", "value": "group"},
                                {"label": "Overlay", "value": "overlay"},
                            ],
                            value="stack",
                            style={"textAlign": "left", "margin": "auto"},
                        ),
                    ],
                    style={"display": "flex", "flexDirection": "column", "marginLeft": 10, "textAlign": "center"},
                ),
            ],
            style={"display": "flex", "justifyContent": "center"},
        ),
        html.H1("Carte des accidents", style={"textAlign": "center", "marginTop": 80}),
        html.Div(
            [
                html.Label("Filtres carte", style={"marginRight": 5}),
                # dropdown choix d'affichage global map
                dcc.Dropdown(
                    id="multi_visual_choice",
                    # options=[{"label": name, "value": name} for name in multi_option_dict.keys()],
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
                        html.Label("Choix à opérer", htmlFor="wtddown", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="wtddown",
                            options=[{"label": "Zoom", "value": "Zoom"}, {"label": "Focus", "value": "Focus"}],
                            style={"width": 250, "textAlign": "left", "marginLeft": 2},
                            multi=True,
                        ),
                    ],
                    style={"textAlign": "center"},
                ),
                html.Button("Go", id="WTDrequest", n_clicks=0, style={"marginLeft": 6, "marginTop": 24}),
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
    ],
    style={"width": "90%", "margin": "auto"},
)

# permet de changer l'histogramme à l'uppuie des radio button
@app.callback(
    Output("histo_main_graph", "figure"),
    [
        Input("histo_values_param_dropdown", "value"),
        Input("histo_color_param_dropdown", "value"),
        Input("histo_histnorm_param_radio_btn", "value"),
        Input("histo_barmode_param_radio_btn", "value"),
    ],
)
def update_histo_main_figure(values_param, color_param, histnorm_param, barmode_param):
    if not values_param:
        raise PreventUpdate

    bargap_param = 0
    # si valeurs et comparaison sont pareil
    if values_param == color_param:
        # empèche la mise a jour
        raise PreventUpdate

    # si pas de choix (none)
    if not histnorm_param:
        histnorm_param = ""

    # valeurs choisie par l'utilisateur
    loc = [values_param]
    if color_param:
        loc += [color_param]

    # récupère que les valeurs choisie dans all_merged
    dataframe = class_map.all_merged.loc[:, loc]
    # si pas de colorParem
    if not color_param:
        fig = px.histogram(dataframe, x=values_param, histnorm=histnorm_param)
    else:
        fig = px.histogram(dataframe, x=values_param, color=color_param, histnorm=histnorm_param, barmode=barmode_param)

    # affichage des pourcentage
    if histnorm_param == "percent":
        fig.update_yaxes(ticksuffix="%")

    # si groupe espace les valeurs
    if barmode_param == "group" and color_param:
        bargap_param = 0.2

    fig.update_layout(
        title_text="Histogramme des accidents de France",
        xaxis_title=values_param,
        yaxis_title="Pourcentage d'accident",
        legend_title=color_param,
        bargap=bargap_param,
    )

    return fig


############################## multi dropdown #################################
# s'occupe de généré les options en fonctions des options déja séléctionné
@app.callback(
    Output("multi_visual_choice", "options"),
    Input("multi_visual_choice", "value"),
    # empeche l'appele au chargement de la map
    prevent_initial_call=True,
)
def update_multi_options(values):
    # si aucune valuer ne fait rien
    if not values:
        return [{"label": name, "value": name} for name in multi_option_dict]
    # si permière valeur ne correspond pas à Color ou point efface les choix
    # et retourne les choix classique
    if values[0] not in ["Color", "Point"]:
        return [{"label": name, "value": name} for name in multi_option_dict]
    # si valeurs choisie point ou 2 change les options pour seulement elles même
    if len(values) >= 2 or values[0] == "Point":
        return [{"label": value, "value": value} for value in values]
    # crée les otpions liés au premier choix
    opts = multi_option_dict[values[0]]
    options = [{"label": value, "value": value} for value in opts]
    options.append({"label": values[0], "value": values[0]})
    return options


############################# click on multi dropdown submit and map #################################
# quand clique sur visual_button prend en compte les valeurs choisie dans
# multi_visual_choice display la map en fonction change aussi les options de
# info_dropdown et wtddown pour adapter à la nouvelle map. info_dropdown
# correspond à tous les item possible (derpatement/commune: numéro nom)
# wtddown correspond au différentes options possible comme point (montre
# tous les coordonnées des accident dans la zone séléctionné),
# color (montre le nombre d'accident par zone departements->communes)

# implémentation futur:
# - au clique sur un objet de la map (département/communes/point) change
# les diagramme graphique s'adpterons pour afficher les informations
# correspondant à l'élement cliqué.
# - crée une sorte d'historique pour revenir à la vision précedante sur la map
@app.callback(
    Output("accident_map", "figure"),
    Output("map_focus_pie", "figure"),
    Output("map_focus_line", "figure"),
    Output("map_focus_pie_choc", "figure"),
    Output("info_dropdown", "value"),
    Output("info_dropdown", "options"),
    Output("wtddown", "options"),
    Input("visual_button", "n_clicks"),
    Input("multi_visual_choice", "value"),
    Input("accident_map", "clickData"),
    Input("wtddown", "value"),
    Input("WTDrequest", "n_clicks"),
    State("info_dropdown", "value"),
    prevent_initial_call=True,
)
def visual_multi_function(
    visual_button,
    multi_visual_choice,
    accident_map,
    wtd_down_value,
    wtd_button,
    info_dropdown_value,
):
    # récupère le context
    ctx = dash.callback_context
    # si aucun context ne fait rien
    if not ctx.triggered:
        raise PreventUpdate
    # récupère l'id de l'élement cliqué
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # si clique sur wtddown dropdown
    if button_id == "wtddown":
        # si aucune valeurs renvoie les valeurs par defaut
        if not wtd_down_value:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                [{"label": "Zoom", "value": "Zoom"}, {"label": "Focus", "value": "Focus"}],
            )
        # si la première valuer n'est pas zoom ou focus, return valeurs par défault
        if wtd_down_value[0] not in ["Zoom", "Focus"]:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                [{"label": "Zoom", "value": "Zoom"}, {"label": "Focus", "value": "Focus"}],
            )
        # si premiere valeurs focus supprime les autre options
        if wtd_down_value[0] == "Focus":
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                [{"label": "Focus", "value": "Focus"}],
            )
        # si 2 valeurs ne peut plus en choisir d'autre
        if len(wtd_down_value) >= 2:
            return (
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                [{"label": value, "value": value} for value in wtd_down_value],
            )
        # return zoom et autre possibilité
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
        )

    # si l'evenèment correspond au click sur le visual_button
    if button_id == "visual_button":
        # si il n'y a pas de value ne fait rien
        if not multi_visual_choice:
            raise PreventUpdate
        # si choix point retourne map point
        if multi_visual_choice[0] == "Point":
            caracteristics = class_map.csv["characteristics"]
            caracteristics["type"] = ["commune_point" for string in range(len(caracteristics.index))]
            miny = min(caracteristics.lat)
            minx = min(caracteristics.long)
            maxy = max(caracteristics.lat)
            maxx = max(caracteristics.long)
            zoom = -math.sqrt((maxx - minx) * (maxy - miny)) * 2 + 11
            return process_module.make_plot_map(caracteristics, zoom), no_update, no_update, no_update, [], [], []
        # si color est multi_visual_choice inférieur à 2 ne fait rien
        if len(multi_visual_choice) < 2:
            raise PreventUpdate
        # si choix Department affiche color department
        if multi_visual_choice[1] == "Department":
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
            )
        # si choix Commune affiche color commune
        if multi_visual_choice[1] == "Commune":
            options_info_dropdown = [
                {
                    "label": class_map.communes_map_info["mergeText"][i],
                    "value": class_map.communes_map_info["mergeText"][i],
                }
                for i in range(class_map.communes_map_info["size"])
            ]
            options_wtd_down = [{"label": "Zoom", "value": "Zoom"}, {"label": "Focus", "value": "Focus"}]
            return class_map.communes_map, no_update, no_update, no_update, [], options_info_dropdown, options_wtd_down

        raise PreventUpdate

    # si clique sur accident_map
    if button_id == "accident_map":
        # récupère type de n'éléement cliqué
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
            )
        # séléctionne automatiquement l'élement cliquer
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            "{} {}".format(accident_map["points"][0]["location"], accident_map["points"][0]["hovertext"]),
            no_update,
            no_update,
        )

    if button_id == "WTDrequest":
        # si aucune valeur
        if not wtd_down_value or not info_dropdown_value:
            raise PreventUpdate

        # récupère le code INSEE et le nom
        try:
            location, name = info_dropdown_value.split(" ")
        except:
            location = info_dropdown_value
            name = None

        # Si choisie focus adapte les graphiques
        if wtd_down_value[0] == "Focus":
            try:
                querry = info_dropdown_value.split()[0]
                if not querry.endswith("A") and not querry.endswith("B"):
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

            return no_update, map_focus_pie, map_focus_line, map_focus_pie_choc, no_update, no_update, no_update

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
            )

        # sinon color
        else:
            # si len < 4 c'est un departement
            if len(str(location)) < 4:
                accident_com_location = class_map.accident_com.loc[
                    class_map.accident_com.insee_com.astype(str).str.startswith(str(location))
                ]
                communes_location = class_map.geojson["communes"].loc[
                    class_map.geojson["communes"].insee_com.astype(str).str.startswith(str(location))
                ]
                option_values = communes_location.loc[:, ["insee_com", "nom_comm"]]
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

                return make_map, no_update, no_update, no_update, [], options_info_dropdown, no_update
            # c'est une commune
            else:
                caracteristics = class_map.csv["characteristics"]
                caracteristics["type"] = ["commune_point" for string in range(len(caracteristics.index))]
                datas = caracteristics.loc[caracteristics.com.astype(str).str.startswith(str(location))]
                options_info_dropdown = [
                    {"label": datas["Num_Acc"][ind], "value": datas["Num_Acc"][ind]} for ind in datas.index
                ]
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
                )

    raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)  # Turn off reloader if inside Jupyter