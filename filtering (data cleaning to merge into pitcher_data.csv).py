import pandas as pd
import os
'''
NOTE: This file deals with the 67 csv files we imported from Baseball Savant 
(https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024%7C&hfSit=&player_type=pitcher&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&hfTeam=NYY%7C&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=is%5C.%5C.remove%5C.%5C.bunts%7C&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&chk_stats_bip=on&chk_team=on#results), 
for the sake of conciseness we have not included it in our submission as we cleaned it into 
pitcher_data.csv, which is all that is needed to run our interactive dashboard.
The 67 csv files we imported come from the 67 pitchers who threw a pitch in the 
2024 season for the Yankees or Red Sox.
'''

def update_strikeout_event(row):
    '''
    For the events column, this function takes it and the descriptions column and creates a
    distinction between strikeouts swinging and strikeouts looking
    '''
    if isinstance(row["description"], str):  # Ensure description is a string
        if row["events"] in ["strikeout", "strikeout_double_play"]:
            if "called_strike" in row["description"]:
                return row["events"].replace("strikeout", "strikeout_looking")
            elif "swinging_strike" in row["description"] or "foul_tip" in row["description"]:
                return row["events"].replace("strikeout", "strikeout_swinging")
    return row["events"]




def update_field_out_event(row):
    '''
        For the events column, this function takes it and the bb_type column and creates a
        distinction between the different types of standard outs, fly out, ground out, line out,
        and popout.
        '''
    if row["events"] == "field_out" and isinstance(row["bb_type"], str):  # Ensure bb_type is a valid string
        if row["bb_type"] == "fly_ball":
            return "fly_out"
        elif row["bb_type"] == "ground_ball":
            return "ground_out"
        elif row["bb_type"] == "line_drive":
            return "line_out"
        elif row["bb_type"] == "popup":
            return "pop_out"
    return row["events"]  # Keep other events unchanged




def main():

# Loading the Data

    # Get the list of all CSV files in the current directory

    subfolder = "All of the csv files (merged into pitcher_data.csv)"
    csv_files = [os.path.join(subfolder, file) for file in os.listdir(subfolder) if file.endswith(".csv")]


    # Define the columns to keep
    columns_to_keep = [
        "player_name", "events", "description", "stand", "p_throws", "balls", "strikes",
        "bb_type", "inning", "outs_when_up", "hit_distance_sc", "launch_speed",
        "effective_speed", "release_spin_rate", "fielder_2", "pitch_name", "bat_win_exp"
    ]

    # Load and filter each CSV into a DataFrame
    dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file, usecols=columns_to_keep)
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {file}: {e}")

    # Check if all DataFrames were loaded successfully
    print(f"Successfully loaded {len(dfs)} DataFrames out of {len(csv_files)} CSV files.")

    # Attempt to combine them after filtering
    try:
        combined_df = pd.concat(dfs, ignore_index=True)
        print("Successfully combined all filtered DataFrames!")
        print(combined_df.head())  # Display first few rows
        # Display total number of rows in the combined DataFrame
        print(f"Total number of rows in the combined DataFrame: {len(combined_df)}")

    except Exception as e:
        print(f"Error combining DataFrames: {e}")

# Filtering the Data

    # Remove rows where "events" column is NaN
    combined_df = combined_df.dropna(subset=["events"])

    # Remove rows where "pitch_name" is NaN
    combined_df = combined_df.dropna(subset=["pitch_name"])

    # Display all unique values in the "pitch_name" column to check that nan is gone
    unique_pitch_types = combined_df["pitch_name"].unique()
    print("Unique pitch types:")
    print(unique_pitch_types)
    print(f"\nTotal unique pitch types: {len(unique_pitch_types)}")


    # Display all unique values in the "events" column to check that nan is gone
    unique_events = combined_df["events"].unique()
    print("Unique values in 'events' column:")
    print(unique_events)
    print(f"Total unique event types: {len(unique_events)}")

    # Display the number of rows after filtering
    print(f"Total number of rows after filtering NaN values from 'events': {len(combined_df)}")

    # Rename columns
    combined_df = combined_df.rename(columns={
        "p_throws": "p_arm",
        "stand": "b_arm",
        "effective_speed": "pitch_speed",
        "release_spin_rate": "spin_rate",
        "bat_win_exp": "win_exp"
    })

    # Fill missing values in hit_distance_sc with 0
    combined_df["hit_distance_sc"] = combined_df["hit_distance_sc"].fillna(0)

    # Invert bat_win_exp values to create win expectancy for the pitcher's team
    combined_df["win_exp"] = 1 - combined_df["win_exp"]

    # Split strikeouts into swingning and looking
    combined_df["events"] = combined_df.apply(update_strikeout_event, axis=1)

    # Split field out into the 4 specified out types
    combined_df["events"] = combined_df.apply(update_field_out_event, axis=1)

    # Display all column names to check if changes applied
    print("Column names in the DataFrame:")
    print(combined_df.columns.tolist())

    # Display all unique values in the "events" column to check if changes applied
    unique_events = combined_df["events"].unique()
    print("\nUnique values in 'events' column:")
    print(unique_events)
    print(f"\nTotal unique event types: {len(unique_events)}")

    # Count occurrences of 'strikeout' in the 'events' column to check if changes applied
    strikeout_count = (combined_df["events"] == "strikeout").sum()
    print(f"Number of rows still classified as 'strikeout': {strikeout_count}")

    # Check if 'field_out' still exists in the dataset
    field_out_count = (combined_df["events"] == "field_out").sum()
    print(f"Number of rows still classified as 'field_out': {field_out_count}")

    # Display updated unique values in the "events" column
    print("\nUpdated unique values in 'events' column:")
    print(combined_df["events"].unique())

    # Display all unique values in the "fielder_2" column to find all mlb ids
    unique_fielders = combined_df["fielder_2"].unique()

    print("Unique values in 'fielder_2' column:")
    print(unique_fielders)
    print(f"\nTotal unique fielder_2 values: {len(unique_fielders)}")

    # Define Red Sox fielder_2 IDs
    red_sox_ids = {643376, 657136, 624512, 623168}

    # Create the 'team' column
    combined_df["team"] = combined_df["fielder_2"].apply(lambda x: "Red Sox" if x in red_sox_ids else "Yankees")

    # Display the first few rows to confirm
    print(combined_df[["fielder_2", "team"]].head())

    # Display the count of each team
    print("\nTeam distribution:")
    print(combined_df["team"].value_counts())

    # Drop the fielder_2 column
    combined_df = combined_df.drop(columns=["fielder_2"])

    # Save the DataFrame to a CSV file
    combined_df.to_csv("pitcher_data.csv", index=False)

    print("File saved as pitcher_data.csv")


if __name__ == "__main__":
    main()
