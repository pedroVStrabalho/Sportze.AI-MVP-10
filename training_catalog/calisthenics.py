# calisthenics.py

CALISTHENICS_CATEGORIES = [
    "Core",
    "Chest",
    "Back",
    "Legs",
    "Shoulders",
    "Arms",
    "Full Body",
]

CALISTHENICS_WORKOUTS = {
    "Core": [
        {
            "name": "Core Strength Foundation",
            "exercises": [
                "Plank – 4×60 sec",
                "Side Plank – 3×45 sec each side",
                "Hollow Hold – 4×30 sec",
                "Dead Bug – 3×20",
            ],
        },
        {
            "name": "Abdominal Volume",
            "exercises": [
                "Sit-Ups – 5×30",
                "Crunches – 5×40",
                "Leg Raises – 5×20",
                "Flutter Kicks – 4×50",
            ],
        },
        {
            "name": "Lower Abs Focus",
            "exercises": [
                "Leg Raises – 6×15",
                "Reverse Crunches – 5×20",
                "Knee Raises – 5×15",
                "Hollow Hold – 4×40 sec",
            ],
        },
        {
            "name": "Static Core Control",
            "exercises": [
                "Hollow Hold – 6×40 sec",
                "Plank – 5×90 sec",
                "Side Plank – 4×60 sec",
                "Superman Hold – 4×45 sec",
            ],
        },
        {
            "name": "Dynamic Core",
            "exercises": [
                "Mountain Climbers – 5×40",
                "Russian Twists – 5×30",
                "V-Ups – 5×20",
                "Toe Touches – 5×25",
            ],
        },
        {
            "name": "Hanging Core",
            "exercises": [
                "Hanging Knee Raises – 5×15",
                "Hanging Leg Raises – 5×12",
                "Toes-to-Bar – 4×10",
                "L-Sit – 5×20 sec",
            ],
        },
        {
            "name": "Core Endurance",
            "exercises": [
                "Plank – 10 min total",
                "Sit-Ups – 200",
                "Leg Raises – 100",
                "Russian Twists – 200",
            ],
        },
        {
            "name": "Gymnast Core",
            "exercises": [
                "Hollow Hold – 5×45 sec",
                "Arch Hold – 5×45 sec",
                "L-Sit – 5×20 sec",
                "V-Ups – 5×20",
            ],
        },
        {
            "name": "Rotational Core",
            "exercises": [
                "Russian Twists – 6×30",
                "Bicycle Crunches – 6×30",
                "Side Plank Rotations – 5×15",
                "Windshield Wipers – 4×12",
            ],
        },
        {
            "name": "Core Conditioning",
            "exercises": [
                "Sit-Ups – 150",
                "Crunches – 150",
                "Leg Raises – 100",
                "Plank – 5×60 sec",
            ],
        },
        {
            "name": "Advanced Core",
            "exercises": [
                "Dragon Flag Negatives – 5×8",
                "Hanging Leg Raises – 5×15",
                "L-Sit – 5×30 sec",
                "V-Ups – 5×25",
            ],
        },
        {
            "name": "Elite Core",
            "exercises": [
                "Dragon Flags – 6×8",
                "Toes-to-Bar – 6×15",
                "L-Sit – 6×30 sec",
                "Hollow Hold – 6×60 sec",
            ],
        },
    ],

    "Chest": [
        {
            "name": "Push-Up Foundation",
            "exercises": [
                "Push-Ups – 5×15",
                "Incline Push-Ups – 4×20",
                "Knee Push-Ups – 4×20",
                "Plank – 3×60 sec",
            ],
        },
        {
            "name": "Chest Volume",
            "exercises": ["Push-Ups – 10×20"],
        },
        {
            "name": "Wide Push-Up Session",
            "exercises": [
                "Wide Push-Ups – 6×20",
                "Standard Push-Ups – 4×20",
            ],
        },
        {
            "name": "Diamond Session",
            "exercises": [
                "Diamond Push-Ups – 6×12",
                "Push-Ups – 4×20",
            ],
        },
        {
            "name": "Decline Session",
            "exercises": [
                "Decline Push-Ups – 6×15",
                "Standard Push-Ups – 4×20",
            ],
        },
        {
            "name": "Tempo Session",
            "exercises": [
                "Slow Push-Ups – 6×10",
                "Wide Push-Ups – 4×15",
            ],
        },
        {
            "name": "Chest Endurance",
            "exercises": ["Push-Ups – 250 total"],
        },
        {
            "name": "Chest Power",
            "exercises": [
                "Explosive Push-Ups – 6×10",
                "Clap Push-Ups – 5×8",
            ],
        },
        {
            "name": "Strength Session",
            "exercises": [
                "Archer Push-Ups – 5×8",
                "Diamond Push-Ups – 5×10",
            ],
        },
        {
            "name": "Advanced Chest",
            "exercises": [
                "Pseudo Planche Push-Ups – 5×10",
                "Archer Push-Ups – 5×8",
            ],
        },
        {
            "name": "Gymnast Chest",
            "exercises": [
                "Ring Push-Ups – 6×12",
                "Ring Dips – 5×10",
            ],
        },
        {
            "name": "Elite Chest",
            "exercises": [
                "One-Arm Push-Up Progression – 6×5",
                "Pseudo Planche Push-Ups – 6×12",
            ],
        },
    ],

    "Back": [
        {
            "name": "Pull-Up Foundation",
            "exercises": [
                "Pull-Ups – 5×5",
                "Dead Hang – 4×30 sec",
                "Scapular Pull-Ups – 4×10",
            ],
        },
        {"name": "Pull-Up Volume", "exercises": ["Pull-Ups – 50 total"]},
        {
            "name": "Chin-Up Session",
            "exercises": [
                "Chin-Ups – 6×8",
                "Dead Hang – 4×30 sec",
            ],
        },
        {
            "name": "Mixed Pull Session",
            "exercises": [
                "Pull-Ups – 5×8",
                "Chin-Ups – 5×8",
            ],
        },
        {"name": "Endurance Pulling", "exercises": ["Pull-Ups – 100 total"]},
        {
            "name": "Wide Grip Session",
            "exercises": [
                "Wide Pull-Ups – 6×6",
                "Pull-Ups – 4×8",
            ],
        },
        {
            "name": "Explosive Pulling",
            "exercises": [
                "Chest-to-Bar Pull-Ups – 6×6",
                "Pull-Ups – 5×8",
            ],
        },
        {
            "name": "Archer Session",
            "exercises": [
                "Archer Pull-Ups – 5×5",
                "Pull-Ups – 5×8",
            ],
        },
        {"name": "Back Strength", "exercises": ["Pull-Ups – 10×10"]},
        {
            "name": "Muscle-Up Prep",
            "exercises": [
                "High Pull-Ups – 6×6",
                "Explosive Pull-Ups – 5×8",
            ],
        },
        {
            "name": "Advanced Pull",
            "exercises": [
                "Typewriter Pull-Ups – 5×5",
                "Archer Pull-Ups – 5×5",
            ],
        },
        {
            "name": "Elite Pull",
            "exercises": [
                "Muscle-Ups – 6×5",
                "Chest-to-Bar Pull-Ups – 6×8",
            ],
        },
    ],

    "Legs": [
        {
            "name": "Squat Foundation",
            "exercises": [
                "Bodyweight Squats – 5×25",
                "Lunges – 4×20",
                "Calf Raises – 5×30",
            ],
        },
        {"name": "Leg Volume", "exercises": ["Squats – 300 total"]},
        {
            "name": "Lunge Session",
            "exercises": [
                "Walking Lunges – 6×20",
                "Squats – 4×25",
            ],
        },
        {
            "name": "Single-Leg Control",
            "exercises": [
                "Bulgarian Split Squats – 5×12",
                "Step-Ups – 5×15",
            ],
        },
        {
            "name": "Explosive Legs",
            "exercises": [
                "Jump Squats – 6×15",
                "Broad Jumps – 5×10",
            ],
        },
        {
            "name": "Plyometric Session",
            "exercises": [
                "Box Jumps – 6×12",
                "Jump Lunges – 5×15",
            ],
        },
        {"name": "Endurance Legs", "exercises": ["Squats – 500 total"]},
        {
            "name": "Strength Legs",
            "exercises": ["Pistol Squat Progressions – 6×8"],
        },
        {
            "name": "Athletic Legs",
            "exercises": [
                "Sprint Intervals – 10×100m",
                "Jump Squats – 5×15",
            ],
        },
        {
            "name": "Advanced Legs",
            "exercises": [
                "Pistol Squats – 6×8",
                "Bulgarian Split Squats – 5×15",
            ],
        },
        {
            "name": "Elite Legs",
            "exercises": [
                "Pistol Squats – 8×10",
                "Jump Lunges – 6×20",
            ],
        },
        {
            "name": "Monster Leg Session",
            "exercises": [
                "Squats – 300",
                "Lunges – 200",
                "Calf Raises – 300",
            ],
        },
    ],

    "Shoulders": [
        {
            "name": "Pike Push-Up Foundation",
            "exercises": [
                "Pike Push-Ups – 5×10",
                "Shoulder Taps – 4×30",
            ],
        },
        {"name": "Shoulder Volume", "exercises": ["Pike Push-Ups – 10×12"]},
        {"name": "Elevated Pike Session", "exercises": ["Elevated Pike Push-Ups – 6×10"]},
        {"name": "Wall Handstand Holds", "exercises": ["Handstand Hold – 8×30 sec"]},
        {"name": "Shoulder Endurance", "exercises": ["Pike Push-Ups – 150 total"]},
        {"name": "Handstand Development", "exercises": ["Wall Handstand – 10 min total"]},
        {"name": "Handstand Push-Up Prep", "exercises": ["Negative Handstand Push-Ups – 6×5"]},
        {"name": "Explosive Shoulders", "exercises": ["Explosive Pike Push-Ups – 6×10"]},
        {"name": "Shoulder Strength", "exercises": ["Elevated Pike Push-Ups – 8×10"]},
        {"name": "Advanced Shoulders", "exercises": ["Handstand Push-Ups – 5×5"]},
        {"name": "Elite Shoulders", "exercises": ["Handstand Push-Ups – 8×6"]},
        {"name": "Gymnast Shoulders", "exercises": ["Handstand Walk Practice – 30 min"]},
    ],

    "Arms": [
        {
            "name": "Dips Foundation",
            "exercises": [
                "Bench Dips – 5×15",
                "Diamond Push-Ups – 4×12",
            ],
        },
        {"name": "Triceps Volume", "exercises": ["Bench Dips – 200 total"]},
        {"name": "Dip Session", "exercises": ["Dips – 6×10"]},
        {"name": "Biceps Focus", "exercises": ["Chin-Ups – 6×10"]},
        {
            "name": "Mixed Arms",
            "exercises": [
                "Dips – 5×12",
                "Chin-Ups – 5×10",
            ],
        },
        {
            "name": "Arm Endurance",
            "exercises": [
                "Dips – 100",
                "Chin-Ups – 50",
            ],
        },
        {"name": "Strength Arms", "exercises": ["Weighted Dips – 5×8"]},
        {"name": "Explosive Arms", "exercises": ["Explosive Dips – 6×8"]},
        {"name": "Advanced Arms", "exercises": ["Korean Dips – 5×8"]},
        {"name": "Ring Arms", "exercises": ["Ring Dips – 6×10"]},
        {"name": "Elite Arms", "exercises": ["Weighted Dips – 8×8"]},
        {
            "name": "Monster Arms",
            "exercises": [
                "Dips – 200",
                "Chin-Ups – 100",
            ],
        },
    ],

    "Full Body": [
        {
            "name": "Beginner Full Body",
            "exercises": [
                "Push-Ups – 20",
                "Pull-Ups – 5",
                "Squats – 30",
                "Plank – 60 sec",
                "Complete 5 rounds",
            ],
        },
        {
            "name": "Full Body Volume",
            "exercises": [
                "Complete 10 rounds",
                "Push-Ups – 15",
                "Pull-Ups – 5",
                "Squats – 20",
            ],
        },
        {
            "name": "Athletic Circuit",
            "exercises": [
                "Complete 8 rounds",
                "Pull-Ups – 10",
                "Push-Ups – 20",
                "Squats – 30",
            ],
        },
        {
            "name": "Endurance Circuit",
            "exercises": ["60 minutes continuous work"],
        },
        {
            "name": "Strength Circuit",
            "exercises": [
                "Pull-Ups – 10×10",
                "Push-Ups – 10×20",
                "Squats – 10×30",
            ],
        },
        {
            "name": "Explosive Circuit",
            "exercises": [
                "Clap Push-Ups – 5×10",
                "Jump Squats – 5×15",
                "Burpees – 5×20",
            ],
        },
        {
            "name": "Military Session",
            "exercises": [
                "Push-Ups – 300",
                "Squats – 300",
                "Sit-Ups – 300",
            ],
        },
        {
            "name": "Calisthenics Athlete",
            "exercises": [
                "Muscle-Ups – 5×5",
                "Dips – 5×15",
                "Pull-Ups – 5×15",
            ],
        },
        {
            "name": "Conditioning Session",
            "exercises": ["Burpees – 200"],
        },
        {
            "name": "Advanced Full Body",
            "exercises": [
                "Pull-Ups – 100",
                "Push-Ups – 300",
                "Squats – 300",
            ],
        },
        {
            "name": "Elite Conditioning",
            "exercises": [
                "Pull-Ups – 100",
                "Push-Ups – 200",
                "Squats – 300",
            ],
        },
        {
            "name": "Ultimate Full Body Challenge",
            "exercises": [
                "Pull-Ups – 100",
                "Dips – 200",
                "Push-Ups – 300",
                "Squats – 400",
                "Sit-Ups – 500",
            ],
        },
    ],
}
