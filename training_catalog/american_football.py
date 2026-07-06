"""American_football.py

American Football training catalog for Sportze.AI.
Generated from the provided American Football exercises document.

Structure:
- AMERICAN_FOOTBALL_CATALOG["training_alone"]["positions"]
- AMERICAN_FOOTBALL_CATALOG["training_alone"]["learn_how_to_play"]
- AMERICAN_FOOTBALL_CATALOG["training_with_2_or_more"]["positions"]
- AMERICAN_FOOTBALL_CATALOG["training_with_2_or_more"]["learn_how_to_play"]
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

AMERICAN_FOOTBALL_CATALOG: Dict[str, Any] = {'sport': 'American Football',
 'training_alone': {'positions': {'QB': {'position': 'Quarterback',
                                         'code': 'QB',
                                         'exercises': [{'name': '10m Target Throws',
                                                        'instructions': 'Throw 20 passes at a wall/net target from 10 '
                                                                        'meters.'},
                                                       {'name': 'Dropback Pass Drill',
                                                        'instructions': 'Take a 3-step drop, set feet, throw to '
                                                                        'target. Do 15 reps.'},
                                                       {'name': 'Rollout Throw',
                                                        'instructions': 'Run 8 meters right/left, then throw while '
                                                                        'moving. Do 10 each side.'},
                                                       {'name': 'Quick Release Drill',
                                                        'instructions': 'Catch snap/ball, throw in under 2 seconds. Do '
                                                                        '20 reps.'},
                                                       {'name': 'Pocket Movement Drill',
                                                        'instructions': 'Shuffle inside a 3x3m box for 5 seconds, then '
                                                                        'throw. Do 12 reps.'},
                                                       {'name': 'Deep Ball Throws',
                                                        'instructions': 'Throw 20–30m passes to a target or partner. '
                                                                        'Do 15 reps.'}]},
                                  'RB/HB': {'position': 'Running Back',
                                            'code': 'RB/HB',
                                            'exercises': [{'name': '40m Ball Sprint',
                                                           'instructions': 'Sprint 40 meters holding the ball tight. '
                                                                           'Do 6 reps.'},
                                                          {'name': 'Cone Cut Run',
                                                           'instructions': 'Run through 5 zigzag cones with the ball. '
                                                                           'Do 8 reps.'},
                                                          {'name': 'Tuck-and-Go Drill',
                                                           'instructions': 'Pick ball from ground, tuck, sprint 20m. '
                                                                           'Do 10 reps.'},
                                                          {'name': 'Spin Move Drill',
                                                           'instructions': 'Sprint 10m, spin around cone, sprint 10m. '
                                                                           'Do 8 reps.'},
                                                          {'name': 'Jump Cut Drill',
                                                           'instructions': 'Sprint forward, jump-cut left/right, '
                                                                           'accelerate 10m. Do 10 reps.'},
                                                          {'name': 'Ball Security Hits',
                                                           'instructions': 'Run 20m while partner taps ball/arms with '
                                                                           'pad. Do 8 reps.'}]},
                                  'FB': {'position': 'Fullback',
                                         'code': 'FB',
                                         'exercises': [{'name': 'Lead Block Drive',
                                                        'instructions': 'Drive into pad/player for 5 meters. Do 8 '
                                                                        'reps.'},
                                                       {'name': 'Short Yardage Carry',
                                                        'instructions': 'Run 10 meters through contact with ball. Do '
                                                                        '10 reps.'},
                                                       {'name': 'Pass Protection Step',
                                                        'instructions': 'Step forward, strike pad, hold block 3 '
                                                                        'seconds. Do 10 reps.'},
                                                       {'name': 'Flat Route Catch',
                                                        'instructions': 'Run 5m sideways, catch pass, turn upfield. Do '
                                                                        '12 reps.'},
                                                       {'name': 'Low Sled/Pad Drive',
                                                        'instructions': 'Stay low and push pad 5 meters. Do 8 reps.'},
                                                       {'name': 'Goal-Line Burst',
                                                        'instructions': 'Start low, explode forward 5 meters with '
                                                                        'ball. Do 12 reps.'}]},
                                  'WR': {'position': 'Wide Receiver',
                                         'code': 'WR',
                                         'exercises': [{'name': 'Slant Route',
                                                        'instructions': 'Sprint 5m, cut inside, catch pass. Do 12 '
                                                                        'reps.'},
                                                       {'name': 'Out Route',
                                                        'instructions': 'Sprint 10m, cut 90° outside, catch pass. Do '
                                                                        '12 reps.'},
                                                       {'name': 'Deep Route Sprint',
                                                        'instructions': 'Sprint 30m straight and catch over shoulder. '
                                                                        'Do 10 reps.'},
                                                       {'name': 'Comeback Route',
                                                        'instructions': 'Sprint 15m, stop, turn back, catch. Do 10 '
                                                                        'reps.'},
                                                       {'name': 'High-Point Catch',
                                                        'instructions': 'Jump and catch ball at highest point. Do 15 '
                                                                        'reps.'},
                                                       {'name': 'Toe-Tap Catch',
                                                        'instructions': 'Catch near sideline and land both feet '
                                                                        'inbounds. Do 10 reps.'}]},
                                  'TE': {'position': 'Tight End',
                                         'code': 'TE',
                                         'exercises': [{'name': 'Block-and-Release',
                                                        'instructions': 'Block pad 2 seconds, then run 10m route. Do '
                                                                        '10 reps.'},
                                                       {'name': 'Short Hook Route',
                                                        'instructions': 'Run 8m, stop, turn, catch. Do 12 reps.'},
                                                       {'name': 'Seam Route Catch',
                                                        'instructions': 'Sprint 20m straight and catch pass. Do 10 '
                                                                        'reps.'},
                                                       {'name': 'Drive Block Drill',
                                                        'instructions': 'Push pad/player backward 5 meters. Do 8 '
                                                                        'reps.'},
                                                       {'name': 'Contact Catch',
                                                        'instructions': 'Catch pass while partner lightly bumps you. '
                                                                        'Do 12 reps.'},
                                                       {'name': 'Red Zone Turn Catch',
                                                        'instructions': 'Run 5m, turn fast, catch chest-high pass. Do '
                                                                        '15 reps.'}]},
                                  'LT/RT': {'position': 'Offensive Tackle',
                                            'code': 'LT/RT',
                                            'exercises': [{'name': 'Kick Slide Drill',
                                                           'instructions': 'Kick-slide backward 5 meters. Do 10 each '
                                                                           'side.'},
                                                          {'name': 'Pass Block Hold',
                                                           'instructions': 'Strike pad and hold block for 4 seconds. '
                                                                           'Do 10 reps.'},
                                                          {'name': 'Edge Rush Mirror',
                                                           'instructions': 'Mirror partner moving left/right for 6 '
                                                                           'seconds. Do 8 reps.'},
                                                          {'name': 'Drive Block',
                                                           'instructions': 'Push pad/player 5 meters forward. Do 8 '
                                                                           'reps.'},
                                                          {'name': 'Low Stance Explode',
                                                           'instructions': 'Start low, explode into pad. Do 12 reps.'},
                                                          {'name': 'Lateral Shuffle Block',
                                                           'instructions': 'Shuffle sideways 5m while staying square. '
                                                                           'Do 10 reps.'}]},
                                  'LG/RG': {'position': 'Offensive Guard',
                                            'code': 'LG/RG',
                                            'exercises': [{'name': 'Short Drive Block',
                                                           'instructions': 'Explode into pad and drive 4 meters. Do 10 '
                                                                           'reps.'},
                                                          {'name': 'Pulling Guard Drill',
                                                           'instructions': 'Start inside, pull outside around cone, '
                                                                           'hit pad. Do 8 reps.'},
                                                          {'name': 'Double-Team Drive',
                                                           'instructions': 'With partner, drive pad/player 5 meters. '
                                                                           'Do 8 reps.'},
                                                          {'name': 'Pass Set Punch',
                                                           'instructions': 'Step back, punch pad with both hands. Do '
                                                                           '12 reps.'},
                                                          {'name': 'Low Bear Crawl Burst',
                                                           'instructions': 'Bear crawl 5m, pop up, hit pad. Do 8 '
                                                                           'reps.'},
                                                          {'name': 'Gap Step Drill',
                                                           'instructions': 'Step left/right into blocking angle and '
                                                                           'strike pad. Do 10 each side.'}]},
                                  'C': {'position': 'Center',
                                        'code': 'C',
                                        'exercises': [{'name': 'Snap Accuracy Drill',
                                                       'instructions': 'Snap ball to target/partner 20 times.'},
                                                      {'name': 'Snap-and-Block',
                                                       'instructions': 'Snap, then immediately strike pad. Do 15 '
                                                                       'reps.'},
                                                      {'name': 'Shotgun Snap Drill',
                                                       'instructions': 'Long snap to QB target 20 times.'},
                                                      {'name': 'A-Gap Drive Block',
                                                       'instructions': 'Drive straight forward 4 meters. Do 10 reps.'},
                                                      {'name': 'Lateral Reach Block',
                                                       'instructions': 'Step sideways and block pad at angle. Do 10 '
                                                                       'each side.'},
                                                      {'name': 'Anchor Drill',
                                                       'instructions': 'Strike pad and resist push for 5 seconds. Do 8 '
                                                                       'reps.'}]},
                                  'DE': {'position': 'Defensive End',
                                         'code': 'DE',
                                         'exercises': [{'name': 'Edge Rush Sprint',
                                                        'instructions': 'Sprint around cone to QB target. Do 10 reps.'},
                                                       {'name': 'Rip Move Drill',
                                                        'instructions': 'Step outside and rip arm under pad. Do 12 '
                                                                        'reps.'},
                                                       {'name': 'Swim Move Drill',
                                                        'instructions': 'Attack pad and swim arm over. Do 12 reps.'},
                                                       {'name': 'Contain Drill',
                                                        'instructions': 'Shuffle outside, keep runner inside, tag. Do '
                                                                        '8 reps.'},
                                                       {'name': 'Get-Off Drill',
                                                        'instructions': 'Explode forward on clap/whistle for 5m. Do 12 '
                                                                        'reps.'},
                                                       {'name': 'Sack Finish',
                                                        'instructions': 'Rush 10m, wrap tackle dummy safely. Do 8 '
                                                                        'reps.'}]},
                                  'DT/NT': {'position': 'Defensive Tackle',
                                            'code': 'DT/NT',
                                            'exercises': [{'name': 'Low Explosion Drill',
                                                           'instructions': 'Start in stance, explode into pad. Do 12 '
                                                                           'reps.'},
                                                          {'name': 'Bull Rush',
                                                           'instructions': 'Drive pad/player backward 5 meters. Do 8 '
                                                                           'reps.'},
                                                          {'name': 'Gap Control Drill',
                                                           'instructions': 'Step into left/right gap and hold '
                                                                           'position. Do 10 each side.'},
                                                          {'name': 'Shed Block Drill',
                                                           'instructions': 'Strike pad, push away, move to ball. Do 10 '
                                                                           'reps.'},
                                                          {'name': 'Short Shuttle Burst',
                                                           'instructions': 'Sprint 5m, shuffle 5m, sprint 5m. Do 6 '
                                                                           'reps.'},
                                                          {'name': 'Tackle Dummy Drive',
                                                           'instructions': 'Hit dummy low and drive 3 meters. Do 8 '
                                                                           'reps.'}]},
                                  'MLB/OLB': {'position': 'Linebacker',
                                              'code': 'MLB/OLB',
                                              'exercises': [{'name': 'Read-and-React',
                                                             'instructions': 'Partner points left/right, sprint 10m '
                                                                             'that way. Do 12 reps.'},
                                                            {'name': 'Backpedal Break',
                                                             'instructions': 'Backpedal 8m, break forward 10m. Do 10 '
                                                                             'reps.'},
                                                            {'name': 'Angle Tackle Drill',
                                                             'instructions': 'Run diagonally and tag/tackle dummy. Do '
                                                                             '8 reps.'},
                                                            {'name': 'Blitz Gap Sprint',
                                                             'instructions': 'Start 5m back, sprint through gap '
                                                                             'between cones. Do 10 reps.'},
                                                            {'name': 'Zone Drop Drill',
                                                             'instructions': 'Drop back 10m, turn, catch/intercept '
                                                                             'ball. Do 10 reps.'},
                                                            {'name': 'Block Shed Drill',
                                                             'instructions': 'Strike pad, shed, sprint to cone. Do 10 '
                                                                             'reps.'}]},
                                  'CB': {'position': 'Cornerback',
                                         'code': 'CB',
                                         'exercises': [{'name': 'Press Footwork Drill',
                                                        'instructions': 'Stay low and mirror receiver for 5 seconds. '
                                                                        'Do 8 reps.'},
                                                       {'name': 'Backpedal Turn Sprint',
                                                        'instructions': 'Backpedal 10m, turn hips, sprint 20m. Do 10 '
                                                                        'reps.'},
                                                       {'name': 'One-on-One Coverage',
                                                        'instructions': 'Cover receiver on a 15–25m route. Do 10 '
                                                                        'reps.'},
                                                       {'name': 'Break on Ball',
                                                        'instructions': 'Backpedal, react to thrown ball, '
                                                                        'intercept/catch. Do 12 reps.'},
                                                       {'name': 'Sideline Coverage Drill',
                                                        'instructions': 'Force receiver toward sideline for 15m. Do 8 '
                                                                        'reps.'},
                                                       {'name': 'Jump Ball Defense',
                                                        'instructions': 'Track high pass and knock it away/catch it. '
                                                                        'Do 10 reps.'}]},
                                  'FS/SS': {'position': 'Safety',
                                            'code': 'FS/SS',
                                            'exercises': [{'name': 'Deep Backpedal Drill',
                                                           'instructions': 'Backpedal 15m, turn, sprint 20m. Do 8 '
                                                                           'reps.'},
                                                          {'name': 'Angle Pursuit Drill',
                                                           'instructions': 'Sprint diagonally to cut off runner. Do 10 '
                                                                           'reps.'},
                                                          {'name': 'Open Field Tag/Tackle',
                                                           'instructions': 'Track ball carrier and tag/tackle safely. '
                                                                           'Do 8 reps.'},
                                                          {'name': 'Interception Drill',
                                                           'instructions': 'Start deep, react to pass, catch ball. Do '
                                                                           '12 reps.'},
                                                          {'name': 'Run Support Drill',
                                                           'instructions': 'Start 10m back, sprint forward, hit pad. '
                                                                           'Do 10 reps.'},
                                                          {'name': 'Two-Receiver Read',
                                                           'instructions': 'Watch two routes, break toward thrown '
                                                                           'ball. Do 10 reps.'}]},
                                  'K': {'position': 'Kicker',
                                        'code': 'K',
                                        'exercises': [{'name': 'Extra Point Kicks',
                                                       'instructions': 'Kick 20 short field goals.'},
                                                      {'name': '30m Field Goal Kicks',
                                                       'instructions': 'Kick 15 field goals from 30m.'},
                                                      {'name': 'Kickoff Distance Drill',
                                                       'instructions': 'Kick ball as far as possible 10 times.'},
                                                      {'name': 'Accuracy Gate Drill',
                                                       'instructions': 'Kick through two cones/posts. Do 20 reps.'},
                                                      {'name': 'One-Step Kicks',
                                                       'instructions': 'Take one step and kick for clean contact. Do '
                                                                       '15 reps.'},
                                                      {'name': 'Pressure Kick Drill',
                                                       'instructions': 'Sprint 10m, reset, kick immediately. Do 10 '
                                                                       'reps.'}]},
                                  'P': {'position': 'Punter',
                                        'code': 'P',
                                        'exercises': [{'name': 'Drop Control Drill',
                                                       'instructions': 'Drop ball from hand to foot cleanly 20 times.'},
                                                      {'name': 'Standing Punt',
                                                       'instructions': 'Punt without steps for clean contact. Do 15 '
                                                                       'reps.'},
                                                      {'name': 'Two-Step Punt',
                                                       'instructions': 'Take two steps and punt for distance. Do 15 '
                                                                       'reps.'},
                                                      {'name': 'Directional Punt',
                                                       'instructions': 'Punt left/right toward target zone. Do 10 each '
                                                                       'side.'},
                                                      {'name': 'Hang Time Punt',
                                                       'instructions': 'Punt as high as possible, track time in air. '
                                                                       'Do 10 reps.'},
                                                      {'name': 'Pressure Punt',
                                                       'instructions': 'Catch snap/pass, punt within 2 seconds. Do 12 '
                                                                       'reps.'}]},
                                  'LS': {'position': 'Long Snapper',
                                         'code': 'LS',
                                         'exercises': [{'name': 'Short Snap Accuracy',
                                                        'instructions': 'Snap to holder target 20 times.'},
                                                       {'name': 'Long Snap Accuracy',
                                                        'instructions': 'Snap 12–14 meters to punter target 20 times.'},
                                                       {'name': 'Snap-and-Sprint',
                                                        'instructions': 'Snap, then sprint 20 meters. Do 10 reps.'},
                                                       {'name': 'Snap-and-Block',
                                                        'instructions': 'Snap, then block pad for 3 seconds. Do 12 '
                                                                        'reps.'},
                                                       {'name': 'Low Stance Hold',
                                                        'instructions': 'Hold snapping stance for 20 seconds. Do 5 '
                                                                        'sets.'},
                                                       {'name': 'Moving Target Snap',
                                                        'instructions': 'Snap to partner moving slightly left/right. '
                                                                        'Do 15 reps.'}]},
                                  'KR/PR': {'position': 'Returner',
                                            'code': 'KR/PR',
                                            'exercises': [{'name': 'Catch-and-Sprint',
                                                           'instructions': 'Catch kick/punt and sprint 30 meters. Do '
                                                                           '10 reps.'},
                                                          {'name': 'Zigzag Return Drill',
                                                           'instructions': 'Catch ball, run through 6 zigzag cones. Do '
                                                                           '8 reps.'},
                                                          {'name': 'First-Cut Drill',
                                                           'instructions': 'Catch ball, sprint 5m, cut left/right, '
                                                                           'sprint 20m. Do 10 reps.'},
                                                          {'name': 'High Ball Catch',
                                                           'instructions': 'Catch 15 high punts/kicks cleanly.'},
                                                          {'name': 'Sideline Return Drill',
                                                           'instructions': 'Run 30m along sideline while staying '
                                                                           'inbounds. Do 8 reps.'},
                                                          {'name': 'Ball Security Return',
                                                           'instructions': 'Run 25m while partner tries to tap ball '
                                                                           'loose. Do 8 reps.'}]}},
                    'learn_how_to_play': [{'number': 1,
                                           'name': 'Wall Pass and Catch',
                                           'instructions': 'Stand 8 meters from a wall. Throw the football against the '
                                                           'wall. Catch the rebound cleanly. Complete 100 catches.'},
                                          {'number': 2,
                                           'name': 'Ball Carry Sprint',
                                           'instructions': 'Hold the football securely against your ribs. Sprint 30 '
                                                           'meters. Complete 10 repetitions.'},
                                          {'number': 3,
                                           'name': 'Zigzag Cone Run',
                                           'instructions': 'Set up 5 cones 3 meters apart. Run through them while '
                                                           'carrying the football. Complete 10 repetitions.'},
                                          {'number': 4,
                                           'name': 'Target Throw Drill',
                                           'instructions': 'Place a target 10 meters away. Throw 50 passes attempting '
                                                           'to hit the target.'},
                                          {'number': 5,
                                           'name': 'Backpedal and Sprint',
                                           'instructions': 'Backpedal 10 meters. Turn and sprint forward 20 meters. '
                                                           'Complete 10 repetitions.'},
                                          {'number': 6,
                                           'name': 'Route Running Practice',
                                           'instructions': 'Run a slant route for 10 meters. Run an out route for 10 '
                                                           'meters. Run a comeback route for 10 meters. Complete each '
                                                           'route 10 times.'},
                                          {'number': 7,
                                           'name': 'Ball Pickup Drill',
                                           'instructions': 'Place the football on the ground. Pick it up, secure it, '
                                                           'and sprint 20 meters. Complete 15 repetitions.'},
                                          {'number': 8,
                                           'name': 'Shuttle Run',
                                           'instructions': 'Sprint 5 meters right. Sprint 10 meters left. Sprint 5 '
                                                           'meters back to the center. Complete 10 repetitions.'},
                                          {'number': 9,
                                           'name': 'High Ball Catch',
                                           'instructions': 'Toss the football high into the air. Catch it at chest '
                                                           'height. Complete 40 catches.'},
                                          {'number': 10,
                                           'name': 'Football Circuit',
                                           'instructions': 'Sprint 20 meters. Perform 5 push-ups. Pick up the '
                                                           'football. Sprint another 20 meters. Complete 8 rounds.'}]},
 'training_with_2_or_more': {'positions': {'QB': {'position': 'Quarterback',
                                                  'code': 'QB',
                                                  'exercises': [{'name': 'Receiver Route Throws',
                                                                 'instructions': 'Throw 20 passes to a receiver '
                                                                                 'running different routes.'},
                                                                {'name': 'Progression Read Drill',
                                                                 'instructions': 'Two receivers run routes. Read '
                                                                                 'Receiver 1 first, then Receiver 2, '
                                                                                 'and throw to the open player. Do 15 '
                                                                                 'reps.'},
                                                                {'name': 'Pressure Escape Drill',
                                                                 'instructions': 'A defender rushes at 50% speed. Move '
                                                                                 'in the pocket and complete a pass. '
                                                                                 'Do 12 reps.'},
                                                                {'name': 'Rollout Pass Drill',
                                                                 'instructions': 'Sprint 8 meters left or right and '
                                                                                 'throw to a moving receiver. Do 10 '
                                                                                 'reps each side.'},
                                                                {'name': 'Red Zone Passing Drill',
                                                                 'instructions': 'Complete 15 passes into a 10-meter '
                                                                                 'end zone area.'},
                                                                {'name': 'Two-Minute Offense Drill',
                                                                 'instructions': 'Run 10 consecutive plays with '
                                                                                 'different receivers and no '
                                                                                 'breaks.'}]},
                                           'RB/HB': {'position': 'Running Back',
                                                     'code': 'RB/HB',
                                                     'exercises': [{'name': 'Handoff and Burst',
                                                                    'instructions': 'Receive handoff from QB and '
                                                                                    'sprint 20 meters. Do 12 reps.'},
                                                                   {'name': 'Gap Run Drill',
                                                                    'instructions': 'Run through a gap created by '
                                                                                    'blockers and finish with a '
                                                                                    '15-meter sprint. Do 10 reps.'},
                                                                   {'name': 'Outside Sweep Drill',
                                                                    'instructions': 'Run around blockers and sprint 25 '
                                                                                    'meters. Do 8 reps.'},
                                                                   {'name': 'Pass Catch Drill',
                                                                    'instructions': 'Catch short passes from QB and '
                                                                                    'run 15 meters after the catch. Do '
                                                                                    '15 reps.'},
                                                                   {'name': 'Defender Avoidance Drill',
                                                                    'instructions': 'One defender attempts a tag while '
                                                                                    'you run 20 meters. Do 10 reps.'},
                                                                   {'name': 'Goal Line Run',
                                                                    'instructions': 'Start 3 meters from defenders and '
                                                                                    'push through to score. Do 10 '
                                                                                    'reps.'}]},
                                           'FB': {'position': 'Fullback',
                                                  'code': 'FB',
                                                  'exercises': [{'name': 'Lead Block Drill',
                                                                 'instructions': 'Lead a running back through a gap '
                                                                                 'and block a defender. Do 12 reps.'},
                                                                {'name': 'Short Yardage Carry',
                                                                 'instructions': 'Receive handoff and gain 5 meters '
                                                                                 'against resistance. Do 10 reps.'},
                                                                {'name': 'Pass Protection Drill',
                                                                 'instructions': 'Stop a defender from reaching the QB '
                                                                                 'for 4 seconds. Do 10 reps.'},
                                                                {'name': 'Flat Route Catch',
                                                                 'instructions': 'Run into the flat, catch pass, gain '
                                                                                 '10 meters. Do 12 reps.'},
                                                                {'name': 'Double-Team Block',
                                                                 'instructions': 'Block with an offensive lineman and '
                                                                                 'drive defender back 5 meters. Do 8 '
                                                                                 'reps.'},
                                                                {'name': 'Goal Line Block',
                                                                 'instructions': 'Create a running lane for a teammate '
                                                                                 'near the goal line. Do 10 reps.'}]},
                                           'WR': {'position': 'Wide Receiver',
                                                  'code': 'WR',
                                                  'exercises': [{'name': 'Slant Route Catch',
                                                                 'instructions': 'Run slant route and catch pass. Do '
                                                                                 '15 reps.'},
                                                                {'name': 'Deep Ball Catch',
                                                                 'instructions': 'Sprint 30 meters and catch '
                                                                                 'over-the-shoulder throw. Do 12 '
                                                                                 'reps.'},
                                                                {'name': 'One-on-One Route',
                                                                 'instructions': 'Beat a cornerback and catch pass. Do '
                                                                                 '12 reps.'},
                                                                {'name': 'Sideline Catch',
                                                                 'instructions': 'Catch pass near boundary and keep '
                                                                                 'both feet in. Do 10 reps.'},
                                                                {'name': 'Jump Ball Drill',
                                                                 'instructions': 'Compete with defender for high pass. '
                                                                                 'Do 12 reps.'},
                                                                {'name': 'Yards After Catch',
                                                                 'instructions': 'Catch pass and evade one defender '
                                                                                 'for 15 meters. Do 10 reps.'}]},
                                           'TE': {'position': 'Tight End',
                                                  'code': 'TE',
                                                  'exercises': [{'name': 'Block Then Release',
                                                                 'instructions': 'Block defender for 2 seconds, run '
                                                                                 'route, catch pass. Do 12 reps.'},
                                                                {'name': 'Seam Route Catch',
                                                                 'instructions': 'Run 20 meters straight and catch '
                                                                                 'pass. Do 12 reps.'},
                                                                {'name': 'Red Zone Catch',
                                                                 'instructions': 'Catch contested pass in end zone. Do '
                                                                                 '10 reps.'},
                                                                {'name': 'Edge Blocking Drill',
                                                                 'instructions': 'Seal defender outside for running '
                                                                                 'play. Do 10 reps.'},
                                                                {'name': 'Middle Traffic Catch',
                                                                 'instructions': 'Catch pass while receiving light '
                                                                                 'contact from defenders. Do 12 reps.'},
                                                                {'name': 'Play Action Release',
                                                                 'instructions': 'Fake block, release into route, '
                                                                                 'catch pass. Do 12 reps.'}]},
                                           'LT/RT': {'position': 'Offensive Tackle',
                                                     'code': 'LT/RT',
                                                     'exercises': [{'name': 'Pass Protection Rep',
                                                                    'instructions': 'Block edge rusher for 5 seconds. '
                                                                                    'Do 12 reps.'},
                                                                   {'name': 'Run Block Drive',
                                                                    'instructions': 'Drive defender back 5 meters. Do '
                                                                                    '10 reps.'},
                                                                   {'name': 'Mirror Drill',
                                                                    'instructions': 'Stay in front of rushing defender '
                                                                                    'for 6 seconds. Do 10 reps.'},
                                                                   {'name': 'Reach Block Drill',
                                                                    'instructions': 'Move laterally and seal defender. '
                                                                                    'Do 10 reps.'},
                                                                   {'name': 'Double-Team Block',
                                                                    'instructions': 'Work with guard to move defender. '
                                                                                    'Do 8 reps.'},
                                                                   {'name': 'Goal Line Protection',
                                                                    'instructions': 'Hold defender out of backfield '
                                                                                    'for 5 seconds. Do 10 reps.'}]},
                                           'LG/RG': {'position': 'Offensive Guard',
                                                     'code': 'LG/RG',
                                                     'exercises': [{'name': 'Pulling Block Drill',
                                                                    'instructions': 'Pull around tackle and block '
                                                                                    'defender. Do 10 reps.'},
                                                                   {'name': 'Drive Block Drill',
                                                                    'instructions': 'Push defender backward 5 meters. '
                                                                                    'Do 12 reps.'},
                                                                   {'name': 'Pass Protection Rep',
                                                                    'instructions': 'Prevent defender from reaching '
                                                                                    'QB. Do 10 reps.'},
                                                                   {'name': 'Combo Block Drill',
                                                                    'instructions': 'Double-team defender with '
                                                                                    'teammate. Do 10 reps.'},
                                                                   {'name': 'Trap Block Drill',
                                                                    'instructions': 'Pull across formation and strike '
                                                                                    'defender. Do 8 reps.'},
                                                                   {'name': 'Goal Line Drive',
                                                                    'instructions': 'Create movement against defender '
                                                                                    'for 3 seconds. Do 10 reps.'}]},
                                           'C': {'position': 'Center',
                                                 'code': 'C',
                                                 'exercises': [{'name': 'Snap and Block',
                                                                'instructions': 'Snap to QB and immediately block '
                                                                                'defender. Do 20 reps.'},
                                                               {'name': 'Shotgun Snap Drill',
                                                                'instructions': 'Deliver accurate shotgun snaps. Do 25 '
                                                                                'reps.'},
                                                               {'name': 'Reach Block Drill',
                                                                'instructions': 'Snap and block defender at an angle. '
                                                                                'Do 10 reps.'},
                                                               {'name': 'Double-Team Drill',
                                                                'instructions': 'Work with guard to move defender. Do '
                                                                                '10 reps.'},
                                                               {'name': 'Pass Protection Drill',
                                                                'instructions': 'Hold interior defender for 5 seconds. '
                                                                                'Do 10 reps.'},
                                                               {'name': 'Goal Line Snap',
                                                                'instructions': 'Snap and block immediately in '
                                                                                'short-yardage situations. Do 12 '
                                                                                'reps.'}]},
                                           'DE': {'position': 'Defensive End',
                                                  'code': 'DE',
                                                  'exercises': [{'name': 'Edge Rush Drill',
                                                                 'instructions': 'Beat tackle and touch QB. Do 12 '
                                                                                 'reps.'},
                                                                {'name': 'Contain Drill',
                                                                 'instructions': 'Keep runner inside and prevent '
                                                                                 'outside run. Do 10 reps.'},
                                                                {'name': 'Rip Move Drill',
                                                                 'instructions': 'Use rip move against blocker and '
                                                                                 'reach QB. Do 12 reps.'},
                                                                {'name': 'Swim Move Drill',
                                                                 'instructions': 'Use swim move to beat blocker. Do 12 '
                                                                                 'reps.'},
                                                                {'name': 'Run Stop Drill',
                                                                 'instructions': 'Shed blocker and tackle runner. Do '
                                                                                 '10 reps.'},
                                                                {'name': 'Strip Sack Drill',
                                                                 'instructions': 'Reach QB and attempt to knock ball '
                                                                                 'loose. Do 10 reps.'}]},
                                           'DT/NT': {'position': 'Defensive Tackle',
                                                     'code': 'DT/NT',
                                                     'exercises': [{'name': 'Bull Rush Drill',
                                                                    'instructions': 'Drive offensive lineman backward. '
                                                                                    'Do 12 reps.'},
                                                                   {'name': 'Gap Penetration Drill',
                                                                    'instructions': 'Shoot through assigned gap and '
                                                                                    'reach runner. Do 10 reps.'},
                                                                   {'name': 'Double-Team Resistance',
                                                                    'instructions': 'Hold position against two '
                                                                                    'blockers for 4 seconds. Do 8 '
                                                                                    'reps.'},
                                                                   {'name': 'Shed and Tackle',
                                                                    'instructions': 'Escape blocker and tackle runner. '
                                                                                    'Do 10 reps.'},
                                                                   {'name': 'Goal Line Defense',
                                                                    'instructions': 'Prevent runner from crossing '
                                                                                    'line. Do 10 reps.'},
                                                                   {'name': 'Interior Pass Rush',
                                                                    'instructions': 'Collapse pocket and reach QB. Do '
                                                                                    '12 reps.'}]},
                                           'MLB/OLB': {'position': 'Linebacker',
                                                       'code': 'MLB/OLB',
                                                       'exercises': [{'name': 'Read and React',
                                                                      'instructions': 'Read coach signal and attack '
                                                                                      'run/pass assignment. Do 12 '
                                                                                      'reps.'},
                                                                     {'name': 'Blitz Drill',
                                                                      'instructions': 'Rush through gap and touch QB. '
                                                                                      'Do 10 reps.'},
                                                                     {'name': 'Zone Coverage',
                                                                      'instructions': 'Drop into coverage and '
                                                                                      'intercept pass. Do 12 reps.'},
                                                                     {'name': 'Run Fill Drill',
                                                                      'instructions': 'Attack running lane and stop '
                                                                                      'RB. Do 10 reps.'},
                                                                     {'name': 'Block Shed Drill',
                                                                      'instructions': 'Defeat blocker and reach ball '
                                                                                      'carrier. Do 10 reps.'},
                                                                     {'name': 'Open Field Tackle',
                                                                      'instructions': 'Stop runner in space. Do 10 '
                                                                                      'reps.'}]},
                                           'CB': {'position': 'Cornerback',
                                                  'code': 'CB',
                                                  'exercises': [{'name': 'Press Coverage Drill',
                                                                 'instructions': 'Jam receiver and stay with route. Do '
                                                                                 '12 reps.'},
                                                                {'name': 'Man Coverage Drill',
                                                                 'instructions': 'Cover receiver on 20-meter route. Do '
                                                                                 '12 reps.'},
                                                                {'name': 'Interception Drill',
                                                                 'instructions': 'Break on thrown ball and catch it. '
                                                                                 'Do 15 reps.'},
                                                                {'name': 'Fade Route Defense',
                                                                 'instructions': 'Defend deep sideline route. Do 10 '
                                                                                 'reps.'},
                                                                {'name': 'Jump Ball Defense',
                                                                 'instructions': 'Contest high throw against receiver. '
                                                                                 'Do 10 reps.'},
                                                                {'name': 'Run Support Drill',
                                                                 'instructions': 'Defeat blocker and stop runner. Do 8 '
                                                                                 'reps.'}]},
                                           'FS/SS': {'position': 'Safety',
                                                     'code': 'FS/SS',
                                                     'exercises': [{'name': 'Deep Coverage Drill',
                                                                    'instructions': 'Stay over top of two receivers '
                                                                                    'and react to pass. Do 10 reps.'},
                                                                   {'name': 'Angle Pursuit Drill',
                                                                    'instructions': 'Take correct angle and stop '
                                                                                    'runner. Do 12 reps.'},
                                                                   {'name': 'Interception Drill',
                                                                    'instructions': 'Break from deep position and '
                                                                                    'catch pass. Do 12 reps.'},
                                                                   {'name': 'Run Support Drill',
                                                                    'instructions': 'Attack line and stop runner. Do '
                                                                                    '10 reps.'},
                                                                   {'name': 'Coverage Communication Drill',
                                                                    'instructions': 'Coordinate with cornerback '
                                                                                    'against routes. Do 10 reps.'},
                                                                   {'name': 'Open Field Tackle Drill',
                                                                    'instructions': 'Stop ball carrier in space. Do 10 '
                                                                                    'reps.'}]},
                                           'K': {'position': 'Kicker',
                                                 'code': 'K',
                                                 'exercises': [{'name': 'Extra Point Competition',
                                                                'instructions': 'Make 20 extra points.'},
                                                               {'name': 'Field Goal Ladder',
                                                                'instructions': 'Make kicks from 20m, 25m, 30m, 35m, '
                                                                                'and 40m.'},
                                                               {'name': 'Pressure Kick Drill',
                                                                'instructions': 'Kick after teammates count down from '
                                                                                '5 seconds.'},
                                                               {'name': 'Directional Kickoff',
                                                                'instructions': 'Land kick in designated zone. Do 15 '
                                                                                'reps.'},
                                                               {'name': 'Onside Kick Drill',
                                                                'instructions': 'Execute 10 onside kicks.'},
                                                               {'name': 'Game-Winner Simulation',
                                                                'instructions': 'Attempt 10 field goals with teammates '
                                                                                'creating game pressure.'}]},
                                           'P': {'position': 'Punter',
                                                 'code': 'P',
                                                 'exercises': [{'name': 'Directional Punt',
                                                                'instructions': 'Punt to left, center, and right '
                                                                                'zones.'},
                                                               {'name': 'Hang Time Competition',
                                                                'instructions': 'Maximize hang time for 10 punts.'},
                                                               {'name': 'Pressure Punt Drill',
                                                                'instructions': 'Receive snap and punt within 2 '
                                                                                'seconds.'},
                                                               {'name': 'Inside-20 Punt',
                                                                'instructions': "Land 10 punts inside the opponent's "
                                                                                '20-yard line.'},
                                                               {'name': 'Rugby Punt Drill',
                                                                'instructions': 'Roll out and punt while moving. Do 10 '
                                                                                'reps.'},
                                                               {'name': 'Coverage Release Drill',
                                                                'instructions': 'Punt and sprint downfield. Do 10 '
                                                                                'reps.'}]},
                                           'LS': {'position': 'Long Snapper',
                                                  'code': 'LS',
                                                  'exercises': [{'name': 'Snap Accuracy Competition',
                                                                 'instructions': 'Hit target 20 times.'},
                                                                {'name': 'Snap and Cover',
                                                                 'instructions': 'Snap then sprint 20 meters.'},
                                                                {'name': 'Snap and Block',
                                                                 'instructions': 'Snap then engage blocker.'},
                                                                {'name': 'Moving Target Snap',
                                                                 'instructions': 'Snap to slightly moving punter.'},
                                                                {'name': 'Pressure Snap Drill',
                                                                 'instructions': 'Deliver snap under time pressure.'},
                                                                {'name': 'Full Operation Drill',
                                                                 'instructions': 'Complete snap, hold, kick sequence. '
                                                                                 'Do 15 reps.'}]},
                                           'KR/PR': {'position': 'Kick Returner / Punt Returner',
                                                     'code': 'KR/PR',
                                                     'exercises': [{'name': 'Live Return Drill',
                                                                    'instructions': 'Catch kick and return 30 meters.'},
                                                                   {'name': 'Coverage Evasion Drill',
                                                                    'instructions': 'Avoid 2 defenders and gain 20 '
                                                                                    'meters.'},
                                                                   {'name': 'High Punt Catch',
                                                                    'instructions': 'Catch 15 punts cleanly.'},
                                                                   {'name': 'Sideline Return',
                                                                    'instructions': 'Return kick while staying '
                                                                                    'inbounds.'},
                                                                   {'name': 'Decision Drill',
                                                                    'instructions': 'Decide whether to return or fair '
                                                                                    'catch 15 kicks.'},
                                                                   {'name': 'Full Return Simulation',
                                                                    'instructions': 'Catch kick and follow blockers to '
                                                                                    'score. Do 10 reps.'}]}},
                             'learn_how_to_play': [{'number': 1,
                                                    'name': 'Partner Passing',
                                                    'instructions': 'Stand 10 meters apart. Throw and catch '
                                                                    'continuously. Complete 100 catches each.'},
                                                   {'number': 2,
                                                    'name': 'Route and Catch',
                                                    'instructions': 'One player runs a slant route. One player throws '
                                                                    'the pass. Complete 20 catches each.'},
                                                   {'number': 3,
                                                    'name': 'Hand-Off Drill',
                                                    'instructions': 'One player acts as quarterback. One player '
                                                                    'receives the handoff and sprints 20 meters. '
                                                                    'Complete 20 repetitions.'},
                                                   {'number': 4,
                                                    'name': 'Catch and Run',
                                                    'instructions': 'One player throws a short pass. Receiver catches '
                                                                    'it and sprints 20 meters. Complete 20 '
                                                                    'repetitions.'},
                                                   {'number': 5,
                                                    'name': 'Ball Security Challenge',
                                                    'instructions': 'Ball carrier runs 20 meters. Partner attempts to '
                                                                    'tap the ball loose. Complete 15 repetitions.'},
                                                   {'number': 6,
                                                    'name': 'Defensive Pursuit Drill',
                                                    'instructions': 'Ball carrier starts with the football. Defender '
                                                                    'starts 5 meters behind and attempts a tag. '
                                                                    'Complete 15 repetitions each.'},
                                                   {'number': 7,
                                                    'name': 'Basic Coverage Drill',
                                                    'instructions': 'Receiver runs a route. Defender mirrors the route '
                                                                    'without contact. Complete 20 repetitions.'},
                                                   {'number': 8,
                                                    'name': 'Reaction Catch Drill',
                                                    'instructions': 'One player points left or right before throwing. '
                                                                    'Receiver reacts and catches the pass. Complete 30 '
                                                                    'catches.'},
                                                   {'number': 9,
                                                    'name': 'Mini Route Tree',
                                                    'instructions': 'Receiver runs: Slant Out Curl Post Go Route Catch '
                                                                    '5 passes on each route.'},
                                                   {'number': 10,
                                                    'name': 'Beginner Mini Game',
                                                    'instructions': 'Play 3-on-3 or 5-on-5 touch football. No '
                                                                    'tackling. Every possession starts at midfield. '
                                                                    'Play for 20 minutes.'}]}}


def get_catalog() -> Dict[str, Any]:
    """Return the complete American Football training catalog."""
    return AMERICAN_FOOTBALL_CATALOG


def get_training_modes() -> List[str]:
    """Return available training modes."""
    return ["training_alone", "training_with_2_or_more"]


def get_positions(mode: str = "training_alone") -> Dict[str, Any]:
    """Return all position groups for a mode."""
    return AMERICAN_FOOTBALL_CATALOG[mode]["positions"]


def get_position_exercises(position_code: str, mode: str = "training_alone") -> List[Dict[str, str]]:
    """Return exercises for a position code, such as QB, WR, MLB/OLB, or KR/PR."""
    positions = AMERICAN_FOOTBALL_CATALOG[mode]["positions"]
    key = position_code.strip().upper()
    return positions.get(key, {}).get("exercises", [])


def get_learn_how_to_play(mode: str = "training_alone") -> List[Dict[str, Any]]:
    """Return the Learn How to Play drills for a mode."""
    return AMERICAN_FOOTBALL_CATALOG[mode]["learn_how_to_play"]


def search_exercises(query: str, mode: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search exercises and drills by name or instruction text."""
    q = query.strip().lower()
    if not q:
        return []

    modes = [mode] if mode else get_training_modes()
    results: List[Dict[str, Any]] = []

    for training_mode in modes:
        section = AMERICAN_FOOTBALL_CATALOG[training_mode]

        for drill in section["learn_how_to_play"]:
            haystack = f"{drill.get('name', '')} {drill.get('instructions', '')}".lower()
            if q in haystack:
                results.append({"mode": training_mode, "category": "learn_how_to_play", **drill})

        for code, position in section["positions"].items():
            for exercise in position["exercises"]:
                haystack = f"{exercise.get('name', '')} {exercise.get('instructions', '')}".lower()
                if q in haystack:
                    results.append({
                        "mode": training_mode,
                        "category": "position",
                        "position": position["position"],
                        "code": code,
                        **exercise,
                    })

    return results


def catalog_summary() -> Dict[str, int]:
    """Return basic counts for verification and UI checks."""
    alone_positions = AMERICAN_FOOTBALL_CATALOG["training_alone"]["positions"]
    group_positions = AMERICAN_FOOTBALL_CATALOG["training_with_2_or_more"]["positions"]
    return {
        "training_alone_positions": len(alone_positions),
        "training_alone_position_exercises": sum(len(p["exercises"]) for p in alone_positions.values()),
        "training_alone_learn_how_to_play_drills": len(AMERICAN_FOOTBALL_CATALOG["training_alone"]["learn_how_to_play"]),
        "training_with_2_or_more_positions": len(group_positions),
        "training_with_2_or_more_position_exercises": sum(len(p["exercises"]) for p in group_positions.values()),
        "training_with_2_or_more_learn_how_to_play_drills": len(AMERICAN_FOOTBALL_CATALOG["training_with_2_or_more"]["learn_how_to_play"]),
    }


if __name__ == "__main__":
    print(catalog_summary())
