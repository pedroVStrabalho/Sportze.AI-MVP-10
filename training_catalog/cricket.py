"""
Sportze.AI Cricket Training Catalog

This module codifies Cricket workouts for the Training Generator.
It uses plain Python dictionaries/lists so it can be imported cleanly by
catalog_manager.py or any Sportze.AI training selector.

Structure:
- CRICKET_CATALOG[category][training_mode][session_key]
- training_mode: "alone" or "with_others"
- each session contains: title, sport, category, focus, training_mode, exercises

Helper functions:
- get_cricket_catalog()
- list_cricket_sessions(category=None, training_mode=None)
- get_cricket_session(session_key, category=None, training_mode=None)
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional

SportSession = Dict[str, Any]
SportCatalog = Dict[str, Dict[str, Dict[str, SportSession]]]

SPORT = "Cricket"


def exercise(name: str, prescription: str, notes: str = "") -> Dict[str, str]:
    """Create a normalized exercise object for Sportze.AI catalogs."""
    item = {"name": name, "prescription": prescription}
    if notes:
        item["notes"] = notes
    return item


def session(
    key: str,
    title: str,
    category: str,
    training_mode: str,
    focus: str,
    exercises: List[Dict[str, str]],
) -> SportSession:
    """Create a normalized cricket session."""
    return {
        "key": key,
        "sport": SPORT,
        "title": title,
        "category": category,
        "training_mode": training_mode,
        "focus": focus,
        "exercises": exercises,
    }


CRICKET_CATALOG: SportCatalog = {
    "learn_how_to_play": {
        "alone": {
            "cricket_learn_alone_bat_swing_practice": session(
                "cricket_learn_alone_bat_swing_practice",
                "Bat Swing Practice",
                "learn_how_to_play",
                "alone",
                "basic batting mechanics",
                [exercise("Swing Cricket Bat", "200 reps")],
            ),
            "cricket_learn_alone_hit_ball_against_wall": session(
                "cricket_learn_alone_hit_ball_against_wall",
                "Hit Ball Against Wall",
                "learn_how_to_play",
                "alone",
                "hand-eye coordination and bat contact",
                [exercise("Hit Tennis Ball Against Wall", "200 reps")],
            ),
            "cricket_learn_alone_catch_rebound_ball": session(
                "cricket_learn_alone_catch_rebound_ball",
                "Catch Rebound Ball",
                "learn_how_to_play",
                "alone",
                "catching reactions",
                [exercise("Catch Tennis Ball From Wall", "200 reps")],
            ),
            "cricket_learn_alone_throw_at_target": session(
                "cricket_learn_alone_throw_at_target",
                "Throw At Target",
                "learn_how_to_play",
                "alone",
                "throwing accuracy",
                [exercise("Throw Ball At Bucket/Stump", "100 throws")],
            ),
            "cricket_learn_alone_pick_up_ground_balls": session(
                "cricket_learn_alone_pick_up_ground_balls",
                "Pick Up Ground Balls",
                "learn_how_to_play",
                "alone",
                "ground fielding",
                [exercise("Roll Ball Away And Collect", "100 reps")],
            ),
            "cricket_learn_alone_bowling_motion_practice": session(
                "cricket_learn_alone_bowling_motion_practice",
                "Bowling Motion Practice",
                "learn_how_to_play",
                "alone",
                "bowling action fundamentals",
                [exercise("Perform Bowling Motion", "200 reps")],
            ),
            "cricket_learn_alone_run_between_markers": session(
                "cricket_learn_alone_run_between_markers",
                "Run Between Markers",
                "learn_how_to_play",
                "alone",
                "running between wickets",
                [exercise("20m Sprint", "50 reps")],
            ),
            "cricket_learn_alone_high_ball_catch": session(
                "cricket_learn_alone_high_ball_catch",
                "High Ball Catch",
                "learn_how_to_play",
                "alone",
                "high catching",
                [exercise("Toss Ball Up And Catch", "100 catches")],
            ),
            "cricket_learn_alone_bat_control_drill": session(
                "cricket_learn_alone_bat_control_drill",
                "Bat Control Drill",
                "learn_how_to_play",
                "alone",
                "bat control",
                [exercise("Hold Bat And Change Direction", "100 reps")],
            ),
            "cricket_learn_alone_cricket_basics_circuit": session(
                "cricket_learn_alone_cricket_basics_circuit",
                "Cricket Basics Circuit",
                "learn_how_to_play",
                "alone",
                "basic cricket circuit",
                [
                    exercise("Throws", "50 reps"),
                    exercise("Catches", "50 reps"),
                    exercise("Swings", "50 reps"),
                    exercise("Sprints", "20 reps"),
                ],
            ),
        },
        "with_others": {
            "cricket_learn_group_partner_catch_drill": session(
                "cricket_learn_group_partner_catch_drill",
                "Partner Catch Drill",
                "learn_how_to_play",
                "with_others",
                "basic catching with partner",
                [exercise("Catch Ball", "200 catches")],
            ),
            "cricket_learn_group_partner_throw_drill": session(
                "cricket_learn_group_partner_throw_drill",
                "Partner Throw Drill",
                "learn_how_to_play",
                "with_others",
                "basic throwing with partner",
                [exercise("Throw Ball To Partner", "200 throws")],
            ),
            "cricket_learn_group_underarm_batting_drill": session(
                "cricket_learn_group_underarm_batting_drill",
                "Underarm Batting Drill",
                "learn_how_to_play",
                "with_others",
                "entry-level batting contact",
                [exercise("Hit Slow Thrown Balls", "100 balls")],
            ),
            "cricket_learn_group_bowling_at_stumps_drill": session(
                "cricket_learn_group_bowling_at_stumps_drill",
                "Bowling At Stumps Drill",
                "learn_how_to_play",
                "with_others",
                "bowling accuracy",
                [exercise("Bowl Ball At Target", "100 deliveries")],
            ),
            "cricket_learn_group_running_between_wickets_drill": session(
                "cricket_learn_group_running_between_wickets_drill",
                "Running Between Wickets Drill",
                "learn_how_to_play",
                "with_others",
                "running between wickets",
                [exercise("Sprint Between Two Markers", "50 reps")],
            ),
            "cricket_learn_group_ground_ball_collection_drill": session(
                "cricket_learn_group_ground_ball_collection_drill",
                "Ground Ball Collection Drill",
                "learn_how_to_play",
                "with_others",
                "ground fielding",
                [exercise("Collect Rolling Balls", "100 reps")],
            ),
            "cricket_learn_group_high_catch_drill": session(
                "cricket_learn_group_high_catch_drill",
                "High Catch Drill",
                "learn_how_to_play",
                "with_others",
                "high catching",
                [exercise("Catch High Balls", "100 catches")],
            ),
            "cricket_learn_group_throwing_accuracy_drill": session(
                "cricket_learn_group_throwing_accuracy_drill",
                "Throwing Accuracy Drill",
                "learn_how_to_play",
                "with_others",
                "throwing accuracy",
                [exercise("Hit Stump Target", "100 throws")],
            ),
            "cricket_learn_group_basic_batting_drill": session(
                "cricket_learn_group_basic_batting_drill",
                "Basic Batting Drill",
                "learn_how_to_play",
                "with_others",
                "basic batting against deliveries",
                [exercise("Face Deliveries", "100 balls")],
            ),
            "cricket_learn_group_mini_cricket_game": session(
                "cricket_learn_group_mini_cricket_game",
                "Mini Cricket Game",
                "learn_how_to_play",
                "with_others",
                "small-sided game play",
                [exercise("Mini Cricket Game", "5 overs")],
            ),
        },
    },
    "opening_batter": {
        "alone": {
            "cricket_opening_batter_alone_bat_swing_repetitions": session(
                "cricket_opening_batter_alone_bat_swing_repetitions",
                "Bat Swing Repetitions",
                "opening_batter",
                "alone",
                "batting repetition volume",
                [exercise("Bat Swings", "300 swings")],
            ),
            "cricket_opening_batter_alone_hit_ball_straight": session(
                "cricket_opening_batter_alone_hit_ball_straight",
                "Hit Ball Straight",
                "opening_batter",
                "alone",
                "straight bat contact",
                [exercise("Hit Ball Straight", "200 hits")],
            ),
            "cricket_opening_batter_alone_reaction_ball_drill": session(
                "cricket_opening_batter_alone_reaction_ball_drill",
                "Reaction Ball Drill",
                "opening_batter",
                "alone",
                "reaction catching and hand-eye speed",
                [exercise("Tennis Ball Bounce Catch", "100 catches")],
            ),
            "cricket_opening_batter_alone_foot_movement_drill": session(
                "cricket_opening_batter_alone_foot_movement_drill",
                "Foot Movement Drill",
                "opening_batter",
                "alone",
                "front-foot and back-foot movement",
                [exercise("Forward Step", "100 reps"), exercise("Backward Step", "100 reps")],
            ),
            "cricket_opening_batter_alone_long_concentration_batting": session(
                "cricket_opening_batter_alone_long_concentration_batting",
                "Long Concentration Batting",
                "opening_batter",
                "alone",
                "batting concentration",
                [exercise("Shadow Batting", "15 minutes")],
            ),
            "cricket_opening_batter_alone_sprint_between_wickets": session(
                "cricket_opening_batter_alone_sprint_between_wickets",
                "Sprint Between Wickets",
                "opening_batter",
                "alone",
                "running between wickets",
                [exercise("20m Sprint", "50 reps")],
            ),
        },
        "with_others": {
            "cricket_opening_batter_group_face_fast_deliveries": session(
                "cricket_opening_batter_group_face_fast_deliveries",
                "Face Fast Deliveries",
                "opening_batter",
                "with_others",
                "batting against pace",
                [exercise("Face Fast Deliveries", "100 balls")],
            ),
            "cricket_opening_batter_group_opening_partnership_drill": session(
                "cricket_opening_batter_group_opening_partnership_drill",
                "Opening Partnership Drill",
                "opening_batter",
                "with_others",
                "partnership running and communication",
                [exercise("Run Between Wickets", "50 reps")],
            ),
            "cricket_opening_batter_group_defensive_batting_drill": session(
                "cricket_opening_batter_group_defensive_batting_drill",
                "Defensive Batting Drill",
                "opening_batter",
                "with_others",
                "defensive batting",
                [exercise("Face Deliveries Defensively", "100 deliveries")],
            ),
            "cricket_opening_batter_group_accuracy_batting_drill": session(
                "cricket_opening_batter_group_accuracy_batting_drill",
                "Accuracy Batting Drill",
                "opening_batter",
                "with_others",
                "target-zone batting",
                [exercise("Hit Target Zones", "100 hits")],
            ),
            "cricket_opening_batter_group_long_batting_session": session(
                "cricket_opening_batter_group_long_batting_session",
                "Long Batting Session",
                "opening_batter",
                "with_others",
                "batting endurance",
                [exercise("Face Deliveries", "150 deliveries")],
            ),
            "cricket_opening_batter_group_match_simulation": session(
                "cricket_opening_batter_group_match_simulation",
                "Match Simulation",
                "opening_batter",
                "with_others",
                "opening innings simulation",
                [exercise("Bat In Match Simulation", "10 overs")],
            ),
        },
    },
    "fast_bowler": {
        "alone": {
            "cricket_fast_bowler_alone_bowling_action_drill": session("cricket_fast_bowler_alone_bowling_action_drill", "Bowling Action Drill", "fast_bowler", "alone", "bowling mechanics", [exercise("Bowling Action Repetitions", "200 reps")]),
            "cricket_fast_bowler_alone_run_up_drill": session("cricket_fast_bowler_alone_run_up_drill", "Run-Up Drill", "fast_bowler", "alone", "run-up rhythm", [exercise("Run-Ups", "50 reps")]),
            "cricket_fast_bowler_alone_sprint_session": session("cricket_fast_bowler_alone_sprint_session", "Sprint Session", "fast_bowler", "alone", "speed and conditioning", [exercise("50m Sprint", "20 reps")]),
            "cricket_fast_bowler_alone_medicine_ball_throws": session("cricket_fast_bowler_alone_medicine_ball_throws", "Medicine Ball Throws", "fast_bowler", "alone", "power development", [exercise("Medicine Ball Throws", "5 sets × 15 reps")]),
            "cricket_fast_bowler_alone_target_bowling": session("cricket_fast_bowler_alone_target_bowling", "Target Bowling", "fast_bowler", "alone", "line and length accuracy", [exercise("Bowl At Marker", "150 deliveries")]),
            "cricket_fast_bowler_alone_jump_training": session("cricket_fast_bowler_alone_jump_training", "Jump Training", "fast_bowler", "alone", "lower-body power", [exercise("Jump Squats", "100 reps")]),
        },
        "with_others": {
            "cricket_fast_bowler_group_bowl_at_batter": session("cricket_fast_bowler_group_bowl_at_batter", "Bowl At Batter", "fast_bowler", "with_others", "live bowling", [exercise("Bowl At Batter", "100 deliveries")]),
            "cricket_fast_bowler_group_accuracy_bowling": session("cricket_fast_bowler_group_accuracy_bowling", "Accuracy Bowling", "fast_bowler", "with_others", "stump accuracy", [exercise("Hit Stumps", "100 deliveries")]),
            "cricket_fast_bowler_group_match_bowling": session("cricket_fast_bowler_group_match_bowling", "Match Bowling", "fast_bowler", "with_others", "match bowling load", [exercise("Bowl Match Overs", "10 overs")]),
            "cricket_fast_bowler_group_yorker_practice": session("cricket_fast_bowler_group_yorker_practice", "Yorker Practice", "fast_bowler", "with_others", "yorker execution", [exercise("Yorker Deliveries", "100 deliveries")]),
            "cricket_fast_bowler_group_bowling_under_pressure": session("cricket_fast_bowler_group_bowling_under_pressure", "Bowling Under Pressure", "fast_bowler", "with_others", "pressure execution", [exercise("Pressure Deliveries", "50 deliveries")]),
            "cricket_fast_bowler_group_game_simulation": session("cricket_fast_bowler_group_game_simulation", "Game Simulation", "fast_bowler", "with_others", "full bowling spell", [exercise("Bowl Full Spell", "1 full spell")]),
        },
    },
    "spin_bowler": {
        "alone": {
            "cricket_spin_bowler_alone_spin_release_practice": session("cricket_spin_bowler_alone_spin_release_practice", "Spin Release Practice", "spin_bowler", "alone", "spin release mechanics", [exercise("Spin Release Deliveries", "200 deliveries")]),
            "cricket_spin_bowler_alone_target_bowling": session("cricket_spin_bowler_alone_target_bowling", "Target Bowling", "spin_bowler", "alone", "spin accuracy", [exercise("Target Deliveries", "150 deliveries")]),
            "cricket_spin_bowler_alone_finger_strength_drill": session("cricket_spin_bowler_alone_finger_strength_drill", "Finger Strength Drill", "spin_bowler", "alone", "finger strength", [exercise("Tennis Ball Squeezes", "200 reps")]),
            "cricket_spin_bowler_alone_bowling_accuracy_drill": session("cricket_spin_bowler_alone_bowling_accuracy_drill", "Bowling Accuracy Drill", "spin_bowler", "alone", "line and length accuracy", [exercise("Accuracy Deliveries", "100 deliveries")]),
            "cricket_spin_bowler_alone_shadow_bowling": session("cricket_spin_bowler_alone_shadow_bowling", "Shadow Bowling", "spin_bowler", "alone", "bowling movement pattern", [exercise("Shadow Bowling", "150 reps")]),
            "cricket_spin_bowler_alone_balance_drill": session("cricket_spin_bowler_alone_balance_drill", "Balance Drill", "spin_bowler", "alone", "single-leg control", [exercise("Single-Leg Balance", "10 minutes")]),
        },
        "with_others": {
            "cricket_spin_bowler_group_bowl_to_batter": session("cricket_spin_bowler_group_bowl_to_batter", "Bowl To Batter", "spin_bowler", "with_others", "live spin bowling", [exercise("Bowl To Batter", "100 deliveries")]),
            "cricket_spin_bowler_group_spin_accuracy_drill": session("cricket_spin_bowler_group_spin_accuracy_drill", "Spin Accuracy Drill", "spin_bowler", "with_others", "spin accuracy", [exercise("Spin Accuracy Deliveries", "100 deliveries")]),
            "cricket_spin_bowler_group_match_bowling": session("cricket_spin_bowler_group_match_bowling", "Match Bowling", "spin_bowler", "with_others", "match bowling load", [exercise("Bowl Match Overs", "10 overs")]),
            "cricket_spin_bowler_group_batter_deception_drill": session("cricket_spin_bowler_group_batter_deception_drill", "Batter Deception Drill", "spin_bowler", "with_others", "deception and variation", [exercise("Deception Deliveries", "100 deliveries")]),
            "cricket_spin_bowler_group_flight_control_drill": session("cricket_spin_bowler_group_flight_control_drill", "Flight Control Drill", "spin_bowler", "with_others", "flight control", [exercise("Flight Control Deliveries", "100 deliveries")]),
            "cricket_spin_bowler_group_game_simulation": session("cricket_spin_bowler_group_game_simulation", "Game Simulation", "spin_bowler", "with_others", "full bowling spell", [exercise("Full Bowling Spell", "1 full spell")]),
        },
    },
    "wicketkeeper": {
        "alone": {
            "cricket_wicketkeeper_alone_wall_catch_drill": session("cricket_wicketkeeper_alone_wall_catch_drill", "Wall Catch Drill", "wicketkeeper", "alone", "reaction catching", [exercise("Wall Catches", "300 catches")]),
            "cricket_wicketkeeper_alone_low_catch_drill": session("cricket_wicketkeeper_alone_low_catch_drill", "Low Catch Drill", "wicketkeeper", "alone", "low catching", [exercise("Low Catches", "200 catches")]),
            "cricket_wicketkeeper_alone_side_movement_drill": session("cricket_wicketkeeper_alone_side_movement_drill", "Side Movement Drill", "wicketkeeper", "alone", "lateral movement", [exercise("Side Movement", "100 reps each side")]),
            "cricket_wicketkeeper_alone_squat_hold": session("cricket_wicketkeeper_alone_squat_hold", "Squat Hold", "wicketkeeper", "alone", "keeper stance endurance", [exercise("Squat Hold", "5 sets × 60 seconds")]),
            "cricket_wicketkeeper_alone_reaction_ball_drill": session("cricket_wicketkeeper_alone_reaction_ball_drill", "Reaction Ball Drill", "wicketkeeper", "alone", "reaction speed", [exercise("Reaction Ball Reactions", "200 reactions")]),
            "cricket_wicketkeeper_alone_sprint_collection_drill": session("cricket_wicketkeeper_alone_sprint_collection_drill", "Sprint Collection Drill", "wicketkeeper", "alone", "collection speed", [exercise("Sprint Collection", "50 reps")]),
        },
        "with_others": {
            "cricket_wicketkeeper_group_wicketkeeper_catch_drill": session("cricket_wicketkeeper_group_wicketkeeper_catch_drill", "Wicketkeeper Catch Drill", "wicketkeeper", "with_others", "keeper catching", [exercise("Wicketkeeper Catches", "200 catches")]),
            "cricket_wicketkeeper_group_stumping_drill": session("cricket_wicketkeeper_group_stumping_drill", "Stumping Drill", "wicketkeeper", "with_others", "stumping speed", [exercise("Stumping Repetitions", "100 reps")]),
            "cricket_wicketkeeper_group_fast_bowling_collection": session("cricket_wicketkeeper_group_fast_bowling_collection", "Fast Bowling Collection", "wicketkeeper", "with_others", "pace collection", [exercise("Collect Fast Bowling", "100 balls")]),
            "cricket_wicketkeeper_group_spin_bowling_collection": session("cricket_wicketkeeper_group_spin_bowling_collection", "Spin Bowling Collection", "wicketkeeper", "with_others", "spin collection", [exercise("Collect Spin Bowling", "100 balls")]),
            "cricket_wicketkeeper_group_throw_at_stumps": session("cricket_wicketkeeper_group_throw_at_stumps", "Throw At Stumps", "wicketkeeper", "with_others", "throwing accuracy", [exercise("Throw At Stumps", "100 throws")]),
            "cricket_wicketkeeper_group_match_simulation": session("cricket_wicketkeeper_group_match_simulation", "Match Simulation", "wicketkeeper", "with_others", "keeper match simulation", [exercise("Keep Wicket In Match Simulation", "10 overs")]),
        },
    },
    "slip_fielder": {
        "alone": {
            "cricket_slip_fielder_alone_wall_catch_drill": session("cricket_slip_fielder_alone_wall_catch_drill", "Wall Catch Drill", "slip_fielder", "alone", "slip catching reactions", [exercise("Wall Catches", "200 catches")]),
            "cricket_slip_fielder_alone_reaction_catch_drill": session("cricket_slip_fielder_alone_reaction_catch_drill", "Reaction Catch Drill", "slip_fielder", "alone", "quick reactions", [exercise("Reaction Catches", "150 catches")]),
            "cricket_slip_fielder_alone_low_catch_drill": session("cricket_slip_fielder_alone_low_catch_drill", "Low Catch Drill", "slip_fielder", "alone", "low catching", [exercise("Low Catches", "150 catches")]),
            "cricket_slip_fielder_alone_high_catch_drill": session("cricket_slip_fielder_alone_high_catch_drill", "High Catch Drill", "slip_fielder", "alone", "high catching", [exercise("High Catches", "100 catches")]),
            "cricket_slip_fielder_alone_sprint_catch_drill": session("cricket_slip_fielder_alone_sprint_catch_drill", "Sprint Catch Drill", "slip_fielder", "alone", "movement into catch", [exercise("Sprint And Catch", "75 reps")]),
            "cricket_slip_fielder_alone_one_hand_catch_drill": session("cricket_slip_fielder_alone_one_hand_catch_drill", "One-Hand Catch Drill", "slip_fielder", "alone", "one-hand control", [exercise("One-Hand Catches", "100 catches")]),
        },
        "with_others": {
            "cricket_slip_fielder_group_slip_catch_drill": session("cricket_slip_fielder_group_slip_catch_drill", "Slip Catch Drill", "slip_fielder", "with_others", "slip catching", [exercise("Slip Catches", "150 catches")]),
            "cricket_slip_fielder_group_deflection_catch_drill": session("cricket_slip_fielder_group_deflection_catch_drill", "Deflection Catch Drill", "slip_fielder", "with_others", "deflection reactions", [exercise("Deflection Catches", "100 catches")]),
            "cricket_slip_fielder_group_reaction_catch_drill": session("cricket_slip_fielder_group_reaction_catch_drill", "Reaction Catch Drill", "slip_fielder", "with_others", "reaction catches", [exercise("Reaction Catches", "150 catches")]),
            "cricket_slip_fielder_group_diving_catch_drill": session("cricket_slip_fielder_group_diving_catch_drill", "Diving Catch Drill", "slip_fielder", "with_others", "diving catches", [exercise("Diving Catches", "75 catches")]),
            "cricket_slip_fielder_group_match_catch_simulation": session("cricket_slip_fielder_group_match_catch_simulation", "Match Catch Simulation", "slip_fielder", "with_others", "match catch decisions", [exercise("Match Catch Simulation", "10 overs")]),
            "cricket_slip_fielder_group_pressure_catch_drill": session("cricket_slip_fielder_group_pressure_catch_drill", "Pressure Catch Drill", "slip_fielder", "with_others", "pressure catching", [exercise("Pressure Catches", "100 catches")]),
        },
    },
    "outfielder": {
        "alone": {
            "cricket_outfielder_alone_high_catch_drill": session("cricket_outfielder_alone_high_catch_drill", "High Catch Drill", "outfielder", "alone", "boundary high catching", [exercise("High Catches", "100 catches")]),
            "cricket_outfielder_alone_long_throw_drill": session("cricket_outfielder_alone_long_throw_drill", "Long Throw Drill", "outfielder", "alone", "long-distance throwing", [exercise("Long Throws", "100 throws")]),
            "cricket_outfielder_alone_sprint_collection_drill": session("cricket_outfielder_alone_sprint_collection_drill", "Sprint Collection Drill", "outfielder", "alone", "sprint and collect", [exercise("Sprint Collection", "75 reps")]),
            "cricket_outfielder_alone_ground_ball_pickup_drill": session("cricket_outfielder_alone_ground_ball_pickup_drill", "Ground Ball Pickup Drill", "outfielder", "alone", "ground fielding", [exercise("Ground Ball Pickups", "150 reps")]),
            "cricket_outfielder_alone_throw_at_target_drill": session("cricket_outfielder_alone_throw_at_target_drill", "Throw At Target Drill", "outfielder", "alone", "throwing accuracy", [exercise("Throw At Target", "100 throws")]),
            "cricket_outfielder_alone_endurance_running_drill": session("cricket_outfielder_alone_endurance_running_drill", "Endurance Running Drill", "outfielder", "alone", "fielding endurance", [exercise("Endurance Run", "20 minutes")]),
        },
        "with_others": {
            "cricket_outfielder_group_boundary_catch_drill": session("cricket_outfielder_group_boundary_catch_drill", "Boundary Catch Drill", "outfielder", "with_others", "boundary catching", [exercise("Boundary Catches", "100 catches")]),
            "cricket_outfielder_group_long_throw_accuracy_drill": session("cricket_outfielder_group_long_throw_accuracy_drill", "Long Throw Accuracy Drill", "outfielder", "with_others", "long throw accuracy", [exercise("Long Throw Accuracy", "100 throws")]),
            "cricket_outfielder_group_relay_throw_drill": session("cricket_outfielder_group_relay_throw_drill", "Relay Throw Drill", "outfielder", "with_others", "relay fielding", [exercise("Relay Throws", "75 reps")]),
            "cricket_outfielder_group_ground_fielding_drill": session("cricket_outfielder_group_ground_fielding_drill", "Ground Fielding Drill", "outfielder", "with_others", "ground fielding", [exercise("Ground Fielding Reps", "150 reps")]),
            "cricket_outfielder_group_chase_and_return_drill": session("cricket_outfielder_group_chase_and_return_drill", "Chase And Return Drill", "outfielder", "with_others", "chase, collect, return", [exercise("Chase And Return", "75 reps")]),
            "cricket_outfielder_group_match_simulation": session("cricket_outfielder_group_match_simulation", "Match Simulation", "outfielder", "with_others", "outfield match simulation", [exercise("Outfield Match Simulation", "10 overs")]),
        },
    },
    "batting_all_rounder": {
        "alone": {
            "cricket_batting_all_rounder_alone_balanced_session": session(
                "cricket_batting_all_rounder_alone_balanced_session",
                "Batting All-Rounder Solo Mix",
                "batting_all_rounder",
                "alone",
                "opening batter + fast bowler mix",
                [
                    exercise("Bat Swings", "150 swings"),
                    exercise("Hit Ball Straight", "100 hits"),
                    exercise("Tennis Ball Bounce Catch", "75 catches"),
                    exercise("Bowling Action Repetitions", "100 reps"),
                    exercise("Bowl At Marker", "75 deliveries"),
                    exercise("20m Sprint", "30 reps"),
                ],
            )
        },
        "with_others": {
            "cricket_batting_all_rounder_group_balanced_session": session(
                "cricket_batting_all_rounder_group_balanced_session",
                "Batting All-Rounder Group Mix",
                "batting_all_rounder",
                "with_others",
                "opening batter + fast bowler match mix",
                [
                    exercise("Face Deliveries", "75 balls"),
                    exercise("Hit Target Zones", "50 hits"),
                    exercise("Run Between Wickets", "30 reps"),
                    exercise("Bowl At Batter", "50 deliveries"),
                    exercise("Hit Stumps", "50 deliveries"),
                    exercise("Mini Match Simulation", "5 overs"),
                ],
            )
        },
    },
    "bowling_all_rounder": {
        "alone": {
            "cricket_bowling_all_rounder_alone_balanced_session": session(
                "cricket_bowling_all_rounder_alone_balanced_session",
                "Bowling All-Rounder Solo Mix",
                "bowling_all_rounder",
                "alone",
                "bowler + batting mix",
                [
                    exercise("Bowling Action Repetitions", "150 reps"),
                    exercise("Run-Ups", "30 reps"),
                    exercise("Bowl At Marker", "100 deliveries"),
                    exercise("Bat Swings", "100 swings"),
                    exercise("Shadow Batting", "10 minutes"),
                    exercise("50m Sprint", "10 reps"),
                ],
            )
        },
        "with_others": {
            "cricket_bowling_all_rounder_group_balanced_session": session(
                "cricket_bowling_all_rounder_group_balanced_session",
                "Bowling All-Rounder Group Mix",
                "bowling_all_rounder",
                "with_others",
                "bowler + batting match mix",
                [
                    exercise("Bowl At Batter", "75 deliveries"),
                    exercise("Pressure Deliveries", "30 deliveries"),
                    exercise("Face Deliveries", "50 balls"),
                    exercise("Hit Target Zones", "50 hits"),
                    exercise("Run Between Wickets", "25 reps"),
                    exercise("Mini Match Simulation", "5 overs"),
                ],
            )
        },
    },
}


CRICKET_SESSION_BANK: List[SportSession] = [
    workout
    for category_data in CRICKET_CATALOG.values()
    for mode_data in category_data.values()
    for workout in mode_data.values()
]


CRICKET_CATEGORIES = list(CRICKET_CATALOG.keys())
CRICKET_TRAINING_MODES = ["alone", "with_others"]


# Common aliases for UI/user input normalization.
CRICKET_CATEGORY_ALIASES = {
    "learn": "learn_how_to_play",
    "learn how to play": "learn_how_to_play",
    "beginner": "learn_how_to_play",
    "opening batter": "opening_batter",
    "opener": "opening_batter",
    "batter": "opening_batter",
    "fast bowler": "fast_bowler",
    "pace bowler": "fast_bowler",
    "spin bowler": "spin_bowler",
    "spinner": "spin_bowler",
    "wicketkeeper": "wicketkeeper",
    "wicket keeper": "wicketkeeper",
    "keeper": "wicketkeeper",
    "slip fielder": "slip_fielder",
    "slip": "slip_fielder",
    "outfielder": "outfielder",
    "fielder": "outfielder",
    "batting all-rounder": "batting_all_rounder",
    "batting all rounder": "batting_all_rounder",
    "bowling all-rounder": "bowling_all_rounder",
    "bowling all rounder": "bowling_all_rounder",
}


CRICKET_MODE_ALIASES = {
    "solo": "alone",
    "alone": "alone",
    "individual": "alone",
    "training alone": "alone",
    "group": "with_others",
    "partner": "with_others",
    "with others": "with_others",
    "2+ people": "with_others",
    "two or more": "with_others",
}


def normalize_cricket_category(category: Optional[str]) -> Optional[str]:
    """Normalize a category/role string to a catalog key."""
    if category is None:
        return None
    key = category.strip().lower().replace("_", " ")
    return CRICKET_CATEGORY_ALIASES.get(key, key.replace(" ", "_"))


def normalize_cricket_training_mode(training_mode: Optional[str]) -> Optional[str]:
    """Normalize a training mode string to 'alone' or 'with_others'."""
    if training_mode is None:
        return None
    key = training_mode.strip().lower().replace("_", " ")
    return CRICKET_MODE_ALIASES.get(key, key.replace(" ", "_"))


def get_cricket_catalog() -> SportCatalog:
    """Return a deep copy of the full cricket catalog."""
    return deepcopy(CRICKET_CATALOG)


def list_cricket_sessions(
    category: Optional[str] = None,
    training_mode: Optional[str] = None,
) -> List[SportSession]:
    """List cricket sessions, optionally filtered by category and training mode."""
    normalized_category = normalize_cricket_category(category)
    normalized_mode = normalize_cricket_training_mode(training_mode)

    sessions: List[SportSession] = []
    for category_key, category_data in CRICKET_CATALOG.items():
        if normalized_category and category_key != normalized_category:
            continue
        for mode_key, mode_data in category_data.items():
            if normalized_mode and mode_key != normalized_mode:
                continue
            sessions.extend(mode_data.values())
    return deepcopy(sessions)


def get_cricket_session(
    session_key: str,
    category: Optional[str] = None,
    training_mode: Optional[str] = None,
) -> Optional[SportSession]:
    """Find one cricket session by key, optionally inside a category/training mode."""
    for item in list_cricket_sessions(category=category, training_mode=training_mode):
        if item["key"] == session_key:
            return item
    return None


# Generic names that catalog_manager.py can use if it expects standard exports.
CATALOG = CRICKET_CATALOG
SESSION_BANK = CRICKET_SESSION_BANK
CATEGORIES = CRICKET_CATEGORIES
TRAINING_MODES = CRICKET_TRAINING_MODES


if __name__ == "__main__":
    print(f"{SPORT} catalog loaded: {len(CRICKET_SESSION_BANK)} sessions")
    for category_name in CRICKET_CATEGORIES:
        count = len(list_cricket_sessions(category=category_name))
        print(f"- {category_name}: {count} sessions")
