# Pitch Outcome Dashboard


## Introduction
This project aims to glean insights on the individual pitching performances of the New York Yankees and Boston Red Sox during the 2024 regular season. At a high level, both teams went in opposite directions overall, with the Yankees winning the American League (AL) East, their third in the past five seasons, and the Red Sox finishing at 81-81 and not making the playoffs. This project breaks down each pitcher that has pitched for each team with filters that allow users to analyze pitch outcomes by pitch type, pitch speed, and batter-pitcher handedness matchups.

## Video Walkthrough
The following link demonstrates the dashboard in action, as posted on my Instagram account dedicated for scorecards: https://www.youtube.com/watch?v=3wbxCXq_i8I

A poster slide summarizing data wrangling and findings can also be found below:
<img src="Liam Miller and Daniel Ku - Poster Slide.png" alt='image' width='500' height='350'>


## Features
- Interactive filters for pitch type, pitch velocity, and handedness matchups
- Pitch outcome visualizations, including strikeouts (swinging and looking), walks, types of hits, other types of balls in play
- Player-level breakdowns for every pitcher on the Yankees and Red Sox in 2024
- Comparison of performance trends across situations (pitch types and matchups)

## Data Source
- MLB Statcast data (via Baseball Savant with every pitcher's individual pitch data downloaded as a CSV, attached in this repo)
- 2024 regular season only

## Tools and Libraries for Implementation
- Python (utilized PyCharm IDE for data wrangling and analysis)
- Pandas for data processing
- Plotly Dash for interactive dashboarding

## How to Run
1. Download all py files and csv files
2. Run the mlb_explorer.py file (some file paths may need to be changed for this to work)
3. A window should pop up on your default web browser with the interactive dashboard

## Acknowledgements
Special thanks to Liam Miller for collaborating on this project with me and providing meaningful guidance along the way in part for our class project 
