# Outsy Recommendation Engine

## Overview

"So... where are we going?"

Outsy is a group recommendation system designed to help friends decide where to hang out. Instead of recommending activities for one person, Outsy considers the preferences and constraints of the entire group to find options that work well for everyone.

This repository contains the recommendation and data-analysis component of Outsy.

## Problem

Choosing a group activity can be difficult because each person may have different:

- Interests
- Budgets
- Transportation options
- Travel-time preferences
- Priorities when choosing an activity

A recommendation that is ideal for one person may be inconvenient or uninteresting to another.

Outsy aims to rank activities based on overall group compatibility while preventing one person's preferences from being ignored.

## Current Features

The prototype currently considers:

- Activity interests (1–5 ratings)
- Budget
- Maximum travel time
- Available transportation methods
- Factors users consider important when choosing a group activity

Activity categories currently include:

- Food
- Cafés
- Entertainment
- Arts
- Sports
- Outdoor activities
- Shopping
- Nightlife

## Dataset

Preference data was collected through a Google Forms survey.

The initial prototype dataset contains 15 responses and includes activity preferences, budget, transportation options, travel tolerance, and decision-making priorities.

Raw responses are cleaned and transformed with Python and pandas before being used by the recommendation algorithm.

> Note: Personally identifying information from survey participants is not included in the public dataset.

## Data Processing

The preprocessing pipeline includes:

1. Cleaning inconsistent survey responses
2. Converting budget values into numerical features
3. Converting travel-time ranges into minutes
4. Multi-hot encoding transportation options
5. Multi-hot encoding recommendation priorities
6. Analyzing individual and group activity preferences

## Initial Findings

Preliminary analysis of the first 15 responses found:

- Food had the highest average interest score: **4.60 / 5**
- Cafés followed at approximately **4.47 / 5**
- Outdoor activities and nightlife averaged approximately **4.27 / 5**
- **11 of 15 respondents** selected "Everyone likes it" as one of their three most important factors when choosing a group activity.

These early results support Outsy's focus on group-level rather than purely individual recommendations.

## Recommendation Approach

The recommendation engine is being designed to evaluate candidate activities using factors such as:

- Group interest compatibility
- Budget compatibility
- Travel time
- Transportation accessibility
- Group agreement
- Safety
- Ratings

A key goal is to account for fairness. A destination with a high average score may still be a poor recommendation if one group member strongly dislikes it or faces a significantly longer trip.

## Project Structure

    outsy-recommendation-engine/
    │
    ├── data/
    │   ├── raw/
    │   └── processed/
    │
    ├── notebooks/
    │   └── 01_cleaning.ipynb
    │
    ├── src/
    │   └── recommender.py
    │
    ├── README.md
    ├── requirements.txt
    └── .gitignore

## Tech Stack

- Python
- pandas
- Jupyter
- Google Forms / Google Sheets

Planned integrations:

- Google Places API
- Google Maps Routes API
- Supabase
- Next.js

## Roadmap

- [x] Collect initial user preference data
- [x] Clean and preprocess survey data
- [x] Encode transportation and decision factors
- [x] Analyze overall activity preferences
- [ ] Create group preference profiles
- [ ] Develop group fairness scoring
- [ ] Build candidate-place dataset
- [ ] Implement recommendation scoring
- [ ] Integrate real place data
- [ ] Incorporate travel-time optimization
- [ ] Connect recommendation engine to Outsy web application

## Status

🚧 **In development**

The current version focuses on preference-data processing and development of the group recommendation algorithm.