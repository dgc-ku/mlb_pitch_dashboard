import panel as pn
from mlbapi import MLBAPI
import sankey as sk

# Loads javascript dependencies and configures Panel (required)
pn.extension()

# Initialize the gad api
api = MLBAPI()
api.load_mlb('pitcher_data.csv')

# WIDGET DECLARATIONS

# Search Widgets
pitches = api.get_pitchtypes()

pitch_type = pn.widgets.Select(name = 'Pitch Type',
                               options = pitches,
                               value = 'Sinker')

outcomes = api.get_all_outcomes()
distinct_outcomes = api.get_distinct_outcomes()

result = pn.widgets.Select(name = 'Pitch Result',
                           options = distinct_outcomes,
                           value = 'hit')

speed_range = pn.widgets.IntRangeSlider(name = 'Pitch Speed',
                                start = 65,
                                end = 105,
                                step = 1,
                                value = (65, 105),
                                bar_color = '#FF474C')

pitcher_hand = pn.widgets.Select(name = 'Pitcher Handedness',
                                 options = ['R', 'L'],
                                value = 'R')
batter_hand = pn.widgets.Select(name = 'Batter Handedness',
                                options = ['R', 'L'],
                                value = 'R')
teams = pn.widgets.Select(name = 'Teams',
                          options = api.get_teams(),
                         value = 'Yankees')


# Plotting widgets
width = pn.widgets.IntSlider(name = 'Width', start = 250, end = 2000, step = 250,
                             value = 1000)
height = pn.widgets.IntSlider(name = 'Height', start = 200, end = 1500, step = 100,
                             value = 800)


# CALLBACK FUNCTIONS
def get_catalog(result, pitch_type, pitcher_hand, batter_hand,
                teams, speed_range):
    global local
    local = api.extract_local_network(result, pitch_type, pitcher_hand,
                                      batter_hand, teams, speed_range)

    table = pn.widgets.Tabulator(local, selectable=False)

    return table

def get_plot(result, pitch_type, pitcher_hand, batter_hand,
             teams, speed_range, width, height):
    return sk.make_sankey(local, 'player_name', 'events', vals = 'occurences',
                         width = width, height = height)



# CALLBACK BINDINGS (Connecting widgets to callback function parameters)
# Changing values of result (outcome), pitch_type, pitcher_hand,
# batter_hand, teams, and speed_range
catalog = pn.bind(get_catalog, result, pitch_type, pitcher_hand,
                  batter_hand, teams, speed_range)
plot = pn.bind(get_plot, result, pitch_type, pitcher_hand, batter_hand,
               teams, speed_range, width, height)

# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 320

search_card = pn.Card(
    pn.Column(
        pitch_type,
        result,
        speed_range,
        pitcher_hand,
        batter_hand,
        teams
    ),
    title="Search", width=card_width, collapsed=False
)


plot_card = pn.Card(
    pn.Column(
        width,
        height
    ),

    title="Plot", width=card_width, collapsed=True
)


# LAYOUT

layout = pn.template.FastListTemplate(
    title="MLB Pitchers Explorer",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("PitchData", catalog),  # second argument is callback binding
            ("PitchView", plot),  # second argument is callback binding
            active=1  # Which tab is active by default?
        )

    ],
    header_background='#1C2841'
).servable()

layout.show()
