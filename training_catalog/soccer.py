"""
Sportze.AI soccer training catalog.

This module contains soccer workouts codified as plain Python data so it can be
imported by the training generator without extra dependencies.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


SOCCER_WORKOUTS: List[Dict[str, Any]] = [
    {
        "id": "soccer_learn_how_to_play",
        "sport": "soccer",
        "title": "Learn How to Play",
        "level": "learn",
        "category": "learn_how_to_play",
        "role": "general",
        "training_type": "alone",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Ball Familiarity Warm-Up",
                "prescription": "Place the ball on the ground. For 5 continuous minutes, lightly tap the top of the ball using alternating feet (right-left-right-left). If the ball rolls away more than 1 meter, bring it back immediately and continue until the full 5 minutes are completed."
            },
            {
                "name": "Inside-Foot Wall Passes",
                "prescription": "Stand 5 meters from a wall. Strike the ball using only the inside of your dominant foot. Receive the rebound, control it with one touch, and immediately pass again. Complete 100 consecutive passes. If the ball misses the wall or travels more than 2 meters away, retrieve it and continue counting."
            },
            {
                "name": "Weak Foot Wall Passes",
                "prescription": "Repeat Exercise 2, but use only your weaker foot. Complete 75 passes."
            },
            {
                "name": "First Touch Control",
                "prescription": "Stand 6 meters from a wall. Pass the ball firmly against the wall. When it returns: Control with inside of right foot. Pass back. Repeat. Then: Inside left foot. Outside right foot. Outside left foot. 25 controls with each surface (100 total)."
            },
            {
                "name": "Straight-Line Dribbling",
                "prescription": "Mark a 25-meter straight line using cones or objects. Dribble to the end using short touches. Turn around. Return. Repeat until you have completed 10 lengths (250 meters total). The ball should never be more than 1 meter away from your feet."
            },
            {
                "name": "Cone Slalom",
                "prescription": "Place 8 cones in a straight line, 2 meters apart. Dribble through all 8 cones. Turn around. Repeat. Complete: 10 runs using both feet. 5 runs using only the right foot. 5 runs using only the left foot. Total: 20 runs."
            },
            {
                "name": "Running With the Ball",
                "prescription": "Mark a 30-meter lane. Push the ball ahead and run at approximately 70% sprint speed while maintaining control. At the end: Stop the ball. Turn. Return. Complete 12 runs."
            },
            {
                "name": "Basic Shooting Accuracy",
                "prescription": "Create a target approximately 1.5 meters wide using two cones or objects. Stand 12 meters away. Shoot: 20 shots with dominant foot. 20 shots with weaker foot. Count how many finish between the cones. Goal: At least 25 accurate shots."
            },
            {
                "name": "Juggling Progression",
                "prescription": "Complete: 20 juggles using any body part except hands. 15 juggles using only the right foot. 15 juggles using only the left foot. 10 alternating feet only. If the ball drops, restart only the current set."
            },
            {
                "name": "Ball Shielding",
                "prescription": "Place the ball inside a 2-meter circle. Move continuously around the circle while keeping your body between an imaginary defender and the ball. Every 5 seconds, change direction. Complete 8 rounds of 45 seconds, resting 20 seconds between rounds."
            },
            {
                "name": "Long Passing Technique",
                "prescription": "Stand 20 meters from a wall or marked target. Strike the ball using the instep (laces). Control the rebound. Repeat. Complete: 40 passes with dominant foot. 30 passes with weaker foot."
            },
            {
                "name": "Sprint Recovery Drill",
                "prescription": "Mark distances of 10 meters and 20 meters. Perform: Sprint 20 meters with the ball. Stop the ball completely. Jog back. Complete 12 repetitions. After the final repetition: Sprint 20 meters without the ball six times. Rest 30 seconds between sprints."
            },
            {
                "name": "Combination Circuit",
                "prescription": "Without stopping, complete: 30 wall passes. Dribble through the cones. Run 25 meters with the ball. Shoot once on target. This equals one round. Complete 8 full rounds. Rest 60 seconds between rounds."
            },
            {
                "name": "Mini Match Simulation",
                "prescription": "Create a continuous circuit: Dribble 20 meters. Perform the cone slalom. Complete 10 wall passes. Run 15 meters with the ball. Shoot once on goal. Retrieve the ball and repeat immediately. Complete the circuit continuously for 20 minutes, maintaining a steady pace while minimizing unnecessary stops."
            }
        ]
    },
    {
        "id": "soccer_beginner_field_player",
        "sport": "soccer",
        "title": "Beginner Field Player",
        "level": "beginner",
        "category": "beginner_field_player",
        "role": "field_player",
        "training_type": "alone",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Two-Foot Passing Accuracy",
                "prescription": "Stand 8 meters from a wall. Complete: 60 inside-foot passes with the right foot. 60 inside-foot passes with the left foot. Use one touch to control every rebound before passing again."
            },
            {
                "name": "First Touch Box",
                "prescription": "Mark a 4 × 4 meter square. Pass the ball against a wall from 6 meters away. Your first touch must keep the ball inside the square before passing again. Complete 80 successful controls."
            },
            {
                "name": "Close-Control Dribbling",
                "prescription": "Place 10 cones in a straight line, 1.5 meters apart. Complete: 8 runs using both feet. 6 runs using only the right foot. 6 runs using only the left foot. 4 runs using only the outside of both feet. Total: 24 runs."
            },
            {
                "name": "Speed Dribble Intervals",
                "prescription": "Mark 30 meters. Dribble to the end at 85% speed. Walk back. Complete 12 repetitions. The ball should never move more than 1.5 meters ahead of you."
            },
            {
                "name": "Finishing Circuit",
                "prescription": "Create a goal or 2-meter-wide target. Shoot: 20 first-touch shots. 20 shots after dribbling 10 meters. 20 shots with the weaker foot. Total: 60 shots."
            },
            {
                "name": "Ball Juggling Challenge",
                "prescription": "Complete: 30 continuous juggles. 20 right-foot only. 20 left-foot only. 15 alternating feet only. 10 alternating thighs then feet. Restart only the failed set if the ball drops."
            },
            {
                "name": "Long Passing Accuracy",
                "prescription": "Mark a target 25 meters away. Complete: 40 driven passes with the dominant foot. 30 driven passes with the weaker foot. Count only passes finishing within 2 meters of the target."
            },
            {
                "name": "Change-of-Direction Dribbling",
                "prescription": "Create a 15 × 15 meter square. Sprint-dribble diagonally to each corner. Change direction sharply at every cone. Complete 16 full laps."
            },
            {
                "name": "Weak Foot Development",
                "prescription": "Using only the weaker foot: 40 passes. 20 dribble slalom runs. 20 shots. 15 long passes. Do not use the dominant foot except for balance."
            },
            {
                "name": "Ball Protection Circuit",
                "prescription": "Mark a 3-meter circle. Move continuously around the circle while shielding the ball. Every 10 seconds perform: One spin turn. One drag-back. One outside cut. Complete 10 rounds of 1 minute."
            },
            {
                "name": "Endurance With Ball",
                "prescription": "Dribble continuously around a 50-meter loop. Complete 12 laps without stopping. Every second lap: Sprint the final 20 meters."
            },
            {
                "name": "Passing & Movement Circuit",
                "prescription": "Perform: 20 wall passes. Run backward 10 meters. Sprint forward. Receive another pass. Repeat. Complete 15 rounds."
            },
            {
                "name": "Reaction Ball Control",
                "prescription": "Kick the ball firmly against the wall from 8 meters. As it rebounds unpredictably: Control it within 2 touches. Pass again immediately. Complete 80 successful recoveries."
            },
            {
                "name": "Beginner Match Circuit",
                "prescription": "Complete continuously: Dribble 20 meters. Cone slalom. 15 wall passes. 25-meter sprint with the ball. Shoot once. Retrieve ball. Repeat for 25 minutes."
            }
        ]
    },
    {
        "id": "soccer_beginner_goalkeeper",
        "sport": "soccer",
        "title": "Beginner Goalkeeper",
        "level": "beginner",
        "category": "beginner_goalkeeper",
        "role": "goalkeeper",
        "training_type": "alone",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Ready Position Footwork",
                "prescription": "Place 6 cones in a straight line, 1.5 meters apart. Shuffle sideways through every cone while maintaining goalkeeper stance. Sprint back. Complete 20 repetitions."
            },
            {
                "name": "Wall Catch Drill",
                "prescription": "Stand 4 meters from a wall. Throw the ball firmly. Catch it cleanly before it hits the ground. Complete: 60 chest-height catches. 40 shoulder-height catches. 30 low catches."
            },
            {
                "name": "Ground Collection",
                "prescription": "Roll the ball 6 meters away. Sprint forward. Collect using the proper \"scoop\" technique. Return. Repeat 50 times. Alternate sides every repetition."
            },
            {
                "name": "Diving Technique",
                "prescription": "Place a mat or soft grass area. Start kneeling. Dive: 20 right. 20 left. Then standing: 20 right. 20 left. Focus on landing technique."
            },
            {
                "name": "Goal Kick Accuracy",
                "prescription": "Mark a 5-meter target zone located 30 meters away. Complete: 30 goal kicks with dominant foot. 20 with weaker foot. Count only accurate kicks."
            },
            {
                "name": "Throwing Distribution",
                "prescription": "Throw the ball overarm toward a target 25 meters away. Complete: 30 throws with dominant arm. 20 with weaker arm."
            },
            {
                "name": "Reaction Wall Saves",
                "prescription": "Throw the ball hard against the wall. As it rebounds: Catch or parry immediately. Complete 80 reactions."
            },
            {
                "name": "Cross Collection Simulation",
                "prescription": "Throw the ball high. Move underneath. Jump. Catch at the highest point. Land balanced. Repeat 40 catches."
            },
            {
                "name": "One-on-One Footwork",
                "prescription": "Place 4 cones in a diamond. Shuffle around the diamond. Sprint forward 3 meters. Drop into save position. Return. Complete 25 repetitions."
            },
            {
                "name": "Recovery Saves",
                "prescription": "Place two balls 5 meters apart. Dive to save Ball 1. Stand immediately. Sprint to Ball 2. Dive again. Complete 20 sets."
            },
            {
                "name": "Distribution Under Pressure",
                "prescription": "Perform: Catch. Roll the ball accurately to a target 15 meters away. Receive it back. Repeat with a throw. Repeat with a goal kick. Complete 25 full cycles."
            },
            {
                "name": "High Ball Handling",
                "prescription": "Throw the ball above head height. Jump. Catch at maximum reach. Land balanced. Repeat 50 catches."
            },
            {
                "name": "Goalkeeper Conditioning Circuit",
                "prescription": "Without stopping: Shuffle 10 meters. Sprint 10 meters. Dive right. Recover. Dive left. Recover. Catch a high ball. Goal kick. Complete 12 rounds."
            },
            {
                "name": "Solo Match Simulation",
                "prescription": "For 25 continuous minutes, rotate through: Footwork through cones. Wall reaction save. High catch. Ground collection. Goal kick. Throw distribution. Dive save. Rest only after completing the full 25-minute circuit."
            }
        ]
    },
    {
        "id": "soccer_goalkeeper_training_alone",
        "sport": "soccer",
        "title": "Goalkeeper - Training Alone",
        "level": "position_specific",
        "category": "goalkeeper",
        "role": "goalkeeper",
        "training_type": "alone",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Low Diving Saves",
                "prescription": "Place two cones 4 meters apart. Start centered between them. Roll the ball 2 meters in front of you toward the right cone, dive and collect it before it crosses the cone. Repeat to the left. 25 dives each side (50 total)."
            },
            {
                "name": "High Ball Collection",
                "prescription": "Throw the ball 4–5 meters into the air directly above yourself. Jump with one knee raised. Catch at the highest point. Land balanced. 50 catches."
            },
            {
                "name": "Goal Kick Accuracy",
                "prescription": "Place targets at 25m, 35m and 45m. Complete: 15 kicks to 25m 15 kicks to 35m 15 kicks to 45m Repeat with weaker foot. 90 kicks total."
            },
            {
                "name": "Reaction Wall Saves",
                "prescription": "Stand 3 meters from a wall. Throw the ball hard. React immediately after the unpredictable rebound. Complete: 40 catches 20 parries 20 one-hand saves"
            },
            {
                "name": "Footwork Ladder",
                "prescription": "Place 10 cones 1 meter apart. Shuffle through. Sprint back. Repeat using: Side shuffle Carioca Forward sprint Backpedal 5 rounds each movement."
            },
            {
                "name": "One-Hand Catch Drill",
                "prescription": "Throw the ball high. Catch only with the right hand. Repeat with the left. 30 catches per hand."
            },
            {
                "name": "Distribution Circuit",
                "prescription": "Perform continuously: Catch Roll 20m Retrieve Throw overarm 30m Retrieve Goal kick 40m Repeat 15 cycles."
            },
            {
                "name": "Dive Recovery",
                "prescription": "Dive right. Stand immediately. Sprint 6 meters. Dive left. Stand. Sprint back. Complete 20 cycles."
            },
            {
                "name": "Cross Simulation",
                "prescription": "Throw the ball high while stepping backward. Judge the flight. Jump. Catch. Land balanced. 40 repetitions."
            },
            {
                "name": "Reflex Tennis Ball Drill",
                "prescription": "Throw a tennis ball against a wall. Catch before second bounce. Complete: 50 right hand 50 left hand 50 both hands"
            },
            {
                "name": "Goalkeeper Conditioning",
                "prescription": "Complete: 10m sprint Backpedal Dive Stand Shuffle High catch Repeat 15 rounds."
            },
            {
                "name": "Weak Foot Distribution",
                "prescription": "Complete: 40 passes 25 goal kicks 20 long driven balls Only weaker foot."
            },
            {
                "name": "Recovery Sprint",
                "prescription": "Start lying face down. Stand. Sprint 12m. Touch cone. Return. Dive. Repeat 20 reps."
            },
            {
                "name": "Full Goalkeeper Match Circuit",
                "prescription": "For 30 minutes, continuously rotate: Goal kick Dive save High catch Throw distribution Shuffle Reflex save Minimal rest."
            }
        ]
    },
    {
        "id": "soccer_fullback_training_alone",
        "sport": "soccer",
        "title": "Fullback - Training Alone",
        "level": "position_specific",
        "category": "fullback",
        "role": "fullback",
        "training_type": "alone",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Overlapping Runs",
                "prescription": "Mark 40 meters. Sprint with the ball. Cross into target. Jog back. 20 repetitions."
            },
            {
                "name": "Crossing Accuracy",
                "prescription": "Place a 3×3m target inside the penalty area. Deliver: 25 right-foot crosses 25 left-foot crosses"
            },
            {
                "name": "Recovery Runs",
                "prescription": "Sprint 35m. Backpedal 15m. Sprint again. Repeat 15 times."
            },
            {
                "name": "Dribble then Cross",
                "prescription": "Dribble through 8 cones. Accelerate 20m. Cross immediately. 25 repetitions."
            },
            {
                "name": "Long Passing",
                "prescription": "Targets at: 20m 30m 40m 15 passes to each target with each foot. 90 passes."
            },
            {
                "name": "One-Touch Wall Passing",
                "prescription": "Stand 7m away. Complete: 80 one-touch passes right foot. 80 left foot."
            },
            {
                "name": "Defensive Footwork",
                "prescription": "Create a 5×5m square. Shuffle around all four sides. Never cross feet. Complete 20 laps."
            },
            {
                "name": "Weak Foot Crossing",
                "prescription": "Using only weaker foot: Deliver 40 crosses."
            },
            {
                "name": "First Touch Into Space",
                "prescription": "Wall pass. First touch must move ball 3 meters forward. Sprint after it. Repeat 60 times."
            },
            {
                "name": "Endurance Ball Carry",
                "prescription": "Dribble 60 meters. Sprint last 20m. Return jogging. Complete 12 repetitions."
            },
            {
                "name": "Crossing Under Fatigue",
                "prescription": "Perform: 20 push-ups. Sprint 30m. Cross. Repeat 15 rounds."
            },
            {
                "name": "Ball Carry Circuit",
                "prescription": "Complete: Slalom. 30m sprint. Cross. Retrieve. Repeat 20 rounds."
            },
            {
                "name": "Shield then Pass",
                "prescription": "Inside a 3m circle, shield the ball for 20 seconds. Exit with a 25m pass. Repeat 25 times."
            },
            {
                "name": "Fullback Match Simulation",
                "prescription": "For 30 minutes: Alternate continuously: Recovery sprint Ball carry Cross Long pass Wall pass Defensive shuffle"
            }
        ]
    },
    {
        "id": "soccer_center_back_training_alone",
        "sport": "soccer",
        "title": "Center Back - Training Alone",
        "level": "position_specific",
        "category": "center_back",
        "role": "center_back",
        "training_type": "alone",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Long Driven Passes",
                "prescription": "Targets: 20m, 30m, 40m. 20 passes to each. 60 passes."
            },
            {
                "name": "Defensive Heading",
                "prescription": "Throw ball high. Jump. Head toward target. Complete 60 headers."
            },
            {
                "name": "Build-Up Passing",
                "prescription": "Wall passing. Receive with one touch. Play long pass. Repeat 50 sequences."
            },
            {
                "name": "Backpedal Recovery",
                "prescription": "Backpedal 15m. Turn. Sprint 20m. Repeat 20 reps."
            },
            {
                "name": "Defensive Clearances",
                "prescription": "Kick ball 40m using laces. Complete 50 clearances."
            },
            {
                "name": "Weak Foot Passing",
                "prescription": "Complete: 60 passes. 30 long balls. Only weaker foot."
            },
            {
                "name": "Aerial Timing",
                "prescription": "Throw high ball. Jump at highest point. Head to target. 40 headers."
            },
            {
                "name": "First Touch Under Pressure",
                "prescription": "Pass to wall. Control. Turn 180°. Pass again. Repeat 80 times."
            },
            {
                "name": "Strength Shielding",
                "prescription": "Inside 4m circle: Hold strong stance while moving with the ball. 10 rounds of 1 minute."
            },
            {
                "name": "Defensive Sprint Circuit",
                "prescription": "Sprint. Shuffle. Backpedal. Sprint. Repeat 20 rounds."
            },
            {
                "name": "Ball Carry Out of Defense",
                "prescription": "Dribble 25 meters. Play long pass. Repeat 30 repetitions."
            },
            {
                "name": "Passing Accuracy Challenge",
                "prescription": "Hit 1m target from 30m. Complete 40 accurate passes."
            },
            {
                "name": "Heading Endurance",
                "prescription": "Complete: 20 standing headers. 20 jumping headers. 20 running headers."
            },
            {
                "name": "Center Back Match Circuit",
                "prescription": "30 continuous minutes rotating: Build-up pass Long ball Header Recovery sprint Ball carry"
            }
        ]
    },
    {
        "id": "soccer_defensive_midfielder_training_alone",
        "sport": "soccer",
        "title": "Defensive Midfielder - Training Alone",
        "level": "position_specific",
        "category": "defensive_midfielder",
        "role": "defensive_midfielder",
        "training_type": "alone",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "360° Wall Passing",
                "prescription": "Pass against wall. Open body before receiving. Play next pass with opposite foot. Complete 120 passes."
            },
            {
                "name": "Switching Play",
                "prescription": "Targets at: 20m left. 20m right. Alternate passes. 80 passes."
            },
            {
                "name": "First Touch Direction",
                "prescription": "Receive from wall. First touch must exit at 45°. Repeat 80 repetitions."
            },
            {
                "name": "Tempo Passing",
                "prescription": "Without stopping: One-touch wall passing for 8 continuous minutes."
            },
            {
                "name": "Ball Recovery Sprint",
                "prescription": "Sprint 15m. Collect stationary ball. Turn. Return. Repeat 30 times."
            },
            {
                "name": "Weak Foot Passing",
                "prescription": "Complete: 80 short passes. 40 long passes. Only weaker foot."
            },
            {
                "name": "Ball Retention Circuit",
                "prescription": "Inside 5×5m square: Perform continuous: Sole roll Drag back Inside cut Outside cut For 12 minutes."
            },
            {
                "name": "Progressive Carry",
                "prescription": "Dribble 35 meters. Play accurate 25m pass. Repeat 25 times."
            },
            {
                "name": "Long Passing Accuracy",
                "prescription": "Hit targets: 20m 30m 40m 15 passes each distance with both feet."
            },
            {
                "name": "Body Orientation Drill",
                "prescription": "Before every wall pass: Look over both shoulders. Receive sideways. Pass immediately. Complete 100 repetitions."
            },
            {
                "name": "Endurance Possession",
                "prescription": "Dribble continuously inside a 15×15m square for 15 minutes, changing direction every 20 seconds."
            },
            {
                "name": "Passing Pyramid",
                "prescription": "Complete: 20 passes at 10m. 20 at 20m. 20 at 30m. 20 at 40m. Repeat with weaker foot."
            },
            {
                "name": "Transition Circuit",
                "prescription": "Complete: Sprint 20m. Receive pass from wall. Turn. Long pass. Jog back. Repeat 20 rounds."
            },
            {
                "name": "Defensive Midfielder Match Simulation",
                "prescription": "For 30 minutes, continuously rotate: One-touch passing Ball carry Long switch Recovery sprint Progressive dribble First-touch turn"
            }
        ]
    },
    {
        "id": "soccer_central_midfielder_cm_training_alone",
        "sport": "soccer",
        "title": "Central Midfielder (CM) - Training Alone",
        "level": "position_specific",
        "category": "central_midfielder",
        "role": "central_midfielder",
        "training_type": "alone",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Two-Touch Passing Circuit",
                "prescription": "Stand 8 meters from a wall. Receive every rebound with one touch and pass back with the second touch. 100 passes right foot 100 passes left foot"
            },
            {
                "name": "Box-to-Box Runs",
                "prescription": "Mark 50 meters. Dribble 25 meters. Sprint 25 meters without the ball. Jog back. Complete 15 repetitions."
            },
            {
                "name": "Progressive Passing",
                "prescription": "Place targets at: 10m 20m 30m 40m Play: 20 passes to each target. Repeat using the weaker foot."
            },
            {
                "name": "360° Ball Control",
                "prescription": "Inside a 6×6m square, continuously: Sole roll Inside cut Outside cut Cruyff turn Drag back Change move every 10 seconds. Continue for 15 minutes."
            },
            {
                "name": "Long Passing Accuracy",
                "prescription": "Place three targets: Left (35m) Center (35m) Right (35m) Complete 25 accurate passes to each."
            },
            {
                "name": "Weak Foot Development",
                "prescription": "Using only the weaker foot: 50 passes 25 long passes 20 shots 20 dribble runs"
            },
            {
                "name": "Ball Carry Under Speed",
                "prescription": "Dribble 40 meters at 85% sprint speed. Return jogging. Complete 15 repetitions."
            },
            {
                "name": "Passing Endurance",
                "prescription": "Perform continuous one-touch wall passing for 10 minutes. If possession is lost, immediately restart."
            },
            {
                "name": "First Touch Into Space",
                "prescription": "Pass against a wall. Your first touch must move the ball 3 meters diagonally before making the next pass. Complete 80 repetitions."
            },
            {
                "name": "Combination Circuit",
                "prescription": "Complete: 20 wall passes Cone slalom 30m dribble Long pass Repeat 15 rounds."
            },
            {
                "name": "Reaction Passing",
                "prescription": "Throw the ball hard against the wall. Control within one touch. Immediately pass again. Complete 100 repetitions."
            },
            {
                "name": "Midfield Endurance",
                "prescription": "Dribble continuously around a 60-meter loop for 20 minutes. Every second lap: Sprint the final 20 meters."
            },
            {
                "name": "Passing Pyramid",
                "prescription": "Complete: 25 passes (10m) 25 passes (20m) 25 passes (30m) 25 passes (40m) Repeat with weaker foot."
            },
            {
                "name": "Match Simulation",
                "prescription": "For 35 continuous minutes, rotate: Passing Dribbling Long ball Ball carry Shooting Recovery sprint"
            }
        ]
    },
    {
        "id": "soccer_attacking_midfielder_cam_training_alone",
        "sport": "soccer",
        "title": "Attacking Midfielder (CAM) - Training Alone",
        "level": "position_specific",
        "category": "attacking_midfielder",
        "role": "attacking_midfielder",
        "training_type": "alone",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Through Ball Accuracy",
                "prescription": "Create a 2-meter gate using cones 25 meters away. Play 60 through balls, aiming to pass cleanly through the gate."
            },
            {
                "name": "Turn and Shoot",
                "prescription": "Pass against a wall. Receive. Turn 180°. Dribble 10 meters. Shoot. Complete 40 repetitions."
            },
            {
                "name": "Tight Space Dribbling",
                "prescription": "Create a 5×5m square. Dribble continuously for 12 minutes, never allowing the ball outside the square."
            },
            {
                "name": "Long-Range Shooting",
                "prescription": "Shoot from: 18m (20 shots) 22m (20 shots) 25m (20 shots) Alternate feet."
            },
            {
                "name": "Creative Passing",
                "prescription": "Place five cone targets around you between 10 and 25 meters away. Randomly choose a target before every pass. Complete 100 passes."
            },
            {
                "name": "Weak Foot Finishing",
                "prescription": "Using only the weaker foot: 40 shots 20 volleys 20 passes"
            },
            {
                "name": "First Touch Escape",
                "prescription": "Pass to the wall. First touch must escape an imaginary defender by 2 meters. Repeat 80 times."
            },
            {
                "name": "Agility Dribble Circuit",
                "prescription": "Complete: Cone slalom 15m sprint Quick stop Turn Sprint back Repeat 20 rounds."
            },
            {
                "name": "Combination Shooting",
                "prescription": "Dribble through 8 cones. Play a wall pass. Receive. Shoot first time. Complete 40 repetitions."
            },
            {
                "name": "Vision Drill",
                "prescription": "Before every wall pass: Look left. Look right. Receive. Pass. Complete 120 repetitions."
            },
            {
                "name": "Long Passing",
                "prescription": "Play: 25 lofted passes 25 driven passes 25 chipped passes Targets 30–40 meters away."
            },
            {
                "name": "Ball Carry",
                "prescription": "Dribble 50 meters. Finish with a shot. Complete 20 repetitions."
            },
            {
                "name": "Playmaker Conditioning",
                "prescription": "Perform continuously: 20m sprint Turn Dribble Pass Shoot Complete 15 rounds."
            },
            {
                "name": "Match Simulation",
                "prescription": "For 35 minutes, rotate: Through ball Dribble Long shot Wall pass Sprint Finish"
            }
        ]
    },
    {
        "id": "soccer_winger_lw_rw_training_alone",
        "sport": "soccer",
        "title": "Winger (LW/RW) - Training Alone",
        "level": "position_specific",
        "category": "winger",
        "role": "winger",
        "training_type": "alone",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Sprint Dribble",
                "prescription": "Mark 40 meters. Sprint with the ball. Keep every touch within 2 meters. Complete 20 runs."
            },
            {
                "name": "1v1 Cone Slalom",
                "prescription": "Place 10 cones. Dribble through them as quickly as possible. Complete 25 runs."
            },
            {
                "name": "Crossing Accuracy",
                "prescription": "Cross into a 3×3m target inside the penalty area. 30 right-foot crosses 30 left-foot crosses"
            },
            {
                "name": "Cut Inside and Shoot",
                "prescription": "Start near the sideline. Dribble diagonally inside 20 meters. Shoot from outside the box. Complete 40 repetitions."
            },
            {
                "name": "Outside Dribble",
                "prescription": "Using only the outside of each foot: Dribble 30 meters. Repeat 20 times."
            },
            {
                "name": "Weak Foot Crossing",
                "prescription": "Using only weaker foot: Deliver 40 crosses."
            },
            {
                "name": "Speed Endurance",
                "prescription": "Sprint 50 meters. Walk back. Complete 18 repetitions."
            },
            {
                "name": "Ball Carry Circuit",
                "prescription": "Dribble: 20m Turn 20m Cross Repeat 20 rounds."
            },
            {
                "name": "First Touch Into Sprint",
                "prescription": "Wall pass. First touch pushes the ball 5 meters ahead. Sprint after it. Complete 50 repetitions."
            },
            {
                "name": "Long Sprint Finishing",
                "prescription": "Sprint 35 meters. Shoot immediately. Repeat 25 times."
            },
            {
                "name": "Technical Circuit",
                "prescription": "Complete: Cone slalom Cut inside Outside cut Cross Repeat 15 rounds."
            },
            {
                "name": "Weak Foot Shooting",
                "prescription": "Using only weaker foot: Complete 40 shots."
            },
            {
                "name": "Wing Conditioning",
                "prescription": "Complete: Sprint Backpedal Sprint Cross Repeat 15 rounds."
            },
            {
                "name": "Match Simulation",
                "prescription": "For 35 minutes, rotate: Sprint Dribble Cross Cut inside Shoot Recover"
            }
        ]
    },
    {
        "id": "soccer_striker_st_training_alone",
        "sport": "soccer",
        "title": "Striker (ST) - Training Alone",
        "level": "position_specific",
        "category": "striker",
        "role": "striker",
        "training_type": "alone",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "First-Time Finishing",
                "prescription": "Stand 12 meters from a wall. Pass firmly. Shoot first time after the rebound. Complete: 40 right foot 40 left foot"
            },
            {
                "name": "One-Touch Finishing",
                "prescription": "Throw the ball slightly forward. Strike without controlling it. Complete 50 shots."
            },
            {
                "name": "Finishing After Sprint",
                "prescription": "Sprint 25 meters. Receive the ball. Shoot immediately. Complete 30 repetitions."
            },
            {
                "name": "Weak Foot Finishing",
                "prescription": "Using only weaker foot: Complete 50 shots."
            },
            {
                "name": "Heading Accuracy",
                "prescription": "Throw the ball above your head. Head into a 2×2m target. Complete 60 headers."
            },
            {
                "name": "Turn and Shoot",
                "prescription": "Receive from the wall. Turn. Shoot within 2 touches. Complete 40 repetitions."
            },
            {
                "name": "Long-Range Shooting",
                "prescription": "Shoot from: 18m 22m 25m 20 shots from each distance."
            },
            {
                "name": "Finishing Circuit",
                "prescription": "Complete: Dribble 15m Shoot Retrieve ball Repeat 30 rounds."
            },
            {
                "name": "Ball Protection",
                "prescription": "Inside a 3m circle, shield the ball for 30 seconds. Exit with a shot. Complete 20 repetitions."
            },
            {
                "name": "Curved Run Simulation",
                "prescription": "Place two cones 8 meters apart. Start behind the first cone. Make a curved run around the second cone, receive the ball after passing it against a wall, and finish with a shot in one or two touches. Complete 30 repetitions."
            },
            {
                "name": "Volley Practice",
                "prescription": "Throw the ball approximately 2 meters into the air. Strike it before it touches the ground. Complete: 25 right-foot volleys 25 left-foot volleys"
            },
            {
                "name": "Finishing Under Fatigue",
                "prescription": "Complete: 15 burpees Sprint 20m Shoot Jog back Repeat 15 rounds."
            },
            {
                "name": "Elite Finishing Challenge",
                "prescription": "Complete: 20 first-touch finishes 20 weak-foot finishes 20 volleys 20 headers 20 shots after dribbling 100 total finishes."
            },
            {
                "name": "Striker Match Simulation",
                "prescription": "For 35 continuous minutes, rotate through: Curved run Sprint to receive First-touch finish Turn and shoot Header Volley Weak-foot finish"
            }
        ]
    },
    {
        "id": "soccer_learn_how_to_play",
        "sport": "soccer",
        "title": "Learn How to Play",
        "level": "learn",
        "category": "learn_how_to_play",
        "role": "general",
        "training_type": "2+ people",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Basic Passing Pairs",
                "prescription": "Stand 8 meters apart. Pass the ball using only the inside of your foot. Control every pass before returning it. Complete 150 successful passes each."
            },
            {
                "name": "Passing While Moving",
                "prescription": "Stand 10 meters apart. Both players jog slowly in the same direction while continuously passing the ball. Continue for 12 minutes without stopping."
            },
            {
                "name": "Triangle Passing",
                "prescription": "Use 3 players. Create a triangle with sides of 8 meters. Pass clockwise for 5 minutes, then counterclockwise for 5 minutes."
            },
            {
                "name": "Follow Your Pass",
                "prescription": "With 4 or more players, stand in a square. Pass to the next player, then immediately run to take their position. Complete 100 passes without breaking the rotation."
            },
            {
                "name": "Dribble Relay Race",
                "prescription": "Create 2 teams. Each player dribbles 25 meters, turns around a cone, returns, and tags the next teammate. First team to complete 10 rounds wins."
            },
            {
                "name": "Give-and-Go Drill",
                "prescription": "Stand 12 meters apart. Player A passes. Player B returns the ball first touch. Player A runs past Player B before receiving the return pass. Repeat 40 give-and-go combinations, then switch roles."
            },
            {
                "name": "Passing Accuracy Challenge",
                "prescription": "Place a 1.5-meter gate between two cones. Stand 15 meters away. Pass through the gate to your teammate. Complete 60 successful passes each."
            },
            {
                "name": "Keep Possession",
                "prescription": "Create a 10 × 10 meter square. With 3–5 players, keep possession using a maximum of 2 touches. Continue for 10 rounds of 2 minutes."
            },
            {
                "name": "First Touch Competition",
                "prescription": "One player serves the ball. The receiving player must control it within a 2-meter square. Complete 40 successful controls, then switch roles."
            },
            {
                "name": "Shooting Rotation",
                "prescription": "One player passes. The other player takes one touch and shoots. Retrieve the ball and switch roles. Complete 40 shots each."
            },
            {
                "name": "Crossing and Finishing",
                "prescription": "Player A dribbles 20 meters and crosses. Player B times their run and finishes first time. Switch roles every 10 crosses. Complete 40 finishes each."
            },
            {
                "name": "Small-Sided Match",
                "prescription": "Play 2v2, 3v3, or 4v4. Play 6 games of 5 minutes, resting 2 minutes between games. Maximum 3 touches per player."
            },
            {
                "name": "Continuous Combination Circuit",
                "prescription": "Complete: Wall-style pass with teammate Give-and-go Dribble 15 meters Pass Receive Shoot Repeat 20 full circuits."
            },
            {
                "name": "Beginner Match",
                "prescription": "Play a continuous 30-minute match. Every player must attempt: 20 completed passes 10 successful dribbles 5 shots 5 successful first touches"
            }
        ]
    },
    {
        "id": "soccer_beginner_field_player",
        "sport": "soccer",
        "title": "Beginner Field Player",
        "level": "beginner",
        "category": "beginner_field_player",
        "role": "field_player",
        "training_type": "2+ people",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "One-Touch Passing",
                "prescription": "Stand 8 meters apart. Complete 100 one-touch passes each. If possession is lost, continue until all 100 are completed."
            },
            {
                "name": "Two-Touch Passing Under Movement",
                "prescription": "Jog continuously around a 20 × 20 meter square while exchanging passes. Continue for 15 minutes."
            },
            {
                "name": "Triangle Combination Play",
                "prescription": "Three players. Complete: Pass Move Receive Pass Complete 150 successful passes."
            },
            {
                "name": "Crossing & Finishing",
                "prescription": "Player A crosses from the wing. Player B finishes first touch. Switch every 10 crosses. Complete 50 finishes each."
            },
            {
                "name": "Give-and-Go Finishing",
                "prescription": "Pass. Receive the return pass while running. Shoot within 2 touches. Complete 40 repetitions each."
            },
            {
                "name": "Possession Under Pressure",
                "prescription": "Play 3v1 or 4v2 inside a 12 × 12 meter square. Maintain possession for 2 minutes. Repeat 8 rounds."
            },
            {
                "name": "Long Passing Accuracy",
                "prescription": "Stand 30 meters apart. Complete: 40 driven passes. 20 lofted passes. Switch roles."
            },
            {
                "name": "Defensive Recovery Relay",
                "prescription": "Player A dribbles forward. Player B starts 5 meters behind and sprints to catch up before the finish cone. Repeat 25 times, then switch."
            },
            {
                "name": "First Touch Under Pressure",
                "prescription": "One player serves difficult passes. Receiver must control and return within 2 touches. Complete 60 receptions."
            },
            {
                "name": "Small Passing Grid",
                "prescription": "Play 4v2 inside a 15 × 15 meter square. Maximum 2 touches. Complete 10 rounds of 3 minutes."
            },
            {
                "name": "Finishing Circuit",
                "prescription": "Pass. Receive. Dribble 10 meters. Shoot. Switch roles. Complete 40 finishes each."
            },
            {
                "name": "Transition Drill",
                "prescription": "Play 3v2. After every shot, defending team immediately attacks in the opposite direction. Continue for 25 minutes."
            },
            {
                "name": "Small-Sided Match",
                "prescription": "Play 5v5 or 6v6. Four games of 8 minutes. Maximum 3 touches."
            },
            {
                "name": "Beginner Match Simulation",
                "prescription": "Play a 40-minute match. Every player should attempt: 30 passes 10 forward passes 5 shots 5 successful tackles 5 successful dribbles"
            }
        ]
    },
    {
        "id": "soccer_beginner_goalkeeper",
        "sport": "soccer",
        "title": "Beginner Goalkeeper",
        "level": "beginner",
        "category": "beginner_goalkeeper",
        "role": "goalkeeper",
        "training_type": "2+ people",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Basic Catching",
                "prescription": "Partner stands 8 meters away. Throw balls at: Chest Waist Knees Catch cleanly. Complete 120 catches."
            },
            {
                "name": "Ground Saves",
                "prescription": "Partner rolls balls to alternating corners. Dive and secure every ball. Complete 60 saves."
            },
            {
                "name": "High Ball Collection",
                "prescription": "Partner throws high balls into the penalty area. Jump. Catch at highest point. Complete 50 catches."
            },
            {
                "name": "Shot Stopping",
                "prescription": "Partner shoots from 12 meters. Complete 60 saves, varying placement between low, medium, and high shots."
            },
            {
                "name": "One-on-One Saves",
                "prescription": "Partner dribbles toward goal from 15 meters. Close the angle and make the save. Complete 40 repetitions."
            },
            {
                "name": "Distribution Accuracy",
                "prescription": "After every save: Roll the ball accurately to a teammate 20 meters away. Then repeat with an overarm throw. Then repeat with a goal kick. Complete 30 full cycles."
            },
            {
                "name": "Reaction Saves",
                "prescription": "Stand 3 meters from a teammate. The teammate quickly throws or lightly strikes the ball without warning. React and save. Complete 80 saves."
            },
            {
                "name": "Cross Collection",
                "prescription": "Partner crosses from both wings. Move off the line. Catch or punch the ball cleanly. Complete 40 crosses from each side."
            },
            {
                "name": "Footwork Circuit",
                "prescription": "Partner points left, right, or forward just before serving the ball. Move quickly into position before making the save. Complete 50 repetitions."
            },
            {
                "name": "Recovery Saves",
                "prescription": "Partner shoots. After making the first save, immediately recover to your feet for a second shot within 3 seconds. Complete 30 double-save sequences."
            },
            {
                "name": "Communication Drill",
                "prescription": "Play 4 attackers vs 3 defenders in front of goal. The goalkeeper must continuously organize the defenders by calling: \"Left\" \"Right\" \"Mark\" \"Step\" \"Keeper\" Continue for 20 minutes."
            },
            {
                "name": "Goalkeeper Distribution Under Pressure",
                "prescription": "Play 3 teammates vs 2 pressing opponents. Receive back passes and distribute the ball without losing possession. Complete 30 successful build-up sequences."
            },
            {
                "name": "Shot Variety Circuit",
                "prescription": "Partner alternates: Low shot High shot Volley Header One-on-one finish Complete 50 total saves."
            },
            {
                "name": "Match Simulation",
                "prescription": "Play a 45-minute small-sided match where the goalkeeper is expected to: Claim crosses Save shots Organize defenders Distribute after every possession Play with feet whenever possible"
            }
        ]
    },
    {
        "id": "soccer_goalkeeper_2_people",
        "sport": "soccer",
        "title": "Goalkeeper - 2+ People",
        "level": "position_specific",
        "category": "goalkeeper",
        "role": "goalkeeper",
        "training_type": "2+ people",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Shot-Stopping Circuit",
                "prescription": "Position 4 shooters around the penalty area: Left edge of the box Center (18m) Right edge of the box Penalty spot Each player shoots once before the next begins. The goalkeeper must recover to the center after every save. Complete 80 shots."
            },
            {
                "name": "Cross Collection",
                "prescription": "Two players stand on opposite wings. Alternate crosses into the penalty area. The goalkeeper must decide whether to: Catch Punch Stay on the line Complete 60 crosses."
            },
            {
                "name": "One-on-One Saves",
                "prescription": "One attacker starts 20 meters from goal. Dribble directly toward goal. Goalkeeper must close the angle and attempt the save. Complete 40 repetitions. Switch attackers every 10 attempts."
            },
            {
                "name": "Build-Up Under Pressure",
                "prescription": "Create: Goalkeeper 2 center backs 2 pressing attackers The goalkeeper begins every sequence. Complete 50 successful build-ups without losing possession."
            },
            {
                "name": "Double Save Drill",
                "prescription": "Coach or teammate shoots. Immediately after the save, another player shoots within 2 seconds. Recover quickly between attempts. Complete 40 double-save sequences."
            },
            {
                "name": "Communication Drill",
                "prescription": "Play: 5 attackers 4 defenders The goalkeeper must continuously organize the defense by calling: Step Drop Left Right Mark Keeper Continue for 25 minutes."
            },
            {
                "name": "Reaction Deflections",
                "prescription": "One player shoots. Another player positioned near goal intentionally deflects the shot. Goalkeeper reacts to the new trajectory. Complete 40 deflected shots."
            },
            {
                "name": "High Ball Chaos",
                "prescription": "Five attackers attack aerial crosses. Goalkeeper must claim or punch every delivery. Complete 50 crosses."
            },
            {
                "name": "Distribution Accuracy",
                "prescription": "After every save: Alternate: Roll to fullback. Throw to midfielder. Goal kick to winger. Complete 60 distributions."
            },
            {
                "name": "Corner Kick Management",
                "prescription": "Defend 40 corner kicks. Focus on: Positioning Catching Punching Communication"
            },
            {
                "name": "Sweeper Keeper Drill",
                "prescription": "Defensive line starts near midfield. Coach plays through balls behind them. Goalkeeper must decide whether to clear or retreat. Complete 40 repetitions."
            },
            {
                "name": "Penalty Practice",
                "prescription": "Face 40 penalties from different players. Each player changes placement every attempt."
            },
            {
                "name": "Match Pressure Circuit",
                "prescription": "Alternate: Corner Free kick Cross Through ball Shot Complete 40 total situations."
            },
            {
                "name": "Match Simulation",
                "prescription": "Play a 60-minute match focused on: Communication Distribution Sweeper actions Crosses Shot stopping"
            }
        ]
    },
    {
        "id": "soccer_fullback_2_people",
        "sport": "soccer",
        "title": "Fullback - 2+ People",
        "level": "position_specific",
        "category": "fullback",
        "role": "fullback",
        "training_type": "2+ people",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Overlap & Cross",
                "prescription": "Winger starts with the ball. Fullback overlaps on the outside. Receive the pass. Deliver a cross. Striker finishes. Complete 40 overlaps. Switch sides."
            },
            {
                "name": "Defensive 1v1",
                "prescription": "Start 15 meters apart. Attacker attempts to beat the defender. Defender must force the attacker wide and win possession. Complete 30 duels."
            },
            {
                "name": "Recovery Sprint",
                "prescription": "Attacker starts 5 meters ahead. Coach plays a through ball. Fullback sprints back and prevents the cross. Complete 30 repetitions."
            },
            {
                "name": "Crossing Accuracy",
                "prescription": "Deliver: 20 early crosses. 20 deep crosses. 20 cut-backs. Strikers attempt to finish every delivery."
            },
            {
                "name": "Passing Combination",
                "prescription": "Triangle: Center back Fullback Winger Complete 150 one-touch passes while rotating positions every 25 passes."
            },
            {
                "name": "Pressing Drill",
                "prescription": "Play 4v4 on one half of the field. Whenever possession is lost, fullback has 5 seconds to press and recover the ball. Continue for 25 minutes."
            },
            {
                "name": "Build-Up Play",
                "prescription": "Receive from goalkeeper. Pass to center back. Receive again. Pass into midfield. Complete 60 build-up sequences."
            },
            {
                "name": "Transition Drill",
                "prescription": "After crossing: Immediately sprint 40 meters back into defensive position. Complete 30 repetitions."
            },
            {
                "name": "Long Passing",
                "prescription": "Play diagonal passes: Fullback to opposite winger. Complete 50 successful switches."
            },
            {
                "name": "Crossing Under Pressure",
                "prescription": "Receive while a defender closes down. Deliver the cross before being tackled. Complete 40 repetitions."
            },
            {
                "name": "Small-Sided Position Game",
                "prescription": "Play 5v5. Fullbacks may only use 2 touches. Continue for 30 minutes."
            },
            {
                "name": "Defensive Shape",
                "prescription": "Play: Back four vs four attackers. Maintain defensive line. Repeat for 30 minutes."
            },
            {
                "name": "Continuous Position Circuit",
                "prescription": "Repeat: Receive. Overlap. Cross. Recover. Defend 1v1. Repeat 20 cycles."
            },
            {
                "name": "Match Simulation",
                "prescription": "Play 60 minutes. Focus objectives: Minimum 20 completed passes. Minimum 8 successful crosses. Win at least 8 defensive duels. Complete every recovery sprint after joining the attack."
            }
        ]
    },
    {
        "id": "soccer_center_back_2_people",
        "sport": "soccer",
        "title": "Center Back - 2+ People",
        "level": "position_specific",
        "category": "center_back",
        "role": "center_back",
        "training_type": "2+ people",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Defensive Heading",
                "prescription": "Coach delivers aerial balls. Clear with headers. Complete 60 headers."
            },
            {
                "name": "1v1 Defending",
                "prescription": "Striker receives with back to goal. Prevent the turn. Win possession. Complete 30 duels."
            },
            {
                "name": "Build-Up Passing",
                "prescription": "Play: Goalkeeper → Center Back → Midfielder. Complete 80 successful sequences."
            },
            {
                "name": "Defensive Line Drill",
                "prescription": "Work with another center back and two fullbacks. Practice: Stepping up Dropping Holding line Continue for 30 minutes."
            },
            {
                "name": "Long Passing",
                "prescription": "Play: 40 diagonal passes. 40 driven passes. Targets are wingers."
            },
            {
                "name": "Through Ball Recovery",
                "prescription": "Coach plays through balls. Sprint back. Shield. Clear. Complete 30 repetitions."
            },
            {
                "name": "Defensive Clearances",
                "prescription": "Coach serves crosses. Clear: By foot. By header. Complete 60 clearances."
            },
            {
                "name": "Press Resistance",
                "prescription": "Receive under pressure. Complete the pass within 2 touches. Repeat 50 times."
            },
            {
                "name": "Defensive Transition",
                "prescription": "Play 5v4. Recover shape immediately after losing possession. Continue 20 minutes."
            },
            {
                "name": "Marking Drill",
                "prescription": "Stay goal side of striker. Prevent receiving. Complete 30 repetitions."
            },
            {
                "name": "Corner Defending",
                "prescription": "Defend 40 corners. Alternate: Zonal marking. Man marking."
            },
            {
                "name": "Communication",
                "prescription": "Organize: Fullbacks. Goalkeeper. Midfield. Continue during 25 minutes of defensive drills."
            },
            {
                "name": "Defensive Circuit",
                "prescription": "Repeat: Header. Sprint. Clear. Build-up pass. Recover. Complete 20 rounds."
            },
            {
                "name": "Match Simulation",
                "prescription": "Play 60 minutes. Objectives: Win aerial duels. Complete build-up passes. Maintain defensive line. Prevent through balls."
            }
        ]
    },
    {
        "id": "soccer_defensive_midfielder_cdm_2_people",
        "sport": "soccer",
        "title": "Defensive Midfielder (CDM) - 2+ People",
        "level": "position_specific",
        "category": "defensive_midfielder",
        "role": "defensive_midfielder",
        "training_type": "2+ people",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "One-Touch Possession",
                "prescription": "Play 5v2. Maximum 2 touches. Complete 20 minutes."
            },
            {
                "name": "Ball Recovery",
                "prescription": "Coach serves loose balls. Sprint. Win possession. Pass immediately. Complete 40 recoveries."
            },
            {
                "name": "Switching Play",
                "prescription": "Receive centrally. Switch play to opposite wing. Complete 60 accurate switches."
            },
            {
                "name": "Press Resistance",
                "prescription": "Play 3v2 inside a 12×12 meter square. Escape pressure using passing and body positioning. Continue 20 minutes."
            },
            {
                "name": "Progressive Passing",
                "prescription": "Receive from center back. Turn. Pass forward. Complete 60 sequences."
            },
            {
                "name": "Defensive Cover",
                "prescription": "Play: Back four + CDM vs five attackers. Protect the space in front of the defense. Continue 30 minutes."
            },
            {
                "name": "Transition Drill",
                "prescription": "After winning possession: Complete 3 passes before shooting. Repeat 30 attacks."
            },
            {
                "name": "Long Passing",
                "prescription": "Play: 30 lofted passes. 30 driven passes. Targets are wide players."
            },
            {
                "name": "Interception Drill",
                "prescription": "Coach plays passes between attackers. Intercept before the receiver controls the ball. Complete 40 interceptions."
            },
            {
                "name": "Body Orientation",
                "prescription": "Receive while marked. Open body before controlling. Pass forward. Complete 80 repetitions."
            },
            {
                "name": "Build-Up Rotation",
                "prescription": "Rotate positions with: Center backs. Central midfielder. Complete 40 build-up sequences."
            },
            {
                "name": "Defensive Pressure",
                "prescription": "Play 6v6. CDM must press immediately after possession is lost. Continue 25 minutes."
            },
            {
                "name": "Complete Midfield Circuit",
                "prescription": "Recover. Pass. Switch play. Support attack. Recover again. Repeat 20 rounds."
            },
            {
                "name": "Match Simulation",
                "prescription": "Play 60 minutes. Objectives: Minimum 30 completed passes. Minimum 10 forward passes. Minimum 8 ball recoveries. Minimum 5 interceptions. Successfully switch play at least 6 times."
            }
        ]
    },
    {
        "id": "soccer_central_midfielder_cm_2_people",
        "sport": "soccer",
        "title": "Central Midfielder (CM) - 2+ People",
        "level": "position_specific",
        "category": "central_midfielder",
        "role": "central_midfielder",
        "training_type": "2+ people",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Box-to-Box Transition",
                "prescription": "Play 6v6. Every time possession changes, sprint from one penalty area to the other before rejoining play. Continue for 25 minutes."
            },
            {
                "name": "Passing Triangle Rotation",
                "prescription": "Three players form a triangle with sides of 10 meters. Pass, follow your pass, and rotate continuously. Complete 200 successful passes."
            },
            {
                "name": "Progressive Passing",
                "prescription": "Receive from a defender. Turn within 2 touches. Play a forward pass to an attacker. Complete 60 successful sequences."
            },
            {
                "name": "Long Switches",
                "prescription": "Stand centrally. Alternate diagonal passes to left and right wingers positioned 35 meters away. Complete 60 switches."
            },
            {
                "name": "One-Touch Possession",
                "prescription": "Play 5v2. Maximum one touch. Continue for 20 minutes."
            },
            {
                "name": "Midfield Support Drill",
                "prescription": "Play 4 attackers vs 4 defenders. The central midfielder must always provide a passing option by moving into space before every pass. Continue for 25 minutes."
            },
            {
                "name": "Through-Ball Timing",
                "prescription": "Striker makes a run. Deliver the pass only after the striker begins the movement. Complete 40 through balls."
            },
            {
                "name": "Transition Circuit",
                "prescription": "Win possession. Play three passes. Sprint forward into the attack. Receive the return pass. Shoot. Repeat 25 repetitions."
            },
            {
                "name": "Defensive Recovery",
                "prescription": "Lose possession intentionally. Sprint back 30 meters. Recover the ball before the attacking team reaches the box. Repeat 20 times."
            },
            {
                "name": "Combination Play",
                "prescription": "Perform: Wall pass Third-man run Through ball Complete 40 complete combinations."
            },
            {
                "name": "Build-Up Under Pressure",
                "prescription": "Play 6v4 from the defensive third. Maintain possession until reaching midfield. Complete 30 successful build-ups."
            },
            {
                "name": "Midfield Possession Match",
                "prescription": "Play 7v7. Every midfielder is limited to 2 touches. Continue 30 minutes."
            },
            {
                "name": "Passing Endurance",
                "prescription": "Complete 300 consecutive team passes. Restart the count if possession is lost."
            },
            {
                "name": "Match Simulation",
                "prescription": "Play 60 minutes. Objectives: 40 completed passes. 10 progressive passes. 6 ball recoveries. 5 long switches. Constant movement to support teammates."
            }
        ]
    },
    {
        "id": "soccer_attacking_midfielder_cam_2_people",
        "sport": "soccer",
        "title": "Attacking Midfielder (CAM) - 2+ People",
        "level": "position_specific",
        "category": "attacking_midfielder",
        "role": "attacking_midfielder",
        "training_type": "2+ people",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Through Ball Drill",
                "prescription": "Two strikers begin level with the defensive line. Wait for one to start a run before playing the through ball. Complete 50 accurate through balls."
            },
            {
                "name": "Turn and Create",
                "prescription": "Receive with your back to goal. Turn within 2 touches. Play the final pass. Complete 40 repetitions."
            },
            {
                "name": "Third-Man Combination",
                "prescription": "Three players perform: Player A → Player B → Player C running behind the defense. Complete 60 successful combinations."
            },
            {
                "name": "Tight-Space Possession",
                "prescription": "Play 4v4 inside a 15×15 meter square. Maximum 2 touches. Continue 20 minutes."
            },
            {
                "name": "Edge-of-the-Box Shooting",
                "prescription": "Receive outside the penalty area. One touch. Shoot. Complete 50 finishes."
            },
            {
                "name": "Creative Passing Challenge",
                "prescription": "Five teammates move continuously. Choose the best passing option before every pass. Complete 100 successful passes."
            },
            {
                "name": "Combination Finishing",
                "prescription": "Pass. Receive the return pass. Play another teammate through on goal. Complete 40 combinations."
            },
            {
                "name": "Playmaker Under Pressure",
                "prescription": "Play 5v5. Every possession must pass through the attacking midfielder before a shot is allowed. Continue 30 minutes."
            },
            {
                "name": "Long Passing",
                "prescription": "Alternate: Lofted passes Driven passes Chipped passes Complete 75 total passes."
            },
            {
                "name": "Vision Drill",
                "prescription": "Before receiving every pass: Look over both shoulders. Control. Play forward. Complete 80 repetitions."
            },
            {
                "name": "Press Escape",
                "prescription": "Play 3v2. Escape pressure within 3 passes. Complete 40 successful escapes."
            },
            {
                "name": "Final Third Decisions",
                "prescription": "Receive near the penalty area. Choose: Shoot Through ball Switch play Decision must be made within 3 seconds. Complete 50 attacks."
            },
            {
                "name": "Attacking Rotation",
                "prescription": "Rotate positions with: Striker Winger Continue for 25 minutes."
            },
            {
                "name": "Match Simulation",
                "prescription": "Play 60 minutes. Objectives: 10 key passes. 5 through balls. 4 shots. 3 assists. Constant movement between midfield and attack."
            }
        ]
    },
    {
        "id": "soccer_winger_lw_rw_2_people",
        "sport": "soccer",
        "title": "Winger (LW/RW) - 2+ People",
        "level": "position_specific",
        "category": "winger",
        "role": "winger",
        "training_type": "2+ people",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "1v1 Attacking",
                "prescription": "Start 20 meters from goal. Beat the defender. Deliver a cross or shoot. Complete 30 duels."
            },
            {
                "name": "Overlap Combination",
                "prescription": "Fullback overlaps. Play the overlap pass. Receive the return ball. Cross. Complete 40 repetitions."
            },
            {
                "name": "Crossing Accuracy",
                "prescription": "Deliver: 20 early crosses. 20 deep crosses. 20 cut-backs. Strikers attempt to finish each cross."
            },
            {
                "name": "Cut Inside and Shoot",
                "prescription": "Receive near the touchline. Dribble diagonally inside. Shoot before entering the six-yard box. Complete 40 repetitions."
            },
            {
                "name": "Counterattack Sprint",
                "prescription": "Start near midfield. Sprint with teammates on a 3v2 counterattack. Finish within 10 seconds. Repeat 30 attacks."
            },
            {
                "name": "Pressing Drill",
                "prescription": "Immediately after losing possession, press the defender for 5 seconds. Continue 25 minutes."
            },
            {
                "name": "Give-and-Go",
                "prescription": "Play a wall pass with the fullback. Receive while running. Cross first time. Complete 40 combinations."
            },
            {
                "name": "Weak Foot Crossing",
                "prescription": "Using only the weaker foot: Deliver 40 crosses."
            },
            {
                "name": "Transition Recovery",
                "prescription": "Attack. Immediately sprint back into defensive shape. Repeat 30 times."
            },
            {
                "name": "Wing Possession",
                "prescription": "Play 5v5. Every attack must include a winger before a shot is taken. Continue 25 minutes."
            },
            {
                "name": "Switch of Play",
                "prescription": "Receive diagonal passes from the opposite side. Control. Attack immediately. Complete 40 receptions."
            },
            {
                "name": "Crossing Under Pressure",
                "prescription": "Defender closes aggressively. Deliver the cross before contact. Complete 40 repetitions."
            },
            {
                "name": "Wide Combination Circuit",
                "prescription": "Complete: Receive Dribble Give-and-go Cross Recover Repeat 20 cycles."
            },
            {
                "name": "Match Simulation",
                "prescription": "Play 60 minutes. Objectives: 10 successful dribbles. 10 crosses. 5 shots. 5 defensive recoveries. Continuous width in attack."
            }
        ]
    },
    {
        "id": "soccer_striker_st_2_people",
        "sport": "soccer",
        "title": "Striker (ST) - 2+ People",
        "level": "position_specific",
        "category": "striker",
        "role": "striker",
        "training_type": "2+ people",
        "equipment": [
            "soccer ball",
            "cones",
            "wall/target",
            "goal or marked target"
        ],
        "exercises": [
            {
                "name": "Finishing From Crosses",
                "prescription": "Two wingers alternate crosses. Finish with one or two touches. Complete 60 finishes."
            },
            {
                "name": "Curved Runs",
                "prescription": "Start level with the defensive line. Curve your run behind the defenders. Receive the through ball. Finish first time whenever possible. Complete 40 runs."
            },
            {
                "name": "Hold-Up Play",
                "prescription": "Receive with your back to goal. Shield the defender for 3 seconds. Lay the ball off to a midfielder. Complete 40 repetitions."
            },
            {
                "name": "One-Touch Finishing",
                "prescription": "Midfielder serves passes inside the penalty area. Finish with a single touch. Complete 50 shots."
            },
            {
                "name": "Volley Practice",
                "prescription": "Partner crosses from the wing. Finish before the ball touches the ground. Complete 40 volleys."
            },
            {
                "name": "Heading Practice",
                "prescription": "Receive aerial crosses. Head toward goal. Complete 50 headers."
            },
            {
                "name": "Near-Post and Far-Post Runs",
                "prescription": "Alternate: Near-post runs. Far-post runs. Receive a cross and finish. Complete 20 runs to each post (40 total)."
            },
            {
                "name": "Pressing From the Front",
                "prescription": "Play 6v6. As soon as the opposing goalkeeper or center back receives the ball, initiate the press. Continue 25 minutes."
            },
            {
                "name": "Counterattack Finishing",
                "prescription": "Play 3v2. Finish every attack within 10 seconds. Complete 30 counterattacks."
            },
            {
                "name": "Combination Play",
                "prescription": "Perform: Wall pass. Spin behind the defender. Receive. Shoot. Complete 40 combinations."
            },
            {
                "name": "Penalty Area Movement",
                "prescription": "Remain inside the penalty area. Continuously adjust your position to stay available for crosses and through balls. Finish every chance created. Continue 20 minutes."
            },
            {
                "name": "Finishing Under Pressure",
                "prescription": "Receive while closely marked by a defender. Finish within 2 touches. Complete 40 repetitions."
            },
            {
                "name": "Elite Finishing Circuit",
                "prescription": "Complete: 20 first-touch finishes. 20 headers. 20 volleys. 20 one-on-one finishes. 20 weak-foot finishes. 100 total finishes."
            },
            {
                "name": "Match Simulation",
                "prescription": "Play 60 minutes. Objectives: 8 shots. 4 shots on target. 5 successful runs behind the defense. 5 successful hold-up plays. Press the opposition whenever possession is lost."
            }
        ]
    }
]


WORKOUTS = SOCCER_WORKOUTS


def get_workouts(
    level: Optional[str] = None,
    training_type: Optional[str] = None,
    role: Optional[str] = None,
    category: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Return soccer workouts filtered by optional catalog fields."""
    results = SOCCER_WORKOUTS

    if level is not None:
        results = [w for w in results if w["level"] == level]

    if training_type is not None:
        results = [w for w in results if w["training_type"] == training_type]

    if role is not None:
        normalized_role = role.lower().replace(" ", "_").replace("-", "_")
        results = [w for w in results if w["role"] == normalized_role]

    if category is not None:
        normalized_category = category.lower().replace(" ", "_").replace("-", "_")
        results = [w for w in results if w["category"] == normalized_category]

    return results


def get_workout_by_id(workout_id: str) -> Optional[Dict[str, Any]]:
    """Return one workout by id, or None if it does not exist."""
    return next((w for w in SOCCER_WORKOUTS if w["id"] == workout_id), None)


def list_categories() -> List[str]:
    """Return all available soccer catalog categories."""
    return sorted({w["category"] for w in SOCCER_WORKOUTS})


def list_roles() -> List[str]:
    """Return all available soccer roles."""
    return sorted({w["role"] for w in SOCCER_WORKOUTS})


def list_training_types() -> List[str]:
    """Return supported training formats for soccer."""
    return sorted({w["training_type"] for w in SOCCER_WORKOUTS})


__all__ = [
    "SOCCER_WORKOUTS",
    "WORKOUTS",
    "get_workouts",
    "get_workout_by_id",
    "list_categories",
    "list_roles",
    "list_training_types",
]
