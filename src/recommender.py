import pandas as pd


def calculate_group_scores(group, interest_columns):
    group_average = group[interest_columns].mean()
    group_disagreement = group[interest_columns].std()
    group_minimum = group[interest_columns].min()

    fair_score = group_average - 0.5 * group_disagreement

    results = pd.DataFrame({
        "average": group_average,
        "disagreement": group_disagreement,
        "minimum": group_minimum,
        "fair_score": fair_score
    })

    return results.sort_values("fair_score", ascending=False)


def check_travel_constraints(travel_times, group):
    travel_check = travel_times.merge(
        group[["user_id", "max_travel_minutes"]],
        on="user_id",
        how="inner"
    )

    travel_check["travel_ok"] = (
        travel_check["travel_minutes"]
        <= travel_check["max_travel_minutes"]
    )

    place_results = (
        travel_check.groupby("place")
        .agg(
            all_within_limit=("travel_ok", "all"),
            members_checked=("user_id", "nunique")
        )
        .reset_index()
    )

    place_results["travel_ok"] = (
        place_results["all_within_limit"]
        & (place_results["members_checked"] == len(group))
    )

    return place_results[["place", "travel_ok"]]


def rank_places(places, group, scores, travel_times):
    results = places.copy()

    # 1. Calculate interest scores
    results["interest_score"] = results["category"].map(
        scores["fair_score"]
    )

    # 2. Check budget
    group_budget = group["budget"].min()

    results["within_budget"] = (
        results["price"] <= group_budget
    )

    # 3. Check travel constraints
    travel_results = check_travel_constraints(
        travel_times, group
    )

    results = results.drop(
        columns=["travel_ok", "place"],
        errors="ignore"
    )

    results = results.merge(
        travel_results,
        left_on="name",
        right_on="place",
        how="left"
    )

    results["travel_ok"] = results["travel_ok"].fillna(False)

    # 4. Calculate average travel time
    group_travel = travel_times[
        travel_times["user_id"].isin(group["user_id"])
    ]

    avg_travel = (
        group_travel.groupby("place")["travel_minutes"]
        .mean()
        .rename("avg_travel_time")
    )

    results["avg_travel_time"] = results["name"].map(
        avg_travel
    )

    # 5. Calculate travel convenience score
    avg_limit = group["max_travel_minutes"].mean()

    results["travel_score"] = (
        5 * (1 - results["avg_travel_time"] / avg_limit)
    ).clip(lower=0, upper=5)

    # 6. Calculate final recommendation score
    results["place_score"] = (
        0.6 * results["interest_score"]
        + 0.2 * results["rating"]
        + 0.2 * results["travel_score"]
    )

    # 7. Filter and rank
    eligible = results[
        results["within_budget"]
        & results["travel_ok"]
    ].copy()

    return eligible.sort_values(
        "place_score", ascending=False
    )