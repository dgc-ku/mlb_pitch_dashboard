import pandas as pd
import sankey as sk

class MLBAPI:
    def load_mlb(self, filename):
        '''Loads the mlb dataset'''
        self.mlb = pd.read_csv(filename) # our dataframe (database) - STATE VARIABLE

    def get_teams(self):
        '''Gets the distinct teams from the filename'''
        if hasattr(self, 'mlb'):
            return list(set(self.mlb.team))

    def get_all_outcomes(self):
        hit_type = ['single', 'double', 'triple', 'home_run']
        on_base = ['walk', 'hit_by_pitch']
        misc = ['truncated_pa', 'catcher_interf', 'sac_fly', 'field_error']

        outcomes = []
        # Loop through each value in the 'events' column and classify it
        for play in self.mlb['events']:
            if play in hit_type:
                outcomes.append('hit')
            elif play in on_base:
                outcomes.append('on base')
            elif play in misc:
                outcomes.append('misc')
            else:
                outcomes.append('out')

        # Add the outcomes list as a new 'outcome' column in the DataFrame
        self.mlb['outcome'] = outcomes

    def get_distinct_outcomes(self):
        if hasattr(self, 'mlb'):
            return list(set(self.mlb.outcome))

    def get_pitchtypes(self):
        '''Gets all the possible pitch types in the dataset'''
        if hasattr(self, 'mlb'):
            return list(set(self.mlb.pitch_name))

    def extract_local_network(self, result, pitch_type, p_hand,
                              b_hand, team_names, speeds):
        '''Extracts the network of the above parameters and returns the
        updated version of the dataframe'''


        mlb_data = self.mlb

    # outcome

        mlb_data = mlb_data[mlb_data.outcome == result]

    # pitch type
        mlb_data = mlb_data[mlb_data['pitch_name'] == pitch_type]

    # Pitcher Handedness
        mlb_data = mlb_data[mlb_data.p_arm == p_hand]

    # Batter Handedness
        mlb_data = mlb_data[mlb_data.b_arm == b_hand]

    # Team Name
        mlb_data = mlb_data[mlb_data.team == team_names]

    # Checking for range in speed
        lower_bound = float(speeds[0])
        upper_bound = float(speeds[1])

        boundaries = ((mlb_data['pitch_speed'] >= lower_bound) &
                      (mlb_data['pitch_speed'] <= upper_bound))

        mlb_data = mlb_data[boundaries]

        local = (mlb_data.groupby(['player_name', 'outcome', 'pitch_name',
                                    'p_arm', 'b_arm', 'team', 'pitch_speed',
                                    'events']).
                 size().reset_index(name='occurences'))

        return local
