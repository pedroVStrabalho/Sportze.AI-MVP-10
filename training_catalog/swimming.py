"""Swimming training catalog for Sportze.AI.

This module codifies the swimming workouts supplied for the Sportze.AI training
catalog. The file is import-safe and exposes a normalized list of sessions that
can be consumed by the catalog manager.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

SPORT = "swimming"
SPORT_NAME = "Swimming"


def exercise(name: str, prescription: str, notes: str | None = None) -> Dict[str, Any]:
    item: Dict[str, Any] = {"name": name, "prescription": prescription}
    if notes:
        item["notes"] = notes
    return item


def session(
    name: str,
    category: str,
    training_type: str,
    exercises: List[Dict[str, Any]],
    level: str | None = None,
    participants: str = "alone",
    focus: str | None = None,
) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "sport": SPORT,
        "name": name,
        "category": category,
        "training_type": training_type,
        "participants": participants,
        "exercises": exercises,
    }
    if level:
        data["level"] = level
    if focus:
        data["focus"] = focus
    return data


RAW_SWIMMING_CATALOG = r'''
Swimming — Learn How to Swim (14 Exercises)
1. Water Confidence Walk
Walk through the shallow end of the pool for 10 minutes, gradually lowering your shoulders underwater every 30 seconds. Finish by submerging your entire head 20 times, exhaling underwater before resurfacing.

2. Floating Practice
Hold onto the pool wall and practice floating face down for 15 seconds before standing up. Repeat 15 times. Then float on your back for 15 seconds another 15 times.

3. Bubble Breathing
Hold the pool edge and place your face underwater. Blow bubbles continuously for 5 seconds, lift your head to inhale, then repeat 40 repetitions.

4. Flutter Kick with Kickboard
Using a kickboard, swim 12 × 25 m using only flutter kicks. Rest 30 seconds between lengths while keeping your legs straight and toes pointed.

5. Back Floating and Kick
Lie on your back holding a kickboard against your chest and kick continuously for 10 × 25 m, focusing on keeping your hips at the surface.

6. Freestyle Arm Introduction
Stand in waist-deep water and perform 100 slow freestyle arm strokes, concentrating on reaching forward and pulling all the way to your thigh.

7. Freestyle Swim
Swim 8 × 25 m freestyle at an easy pace, resting 45 seconds between repetitions. Focus only on completing each length with good body position.

8. Basic Backstroke
Swim 8 × 25 m backstroke, keeping your eyes facing the ceiling throughout every repetition.

9. Basic Breaststroke
Swim 8 × 25 m breaststroke, pausing briefly after every glide to learn proper stroke timing.

10. Dolphin Kick Introduction
Hold a kickboard with both hands and perform 10 × 25 m dolphin kick, focusing on generating movement from your hips rather than your knees.

11. Treading Water
Tread water continuously for 8 minutes, taking a 30-second rest after every 2 minutes if needed.

12. Basic Wall Push-Offs
Push off the wall into a streamlined position and glide as far as possible before standing up. Perform 30 push-offs.

13. Continuous Swim
Swim continuously for 400 m using any comfortable stroke without stopping. Slow down whenever necessary but keep moving until the full distance is completed.

14. Mixed Stroke Practice
Complete:
100 m freestyle
100 m backstroke
100 m breaststroke
50 m freestyle
50 m backstroke
Rest 30 seconds between each segment.

Swimming — Beginner (14 Exercises)
1. Freestyle Technique Endurance
Swim 10 × 50 m freestyle at a comfortable pace, resting 20 seconds after each repetition while maintaining consistent stroke technique.

2. Bilateral Breathing
Swim 8 × 50 m freestyle, breathing every 3 strokes throughout each repetition. Rest 25 seconds.

3. Kick Endurance
Using a kickboard, complete:
6 × 50 m flutter kick
6 × 50 m breaststroke kick
Rest 20 seconds after each repetition.

4. Pull Technique
Place a pull buoy between your legs and swim 8 × 50 m freestyle, using only your arms. Rest 20 seconds.

5. Freestyle Distance Build
Complete:
100 m
200 m
300 m
200 m
100 m
Rest 30 seconds between each swim.

6. Stroke Rotation Session
Complete:
4 × 50 m freestyle
4 × 50 m backstroke
4 × 50 m breaststroke
Rest 20 seconds after every repetition.

7. Flip Turn Introduction
Swim 12 × 25 m freestyle, performing a flip turn at every wall instead of touching and turning manually.

8. Speed Introduction
Complete:
8 × 25 m freestyle at 90% effort
8 × 25 m easy recovery freestyle
Alternate between fast and easy repetitions with 30 seconds of rest.

9. Continuous Endurance Swim
Swim 1,000 m continuously at an easy pace without stopping. Focus on maintaining a steady rhythm throughout the swim.

10. Mixed Kick and Swim
Complete:
200 m kickboard flutter kick
200 m freestyle
200 m kickboard breaststroke kick
200 m freestyle
Rest 30 seconds after each 200 m.

11. Pull and Swim Combination
Repeat 5 rounds of:
100 m freestyle with pull buoy
100 m normal freestyle
Rest 20 seconds between each swim.

12. Pace Control Session
Complete:
100 m easy
100 m moderate
100 m fast
Repeat the sequence 3 times for a total of 900 m, resting 20 seconds between each 100 m.

13. Stroke Endurance Challenge
Complete:
300 m freestyle
200 m backstroke
200 m breaststroke
300 m freestyle
Rest 30 seconds between segments.

14. Beginner Mini Distance Session
Complete:
400 m freestyle
200 m backstroke
200 m breaststroke
200 m freestyle
Finish with 4 × 25 m freestyle sprints at maximum effort, resting 30 seconds after each sprint.

Freestyle — 50 m Sprint
1. Swim 12 × 50 m freestyle at 95% effort, resting 60 seconds after each repetition. Maintain maximum stroke rate from the first stroke until touching the wall.
2. Complete 8 × 50 m freestyle. The first 25 m is easy, then accelerate to maximum speed for the final 25 m. Rest 45 seconds.
3. Swim 10 × 50 m freestyle using only 6 strokes before reaching full speed, emphasizing explosive acceleration from every wall push-off. Rest 60 seconds.
4. Complete 14 × 50 m freestyle at 90% effort, aiming to keep every repetition within ±1 second of the first swim. Rest 40 seconds.
5. Swim 10 × 50 m freestyle while breathing every 5 strokes. Maintain sprint speed while minimizing head movement. Rest 50 seconds.
6. Perform 16 × 25 m maximum freestyle sprints, resting 30 seconds after each, then finish with 2 × 50 m freestyle at race pace.

Freestyle — 100 m Middle Distance
7. Swim 8 × 100 m freestyle at 85% effort, resting 30 seconds between repetitions. Hold a consistent pace throughout every swim.
8. Complete 6 × 100 m freestyle. Swim the first 50 m at moderate pace and the second 50 m faster than the first. Rest 40 seconds.
9. Swim 10 × 100 m freestyle using bilateral breathing every 3 strokes. Rest 25 seconds.
10. Complete 5 × 100 m freestyle, descending the time on every repetition until the final swim is your fastest. Rest 45 seconds.
11. Swim 12 × 100 m freestyle while maintaining exactly the same stroke count for every length. Rest 25 seconds.
12. Perform 4 × 100 m freestyle at race pace, followed immediately by 50 m easy recovery freestyle after each repetition.

Freestyle — 200 m Long Distance Pool
13. Swim 6 × 200 m freestyle at 80% effort, resting 40 seconds after each repetition.
14. Complete 5 × 200 m freestyle, increasing your speed every 50 m until finishing the final 50 m at race pace.
15. Swim 4 × 200 m freestyle while breathing every 5 strokes during the first 100 m and every 3 strokes during the second 100 m.
16. Complete 8 × 200 m freestyle pull buoy, using only your arms. Rest 30 seconds.
17. Swim 3 × 200 m freestyle, maintaining identical split times for every 50 m. Rest 60 seconds.
18. Complete 200 m freestyle, 150 m freestyle, 100 m freestyle, and 50 m freestyle. Increase your pace with each swim. Rest 45 seconds between repetitions.

Backstroke — 50 m
1. Swim 12 × 50 m backstroke at 95% effort, resting 60 seconds after each repetition. Focus on explosive starts and strong underwater dolphin kicks.
2. Complete 10 × 50 m backstroke, holding the same stroke count every repetition. Rest 40 seconds.
3. Swim 8 × 50 m backstroke, accelerating every final 15 m until maximum speed. Rest 45 seconds.
4. Complete 14 × 50 m backstroke, emphasizing fast arm turnover while maintaining hip rotation. Rest 35 seconds.
5. Swim 10 × 50 m backstroke, performing at least 8 underwater dolphin kicks after every push-off before surfacing. Rest 50 seconds.
6. Perform 16 × 25 m backstroke sprints, resting 30 seconds, then finish with 2 × 50 m race pace.

Backstroke — 100 m
7. Swim 8 × 100 m backstroke at 85% effort, resting 30 seconds.
8. Complete 6 × 100 m backstroke, negative splitting every repetition. Rest 35 seconds.
9. Swim 10 × 100 m backstroke, maintaining constant kick rhythm throughout. Rest 30 seconds.
10. Perform 5 × 100 m backstroke, descending each repetition until the last is your fastest.
11. Complete 8 × 100 m backstroke, minimizing strokes per length without reducing speed.
12. Swim 4 × 100 m race pace, followed immediately by 50 m easy recovery backstroke.

Backstroke — 200 m
13. Swim 6 × 200 m backstroke at aerobic pace. Rest 40 seconds.
14. Complete 5 × 200 m, increasing speed every 50 m.
15. Swim 4 × 200 m, keeping every 50 m within 2 seconds of each other.
16. Complete 6 × 200 m, emphasizing powerful underwater phases after every turn.
17. Swim 3 × 200 m backstroke at race pace, resting 90 seconds.
18. Complete 200 m, 150 m, 100 m, and 50 m. Increase pace after every swim.

Breaststroke — 50 m
1. Swim 12 × 50 m breaststroke at 95% effort, resting 60 seconds after each repetition. Focus on explosive pullouts after every wall.
2. Complete 10 × 50 m breaststroke, emphasizing maximum glide after every kick. Rest 45 seconds.
3. Swim 8 × 50 m breaststroke, accelerating over the final 15 m of every repetition. Rest 45 seconds.
4. Perform 14 × 50 m breaststroke, maintaining identical stroke timing throughout every repetition.
5. Swim 10 × 50 m breaststroke, counting strokes and reducing one stroke every second repetition while maintaining speed.
6. Complete 16 × 25 m breaststroke sprints, resting 30 seconds, then finish with 2 × 50 m race pace.

Breaststroke — 100 m
7. Swim 8 × 100 m breaststroke at 85% effort, resting 35 seconds.
8. Complete 6 × 100 m breaststroke, negative splitting each repetition.
9. Swim 10 × 100 m breaststroke, holding exactly the same stroke count every 25 m.
10. Perform 5 × 100 m breaststroke, descending the time every repetition.
11. Swim 8 × 100 m breaststroke, emphasizing long glides and efficient recovery.
12. Complete 4 × 100 m race pace, followed by 50 m easy breaststroke recovery.

Breaststroke — 200 m
13. Swim 6 × 200 m breaststroke at aerobic pace, resting 40 seconds.
14. Complete 5 × 200 m, increasing speed every 50 m until finishing at race pace.
15. Swim 4 × 200 m breaststroke, keeping every 50 m split within 2 seconds of each other.
16. Complete 6 × 200 m, focusing on powerful pullouts after every turn.
17. Swim 3 × 200 m breaststroke at race pace, resting 90 seconds.
18. Complete 200 m breaststroke, 150 m breaststroke, 100 m breaststroke, and 50 m breaststroke. Increase your pace after every swim while maintaining clean technique.

Butterfly — 50 m Sprint
1. Swim 12 × 50 m butterfly at 95% effort, resting 75 seconds after each repetition. Focus on explosive starts and maintaining two dolphin kicks per arm cycle.
2. Complete 10 × 50 m butterfly. Swim the first 25 m at controlled race pace and accelerate to maximum speed during the final 25 m. Rest 60 seconds.
3. Swim 8 × 50 m butterfly, performing 8 underwater dolphin kicks after every push-off before surfacing. Rest 60 seconds.
4. Complete 14 × 50 m butterfly, keeping every repetition within ±2 seconds of your first swim. Rest 50 seconds.
5. Swim 10 × 50 m butterfly, concentrating on maintaining identical stroke timing from the first stroke to the finish. Rest 60 seconds.
6. Perform 16 × 25 m butterfly sprints at maximum effort, resting 35 seconds after each repetition. Finish with 2 × 50 m butterfly at race pace.

Butterfly — 100 m Middle Distance
7. Swim 8 × 100 m butterfly at 85% effort, resting 45 seconds between repetitions while maintaining consistent rhythm.
8. Complete 6 × 100 m butterfly, swimming the second 50 m faster than the first. Rest 50 seconds.
9. Swim 10 × 100 m butterfly, maintaining exactly the same number of strokes every 25 m. Rest 40 seconds.
10. Complete 5 × 100 m butterfly, descending your time on every repetition until the final swim is your fastest. Rest 60 seconds.
11. Swim 8 × 100 m butterfly, emphasizing long, efficient strokes instead of increasing stroke rate. Rest 45 seconds.
12. Perform 4 × 100 m butterfly at race pace, followed immediately by 50 m easy freestyle recovery after every repetition.

Butterfly — 200 m Long Distance Pool
13. Swim 6 × 200 m butterfly at 80% effort, resting 60 seconds between repetitions while maintaining consistent pacing.
14. Complete 5 × 200 m butterfly, increasing your speed every 50 m until the final 50 m is at race pace.
15. Swim 4 × 200 m butterfly, keeping every 50 m split within 2 seconds of one another. Rest 75 seconds.
16. Complete 6 × 200 m butterfly, focusing on maintaining powerful dolphin kicks throughout the entire swim. Rest 50 seconds.
17. Swim 3 × 200 m butterfly at race pace, resting 90 seconds after each repetition.
18. Complete 200 m butterfly, 150 m butterfly, 100 m butterfly, and 50 m butterfly. Increase your pace after every swim while maintaining stroke efficiency.

Individual Medley — 100 IM
1. Swim 10 × 100 m Individual Medley at 90% effort, resting 45 seconds after each repetition. Perform 25 m butterfly, 25 m backstroke, 25 m breaststroke, and 25 m freestyle in every repetition.
2. Complete 8 × 100 m IM, swimming the second 50 m faster than the first. Rest 40 seconds.
3. Swim 6 × 100 m IM, emphasizing clean transitions between every stroke. Rest 45 seconds.
4. Complete 12 × 100 m IM, maintaining identical split times for every repetition. Rest 35 seconds.
5. Swim 8 × 100 m IM, increasing your pace every 25 m until finishing the freestyle leg at maximum effort. Rest 45 seconds.
6. Perform 4 × 100 m IM at race pace, followed immediately by 100 m easy freestyle recovery.

Individual Medley — 200 IM
7. Swim 8 × 200 m IM at 85% effort, resting 60 seconds between repetitions.
8. Complete 6 × 200 m IM, swimming every second 100 m faster than the first. Rest 60 seconds.
9. Swim 5 × 200 m IM, maintaining consistent pacing across all four strokes. Rest 75 seconds.
10. Complete 6 × 200 m IM, focusing on reducing transition time between strokes without sacrificing technique. Rest 60 seconds.
11. Swim 4 × 200 m IM, descending every repetition until the final swim is your fastest. Rest 90 seconds.
12. Perform 3 × 200 m IM at race pace, followed immediately by 100 m easy freestyle recovery after each repetition.

Individual Medley — 400 IM
13. Swim 5 × 400 m IM at aerobic pace, resting 90 seconds after each repetition.
14. Complete 4 × 400 m IM, increasing your pace every 100 m until finishing the freestyle leg at race speed.
15. Swim 3 × 400 m IM, keeping every 100 m split within 3 seconds of one another. Rest 2 minutes.
16. Complete 4 × 400 m IM, emphasizing efficient stroke transitions and consistent pacing throughout every repetition. Rest 90 seconds.
17. Swim 2 × 400 m IM at race pace, resting 3 minutes after the first repetition before starting the second.
18. Complete a descending ladder: 400 m IM, 300 m IM, 200 m IM, 100 m IM. Rest 90 seconds between each swim while increasing your pace after every repetition.

Competitive Long Distance Swimming — 400 m Specialists
1. Swim 8 × 400 m freestyle at 85% effort, resting 45 seconds between repetitions. Hold every 100 m split within 2 seconds of the previous one.
2. Complete 6 × 400 m freestyle, increasing your pace every 100 m until the final 100 m is at race pace. Rest 60 seconds after each repetition.
3. Swim 10 × 400 m freestyle at threshold pace, maintaining a stroke rate within ±2 strokes per minute throughout every repetition. Rest 30 seconds.
4. Complete 5 × 400 m freestyle at race pace, resting 90 seconds after each swim. Record every 50 m split and keep each split within 1 second of your target pace.
5. Swim 4 × 400 m freestyle, breathing every 3 strokes during the first 200 m and every 5 strokes during the second 200 m. Rest 60 seconds.
6. Complete 400 m freestyle, 300 m freestyle, 200 m freestyle, and 100 m freestyle. Increase your pace with every swim. Rest 45 seconds between repetitions.

Competitive Long Distance Swimming — 800 m Specialists
7. Swim 5 × 800 m freestyle at 80% effort, resting 60 seconds between repetitions while maintaining even pacing.
8. Complete 4 × 800 m freestyle, swimming the second 400 m faster than the first. Rest 75 seconds.
9. Swim 6 × 800 m freestyle, maintaining identical 100 m split times throughout every repetition. Rest 45 seconds.
10. Complete 3 × 800 m freestyle at race pace, resting 2 minutes after each repetition.
11. Swim 4 × 800 m freestyle, breathing every 5 strokes during the first 400 m and every 3 strokes during the final 400 m. Rest 60 seconds.
12. Complete 800 m freestyle, 600 m freestyle, 400 m freestyle, and 200 m freestyle. Increase your pace after every swim while maintaining smooth technique. Rest 60 seconds.

Competitive Long Distance Swimming — 1500 m Specialists
13. Swim 3 × 1500 m freestyle at aerobic race pace, resting 2 minutes after each repetition.
14. Complete 2 × 1500 m freestyle, swimming the second 750 m faster than the first. Rest 3 minutes.
15. Swim 4 × 1500 m freestyle, maintaining every 100 m split within 2 seconds of one another. Rest 90 seconds.
16. Complete 2 × 1500 m freestyle at race pace, recording every 100 m split and holding your target pace throughout the swim. Rest 4 minutes.
17. Swim 1500 m freestyle, 1000 m freestyle, and 500 m freestyle. Increase your pace with each swim while maintaining efficient technique. Rest 2 minutes between repetitions.
18. Complete the endurance ladder: 400 m, 800 m, 1200 m, 1500 m, 1200 m, 800 m, 400 m. Rest 60 seconds after each swim while maintaining race-level technique and consistent pacing.

Intermediate Endurance Swimming
1. Continuous Endurance Swim
Swim continuously until reaching your selected total distance at a comfortable aerobic pace. Maintain consistent stroke technique and breathing rhythm throughout the session without stopping unless absolutely necessary.
2. Negative Split Session
Divide your chosen total distance into two equal halves. Swim the first half at an easy, controlled pace, then complete the second half approximately 10–15% faster while maintaining efficient technique.
3. Progressive Pace Swim
Divide your selected distance into four equal segments. Swim each segment faster than the previous one, finishing the final quarter at approximately 90% effort.
4. Interval Endurance
Divide your chosen distance into equal intervals of 100 m or 200 m depending on the total distance. Rest 20 seconds after every interval while maintaining identical pacing throughout the workout.
5. Pyramid Endurance
Complete the pyramid 100 m, 200 m, 300 m, 400 m, 300 m, 200 m, 100 m until reaching the selected total distance. Rest 20 seconds after every swim.
6. Tempo Endurance
Swim your chosen total distance while alternating 200 m at moderate pace and 200 m at strong tempo pace. Rest 15 seconds after every 200 m.
7. Pull Buoy Endurance
Complete approximately 40% of your selected distance using a pull buoy, then swim the remaining distance with normal freestyle. Maintain smooth body position and consistent stroke length throughout.
8. Kick Endurance
Swim approximately 30% of your chosen distance using a kickboard with flutter kicks. Complete the remaining distance using freestyle at a steady aerobic pace. Rest 20 seconds after each kick interval.
9. Stroke Variation Endurance
Alternate 200 m freestyle, 100 m backstroke, and 100 m breaststroke until your target distance is reached. Substitute butterfly with freestyle if fatigue significantly affects technique.
10. Technique Under Fatigue
Swim your selected total distance continuously. During the final 25%, maintain the same stroke count, body position, and breathing rhythm used during the opening section.
11. Threshold Endurance Session
Divide your chosen distance into equal 200 m intervals. Swim every interval at approximately 85% effort, resting only 15 seconds between repetitions while keeping every interval within 3 seconds of one another.
12. Endurance Challenge
Complete your chosen total distance as: first 25% easy pace, second 25% moderate pace, third 25% strong pace, final 25% maximum sustainable pace. Finish with 200 m easy recovery freestyle.

Open Water / Marathon Swimming — 5 km Specialists
1. Swim 5 km continuously, maintaining 75–80% effort throughout. Every 500 m, increase your pace for 100 m before returning to your aerobic pace.
2. Complete 5 × 1 km freestyle, resting 45 seconds after every kilometer. Swim each kilometer faster than the previous one.
3. Swim 5 km continuously, lifting your head to sight every 8–10 strokes while maintaining body position and stroke rhythm.
4. Complete 1 km moderate, 500 m strong, 1 km moderate, 500 m race pace, and 2 km aerobic. Rest 30 seconds between segments.
5. Swim 10 × 500 m freestyle, resting 20 seconds after each repetition while keeping every 500 m within 5 seconds of one another.
6. Complete a continuous 5 km swim, increasing your pace every kilometer until the final kilometer is completed at race pace.

Open Water / Marathon Swimming — 10 km Specialists
7. Swim 10 km continuously at aerobic race pace. Every 2 km, increase your speed for 200 m before returning to your normal pace.
8. Complete 5 × 2 km freestyle, resting 60 seconds between repetitions while maintaining identical pacing throughout.
9. Swim 10 km continuously, practicing race nutrition by consuming fluids or carbohydrates every 20–30 minutes, exactly as you would during competition.
10. Complete 2 km easy, 2 km moderate, 2 km race pace, 2 km moderate, and 2 km strong finish. Rest 45 seconds between segments.
11. Swim 20 × 500 m freestyle, resting 15 seconds after each repetition while maintaining consistent pacing and efficient technique.
12. Complete a continuous 10 km swim, increasing your pace during the final 2 km until finishing at maximum sustainable effort.

Open Water / Marathon Swimming — Ultra Endurance 15–25 km
13. Swim 15 km continuously at comfortable aerobic pace. Practice race hydration and nutrition every 25–30 minutes, maintaining efficient technique throughout.
14. Complete 5 × 3 km freestyle, resting 90 seconds after every repetition. Increase your pace during the final kilometer of each repetition.
15. Swim 20 km continuously, lifting your head to sight every 10 strokes and concentrating on maintaining identical stroke rhythm from start to finish.
16. Complete 5 km aerobic, 5 km moderate, and 5 km race pace. Rest 2 minutes between segments before continuing.
17. Swim 25 km continuously, simulating race conditions by following your complete hydration, nutrition, and pacing plan exactly as planned for competition.
18. Complete the endurance ladder: 3 km, 5 km, 7 km, 5 km, 3 km. Rest 2 minutes between segments while maintaining race-level technique and consistent pacing throughout the session.
'''


def _infer_level(category: str) -> str | None:
    lower = category.lower()
    if "learn" in lower:
        return "learn"
    if "beginner" in lower:
        return "beginner"
    if "intermediate" in lower:
        return "intermediate"
    if "competitive" in lower or "specialists" in lower or "race" in lower:
        return "advanced"
    return None


def _infer_training_type(category: str) -> str:
    lower = category.lower()
    if "sprint" in lower or "50 m" in lower:
        return "speed"
    if "endurance" in lower or "distance" in lower or "open water" in lower or "marathon" in lower or "400" in lower or "800" in lower or "1500" in lower:
        return "endurance"
    if "learn" in lower or "beginner" in lower:
        return "balanced"
    return "technical"


def _infer_focus(category: str) -> str:
    lower = category.lower()
    if "freestyle" in lower:
        return "freestyle"
    if "backstroke" in lower:
        return "backstroke"
    if "breaststroke" in lower:
        return "breaststroke"
    if "butterfly" in lower:
        return "butterfly"
    if "individual medley" in lower or "im" in lower:
        return "individual medley"
    if "open water" in lower or "marathon" in lower:
        return "open water endurance"
    if "long distance" in lower or "endurance" in lower:
        return "distance swimming"
    if "learn" in lower:
        return "water confidence and stroke fundamentals"
    if "beginner" in lower:
        return "beginner swimming foundation"
    return "swimming"


def _parse_catalog(raw_text: str) -> List[Dict[str, Any]]:
    sessions: List[Dict[str, Any]] = []
    current_heading: str | None = None
    current_items: List[Dict[str, str]] = []
    current_name: str | None = None
    current_lines: List[str] = []

    def flush_item() -> None:
        nonlocal current_name, current_lines
        if current_name is None:
            return
        prescription = "\n".join(line.strip() for line in current_lines if line.strip()).strip()
        current_items.append({"name": current_name.strip(), "prescription": prescription or current_name.strip()})
        current_name = None
        current_lines = []

    def flush_session() -> None:
        nonlocal current_heading, current_items
        flush_item()
        if current_heading and current_items:
            exercises = [exercise(item["name"], item["prescription"]) for item in current_items]
            sessions.append(
                session(
                    name=current_heading,
                    category=current_heading,
                    training_type=_infer_training_type(current_heading),
                    exercises=exercises,
                    level=_infer_level(current_heading),
                    participants="alone",
                    focus=_infer_focus(current_heading),
                )
            )
        current_items = []

    heading_pattern = re.compile(r"^[A-Za-z].*(?:—|Swimming|Freestyle|Backstroke|Breaststroke|Butterfly|Individual Medley|Open Water|Intermediate Endurance).*$")
    item_pattern = re.compile(r"^(\d+)\.\s*(.*)$")

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        item_match = item_pattern.match(line)
        is_heading = bool(heading_pattern.match(line)) and not item_match and len(line) < 90
        if is_heading:
            flush_session()
            current_heading = line.replace("Swimming — ", "").strip()
            continue
        if item_match:
            flush_item()
            number, remainder = item_match.groups()
            current_name = remainder.strip() or f"Exercise {number}"
            current_lines = []
            # If the numbered line is itself the whole workout, keep it as the prescription too.
            if remainder.strip() and (remainder.lower().startswith(("swim", "complete", "perform", "divide", "alternate", "using", "place", "stand", "hold", "tread", "push"))):
                current_lines.append(remainder.strip())
            continue
        if current_name is not None:
            current_lines.append(line)

    flush_session()
    return sessions


SWIMMING_SESSIONS: List[Dict[str, Any]] = _parse_catalog(RAW_SWIMMING_CATALOG)

# Common aliases used by the Sportze.AI catalog manager in other sport modules.
WORKOUTS = SWIMMING_SESSIONS
SESSIONS = SWIMMING_SESSIONS
TRAINING_SESSIONS = SWIMMING_SESSIONS


def get_sessions() -> List[Dict[str, Any]]:
    """Return all codified swimming sessions."""
    return SWIMMING_SESSIONS


def get_workouts() -> List[Dict[str, Any]]:
    """Return all codified swimming workouts."""
    return SWIMMING_SESSIONS


def get_sessions_by_level(level: str) -> List[Dict[str, Any]]:
    """Return swimming sessions matching a level such as learn, beginner, or advanced."""
    normalized = level.lower().strip()
    return [item for item in SWIMMING_SESSIONS if str(item.get("level", "")).lower() == normalized]


def get_sessions_by_focus(focus: str) -> List[Dict[str, Any]]:
    """Return swimming sessions whose focus or category matches a keyword."""
    normalized = focus.lower().strip()
    return [
        item
        for item in SWIMMING_SESSIONS
        if normalized in str(item.get("focus", "")).lower()
        or normalized in str(item.get("category", "")).lower()
        or normalized in str(item.get("name", "")).lower()
    ]


__all__ = [
    "SPORT",
    "SPORT_NAME",
    "SWIMMING_SESSIONS",
    "WORKOUTS",
    "SESSIONS",
    "TRAINING_SESSIONS",
    "get_sessions",
    "get_workouts",
    "get_sessions_by_level",
    "get_sessions_by_focus",
]
