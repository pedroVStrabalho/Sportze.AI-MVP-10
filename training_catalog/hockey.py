"""Hockey training catalog for Sportze.AI.

This module codifies solo and 2+ people hockey workouts into a clean,
implementation-ready structure for the Training Generator catalog.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional

SportSession = Dict[str, Any]
SportCatalog = Dict[str, Dict[str, Dict[str, SportSession]]]

SPORT = "Hockey"


HOCKEY_CATALOG: SportCatalog = {'goalkeeper': {'alone': {'hockey_goalkeeper_alone_tennis_ball_wall_reactions': {'key': 'hockey_goalkeeper_alone_tennis_ball_wall_reactions',
                                                                                 'sport': 'Hockey',
                                                                                 'title': 'Tennis '
                                                                                          'Ball '
                                                                                          'Wall '
                                                                                          'Reactions',
                                                                                 'category': 'goalkeeper',
                                                                                 'training_mode': 'alone',
                                                                                 'level': 'all_levels',
                                                                                 'focus': 'goalkeeper',
                                                                                 'exercises': [{'name': 'Tennis '
                                                                                                        'Ball '
                                                                                                        'Wall '
                                                                                                        'Reactions',
                                                                                                'prescription': '4 '
                                                                                                                'x '
                                                                                                                '20 '
                                                                                                                'catches',
                                                                                                'notes': 'Stand '
                                                                                                         '2 '
                                                                                                         'meters '
                                                                                                         'from '
                                                                                                         'a '
                                                                                                         'wall. '
                                                                                                         'Throw '
                                                                                                         'a '
                                                                                                         'tennis '
                                                                                                         'ball '
                                                                                                         'hard '
                                                                                                         'against '
                                                                                                         'the '
                                                                                                         'wall. '
                                                                                                         'Catch '
                                                                                                         'it '
                                                                                                         'before '
                                                                                                         'the '
                                                                                                         'second '
                                                                                                         'bounce.'}]},
                          'hockey_goalkeeper_alone_left_right_goal_line_movement': {'key': 'hockey_goalkeeper_alone_left_right_goal_line_movement',
                                                                                    'sport': 'Hockey',
                                                                                    'title': 'Left-Right '
                                                                                             'Goal '
                                                                                             'Line '
                                                                                             'Movement',
                                                                                    'category': 'goalkeeper',
                                                                                    'training_mode': 'alone',
                                                                                    'level': 'all_levels',
                                                                                    'focus': 'goalkeeper',
                                                                                    'exercises': [{'name': 'Left-Right '
                                                                                                           'Goal '
                                                                                                           'Line '
                                                                                                           'Movement',
                                                                                                   'prescription': '5 '
                                                                                                                   'x '
                                                                                                                   '30 '
                                                                                                                   'seconds',
                                                                                                   'notes': 'Place '
                                                                                                            'two '
                                                                                                            'cones '
                                                                                                            '3 '
                                                                                                            'meters '
                                                                                                            'apart. '
                                                                                                            'Start '
                                                                                                            'at '
                                                                                                            'one '
                                                                                                            'cone. '
                                                                                                            'Shuffle '
                                                                                                            'sideways '
                                                                                                            'to '
                                                                                                            'the '
                                                                                                            'other '
                                                                                                            'cone '
                                                                                                            'and '
                                                                                                            'touch '
                                                                                                            'it. '
                                                                                                            'Return '
                                                                                                            'immediately.'}]},
                          'hockey_goalkeeper_alone_low_bounce_saves': {'key': 'hockey_goalkeeper_alone_low_bounce_saves',
                                                                       'sport': 'Hockey',
                                                                       'title': 'Low Bounce Saves',
                                                                       'category': 'goalkeeper',
                                                                       'training_mode': 'alone',
                                                                       'level': 'all_levels',
                                                                       'focus': 'goalkeeper',
                                                                       'exercises': [{'name': 'Low '
                                                                                              'Bounce '
                                                                                              'Saves',
                                                                                      'prescription': '4 '
                                                                                                      'x '
                                                                                                      '15 '
                                                                                                      'saves',
                                                                                      'notes': 'Stand '
                                                                                               '3 '
                                                                                               'meters '
                                                                                               'from '
                                                                                               'a '
                                                                                               'wall. '
                                                                                               'Throw '
                                                                                               'a '
                                                                                               'tennis '
                                                                                               'ball '
                                                                                               'so '
                                                                                               'it '
                                                                                               'hits '
                                                                                               'the '
                                                                                               'wall '
                                                                                               'and '
                                                                                               'bounces '
                                                                                               'on '
                                                                                               'the '
                                                                                               'floor. '
                                                                                               'Block '
                                                                                               'it '
                                                                                               'before '
                                                                                               'it '
                                                                                               'passes '
                                                                                               'your '
                                                                                               'feet.'}]},
                          'hockey_goalkeeper_alone_high_bounce_hand_saves': {'key': 'hockey_goalkeeper_alone_high_bounce_hand_saves',
                                                                             'sport': 'Hockey',
                                                                             'title': 'High Bounce '
                                                                                      'Hand Saves',
                                                                             'category': 'goalkeeper',
                                                                             'training_mode': 'alone',
                                                                             'level': 'all_levels',
                                                                             'focus': 'goalkeeper',
                                                                             'exercises': [{'name': 'High '
                                                                                                    'Bounce '
                                                                                                    'Hand '
                                                                                                    'Saves',
                                                                                            'prescription': '4 '
                                                                                                            'x '
                                                                                                            '15 '
                                                                                                            'catches',
                                                                                            'notes': 'Throw '
                                                                                                     'a '
                                                                                                     'tennis '
                                                                                                     'ball '
                                                                                                     'high '
                                                                                                     'against '
                                                                                                     'a '
                                                                                                     'wall. '
                                                                                                     'Catch '
                                                                                                     'it '
                                                                                                     'above '
                                                                                                     'shoulder '
                                                                                                     'height. '
                                                                                                     'Alternate '
                                                                                                     'left '
                                                                                                     'and '
                                                                                                     'right '
                                                                                                     'hand.'}]},
                          'hockey_goalkeeper_alone_drop_and_recover': {'key': 'hockey_goalkeeper_alone_drop_and_recover',
                                                                       'sport': 'Hockey',
                                                                       'title': 'Drop And Recover',
                                                                       'category': 'goalkeeper',
                                                                       'training_mode': 'alone',
                                                                       'level': 'all_levels',
                                                                       'focus': 'goalkeeper',
                                                                       'exercises': [{'name': 'Drop '
                                                                                              'And '
                                                                                              'Recover',
                                                                                      'prescription': '4 '
                                                                                                      'x '
                                                                                                      '20 '
                                                                                                      'reps',
                                                                                      'notes': 'Start '
                                                                                               'standing. '
                                                                                               'Drop '
                                                                                               'into '
                                                                                               'goalkeeper '
                                                                                               'save '
                                                                                               'position. '
                                                                                               'Immediately '
                                                                                               'stand '
                                                                                               'back '
                                                                                               'up.'}]},
                          'hockey_goalkeeper_alone_post_to_post_shuffle': {'key': 'hockey_goalkeeper_alone_post_to_post_shuffle',
                                                                           'sport': 'Hockey',
                                                                           'title': 'Post-To-Post '
                                                                                    'Shuffle',
                                                                           'category': 'goalkeeper',
                                                                           'training_mode': 'alone',
                                                                           'level': 'all_levels',
                                                                           'focus': 'goalkeeper',
                                                                           'exercises': [{'name': 'Post-To-Post '
                                                                                                  'Shuffle',
                                                                                          'prescription': '5 '
                                                                                                          'x '
                                                                                                          '30 '
                                                                                                          'seconds',
                                                                                          'notes': 'Place '
                                                                                                   'two '
                                                                                                   'cones '
                                                                                                   '4 '
                                                                                                   'meters '
                                                                                                   'apart. '
                                                                                                   'Shuffle '
                                                                                                   'between '
                                                                                                   'them '
                                                                                                   'while '
                                                                                                   'staying '
                                                                                                   'low. '
                                                                                                   'Touch '
                                                                                                   'each '
                                                                                                   'cone.'}]},
                          'hockey_goalkeeper_alone_forward_dive_onto_mat': {'key': 'hockey_goalkeeper_alone_forward_dive_onto_mat',
                                                                            'sport': 'Hockey',
                                                                            'title': 'Forward Dive '
                                                                                     'Onto Mat',
                                                                            'category': 'goalkeeper',
                                                                            'training_mode': 'alone',
                                                                            'level': 'all_levels',
                                                                            'focus': 'goalkeeper',
                                                                            'exercises': [{'name': 'Forward '
                                                                                                   'Dive '
                                                                                                   'Onto '
                                                                                                   'Mat',
                                                                                           'prescription': '4 '
                                                                                                           'x '
                                                                                                           '10 '
                                                                                                           'reps',
                                                                                           'notes': 'Place '
                                                                                                    'a '
                                                                                                    'mat '
                                                                                                    'or '
                                                                                                    'soft '
                                                                                                    'surface '
                                                                                                    'in '
                                                                                                    'front. '
                                                                                                    'Start '
                                                                                                    'kneeling. '
                                                                                                    'Dive '
                                                                                                    'forward '
                                                                                                    'and '
                                                                                                    'land '
                                                                                                    'with '
                                                                                                    'arms '
                                                                                                    'extended. '
                                                                                                    'Return '
                                                                                                    'to '
                                                                                                    'start.'}]},
                          'hockey_goalkeeper_alone_rapid_ground_ball_pickups': {'key': 'hockey_goalkeeper_alone_rapid_ground_ball_pickups',
                                                                                'sport': 'Hockey',
                                                                                'title': 'Rapid '
                                                                                         'Ground '
                                                                                         'Ball '
                                                                                         'Pickups',
                                                                                'category': 'goalkeeper',
                                                                                'training_mode': 'alone',
                                                                                'level': 'all_levels',
                                                                                'focus': 'goalkeeper',
                                                                                'exercises': [{'name': 'Rapid '
                                                                                                       'Ground '
                                                                                                       'Ball '
                                                                                                       'Pickups',
                                                                                               'prescription': '4 '
                                                                                                               'rounds',
                                                                                               'notes': 'Place '
                                                                                                        '10 '
                                                                                                        'tennis '
                                                                                                        'balls '
                                                                                                        'on '
                                                                                                        'the '
                                                                                                        'ground. '
                                                                                                        'Pick '
                                                                                                        'them '
                                                                                                        'up '
                                                                                                        'one '
                                                                                                        'by '
                                                                                                        'one '
                                                                                                        'as '
                                                                                                        'fast '
                                                                                                        'as '
                                                                                                        'possible. '
                                                                                                        'Repeat.'}]},
                          'hockey_goalkeeper_alone_single_leg_goalkeeper_balance': {'key': 'hockey_goalkeeper_alone_single_leg_goalkeeper_balance',
                                                                                    'sport': 'Hockey',
                                                                                    'title': 'Single-Leg '
                                                                                             'Goalkeeper '
                                                                                             'Balance',
                                                                                    'category': 'goalkeeper',
                                                                                    'training_mode': 'alone',
                                                                                    'level': 'all_levels',
                                                                                    'focus': 'goalkeeper',
                                                                                    'exercises': [{'name': 'Single-Leg '
                                                                                                           'Goalkeeper '
                                                                                                           'Balance',
                                                                                                   'prescription': '3 '
                                                                                                                   'x '
                                                                                                                   '45 '
                                                                                                                   'seconds '
                                                                                                                   'each '
                                                                                                                   'leg',
                                                                                                   'notes': 'Stand '
                                                                                                            'on '
                                                                                                            'one '
                                                                                                            'leg. '
                                                                                                            'Hold '
                                                                                                            'a '
                                                                                                            'hockey '
                                                                                                            'stick '
                                                                                                            'horizontally. '
                                                                                                            'Maintain '
                                                                                                            'balance.'}]},
                          'hockey_goalkeeper_alone_goalkeeper_shuttle_sprint': {'key': 'hockey_goalkeeper_alone_goalkeeper_shuttle_sprint',
                                                                                'sport': 'Hockey',
                                                                                'title': 'Goalkeeper '
                                                                                         'Shuttle '
                                                                                         'Sprint',
                                                                                'category': 'goalkeeper',
                                                                                'training_mode': 'alone',
                                                                                'level': 'all_levels',
                                                                                'focus': 'goalkeeper',
                                                                                'exercises': [{'name': 'Goalkeeper '
                                                                                                       'Shuttle '
                                                                                                       'Sprint',
                                                                                               'prescription': '6 '
                                                                                                               'rounds',
                                                                                               'notes': 'Place '
                                                                                                        'cones '
                                                                                                        'at '
                                                                                                        '5m, '
                                                                                                        '10m '
                                                                                                        'and '
                                                                                                        '15m. '
                                                                                                        'Sprint '
                                                                                                        'to '
                                                                                                        '5m '
                                                                                                        'and '
                                                                                                        'back. '
                                                                                                        'Sprint '
                                                                                                        'to '
                                                                                                        '10m '
                                                                                                        'and '
                                                                                                        'back. '
                                                                                                        'Sprint '
                                                                                                        'to '
                                                                                                        '15m '
                                                                                                        'and '
                                                                                                        'back.'}]},
                          'hockey_goalkeeper_alone_random_reaction_saves': {'key': 'hockey_goalkeeper_alone_random_reaction_saves',
                                                                            'sport': 'Hockey',
                                                                            'title': 'Random '
                                                                                     'Reaction '
                                                                                     'Saves',
                                                                            'category': 'goalkeeper',
                                                                            'training_mode': 'alone',
                                                                            'level': 'all_levels',
                                                                            'focus': 'goalkeeper',
                                                                            'exercises': [{'name': 'Random '
                                                                                                   'Reaction '
                                                                                                   'Saves',
                                                                                           'prescription': '4 '
                                                                                                           'x '
                                                                                                           '20 '
                                                                                                           'reps',
                                                                                           'notes': 'Number '
                                                                                                    '4 '
                                                                                                    'corners '
                                                                                                    'of '
                                                                                                    'a '
                                                                                                    'wall. '
                                                                                                    'Use '
                                                                                                    'a '
                                                                                                    'phone '
                                                                                                    'random '
                                                                                                    'number '
                                                                                                    'generator. '
                                                                                                    'Throw '
                                                                                                    'ball '
                                                                                                    'to '
                                                                                                    'the '
                                                                                                    'called '
                                                                                                    'corner '
                                                                                                    'and '
                                                                                                    'catch '
                                                                                                    'rebound.'}]},
                          'hockey_goalkeeper_alone_save_recovery_circuit': {'key': 'hockey_goalkeeper_alone_save_recovery_circuit',
                                                                            'sport': 'Hockey',
                                                                            'title': 'Save-Recovery '
                                                                                     'Circuit',
                                                                            'category': 'goalkeeper',
                                                                            'training_mode': 'alone',
                                                                            'level': 'all_levels',
                                                                            'focus': 'goalkeeper',
                                                                            'exercises': [{'name': 'Save-Recovery '
                                                                                                   'Circuit',
                                                                                           'prescription': '4 '
                                                                                                           'rounds',
                                                                                           'notes': 'Drop '
                                                                                                    'into '
                                                                                                    'save '
                                                                                                    'position. '
                                                                                                    'Stand '
                                                                                                    'up. '
                                                                                                    'Shuffle '
                                                                                                    '3m '
                                                                                                    'right. '
                                                                                                    'Shuffle '
                                                                                                    '3m '
                                                                                                    'left. '
                                                                                                    'Sprint '
                                                                                                    '5m '
                                                                                                    'forward. '
                                                                                                    'Return '
                                                                                                    'to '
                                                                                                    'start.'}]}},
                'with_others': {'hockey_goalkeeper_with_others_close_range_shot_saves': {'key': 'hockey_goalkeeper_with_others_close_range_shot_saves',
                                                                                         'sport': 'Hockey',
                                                                                         'title': 'Close '
                                                                                                  'Range '
                                                                                                  'Shot '
                                                                                                  'Saves',
                                                                                         'category': 'goalkeeper',
                                                                                         'training_mode': 'with_others',
                                                                                         'level': 'all_levels',
                                                                                         'focus': 'goalkeeper',
                                                                                         'exercises': [{'name': 'Close '
                                                                                                                'Range '
                                                                                                                'Shot '
                                                                                                                'Saves',
                                                                                                        'prescription': '3 '
                                                                                                                        'rounds',
                                                                                                        'notes': 'One '
                                                                                                                 'player '
                                                                                                                 'stands '
                                                                                                                 '5m '
                                                                                                                 'from '
                                                                                                                 'goal. '
                                                                                                                 'Shoot '
                                                                                                                 '20 '
                                                                                                                 'balls '
                                                                                                                 'toward '
                                                                                                                 'goal. '
                                                                                                                 'Goalkeeper '
                                                                                                                 'attempts '
                                                                                                                 'to '
                                                                                                                 'save '
                                                                                                                 'each '
                                                                                                                 'shot.'}]},
                                'hockey_goalkeeper_with_others_left_right_shot_reaction': {'key': 'hockey_goalkeeper_with_others_left_right_shot_reaction',
                                                                                           'sport': 'Hockey',
                                                                                           'title': 'Left-Right '
                                                                                                    'Shot '
                                                                                                    'Reaction',
                                                                                           'category': 'goalkeeper',
                                                                                           'training_mode': 'with_others',
                                                                                           'level': 'all_levels',
                                                                                           'focus': 'goalkeeper',
                                                                                           'exercises': [{'name': 'Left-Right '
                                                                                                                  'Shot '
                                                                                                                  'Reaction',
                                                                                                          'prescription': '30 '
                                                                                                                          'shots',
                                                                                                          'notes': 'Two '
                                                                                                                   'shooters '
                                                                                                                   'stand '
                                                                                                                   '5m '
                                                                                                                   'apart. '
                                                                                                                   'Alternate '
                                                                                                                   'shots '
                                                                                                                   'every '
                                                                                                                   '3 '
                                                                                                                   'seconds. '
                                                                                                                   'Goalkeeper '
                                                                                                                   'reacts '
                                                                                                                   'and '
                                                                                                                   'saves.'}]},
                                'hockey_goalkeeper_with_others_rebound_recovery': {'key': 'hockey_goalkeeper_with_others_rebound_recovery',
                                                                                   'sport': 'Hockey',
                                                                                   'title': 'Rebound '
                                                                                            'Recovery',
                                                                                   'category': 'goalkeeper',
                                                                                   'training_mode': 'with_others',
                                                                                   'level': 'all_levels',
                                                                                   'focus': 'goalkeeper',
                                                                                   'exercises': [{'name': 'Rebound '
                                                                                                          'Recovery',
                                                                                                  'prescription': '20 '
                                                                                                                  'sequences',
                                                                                                  'notes': 'Shooter '
                                                                                                           'takes '
                                                                                                           'a '
                                                                                                           'shot. '
                                                                                                           'Immediately '
                                                                                                           'shoots '
                                                                                                           'again '
                                                                                                           'if '
                                                                                                           'goalkeeper '
                                                                                                           'gives '
                                                                                                           'a '
                                                                                                           'rebound.'}]},
                                'hockey_goalkeeper_with_others_high_low_save_series': {'key': 'hockey_goalkeeper_with_others_high_low_save_series',
                                                                                       'sport': 'Hockey',
                                                                                       'title': 'High-Low '
                                                                                                'Save '
                                                                                                'Series',
                                                                                       'category': 'goalkeeper',
                                                                                       'training_mode': 'with_others',
                                                                                       'level': 'all_levels',
                                                                                       'focus': 'goalkeeper',
                                                                                       'exercises': [{'name': 'High-Low '
                                                                                                              'Save '
                                                                                                              'Series',
                                                                                                      'prescription': '20 '
                                                                                                                      'sequences',
                                                                                                      'notes': 'First '
                                                                                                               'shot '
                                                                                                               'must '
                                                                                                               'be '
                                                                                                               'aimed '
                                                                                                               'low. '
                                                                                                               'Second '
                                                                                                               'shot '
                                                                                                               'aimed '
                                                                                                               'high. '
                                                                                                               'Alternate '
                                                                                                               'continuously.'}]},
                                'hockey_goalkeeper_with_others_rapid_fire_saves': {'key': 'hockey_goalkeeper_with_others_rapid_fire_saves',
                                                                                   'sport': 'Hockey',
                                                                                   'title': 'Rapid '
                                                                                            'Fire '
                                                                                            'Saves',
                                                                                   'category': 'goalkeeper',
                                                                                   'training_mode': 'with_others',
                                                                                   'level': 'all_levels',
                                                                                   'focus': 'goalkeeper',
                                                                                   'exercises': [{'name': 'Rapid '
                                                                                                          'Fire '
                                                                                                          'Saves',
                                                                                                  'prescription': 'Goalkeeper '
                                                                                                                  'faces '
                                                                                                                  '30 '
                                                                                                                  'total '
                                                                                                                  'shots.',
                                                                                                  'notes': 'Three '
                                                                                                           'players '
                                                                                                           'stand '
                                                                                                           'around '
                                                                                                           'shooting '
                                                                                                           'circle. '
                                                                                                           'One '
                                                                                                           'shot '
                                                                                                           'each '
                                                                                                           'in '
                                                                                                           'sequence.'}]},
                                'hockey_goalkeeper_with_others_deflection_saves': {'key': 'hockey_goalkeeper_with_others_deflection_saves',
                                                                                   'sport': 'Hockey',
                                                                                   'title': 'Deflection '
                                                                                            'Saves',
                                                                                   'category': 'goalkeeper',
                                                                                   'training_mode': 'with_others',
                                                                                   'level': 'all_levels',
                                                                                   'focus': 'goalkeeper',
                                                                                   'exercises': [{'name': 'Deflection '
                                                                                                          'Saves',
                                                                                                  'prescription': '20 '
                                                                                                                  'shots',
                                                                                                  'notes': 'One '
                                                                                                           'player '
                                                                                                           'shoots. '
                                                                                                           'Another '
                                                                                                           'player '
                                                                                                           'attempts '
                                                                                                           'slight '
                                                                                                           'deflection. '
                                                                                                           'Goalkeeper '
                                                                                                           'reacts.'}]},
                                'hockey_goalkeeper_with_others_one_on_one_breakaway': {'key': 'hockey_goalkeeper_with_others_one_on_one_breakaway',
                                                                                       'sport': 'Hockey',
                                                                                       'title': 'One-on-One '
                                                                                                'Breakaway',
                                                                                       'category': 'goalkeeper',
                                                                                       'training_mode': 'with_others',
                                                                                       'level': 'all_levels',
                                                                                       'focus': 'goalkeeper',
                                                                                       'exercises': [{'name': 'One-on-One '
                                                                                                              'Breakaway',
                                                                                                      'prescription': '15 '
                                                                                                                      'attempts',
                                                                                                      'notes': 'Attacker '
                                                                                                               'starts '
                                                                                                               '20m '
                                                                                                               'away. '
                                                                                                               'Dribbles '
                                                                                                               'toward '
                                                                                                               'goal. '
                                                                                                               'Goalkeeper '
                                                                                                               'attempts '
                                                                                                               'stop.'}]},
                                'hockey_goalkeeper_with_others_cross_goal_movement': {'key': 'hockey_goalkeeper_with_others_cross_goal_movement',
                                                                                      'sport': 'Hockey',
                                                                                      'title': 'Cross '
                                                                                               'Goal '
                                                                                               'Movement',
                                                                                      'category': 'goalkeeper',
                                                                                      'training_mode': 'with_others',
                                                                                      'level': 'all_levels',
                                                                                      'focus': 'goalkeeper',
                                                                                      'exercises': [{'name': 'Cross '
                                                                                                             'Goal '
                                                                                                             'Movement',
                                                                                                     'prescription': '20 '
                                                                                                                     'shots',
                                                                                                     'notes': 'Two '
                                                                                                              'shooters '
                                                                                                              'stand '
                                                                                                              'on '
                                                                                                              'opposite '
                                                                                                              'sides. '
                                                                                                              'Pass '
                                                                                                              'across '
                                                                                                              'goal '
                                                                                                              'before '
                                                                                                              'shooting. '
                                                                                                              'Goalkeeper '
                                                                                                              'must '
                                                                                                              'reposition.'}]},
                                'hockey_goalkeeper_with_others_number_call_reaction': {'key': 'hockey_goalkeeper_with_others_number_call_reaction',
                                                                                       'sport': 'Hockey',
                                                                                       'title': 'Number '
                                                                                                'Call '
                                                                                                'Reaction',
                                                                                       'category': 'goalkeeper',
                                                                                       'training_mode': 'with_others',
                                                                                       'level': 'all_levels',
                                                                                       'focus': 'goalkeeper',
                                                                                       'exercises': [{'name': 'Number '
                                                                                                              'Call '
                                                                                                              'Reaction',
                                                                                                      'prescription': '20 '
                                                                                                                      'reps',
                                                                                                      'notes': 'Coach '
                                                                                                               'or '
                                                                                                               'teammate '
                                                                                                               'calls '
                                                                                                               'left '
                                                                                                               'or '
                                                                                                               'right. '
                                                                                                               'Shot '
                                                                                                               'follows '
                                                                                                               'immediately.'}]},
                                'hockey_goalkeeper_with_others_save_and_distribution': {'key': 'hockey_goalkeeper_with_others_save_and_distribution',
                                                                                        'sport': 'Hockey',
                                                                                        'title': 'Save '
                                                                                                 'and '
                                                                                                 'Distribution',
                                                                                        'category': 'goalkeeper',
                                                                                        'training_mode': 'with_others',
                                                                                        'level': 'all_levels',
                                                                                        'focus': 'goalkeeper',
                                                                                        'exercises': [{'name': 'Save '
                                                                                                               'and '
                                                                                                               'Distribution',
                                                                                                       'prescription': '20 '
                                                                                                                       'reps',
                                                                                                       'notes': 'Make '
                                                                                                                'save. '
                                                                                                                'Immediately '
                                                                                                                'pass '
                                                                                                                'ball '
                                                                                                                'to '
                                                                                                                'teammate '
                                                                                                                '15m '
                                                                                                                'away.'}]},
                                'hockey_goalkeeper_with_others_shoot_rebound_shoot': {'key': 'hockey_goalkeeper_with_others_shoot_rebound_shoot',
                                                                                      'sport': 'Hockey',
                                                                                      'title': 'Shoot-Rebound-Shoot',
                                                                                      'category': 'goalkeeper',
                                                                                      'training_mode': 'with_others',
                                                                                      'level': 'all_levels',
                                                                                      'focus': 'goalkeeper',
                                                                                      'exercises': [{'name': 'Shoot-Rebound-Shoot',
                                                                                                     'prescription': '20 '
                                                                                                                     'sequences',
                                                                                                     'notes': 'Same '
                                                                                                              'attacker '
                                                                                                              'shoots '
                                                                                                              'twice '
                                                                                                              'consecutively. '
                                                                                                              'Goalkeeper '
                                                                                                              'recovers '
                                                                                                              'between '
                                                                                                              'attempts.'}]},
                                'hockey_goalkeeper_with_others_goalkeeper_match_simulation': {'key': 'hockey_goalkeeper_with_others_goalkeeper_match_simulation',
                                                                                              'sport': 'Hockey',
                                                                                              'title': 'Goalkeeper '
                                                                                                       'Match '
                                                                                                       'Simulation',
                                                                                              'category': 'goalkeeper',
                                                                                              'training_mode': 'with_others',
                                                                                              'level': 'all_levels',
                                                                                              'focus': 'goalkeeper',
                                                                                              'exercises': [{'name': 'Goalkeeper '
                                                                                                                     'Match '
                                                                                                                     'Simulation',
                                                                                                             'prescription': '5 '
                                                                                                                             'rounds',
                                                                                                             'notes': '3 '
                                                                                                                      'attackers '
                                                                                                                      'versus '
                                                                                                                      'goalkeeper. '
                                                                                                                      'Continuous '
                                                                                                                      'attacks '
                                                                                                                      'for '
                                                                                                                      '60 '
                                                                                                                      'seconds.'}]}}},
 'defender': {'alone': {'hockey_defender_alone_backpedal_and_recover': {'key': 'hockey_defender_alone_backpedal_and_recover',
                                                                        'sport': 'Hockey',
                                                                        'title': 'Backpedal and '
                                                                                 'Recover',
                                                                        'category': 'defender',
                                                                        'training_mode': 'alone',
                                                                        'level': 'all_levels',
                                                                        'focus': 'defender',
                                                                        'exercises': [{'name': 'Backpedal '
                                                                                               'and '
                                                                                               'Recover',
                                                                                       'prescription': '6 '
                                                                                                       'rounds',
                                                                                       'notes': 'Place '
                                                                                                'two '
                                                                                                'cones '
                                                                                                '15m '
                                                                                                'apart. '
                                                                                                'Backpedal '
                                                                                                'from '
                                                                                                'cone '
                                                                                                'A '
                                                                                                'to '
                                                                                                'cone '
                                                                                                'B. '
                                                                                                'Turn '
                                                                                                'and '
                                                                                                'sprint '
                                                                                                'back '
                                                                                                'to '
                                                                                                'cone '
                                                                                                'A.'}]},
                        'hockey_defender_alone_interception_footwork': {'key': 'hockey_defender_alone_interception_footwork',
                                                                        'sport': 'Hockey',
                                                                        'title': 'Interception '
                                                                                 'Footwork',
                                                                        'category': 'defender',
                                                                        'training_mode': 'alone',
                                                                        'level': 'all_levels',
                                                                        'focus': 'defender',
                                                                        'exercises': [{'name': 'Interception '
                                                                                               'Footwork',
                                                                                       'prescription': '5 '
                                                                                                       'rounds',
                                                                                       'notes': 'Place '
                                                                                                '5 '
                                                                                                'cones '
                                                                                                'in '
                                                                                                'a '
                                                                                                'zigzag, '
                                                                                                '2m '
                                                                                                'apart. '
                                                                                                'Side '
                                                                                                'shuffle '
                                                                                                'through '
                                                                                                'all '
                                                                                                'cones. '
                                                                                                'Touch '
                                                                                                'each '
                                                                                                'cone '
                                                                                                'with '
                                                                                                'your '
                                                                                                'stick.'}]},
                        'hockey_defender_alone_wall_pass_and_control': {'key': 'hockey_defender_alone_wall_pass_and_control',
                                                                        'sport': 'Hockey',
                                                                        'title': 'Wall Pass and '
                                                                                 'Control',
                                                                        'category': 'defender',
                                                                        'training_mode': 'alone',
                                                                        'level': 'all_levels',
                                                                        'focus': 'defender',
                                                                        'exercises': [{'name': 'Wall '
                                                                                               'Pass '
                                                                                               'and '
                                                                                               'Control',
                                                                                       'prescription': '100 '
                                                                                                       'passes',
                                                                                       'notes': 'Stand '
                                                                                                '5m '
                                                                                                'from '
                                                                                                'a '
                                                                                                'wall. '
                                                                                                'Pass '
                                                                                                'the '
                                                                                                'ball '
                                                                                                'against '
                                                                                                'the '
                                                                                                'wall. '
                                                                                                'Control '
                                                                                                'it '
                                                                                                'with '
                                                                                                'one '
                                                                                                'touch. '
                                                                                                'Pass '
                                                                                                'again '
                                                                                                'immediately.'}]},
                        'hockey_defender_alone_long_outlet_passing': {'key': 'hockey_defender_alone_long_outlet_passing',
                                                                      'sport': 'Hockey',
                                                                      'title': 'Long Outlet '
                                                                               'Passing',
                                                                      'category': 'defender',
                                                                      'training_mode': 'alone',
                                                                      'level': 'all_levels',
                                                                      'focus': 'defender',
                                                                      'exercises': [{'name': 'Long '
                                                                                             'Outlet '
                                                                                             'Passing',
                                                                                     'prescription': '50 '
                                                                                                     'passes',
                                                                                     'notes': 'Place '
                                                                                              'a '
                                                                                              'target '
                                                                                              'cone '
                                                                                              '20m '
                                                                                              'away. '
                                                                                              'Hit '
                                                                                              'the '
                                                                                              'target '
                                                                                              'with '
                                                                                              'a '
                                                                                              'push '
                                                                                              'pass. '
                                                                                              'Retrieve '
                                                                                              'the '
                                                                                              'ball '
                                                                                              'and '
                                                                                              'repeat.'}]},
                        'hockey_defender_alone_defensive_recovery_sprint': {'key': 'hockey_defender_alone_defensive_recovery_sprint',
                                                                            'sport': 'Hockey',
                                                                            'title': 'Defensive '
                                                                                     'Recovery '
                                                                                     'Sprint',
                                                                            'category': 'defender',
                                                                            'training_mode': 'alone',
                                                                            'level': 'all_levels',
                                                                            'focus': 'defender',
                                                                            'exercises': [{'name': 'Defensive '
                                                                                                   'Recovery '
                                                                                                   'Sprint',
                                                                                           'prescription': '8 '
                                                                                                           'reps',
                                                                                           'notes': 'Sprint '
                                                                                                    '20m '
                                                                                                    'forward. '
                                                                                                    'Turn '
                                                                                                    'immediately. '
                                                                                                    'Sprint '
                                                                                                    '20m '
                                                                                                    'back.'}]},
                        'hockey_defender_alone_block_the_lane': {'key': 'hockey_defender_alone_block_the_lane',
                                                                 'sport': 'Hockey',
                                                                 'title': 'Block the Lane',
                                                                 'category': 'defender',
                                                                 'training_mode': 'alone',
                                                                 'level': 'all_levels',
                                                                 'focus': 'defender',
                                                                 'exercises': [{'name': 'Block the '
                                                                                        'Lane',
                                                                                'prescription': '5 '
                                                                                                'x '
                                                                                                '45 '
                                                                                                'seconds',
                                                                                'notes': 'Place '
                                                                                         'two '
                                                                                         'cones 4m '
                                                                                         'apart. '
                                                                                         'Shuffle '
                                                                                         'continuously '
                                                                                         'between '
                                                                                         'them. '
                                                                                         'Keep '
                                                                                         'stick '
                                                                                         'low on '
                                                                                         'the '
                                                                                         'ground.'}]},
                        'hockey_defender_alone_figure_8_defensive_movement': {'key': 'hockey_defender_alone_figure_8_defensive_movement',
                                                                              'sport': 'Hockey',
                                                                              'title': 'Figure-8 '
                                                                                       'Defensive '
                                                                                       'Movement',
                                                                              'category': 'defender',
                                                                              'training_mode': 'alone',
                                                                              'level': 'all_levels',
                                                                              'focus': 'defender',
                                                                              'exercises': [{'name': 'Figure-8 '
                                                                                                     'Defensive '
                                                                                                     'Movement',
                                                                                             'prescription': '5 '
                                                                                                             'rounds',
                                                                                             'notes': 'Place '
                                                                                                      'two '
                                                                                                      'cones '
                                                                                                      '3m '
                                                                                                      'apart. '
                                                                                                      'Run '
                                                                                                      'figure-8 '
                                                                                                      'patterns '
                                                                                                      'around '
                                                                                                      'them. '
                                                                                                      'Keep '
                                                                                                      'stick '
                                                                                                      'in '
                                                                                                      'defensive '
                                                                                                      'position.'}]},
                        'hockey_defender_alone_defensive_reach_drill': {'key': 'hockey_defender_alone_defensive_reach_drill',
                                                                        'sport': 'Hockey',
                                                                        'title': 'Defensive Reach '
                                                                                 'Drill',
                                                                        'category': 'defender',
                                                                        'training_mode': 'alone',
                                                                        'level': 'all_levels',
                                                                        'focus': 'defender',
                                                                        'exercises': [{'name': 'Defensive '
                                                                                               'Reach '
                                                                                               'Drill',
                                                                                       'prescription': '4 '
                                                                                                       'rounds',
                                                                                       'notes': 'Place '
                                                                                                '10 '
                                                                                                'balls '
                                                                                                'around '
                                                                                                'a '
                                                                                                '3m '
                                                                                                'circle. '
                                                                                                'Start '
                                                                                                'in '
                                                                                                'the '
                                                                                                'center. '
                                                                                                'Reach '
                                                                                                'each '
                                                                                                'ball '
                                                                                                'with '
                                                                                                'your '
                                                                                                'stick '
                                                                                                'without '
                                                                                                'moving '
                                                                                                'feet.'}]},
                        'hockey_defender_alone_sprint_and_clear': {'key': 'hockey_defender_alone_sprint_and_clear',
                                                                   'sport': 'Hockey',
                                                                   'title': 'Sprint and Clear',
                                                                   'category': 'defender',
                                                                   'training_mode': 'alone',
                                                                   'level': 'all_levels',
                                                                   'focus': 'defender',
                                                                   'exercises': [{'name': 'Sprint '
                                                                                          'and '
                                                                                          'Clear',
                                                                                  'prescription': '10 '
                                                                                                  'reps',
                                                                                  'notes': 'Sprint '
                                                                                           '15m to '
                                                                                           'a '
                                                                                           'ball. '
                                                                                           'Hit a '
                                                                                           'clearance '
                                                                                           'pass '
                                                                                           '20m. '
                                                                                           'Jog '
                                                                                           'back.'}]},
                        'hockey_defender_alone_defensive_agility_square': {'key': 'hockey_defender_alone_defensive_agility_square',
                                                                           'sport': 'Hockey',
                                                                           'title': 'Defensive '
                                                                                    'Agility '
                                                                                    'Square',
                                                                           'category': 'defender',
                                                                           'training_mode': 'alone',
                                                                           'level': 'all_levels',
                                                                           'focus': 'defender',
                                                                           'exercises': [{'name': 'Defensive '
                                                                                                  'Agility '
                                                                                                  'Square',
                                                                                          'prescription': '5 '
                                                                                                          'rounds '
                                                                                                          'counterclockwise.',
                                                                                          'notes': 'Create '
                                                                                                   'a '
                                                                                                   '5m '
                                                                                                   'square '
                                                                                                   'with '
                                                                                                   'cones. '
                                                                                                   'Shuffle '
                                                                                                   'around '
                                                                                                   'all '
                                                                                                   'four '
                                                                                                   'sides. '
                                                                                                   '5 '
                                                                                                   'rounds '
                                                                                                   'clockwise.'}]},
                        'hockey_defender_alone_one_touch_clearance': {'key': 'hockey_defender_alone_one_touch_clearance',
                                                                      'sport': 'Hockey',
                                                                      'title': 'One-Touch '
                                                                               'Clearance',
                                                                      'category': 'defender',
                                                                      'training_mode': 'alone',
                                                                      'level': 'all_levels',
                                                                      'focus': 'defender',
                                                                      'exercises': [{'name': 'One-Touch '
                                                                                             'Clearance',
                                                                                     'prescription': '50 '
                                                                                                     'reps',
                                                                                     'notes': 'Pass '
                                                                                              'ball '
                                                                                              'against '
                                                                                              'wall. '
                                                                                              'Clear '
                                                                                              'immediately '
                                                                                              'with '
                                                                                              'first '
                                                                                              'touch.'}]},
                        'hockey_defender_alone_full_field_recovery_run': {'key': 'hockey_defender_alone_full_field_recovery_run',
                                                                          'sport': 'Hockey',
                                                                          'title': 'Full Field '
                                                                                   'Recovery Run',
                                                                          'category': 'defender',
                                                                          'training_mode': 'alone',
                                                                          'level': 'all_levels',
                                                                          'focus': 'defender',
                                                                          'exercises': [{'name': 'Full '
                                                                                                 'Field '
                                                                                                 'Recovery '
                                                                                                 'Run',
                                                                                         'prescription': '8 '
                                                                                                         'reps',
                                                                                         'notes': 'Run '
                                                                                                  '50m. '
                                                                                                  'Jog '
                                                                                                  'back. '
                                                                                                  'Repeat.'}]}},
              'with_others': {'hockey_defender_with_others_1v1_channel_defense': {'key': 'hockey_defender_with_others_1v1_channel_defense',
                                                                                  'sport': 'Hockey',
                                                                                  'title': '1v1 '
                                                                                           'Channel '
                                                                                           'Defense',
                                                                                  'category': 'defender',
                                                                                  'training_mode': 'with_others',
                                                                                  'level': 'all_levels',
                                                                                  'focus': 'defender',
                                                                                  'exercises': [{'name': '1v1 '
                                                                                                         'Channel '
                                                                                                         'Defense',
                                                                                                 'prescription': '15 '
                                                                                                                 'attempts '
                                                                                                                 'each',
                                                                                                 'notes': 'Create '
                                                                                                          'a '
                                                                                                          '5m '
                                                                                                          'wide '
                                                                                                          'channel. '
                                                                                                          'Attacker '
                                                                                                          'tries '
                                                                                                          'to '
                                                                                                          'dribble '
                                                                                                          'through. '
                                                                                                          'Defender '
                                                                                                          'prevents '
                                                                                                          'progress.'}]},
                              'hockey_defender_with_others_intercept_the_pass': {'key': 'hockey_defender_with_others_intercept_the_pass',
                                                                                 'sport': 'Hockey',
                                                                                 'title': 'Intercept '
                                                                                          'The '
                                                                                          'Pass',
                                                                                 'category': 'defender',
                                                                                 'training_mode': 'with_others',
                                                                                 'level': 'all_levels',
                                                                                 'focus': 'defender',
                                                                                 'exercises': [{'name': 'Intercept '
                                                                                                        'The '
                                                                                                        'Pass',
                                                                                                'prescription': 'Intercept '
                                                                                                                '20 '
                                                                                                                'passes.',
                                                                                                'notes': 'Two '
                                                                                                         'attackers '
                                                                                                         'pass '
                                                                                                         'ball. '
                                                                                                         'Defender '
                                                                                                         'stands '
                                                                                                         'between '
                                                                                                         'them.'}]},
                              'hockey_defender_with_others_shadow_defending': {'key': 'hockey_defender_with_others_shadow_defending',
                                                                               'sport': 'Hockey',
                                                                               'title': 'Shadow '
                                                                                        'Defending',
                                                                               'category': 'defender',
                                                                               'training_mode': 'with_others',
                                                                               'level': 'all_levels',
                                                                               'focus': 'defender',
                                                                               'exercises': [{'name': 'Shadow '
                                                                                                      'Defending',
                                                                                              'prescription': '5 '
                                                                                                              'x '
                                                                                                              '30 '
                                                                                                              'seconds',
                                                                                              'notes': 'Attacker '
                                                                                                       'dribbles '
                                                                                                       'freely. '
                                                                                                       'Defender '
                                                                                                       'stays '
                                                                                                       'within '
                                                                                                       '1m.'}]},
                              'hockey_defender_with_others_tackle_timing_drill': {'key': 'hockey_defender_with_others_tackle_timing_drill',
                                                                                  'sport': 'Hockey',
                                                                                  'title': 'Tackle '
                                                                                           'Timing '
                                                                                           'Drill',
                                                                                  'category': 'defender',
                                                                                  'training_mode': 'with_others',
                                                                                  'level': 'all_levels',
                                                                                  'focus': 'defender',
                                                                                  'exercises': [{'name': 'Tackle '
                                                                                                         'Timing '
                                                                                                         'Drill',
                                                                                                 'prescription': '20 '
                                                                                                                 'attempts',
                                                                                                 'notes': 'Attacker '
                                                                                                          'dribbles '
                                                                                                          '15m. '
                                                                                                          'Defender '
                                                                                                          'attempts '
                                                                                                          'clean '
                                                                                                          'tackle.'}]},
                              'hockey_defender_with_others_recovery_race': {'key': 'hockey_defender_with_others_recovery_race',
                                                                            'sport': 'Hockey',
                                                                            'title': 'Recovery '
                                                                                     'Race',
                                                                            'category': 'defender',
                                                                            'training_mode': 'with_others',
                                                                            'level': 'all_levels',
                                                                            'focus': 'defender',
                                                                            'exercises': [{'name': 'Recovery '
                                                                                                   'Race',
                                                                                           'prescription': '10 '
                                                                                                           'reps',
                                                                                           'notes': 'Attacker '
                                                                                                    'starts '
                                                                                                    '3m '
                                                                                                    'ahead. '
                                                                                                    'Both '
                                                                                                    'sprint '
                                                                                                    '25m. '
                                                                                                    'Defender '
                                                                                                    'must '
                                                                                                    'catch '
                                                                                                    'attacker.'}]},
                              'hockey_defender_with_others_clearance_under_pressure': {'key': 'hockey_defender_with_others_clearance_under_pressure',
                                                                                       'sport': 'Hockey',
                                                                                       'title': 'Clearance '
                                                                                                'Under '
                                                                                                'Pressure',
                                                                                       'category': 'defender',
                                                                                       'training_mode': 'with_others',
                                                                                       'level': 'all_levels',
                                                                                       'focus': 'defender',
                                                                                       'exercises': [{'name': 'Clearance '
                                                                                                              'Under '
                                                                                                              'Pressure',
                                                                                                      'prescription': '20 '
                                                                                                                      'reps',
                                                                                                      'notes': 'Attacker '
                                                                                                               'pressures '
                                                                                                               'defender. '
                                                                                                               'Defender '
                                                                                                               'clears '
                                                                                                               'ball '
                                                                                                               'to '
                                                                                                               'target '
                                                                                                               'zone.'}]},
                              'hockey_defender_with_others_defensive_triangle': {'key': 'hockey_defender_with_others_defensive_triangle',
                                                                                 'sport': 'Hockey',
                                                                                 'title': 'Defensive '
                                                                                          'Triangle',
                                                                                 'category': 'defender',
                                                                                 'training_mode': 'with_others',
                                                                                 'level': 'all_levels',
                                                                                 'focus': 'defender',
                                                                                 'exercises': [{'name': 'Defensive '
                                                                                                        'Triangle',
                                                                                                'prescription': '5 '
                                                                                                                'x '
                                                                                                                '60 '
                                                                                                                'seconds',
                                                                                                'notes': 'Three '
                                                                                                         'attackers '
                                                                                                         'pass '
                                                                                                         'around '
                                                                                                         'defender. '
                                                                                                         'Defender '
                                                                                                         'attempts '
                                                                                                         'interception.'}]},
                              'hockey_defender_with_others_sideline_containment': {'key': 'hockey_defender_with_others_sideline_containment',
                                                                                   'sport': 'Hockey',
                                                                                   'title': 'Sideline '
                                                                                            'Containment',
                                                                                   'category': 'defender',
                                                                                   'training_mode': 'with_others',
                                                                                   'level': 'all_levels',
                                                                                   'focus': 'defender',
                                                                                   'exercises': [{'name': 'Sideline '
                                                                                                          'Containment',
                                                                                                  'prescription': '15 '
                                                                                                                  'reps',
                                                                                                  'notes': 'Attacker '
                                                                                                           'advances '
                                                                                                           'along '
                                                                                                           'sideline. '
                                                                                                           'Defender '
                                                                                                           'forces '
                                                                                                           'attacker '
                                                                                                           'outward.'}]},
                              'hockey_defender_with_others_2v1_defense': {'key': 'hockey_defender_with_others_2v1_defense',
                                                                          'sport': 'Hockey',
                                                                          'title': '2v1 Defense',
                                                                          'category': 'defender',
                                                                          'training_mode': 'with_others',
                                                                          'level': 'all_levels',
                                                                          'focus': 'defender',
                                                                          'exercises': [{'name': '2v1 '
                                                                                                 'Defense',
                                                                                         'prescription': '15 '
                                                                                                         'rounds',
                                                                                         'notes': 'Two '
                                                                                                  'attackers '
                                                                                                  'versus '
                                                                                                  'one '
                                                                                                  'defender. '
                                                                                                  'Defender '
                                                                                                  'delays '
                                                                                                  'attack.'}]},
                              'hockey_defender_with_others_block_the_shot': {'key': 'hockey_defender_with_others_block_the_shot',
                                                                             'sport': 'Hockey',
                                                                             'title': 'Block The '
                                                                                      'Shot',
                                                                             'category': 'defender',
                                                                             'training_mode': 'with_others',
                                                                             'level': 'all_levels',
                                                                             'focus': 'defender',
                                                                             'exercises': [{'name': 'Block '
                                                                                                    'The '
                                                                                                    'Shot',
                                                                                            'prescription': '20 '
                                                                                                            'shots',
                                                                                            'notes': 'Attacker '
                                                                                                     'shoots '
                                                                                                     'from '
                                                                                                     '10m. '
                                                                                                     'Defender '
                                                                                                     'attempts '
                                                                                                     'block.'}]},
                              'hockey_defender_with_others_pressure_and_recover': {'key': 'hockey_defender_with_others_pressure_and_recover',
                                                                                   'sport': 'Hockey',
                                                                                   'title': 'Pressure '
                                                                                            'and '
                                                                                            'Recover',
                                                                                   'category': 'defender',
                                                                                   'training_mode': 'with_others',
                                                                                   'level': 'all_levels',
                                                                                   'focus': 'defender',
                                                                                   'exercises': [{'name': 'Pressure '
                                                                                                          'and '
                                                                                                          'Recover',
                                                                                                  'prescription': '15 '
                                                                                                                  'reps',
                                                                                                  'notes': 'Defender '
                                                                                                           'pressures '
                                                                                                           'attacker. '
                                                                                                           'Retreats '
                                                                                                           '5m. '
                                                                                                           'Pressures '
                                                                                                           'again.'}]},
                              'hockey_defender_with_others_defender_match_simulation': {'key': 'hockey_defender_with_others_defender_match_simulation',
                                                                                        'sport': 'Hockey',
                                                                                        'title': 'Defender '
                                                                                                 'Match '
                                                                                                 'Simulation',
                                                                                        'category': 'defender',
                                                                                        'training_mode': 'with_others',
                                                                                        'level': 'all_levels',
                                                                                        'focus': 'defender',
                                                                                        'exercises': [{'name': 'Defender '
                                                                                                               'Match '
                                                                                                               'Simulation',
                                                                                                       'prescription': '5 '
                                                                                                                       'rounds',
                                                                                                       'notes': 'Continuous '
                                                                                                                'defending '
                                                                                                                'against '
                                                                                                                'attackers. '
                                                                                                                '60-second '
                                                                                                                'rounds.'}]}}},
 'center_midfielder': {'alone': {'hockey_center_midfielder_alone_continuous_wall_passing': {'key': 'hockey_center_midfielder_alone_continuous_wall_passing',
                                                                                            'sport': 'Hockey',
                                                                                            'title': 'Continuous '
                                                                                                     'Wall '
                                                                                                     'Passing',
                                                                                            'category': 'center_midfielder',
                                                                                            'training_mode': 'alone',
                                                                                            'level': 'all_levels',
                                                                                            'focus': 'center '
                                                                                                     'midfielder',
                                                                                            'exercises': [{'name': 'Continuous '
                                                                                                                   'Wall '
                                                                                                                   'Passing',
                                                                                                           'prescription': '150 '
                                                                                                                           'passes',
                                                                                                           'notes': 'Stand '
                                                                                                                    '5m '
                                                                                                                    'from '
                                                                                                                    'wall. '
                                                                                                                    'Pass '
                                                                                                                    'and '
                                                                                                                    'receive '
                                                                                                                    'continuously. '
                                                                                                                    'No '
                                                                                                                    'stopping.'}]},
                                 'hockey_center_midfielder_alone_receive_turn_pass': {'key': 'hockey_center_midfielder_alone_receive_turn_pass',
                                                                                      'sport': 'Hockey',
                                                                                      'title': 'Receive-Turn-Pass',
                                                                                      'category': 'center_midfielder',
                                                                                      'training_mode': 'alone',
                                                                                      'level': 'all_levels',
                                                                                      'focus': 'center '
                                                                                               'midfielder',
                                                                                      'exercises': [{'name': 'Receive-Turn-Pass',
                                                                                                     'prescription': '60 '
                                                                                                                     'reps',
                                                                                                     'notes': 'Pass '
                                                                                                              'against '
                                                                                                              'wall. '
                                                                                                              'Receive. '
                                                                                                              'Turn '
                                                                                                              '180°. '
                                                                                                              'Turn '
                                                                                                              'back '
                                                                                                              'and '
                                                                                                              'pass '
                                                                                                              'again.'}]},
                                 'hockey_center_midfielder_alone_figure_8_dribbling': {'key': 'hockey_center_midfielder_alone_figure_8_dribbling',
                                                                                       'sport': 'Hockey',
                                                                                       'title': 'Figure-8 '
                                                                                                'Dribbling',
                                                                                       'category': 'center_midfielder',
                                                                                       'training_mode': 'alone',
                                                                                       'level': 'all_levels',
                                                                                       'focus': 'center '
                                                                                                'midfielder',
                                                                                       'exercises': [{'name': 'Figure-8 '
                                                                                                              'Dribbling',
                                                                                                      'prescription': '5 '
                                                                                                                      'x '
                                                                                                                      '60 '
                                                                                                                      'seconds',
                                                                                                      'notes': 'Place '
                                                                                                               'two '
                                                                                                               'cones '
                                                                                                               '2m '
                                                                                                               'apart. '
                                                                                                               'Dribble '
                                                                                                               'around '
                                                                                                               'both '
                                                                                                               'in '
                                                                                                               'a '
                                                                                                               'figure-8.'}]},
                                 'hockey_center_midfielder_alone_end_to_end_carry': {'key': 'hockey_center_midfielder_alone_end_to_end_carry',
                                                                                     'sport': 'Hockey',
                                                                                     'title': 'End-to-End '
                                                                                              'Carry',
                                                                                     'category': 'center_midfielder',
                                                                                     'training_mode': 'alone',
                                                                                     'level': 'all_levels',
                                                                                     'focus': 'center '
                                                                                              'midfielder',
                                                                                     'exercises': [{'name': 'End-to-End '
                                                                                                            'Carry',
                                                                                                    'prescription': '10 '
                                                                                                                    'reps',
                                                                                                    'notes': 'Dribble '
                                                                                                             'ball '
                                                                                                             '30m. '
                                                                                                             'Turn. '
                                                                                                             'Return '
                                                                                                             'while '
                                                                                                             'maintaining '
                                                                                                             'control.'}]},
                                 'hockey_center_midfielder_alone_four_corner_passing': {'key': 'hockey_center_midfielder_alone_four_corner_passing',
                                                                                        'sport': 'Hockey',
                                                                                        'title': 'Four-Corner '
                                                                                                 'Passing',
                                                                                        'category': 'center_midfielder',
                                                                                        'training_mode': 'alone',
                                                                                        'level': 'all_levels',
                                                                                        'focus': 'center '
                                                                                                 'midfielder',
                                                                                        'exercises': [{'name': 'Four-Corner '
                                                                                                               'Passing',
                                                                                                       'prescription': '8 '
                                                                                                                       'rounds',
                                                                                                       'notes': 'Place '
                                                                                                                'four '
                                                                                                                'cones '
                                                                                                                'in '
                                                                                                                'a '
                                                                                                                'square. '
                                                                                                                'Dribble '
                                                                                                                'to '
                                                                                                                'each '
                                                                                                                'cone. '
                                                                                                                'Stop '
                                                                                                                'ball '
                                                                                                                'at '
                                                                                                                'each '
                                                                                                                'cone.'}]},
                                 'hockey_center_midfielder_alone_first_touch_control': {'key': 'hockey_center_midfielder_alone_first_touch_control',
                                                                                        'sport': 'Hockey',
                                                                                        'title': 'First '
                                                                                                 'Touch '
                                                                                                 'Control',
                                                                                        'category': 'center_midfielder',
                                                                                        'training_mode': 'alone',
                                                                                        'level': 'all_levels',
                                                                                        'focus': 'center '
                                                                                                 'midfielder',
                                                                                        'exercises': [{'name': 'First '
                                                                                                               'Touch '
                                                                                                               'Control',
                                                                                                       'prescription': '100 '
                                                                                                                       'reps',
                                                                                                       'notes': 'Pass '
                                                                                                                'against '
                                                                                                                'wall. '
                                                                                                                'Stop '
                                                                                                                'ball '
                                                                                                                'within '
                                                                                                                'one '
                                                                                                                'stick '
                                                                                                                'length. '
                                                                                                                'Repeat.'}]},
                                 'hockey_center_midfielder_alone_long_passing_accuracy': {'key': 'hockey_center_midfielder_alone_long_passing_accuracy',
                                                                                          'sport': 'Hockey',
                                                                                          'title': 'Long '
                                                                                                   'Passing '
                                                                                                   'Accuracy',
                                                                                          'category': 'center_midfielder',
                                                                                          'training_mode': 'alone',
                                                                                          'level': 'all_levels',
                                                                                          'focus': 'center '
                                                                                                   'midfielder',
                                                                                          'exercises': [{'name': 'Long '
                                                                                                                 'Passing '
                                                                                                                 'Accuracy',
                                                                                                         'prescription': '50 '
                                                                                                                         'passes',
                                                                                                         'notes': 'Target '
                                                                                                                  '20m '
                                                                                                                  'away. '
                                                                                                                  'Hit '
                                                                                                                  'target '
                                                                                                                  'cone.'}]},
                                 'hockey_center_midfielder_alone_sprint_pass_sprint': {'key': 'hockey_center_midfielder_alone_sprint_pass_sprint',
                                                                                       'sport': 'Hockey',
                                                                                       'title': 'Sprint-Pass-Sprint',
                                                                                       'category': 'center_midfielder',
                                                                                       'training_mode': 'alone',
                                                                                       'level': 'all_levels',
                                                                                       'focus': 'center '
                                                                                                'midfielder',
                                                                                       'exercises': [{'name': 'Sprint-Pass-Sprint',
                                                                                                      'prescription': '10 '
                                                                                                                      'reps',
                                                                                                      'notes': 'Sprint '
                                                                                                               '10m. '
                                                                                                               'Pass '
                                                                                                               'ball '
                                                                                                               'to '
                                                                                                               'wall. '
                                                                                                               'Receive. '
                                                                                                               'Sprint '
                                                                                                               'back.'}]},
                                 'hockey_center_midfielder_alone_cone_slalom_carry': {'key': 'hockey_center_midfielder_alone_cone_slalom_carry',
                                                                                      'sport': 'Hockey',
                                                                                      'title': 'Cone '
                                                                                               'Slalom '
                                                                                               'Carry',
                                                                                      'category': 'center_midfielder',
                                                                                      'training_mode': 'alone',
                                                                                      'level': 'all_levels',
                                                                                      'focus': 'center '
                                                                                               'midfielder',
                                                                                      'exercises': [{'name': 'Cone '
                                                                                                             'Slalom '
                                                                                                             'Carry',
                                                                                                     'prescription': '8 '
                                                                                                                     'rounds',
                                                                                                     'notes': 'Place '
                                                                                                              '8 '
                                                                                                              'cones '
                                                                                                              '2m '
                                                                                                              'apart. '
                                                                                                              'Dribble '
                                                                                                              'through '
                                                                                                              'all '
                                                                                                              'cones. '
                                                                                                              'Return.'}]},
                                 'hockey_center_midfielder_alone_30_second_possession_challenge': {'key': 'hockey_center_midfielder_alone_30_second_possession_challenge',
                                                                                                   'sport': 'Hockey',
                                                                                                   'title': '30-Second '
                                                                                                            'Possession '
                                                                                                            'Challenge',
                                                                                                   'category': 'center_midfielder',
                                                                                                   'training_mode': 'alone',
                                                                                                   'level': 'all_levels',
                                                                                                   'focus': 'center '
                                                                                                            'midfielder',
                                                                                                   'exercises': [{'name': '30-Second '
                                                                                                                          'Possession '
                                                                                                                          'Challenge',
                                                                                                                  'prescription': '6 '
                                                                                                                                  'rounds',
                                                                                                                  'notes': 'Stay '
                                                                                                                           'inside '
                                                                                                                           'a '
                                                                                                                           '5m '
                                                                                                                           'square. '
                                                                                                                           'Keep '
                                                                                                                           'ball '
                                                                                                                           'moving '
                                                                                                                           'continuously.'}]},
                                 'hockey_center_midfielder_alone_shuttle_conditioning': {'key': 'hockey_center_midfielder_alone_shuttle_conditioning',
                                                                                         'sport': 'Hockey',
                                                                                         'title': 'Shuttle '
                                                                                                  'Conditioning',
                                                                                         'category': 'center_midfielder',
                                                                                         'training_mode': 'alone',
                                                                                         'level': 'all_levels',
                                                                                         'focus': 'center '
                                                                                                  'midfielder',
                                                                                         'exercises': [{'name': 'Shuttle '
                                                                                                                'Conditioning',
                                                                                                        'prescription': '6 '
                                                                                                                        'rounds',
                                                                                                        'notes': 'Run '
                                                                                                                 '10m '
                                                                                                                 'and '
                                                                                                                 'back. '
                                                                                                                 'Run '
                                                                                                                 '20m '
                                                                                                                 'and '
                                                                                                                 'back. '
                                                                                                                 'Run '
                                                                                                                 '30m '
                                                                                                                 'and '
                                                                                                                 'back.'}]},
                                 'hockey_center_midfielder_alone_midfielder_circuit': {'key': 'hockey_center_midfielder_alone_midfielder_circuit',
                                                                                       'sport': 'Hockey',
                                                                                       'title': 'Midfielder '
                                                                                                'Circuit',
                                                                                       'category': 'center_midfielder',
                                                                                       'training_mode': 'alone',
                                                                                       'level': 'all_levels',
                                                                                       'focus': 'center '
                                                                                                'midfielder',
                                                                                       'exercises': [{'name': 'Midfielder '
                                                                                                              'Circuit',
                                                                                                      'prescription': '5 '
                                                                                                                      'rounds',
                                                                                                      'notes': 'Dribble '
                                                                                                               '20m. '
                                                                                                               'Pass '
                                                                                                               'to '
                                                                                                               'wall. '
                                                                                                               'Receive. '
                                                                                                               'Sprint '
                                                                                                               '20m. '
                                                                                                               'Repeat.'}]}},
                       'with_others': {'hockey_center_midfielder_with_others_one_touch_passing_circle': {'key': 'hockey_center_midfielder_with_others_one_touch_passing_circle',
                                                                                                         'sport': 'Hockey',
                                                                                                         'title': 'One-Touch '
                                                                                                                  'Passing '
                                                                                                                  'Circle',
                                                                                                         'category': 'center_midfielder',
                                                                                                         'training_mode': 'with_others',
                                                                                                         'level': 'all_levels',
                                                                                                         'focus': 'center '
                                                                                                                  'midfielder',
                                                                                                         'exercises': [{'name': 'One-Touch '
                                                                                                                                'Passing '
                                                                                                                                'Circle',
                                                                                                                        'prescription': '100 '
                                                                                                                                        'passes',
                                                                                                                        'notes': 'Three '
                                                                                                                                 'players '
                                                                                                                                 'form '
                                                                                                                                 'triangle. '
                                                                                                                                 'Pass '
                                                                                                                                 'using '
                                                                                                                                 'one '
                                                                                                                                 'touch '
                                                                                                                                 'only.'}]},
                                       'hockey_center_midfielder_with_others_pass_and_move': {'key': 'hockey_center_midfielder_with_others_pass_and_move',
                                                                                              'sport': 'Hockey',
                                                                                              'title': 'Pass '
                                                                                                       'and '
                                                                                                       'Move',
                                                                                              'category': 'center_midfielder',
                                                                                              'training_mode': 'with_others',
                                                                                              'level': 'all_levels',
                                                                                              'focus': 'center '
                                                                                                       'midfielder',
                                                                                              'exercises': [{'name': 'Pass '
                                                                                                                     'and '
                                                                                                                     'Move',
                                                                                                             'prescription': '30 '
                                                                                                                             'reps',
                                                                                                             'notes': 'Pass '
                                                                                                                      'to '
                                                                                                                      'teammate. '
                                                                                                                      'Sprint '
                                                                                                                      'to '
                                                                                                                      'new '
                                                                                                                      'cone. '
                                                                                                                      'Receive '
                                                                                                                      'next '
                                                                                                                      'pass.'}]},
                                       'hockey_center_midfielder_with_others_triangle_possession': {'key': 'hockey_center_midfielder_with_others_triangle_possession',
                                                                                                    'sport': 'Hockey',
                                                                                                    'title': 'Triangle '
                                                                                                             'Possession',
                                                                                                    'category': 'center_midfielder',
                                                                                                    'training_mode': 'with_others',
                                                                                                    'level': 'all_levels',
                                                                                                    'focus': 'center '
                                                                                                             'midfielder',
                                                                                                    'exercises': [{'name': 'Triangle '
                                                                                                                           'Possession',
                                                                                                                   'prescription': '5 '
                                                                                                                                   'x '
                                                                                                                                   '60 '
                                                                                                                                   'seconds',
                                                                                                                   'notes': 'Three '
                                                                                                                            'players '
                                                                                                                            'maintain '
                                                                                                                            'possession. '
                                                                                                                            'No '
                                                                                                                            'player '
                                                                                                                            'stationary.'}]},
                                       'hockey_center_midfielder_with_others_long_pass_exchange': {'key': 'hockey_center_midfielder_with_others_long_pass_exchange',
                                                                                                   'sport': 'Hockey',
                                                                                                   'title': 'Long '
                                                                                                            'Pass '
                                                                                                            'Exchange',
                                                                                                   'category': 'center_midfielder',
                                                                                                   'training_mode': 'with_others',
                                                                                                   'level': 'all_levels',
                                                                                                   'focus': 'center '
                                                                                                            'midfielder',
                                                                                                   'exercises': [{'name': 'Long '
                                                                                                                          'Pass '
                                                                                                                          'Exchange',
                                                                                                                  'prescription': '50 '
                                                                                                                                  'passes '
                                                                                                                                  'each',
                                                                                                                  'notes': 'Partners '
                                                                                                                           'stand '
                                                                                                                           '20m '
                                                                                                                           'apart. '
                                                                                                                           'Exchange '
                                                                                                                           'passes.'}]},
                                       'hockey_center_midfielder_with_others_through_ball_practice': {'key': 'hockey_center_midfielder_with_others_through_ball_practice',
                                                                                                      'sport': 'Hockey',
                                                                                                      'title': 'Through '
                                                                                                               'Ball '
                                                                                                               'Practice',
                                                                                                      'category': 'center_midfielder',
                                                                                                      'training_mode': 'with_others',
                                                                                                      'level': 'all_levels',
                                                                                                      'focus': 'center '
                                                                                                               'midfielder',
                                                                                                      'exercises': [{'name': 'Through '
                                                                                                                             'Ball '
                                                                                                                             'Practice',
                                                                                                                     'prescription': '30 '
                                                                                                                                     'reps',
                                                                                                                     'notes': 'One '
                                                                                                                              'player '
                                                                                                                              'runs. '
                                                                                                                              'Other '
                                                                                                                              'player '
                                                                                                                              'passes '
                                                                                                                              'into '
                                                                                                                              'space.'}]},
                                       'hockey_center_midfielder_with_others_receive_under_pressure': {'key': 'hockey_center_midfielder_with_others_receive_under_pressure',
                                                                                                       'sport': 'Hockey',
                                                                                                       'title': 'Receive '
                                                                                                                'Under '
                                                                                                                'Pressure',
                                                                                                       'category': 'center_midfielder',
                                                                                                       'training_mode': 'with_others',
                                                                                                       'level': 'all_levels',
                                                                                                       'focus': 'center '
                                                                                                                'midfielder',
                                                                                                       'exercises': [{'name': 'Receive '
                                                                                                                              'Under '
                                                                                                                              'Pressure',
                                                                                                                      'prescription': '20 '
                                                                                                                                      'reps',
                                                                                                                      'notes': 'Teammate '
                                                                                                                               'passes. '
                                                                                                                               'Defender '
                                                                                                                               'pressures '
                                                                                                                               'immediately.'}]},
                                       'hockey_center_midfielder_with_others_switch_play_drill': {'key': 'hockey_center_midfielder_with_others_switch_play_drill',
                                                                                                  'sport': 'Hockey',
                                                                                                  'title': 'Switch '
                                                                                                           'Play '
                                                                                                           'Drill',
                                                                                                  'category': 'center_midfielder',
                                                                                                  'training_mode': 'with_others',
                                                                                                  'level': 'all_levels',
                                                                                                  'focus': 'center '
                                                                                                           'midfielder',
                                                                                                  'exercises': [{'name': 'Switch '
                                                                                                                         'Play '
                                                                                                                         'Drill',
                                                                                                                 'prescription': '30 '
                                                                                                                                 'passes',
                                                                                                                 'notes': 'Pass '
                                                                                                                          'from '
                                                                                                                          'one '
                                                                                                                          'side '
                                                                                                                          'of '
                                                                                                                          'field '
                                                                                                                          'to '
                                                                                                                          'other. '
                                                                                                                          'Control '
                                                                                                                          'and '
                                                                                                                          'return.'}]},
                                       'hockey_center_midfielder_with_others_four_player_passing_square': {'key': 'hockey_center_midfielder_with_others_four_player_passing_square',
                                                                                                           'sport': 'Hockey',
                                                                                                           'title': 'Four '
                                                                                                                    'Player '
                                                                                                                    'Passing '
                                                                                                                    'Square',
                                                                                                           'category': 'center_midfielder',
                                                                                                           'training_mode': 'with_others',
                                                                                                           'level': 'all_levels',
                                                                                                           'focus': 'center '
                                                                                                                    'midfielder',
                                                                                                           'exercises': [{'name': 'Four '
                                                                                                                                  'Player '
                                                                                                                                  'Passing '
                                                                                                                                  'Square',
                                                                                                                          'prescription': '10 '
                                                                                                                                          'minutes',
                                                                                                                          'notes': 'Four '
                                                                                                                                   'players '
                                                                                                                                   'on '
                                                                                                                                   'square '
                                                                                                                                   'corners. '
                                                                                                                                   'Follow '
                                                                                                                                   'every '
                                                                                                                                   'pass.'}]},
                                       'hockey_center_midfielder_with_others_possession_box': {'key': 'hockey_center_midfielder_with_others_possession_box',
                                                                                               'sport': 'Hockey',
                                                                                               'title': 'Possession '
                                                                                                        'Box',
                                                                                               'category': 'center_midfielder',
                                                                                               'training_mode': 'with_others',
                                                                                               'level': 'all_levels',
                                                                                               'focus': 'center '
                                                                                                        'midfielder',
                                                                                               'exercises': [{'name': 'Possession '
                                                                                                                      'Box',
                                                                                                              'prescription': '5 '
                                                                                                                              'x '
                                                                                                                              '60 '
                                                                                                                              'seconds',
                                                                                                              'notes': '3 '
                                                                                                                       'attackers '
                                                                                                                       'vs '
                                                                                                                       '1 '
                                                                                                                       'defender. '
                                                                                                                       'Maintain '
                                                                                                                       'possession.'}]},
                                       'hockey_center_midfielder_with_others_midfield_shuttle_passing': {'key': 'hockey_center_midfielder_with_others_midfield_shuttle_passing',
                                                                                                         'sport': 'Hockey',
                                                                                                         'title': 'Midfield '
                                                                                                                  'Shuttle '
                                                                                                                  'Passing',
                                                                                                         'category': 'center_midfielder',
                                                                                                         'training_mode': 'with_others',
                                                                                                         'level': 'all_levels',
                                                                                                         'focus': 'center '
                                                                                                                  'midfielder',
                                                                                                         'exercises': [{'name': 'Midfield '
                                                                                                                                'Shuttle '
                                                                                                                                'Passing',
                                                                                                                        'prescription': '20 '
                                                                                                                                        'reps',
                                                                                                                        'notes': 'Sprint '
                                                                                                                                 '15m. '
                                                                                                                                 'Receive '
                                                                                                                                 'pass. '
                                                                                                                                 'Pass '
                                                                                                                                 'to '
                                                                                                                                 'teammate. '
                                                                                                                                 'Sprint '
                                                                                                                                 'back.'}]},
                                       'hockey_center_midfielder_with_others_quick_combination_passing': {'key': 'hockey_center_midfielder_with_others_quick_combination_passing',
                                                                                                          'sport': 'Hockey',
                                                                                                          'title': 'Quick '
                                                                                                                   'Combination '
                                                                                                                   'Passing',
                                                                                                          'category': 'center_midfielder',
                                                                                                          'training_mode': 'with_others',
                                                                                                          'level': 'all_levels',
                                                                                                          'focus': 'center '
                                                                                                                   'midfielder',
                                                                                                          'exercises': [{'name': 'Quick '
                                                                                                                                 'Combination '
                                                                                                                                 'Passing',
                                                                                                                         'prescription': '5 '
                                                                                                                                         'minutes',
                                                                                                                         'notes': 'Three '
                                                                                                                                  'players. '
                                                                                                                                  'Pass-pass-pass '
                                                                                                                                  'sequence. '
                                                                                                                                  'Repeat '
                                                                                                                                  'continuously.'}]},
                                       'hockey_center_midfielder_with_others_midfielder_game_simulation': {'key': 'hockey_center_midfielder_with_others_midfielder_game_simulation',
                                                                                                           'sport': 'Hockey',
                                                                                                           'title': 'Midfielder '
                                                                                                                    'Game '
                                                                                                                    'Simulation',
                                                                                                           'category': 'center_midfielder',
                                                                                                           'training_mode': 'with_others',
                                                                                                           'level': 'all_levels',
                                                                                                           'focus': 'center '
                                                                                                                    'midfielder',
                                                                                                           'exercises': [{'name': 'Midfielder '
                                                                                                                                  'Game '
                                                                                                                                  'Simulation',
                                                                                                                          'prescription': '5 '
                                                                                                                                          'rounds',
                                                                                                                          'notes': 'Continuous '
                                                                                                                                   'transition '
                                                                                                                                   'play. '
                                                                                                                                   '60-second '
                                                                                                                                   'rounds.'}]}}},
 'attacker_winger': {'alone': {'hockey_attacker_winger_alone_sprint_dribble_attack': {'key': 'hockey_attacker_winger_alone_sprint_dribble_attack',
                                                                                      'sport': 'Hockey',
                                                                                      'title': 'Sprint '
                                                                                               'Dribble '
                                                                                               'Attack',
                                                                                      'category': 'attacker_winger',
                                                                                      'training_mode': 'alone',
                                                                                      'level': 'all_levels',
                                                                                      'focus': 'attacker '
                                                                                               'winger',
                                                                                      'exercises': [{'name': 'Sprint '
                                                                                                             'Dribble '
                                                                                                             'Attack',
                                                                                                     'prescription': '10 '
                                                                                                                     'reps',
                                                                                                     'notes': 'Dribble '
                                                                                                              'ball '
                                                                                                              '30m '
                                                                                                              'at '
                                                                                                              'maximum '
                                                                                                              'speed. '
                                                                                                              'Walk '
                                                                                                              'back.'}]},
                               'hockey_attacker_winger_alone_cone_slalom_finish': {'key': 'hockey_attacker_winger_alone_cone_slalom_finish',
                                                                                   'sport': 'Hockey',
                                                                                   'title': 'Cone '
                                                                                            'Slalom '
                                                                                            'Finish',
                                                                                   'category': 'attacker_winger',
                                                                                   'training_mode': 'alone',
                                                                                   'level': 'all_levels',
                                                                                   'focus': 'attacker '
                                                                                            'winger',
                                                                                   'exercises': [{'name': 'Cone '
                                                                                                          'Slalom '
                                                                                                          'Finish',
                                                                                                  'prescription': '20 '
                                                                                                                  'reps',
                                                                                                  'notes': 'Dribble '
                                                                                                           'through '
                                                                                                           '6 '
                                                                                                           'cones. '
                                                                                                           'Shoot '
                                                                                                           'immediately '
                                                                                                           'after '
                                                                                                           'final '
                                                                                                           'cone.'}]},
                               'hockey_attacker_winger_alone_baseline_attack_run': {'key': 'hockey_attacker_winger_alone_baseline_attack_run',
                                                                                    'sport': 'Hockey',
                                                                                    'title': 'Baseline '
                                                                                             'Attack '
                                                                                             'Run',
                                                                                    'category': 'attacker_winger',
                                                                                    'training_mode': 'alone',
                                                                                    'level': 'all_levels',
                                                                                    'focus': 'attacker '
                                                                                             'winger',
                                                                                    'exercises': [{'name': 'Baseline '
                                                                                                           'Attack '
                                                                                                           'Run',
                                                                                                   'prescription': '15 '
                                                                                                                   'reps',
                                                                                                   'notes': 'Start '
                                                                                                            'on '
                                                                                                            'sideline. '
                                                                                                            'Sprint '
                                                                                                            '25m '
                                                                                                            'with '
                                                                                                            'ball. '
                                                                                                            'Shoot.'}]},
                               'hockey_attacker_winger_alone_cut_inside_and_shoot': {'key': 'hockey_attacker_winger_alone_cut_inside_and_shoot',
                                                                                     'sport': 'Hockey',
                                                                                     'title': 'Cut '
                                                                                              'Inside '
                                                                                              'and '
                                                                                              'Shoot',
                                                                                     'category': 'attacker_winger',
                                                                                     'training_mode': 'alone',
                                                                                     'level': 'all_levels',
                                                                                     'focus': 'attacker '
                                                                                              'winger',
                                                                                     'exercises': [{'name': 'Cut '
                                                                                                            'Inside '
                                                                                                            'and '
                                                                                                            'Shoot',
                                                                                                    'prescription': '20 '
                                                                                                                    'reps',
                                                                                                    'notes': 'Dribble '
                                                                                                             '10m '
                                                                                                             'wide. '
                                                                                                             'Cut '
                                                                                                             'sharply '
                                                                                                             'inside '
                                                                                                             'around '
                                                                                                             'cone. '
                                                                                                             'Shoot.'}]},
                               'hockey_attacker_winger_alone_quick_release_shooting': {'key': 'hockey_attacker_winger_alone_quick_release_shooting',
                                                                                       'sport': 'Hockey',
                                                                                       'title': 'Quick '
                                                                                                'Release '
                                                                                                'Shooting',
                                                                                       'category': 'attacker_winger',
                                                                                       'training_mode': 'alone',
                                                                                       'level': 'all_levels',
                                                                                       'focus': 'attacker '
                                                                                                'winger',
                                                                                       'exercises': [{'name': 'Quick '
                                                                                                              'Release '
                                                                                                              'Shooting',
                                                                                                      'prescription': '2 '
                                                                                                                      'rounds',
                                                                                                      'notes': 'Place '
                                                                                                               '20 '
                                                                                                               'balls '
                                                                                                               'around '
                                                                                                               'shooting '
                                                                                                               'area. '
                                                                                                               'Shoot '
                                                                                                               'each '
                                                                                                               'ball '
                                                                                                               'immediately.'}]},
                               'hockey_attacker_winger_alone_reverse_direction_dribble': {'key': 'hockey_attacker_winger_alone_reverse_direction_dribble',
                                                                                          'sport': 'Hockey',
                                                                                          'title': 'Reverse '
                                                                                                   'Direction '
                                                                                                   'Dribble',
                                                                                          'category': 'attacker_winger',
                                                                                          'training_mode': 'alone',
                                                                                          'level': 'all_levels',
                                                                                          'focus': 'attacker '
                                                                                                   'winger',
                                                                                          'exercises': [{'name': 'Reverse '
                                                                                                                 'Direction '
                                                                                                                 'Dribble',
                                                                                                         'prescription': '15 '
                                                                                                                         'reps',
                                                                                                         'notes': 'Dribble '
                                                                                                                  '15m '
                                                                                                                  'forward. '
                                                                                                                  'Pull '
                                                                                                                  'ball '
                                                                                                                  'backward. '
                                                                                                                  'Change '
                                                                                                                  'direction. '
                                                                                                                  'Return.'}]},
                               'hockey_attacker_winger_alone_acceleration_sprint': {'key': 'hockey_attacker_winger_alone_acceleration_sprint',
                                                                                    'sport': 'Hockey',
                                                                                    'title': 'Acceleration '
                                                                                             'Sprint',
                                                                                    'category': 'attacker_winger',
                                                                                    'training_mode': 'alone',
                                                                                    'level': 'all_levels',
                                                                                    'focus': 'attacker '
                                                                                             'winger',
                                                                                    'exercises': [{'name': 'Acceleration '
                                                                                                           'Sprint',
                                                                                                   'prescription': '10 '
                                                                                                                   'reps',
                                                                                                   'notes': 'Sprint '
                                                                                                            '15m '
                                                                                                            'from '
                                                                                                            'standing '
                                                                                                            'start. '
                                                                                                            'Walk '
                                                                                                            'back.'}]},
                               'hockey_attacker_winger_alone_figure_8_attack_moves': {'key': 'hockey_attacker_winger_alone_figure_8_attack_moves',
                                                                                      'sport': 'Hockey',
                                                                                      'title': 'Figure-8 '
                                                                                               'Attack '
                                                                                               'Moves',
                                                                                      'category': 'attacker_winger',
                                                                                      'training_mode': 'alone',
                                                                                      'level': 'all_levels',
                                                                                      'focus': 'attacker '
                                                                                               'winger',
                                                                                      'exercises': [{'name': 'Figure-8 '
                                                                                                             'Attack '
                                                                                                             'Moves',
                                                                                                     'prescription': '8 '
                                                                                                                     'rounds',
                                                                                                     'notes': 'Place '
                                                                                                              'two '
                                                                                                              'cones '
                                                                                                              '3m '
                                                                                                              'apart. '
                                                                                                              'Dribble '
                                                                                                              'figure-8 '
                                                                                                              'pattern. '
                                                                                                              'Perform '
                                                                                                              'a '
                                                                                                              'fake '
                                                                                                              'at '
                                                                                                              'each '
                                                                                                              'cone.'}]},
                               'hockey_attacker_winger_alone_fast_break_run': {'key': 'hockey_attacker_winger_alone_fast_break_run',
                                                                               'sport': 'Hockey',
                                                                               'title': 'Fast '
                                                                                        'Break Run',
                                                                               'category': 'attacker_winger',
                                                                               'training_mode': 'alone',
                                                                               'level': 'all_levels',
                                                                               'focus': 'attacker '
                                                                                        'winger',
                                                                               'exercises': [{'name': 'Fast '
                                                                                                      'Break '
                                                                                                      'Run',
                                                                                              'prescription': '10 '
                                                                                                              'reps',
                                                                                              'notes': 'Sprint '
                                                                                                       '40m '
                                                                                                       'while '
                                                                                                       'dribbling. '
                                                                                                       'Finish '
                                                                                                       'with '
                                                                                                       'shot.'}]},
                               'hockey_attacker_winger_alone_shooting_accuracy_challenge': {'key': 'hockey_attacker_winger_alone_shooting_accuracy_challenge',
                                                                                            'sport': 'Hockey',
                                                                                            'title': 'Shooting '
                                                                                                     'Accuracy '
                                                                                                     'Challenge',
                                                                                            'category': 'attacker_winger',
                                                                                            'training_mode': 'alone',
                                                                                            'level': 'all_levels',
                                                                                            'focus': 'attacker '
                                                                                                     'winger',
                                                                                            'exercises': [{'name': 'Shooting '
                                                                                                                   'Accuracy '
                                                                                                                   'Challenge',
                                                                                                           'prescription': '40 '
                                                                                                                           'shots',
                                                                                                           'notes': 'Place '
                                                                                                                    '4 '
                                                                                                                    'targets '
                                                                                                                    'inside '
                                                                                                                    'goal. '
                                                                                                                    'Hit '
                                                                                                                    'each '
                                                                                                                    'target '
                                                                                                                    '10 '
                                                                                                                    'times.'}]},
                               'hockey_attacker_winger_alone_1v0_attack_simulation': {'key': 'hockey_attacker_winger_alone_1v0_attack_simulation',
                                                                                      'sport': 'Hockey',
                                                                                      'title': '1v0 '
                                                                                               'Attack '
                                                                                               'Simulation',
                                                                                      'category': 'attacker_winger',
                                                                                      'training_mode': 'alone',
                                                                                      'level': 'all_levels',
                                                                                      'focus': 'attacker '
                                                                                               'winger',
                                                                                      'exercises': [{'name': '1v0 '
                                                                                                             'Attack '
                                                                                                             'Simulation',
                                                                                                     'prescription': '20 '
                                                                                                                     'reps',
                                                                                                     'notes': 'Dribble '
                                                                                                              'from '
                                                                                                              'midfield. '
                                                                                                              'Perform '
                                                                                                              'one '
                                                                                                              'fake '
                                                                                                              'move '
                                                                                                              'at '
                                                                                                              'cone. '
                                                                                                              'Finish '
                                                                                                              'with '
                                                                                                              'shot.'}]},
                               'hockey_attacker_winger_alone_winger_circuit': {'key': 'hockey_attacker_winger_alone_winger_circuit',
                                                                               'sport': 'Hockey',
                                                                               'title': 'Winger '
                                                                                        'Circuit',
                                                                               'category': 'attacker_winger',
                                                                               'training_mode': 'alone',
                                                                               'level': 'all_levels',
                                                                               'focus': 'attacker '
                                                                                        'winger',
                                                                               'exercises': [{'name': 'Winger '
                                                                                                      'Circuit',
                                                                                              'prescription': '8 '
                                                                                                              'rounds',
                                                                                              'notes': 'Sprint '
                                                                                                       '20m. '
                                                                                                       'Dribble '
                                                                                                       'through '
                                                                                                       '4 '
                                                                                                       'cones. '
                                                                                                       'Shoot. '
                                                                                                       'Jog '
                                                                                                       'back.'}]}},
                     'with_others': {'hockey_attacker_winger_with_others_give_and_go_attack': {'key': 'hockey_attacker_winger_with_others_give_and_go_attack',
                                                                                               'sport': 'Hockey',
                                                                                               'title': 'Give-and-Go '
                                                                                                        'Attack',
                                                                                               'category': 'attacker_winger',
                                                                                               'training_mode': 'with_others',
                                                                                               'level': 'all_levels',
                                                                                               'focus': 'attacker '
                                                                                                        'winger',
                                                                                               'exercises': [{'name': 'Give-and-Go '
                                                                                                                      'Attack',
                                                                                                              'prescription': '20 '
                                                                                                                              'reps',
                                                                                                              'notes': 'Pass '
                                                                                                                       'to '
                                                                                                                       'teammate. '
                                                                                                                       'Sprint '
                                                                                                                       'around '
                                                                                                                       'cone. '
                                                                                                                       'Receive '
                                                                                                                       'return '
                                                                                                                       'pass. '
                                                                                                                       'Shoot.'}]},
                                     'hockey_attacker_winger_with_others_crossing_and_finish': {'key': 'hockey_attacker_winger_with_others_crossing_and_finish',
                                                                                                'sport': 'Hockey',
                                                                                                'title': 'Crossing '
                                                                                                         'and '
                                                                                                         'Finish',
                                                                                                'category': 'attacker_winger',
                                                                                                'training_mode': 'with_others',
                                                                                                'level': 'all_levels',
                                                                                                'focus': 'attacker '
                                                                                                         'winger',
                                                                                                'exercises': [{'name': 'Crossing '
                                                                                                                       'and '
                                                                                                                       'Finish',
                                                                                                               'prescription': '20 '
                                                                                                                               'reps',
                                                                                                               'notes': 'Winger '
                                                                                                                        'dribbles '
                                                                                                                        'down '
                                                                                                                        'sideline. '
                                                                                                                        'Passes '
                                                                                                                        'across '
                                                                                                                        'goal. '
                                                                                                                        'Attacker '
                                                                                                                        'finishes.'}]},
                                     'hockey_attacker_winger_with_others_through_ball_finish': {'key': 'hockey_attacker_winger_with_others_through_ball_finish',
                                                                                                'sport': 'Hockey',
                                                                                                'title': 'Through '
                                                                                                         'Ball '
                                                                                                         'Finish',
                                                                                                'category': 'attacker_winger',
                                                                                                'training_mode': 'with_others',
                                                                                                'level': 'all_levels',
                                                                                                'focus': 'attacker '
                                                                                                         'winger',
                                                                                                'exercises': [{'name': 'Through '
                                                                                                                       'Ball '
                                                                                                                       'Finish',
                                                                                                               'prescription': '20 '
                                                                                                                               'reps',
                                                                                                               'notes': 'Teammate '
                                                                                                                        'plays '
                                                                                                                        'through '
                                                                                                                        'ball. '
                                                                                                                        'Attacker '
                                                                                                                        'runs '
                                                                                                                        'onto '
                                                                                                                        'it. '
                                                                                                                        'Shoots.'}]},
                                     'hockey_attacker_winger_with_others_1v1_attack': {'key': 'hockey_attacker_winger_with_others_1v1_attack',
                                                                                       'sport': 'Hockey',
                                                                                       'title': '1v1 '
                                                                                                'Attack',
                                                                                       'category': 'attacker_winger',
                                                                                       'training_mode': 'with_others',
                                                                                       'level': 'all_levels',
                                                                                       'focus': 'attacker '
                                                                                                'winger',
                                                                                       'exercises': [{'name': '1v1 '
                                                                                                              'Attack',
                                                                                                      'prescription': '15 '
                                                                                                                      'reps '
                                                                                                                      'each',
                                                                                                      'notes': 'Defender '
                                                                                                               'starts '
                                                                                                               '5m '
                                                                                                               'away. '
                                                                                                               'Attacker '
                                                                                                               'attempts '
                                                                                                               'to '
                                                                                                               'beat '
                                                                                                               'defender.'}]},
                                     'hockey_attacker_winger_with_others_fast_break_attack': {'key': 'hockey_attacker_winger_with_others_fast_break_attack',
                                                                                              'sport': 'Hockey',
                                                                                              'title': 'Fast '
                                                                                                       'Break '
                                                                                                       'Attack',
                                                                                              'category': 'attacker_winger',
                                                                                              'training_mode': 'with_others',
                                                                                              'level': 'all_levels',
                                                                                              'focus': 'attacker '
                                                                                                       'winger',
                                                                                              'exercises': [{'name': 'Fast '
                                                                                                                     'Break '
                                                                                                                     'Attack',
                                                                                                             'prescription': '15 '
                                                                                                                             'reps',
                                                                                                             'notes': 'Two '
                                                                                                                      'attackers '
                                                                                                                      'sprint '
                                                                                                                      'from '
                                                                                                                      'midfield. '
                                                                                                                      'Finish '
                                                                                                                      'attack '
                                                                                                                      'within '
                                                                                                                      '10 '
                                                                                                                      'seconds.'}]},
                                     'hockey_attacker_winger_with_others_rebound_finishing': {'key': 'hockey_attacker_winger_with_others_rebound_finishing',
                                                                                              'sport': 'Hockey',
                                                                                              'title': 'Rebound '
                                                                                                       'Finishing',
                                                                                              'category': 'attacker_winger',
                                                                                              'training_mode': 'with_others',
                                                                                              'level': 'all_levels',
                                                                                              'focus': 'attacker '
                                                                                                       'winger',
                                                                                              'exercises': [{'name': 'Rebound '
                                                                                                                     'Finishing',
                                                                                                             'prescription': '20 '
                                                                                                                             'reps',
                                                                                                             'notes': 'First '
                                                                                                                      'player '
                                                                                                                      'shoots. '
                                                                                                                      'Second '
                                                                                                                      'player '
                                                                                                                      'finishes '
                                                                                                                      'rebound.'}]},
                                     'hockey_attacker_winger_with_others_overlap_run': {'key': 'hockey_attacker_winger_with_others_overlap_run',
                                                                                        'sport': 'Hockey',
                                                                                        'title': 'Overlap '
                                                                                                 'Run',
                                                                                        'category': 'attacker_winger',
                                                                                        'training_mode': 'with_others',
                                                                                        'level': 'all_levels',
                                                                                        'focus': 'attacker '
                                                                                                 'winger',
                                                                                        'exercises': [{'name': 'Overlap '
                                                                                                               'Run',
                                                                                                       'prescription': '15 '
                                                                                                                       'reps',
                                                                                                       'notes': 'Winger '
                                                                                                                'passes. '
                                                                                                                'Teammate '
                                                                                                                'overlaps '
                                                                                                                'outside. '
                                                                                                                'Return '
                                                                                                                'pass '
                                                                                                                'and '
                                                                                                                'cross.'}]},
                                     'hockey_attacker_winger_with_others_quick_shot_challenge': {'key': 'hockey_attacker_winger_with_others_quick_shot_challenge',
                                                                                                 'sport': 'Hockey',
                                                                                                 'title': 'Quick '
                                                                                                          'Shot '
                                                                                                          'Challenge',
                                                                                                 'category': 'attacker_winger',
                                                                                                 'training_mode': 'with_others',
                                                                                                 'level': 'all_levels',
                                                                                                 'focus': 'attacker '
                                                                                                          'winger',
                                                                                                 'exercises': [{'name': 'Quick '
                                                                                                                        'Shot '
                                                                                                                        'Challenge',
                                                                                                                'prescription': '30 '
                                                                                                                                'shots',
                                                                                                                'notes': 'Receive '
                                                                                                                         'pass. '
                                                                                                                         'Shoot '
                                                                                                                         'within '
                                                                                                                         '2 '
                                                                                                                         'seconds.'}]},
                                     'hockey_attacker_winger_with_others_2v1_attack': {'key': 'hockey_attacker_winger_with_others_2v1_attack',
                                                                                       'sport': 'Hockey',
                                                                                       'title': '2v1 '
                                                                                                'Attack',
                                                                                       'category': 'attacker_winger',
                                                                                       'training_mode': 'with_others',
                                                                                       'level': 'all_levels',
                                                                                       'focus': 'attacker '
                                                                                                'winger',
                                                                                       'exercises': [{'name': '2v1 '
                                                                                                              'Attack',
                                                                                                      'prescription': '15 '
                                                                                                                      'reps',
                                                                                                      'notes': 'Two '
                                                                                                               'attackers '
                                                                                                               'against '
                                                                                                               'one '
                                                                                                               'defender. '
                                                                                                               'Create '
                                                                                                               'shot '
                                                                                                               'opportunity.'}]},
                                     'hockey_attacker_winger_with_others_baseline_cutback': {'key': 'hockey_attacker_winger_with_others_baseline_cutback',
                                                                                             'sport': 'Hockey',
                                                                                             'title': 'Baseline '
                                                                                                      'Cutback',
                                                                                             'category': 'attacker_winger',
                                                                                             'training_mode': 'with_others',
                                                                                             'level': 'all_levels',
                                                                                             'focus': 'attacker '
                                                                                                      'winger',
                                                                                             'exercises': [{'name': 'Baseline '
                                                                                                                    'Cutback',
                                                                                                            'prescription': '20 '
                                                                                                                            'reps',
                                                                                                            'notes': 'Winger '
                                                                                                                     'reaches '
                                                                                                                     'baseline. '
                                                                                                                     'Cuts '
                                                                                                                     'ball '
                                                                                                                     'back. '
                                                                                                                     'Teammate '
                                                                                                                     'finishes.'}]},
                                     'hockey_attacker_winger_with_others_three_pass_goal_drill': {'key': 'hockey_attacker_winger_with_others_three_pass_goal_drill',
                                                                                                  'sport': 'Hockey',
                                                                                                  'title': 'Three-Pass '
                                                                                                           'Goal '
                                                                                                           'Drill',
                                                                                                  'category': 'attacker_winger',
                                                                                                  'training_mode': 'with_others',
                                                                                                  'level': 'all_levels',
                                                                                                  'focus': 'attacker '
                                                                                                           'winger',
                                                                                                  'exercises': [{'name': 'Three-Pass '
                                                                                                                         'Goal '
                                                                                                                         'Drill',
                                                                                                                 'prescription': '20 '
                                                                                                                                 'attacks',
                                                                                                                 'notes': 'Team '
                                                                                                                          'must '
                                                                                                                          'complete '
                                                                                                                          '3 '
                                                                                                                          'passes. '
                                                                                                                          'Then '
                                                                                                                          'shoot.'}]},
                                     'hockey_attacker_winger_with_others_attacker_match_simulation': {'key': 'hockey_attacker_winger_with_others_attacker_match_simulation',
                                                                                                      'sport': 'Hockey',
                                                                                                      'title': 'Attacker '
                                                                                                               'Match '
                                                                                                               'Simulation',
                                                                                                      'category': 'attacker_winger',
                                                                                                      'training_mode': 'with_others',
                                                                                                      'level': 'all_levels',
                                                                                                      'focus': 'attacker '
                                                                                                               'winger',
                                                                                                      'exercises': [{'name': 'Attacker '
                                                                                                                             'Match '
                                                                                                                             'Simulation',
                                                                                                                     'prescription': '5 '
                                                                                                                                     'rounds',
                                                                                                                     'notes': 'Continuous '
                                                                                                                              'attacking '
                                                                                                                              'against '
                                                                                                                              'defenders. '
                                                                                                                              '60-second '
                                                                                                                              'rounds.'}]}}},
 'learn_how_to_play': {'alone': {'hockey_learn_how_to_play_alone_basic_stick_grip': {'key': 'hockey_learn_how_to_play_alone_basic_stick_grip',
                                                                                     'sport': 'Hockey',
                                                                                     'title': 'Basic '
                                                                                              'Stick '
                                                                                              'Grip',
                                                                                     'category': 'learn_how_to_play',
                                                                                     'training_mode': 'alone',
                                                                                     'level': 'learn',
                                                                                     'focus': 'learn '
                                                                                              'how '
                                                                                              'to '
                                                                                              'play',
                                                                                     'exercises': [{'name': 'Basic '
                                                                                                            'Stick '
                                                                                                            'Grip',
                                                                                                    'prescription': '5 '
                                                                                                                    'minutes',
                                                                                                    'notes': 'Hold '
                                                                                                             'hockey '
                                                                                                             'stick '
                                                                                                             'correctly. '
                                                                                                             'Walk '
                                                                                                             'around '
                                                                                                             'field '
                                                                                                             'while '
                                                                                                             'carrying '
                                                                                                             'it.'}]},
                                 'hockey_learn_how_to_play_alone_stationary_ball_taps': {'key': 'hockey_learn_how_to_play_alone_stationary_ball_taps',
                                                                                         'sport': 'Hockey',
                                                                                         'title': 'Stationary '
                                                                                                  'Ball '
                                                                                                  'Taps',
                                                                                         'category': 'learn_how_to_play',
                                                                                         'training_mode': 'alone',
                                                                                         'level': 'learn',
                                                                                         'focus': 'learn '
                                                                                                  'how '
                                                                                                  'to '
                                                                                                  'play',
                                                                                         'exercises': [{'name': 'Stationary '
                                                                                                                'Ball '
                                                                                                                'Taps',
                                                                                                        'prescription': '3 '
                                                                                                                        'x '
                                                                                                                        '60 '
                                                                                                                        'seconds',
                                                                                                        'notes': 'Tap '
                                                                                                                 'ball '
                                                                                                                 'gently '
                                                                                                                 'left-right. '
                                                                                                                 'Keep '
                                                                                                                 'ball '
                                                                                                                 'within '
                                                                                                                 '30cm.'}]},
                                 'hockey_learn_how_to_play_alone_straight_line_dribble': {'key': 'hockey_learn_how_to_play_alone_straight_line_dribble',
                                                                                          'sport': 'Hockey',
                                                                                          'title': 'Straight '
                                                                                                   'Line '
                                                                                                   'Dribble',
                                                                                          'category': 'learn_how_to_play',
                                                                                          'training_mode': 'alone',
                                                                                          'level': 'learn',
                                                                                          'focus': 'learn '
                                                                                                   'how '
                                                                                                   'to '
                                                                                                   'play',
                                                                                          'exercises': [{'name': 'Straight '
                                                                                                                 'Line '
                                                                                                                 'Dribble',
                                                                                                         'prescription': '10 '
                                                                                                                         'reps',
                                                                                                         'notes': 'Dribble '
                                                                                                                  'ball '
                                                                                                                  '20m. '
                                                                                                                  'Turn. '
                                                                                                                  'Return.'}]},
                                 'hockey_learn_how_to_play_alone_push_pass_to_wall': {'key': 'hockey_learn_how_to_play_alone_push_pass_to_wall',
                                                                                      'sport': 'Hockey',
                                                                                      'title': 'Push '
                                                                                               'Pass '
                                                                                               'To '
                                                                                               'Wall',
                                                                                      'category': 'learn_how_to_play',
                                                                                      'training_mode': 'alone',
                                                                                      'level': 'learn',
                                                                                      'focus': 'learn '
                                                                                               'how '
                                                                                               'to '
                                                                                               'play',
                                                                                      'exercises': [{'name': 'Push '
                                                                                                             'Pass '
                                                                                                             'To '
                                                                                                             'Wall',
                                                                                                     'prescription': '50 '
                                                                                                                     'passes',
                                                                                                     'notes': 'Stand '
                                                                                                              '3m '
                                                                                                              'from '
                                                                                                              'wall. '
                                                                                                              'Push '
                                                                                                              'pass. '
                                                                                                              'Receive. '
                                                                                                              'Repeat.'}]},
                                 'hockey_learn_how_to_play_alone_ball_stop_practice': {'key': 'hockey_learn_how_to_play_alone_ball_stop_practice',
                                                                                       'sport': 'Hockey',
                                                                                       'title': 'Ball '
                                                                                                'Stop '
                                                                                                'Practice',
                                                                                       'category': 'learn_how_to_play',
                                                                                       'training_mode': 'alone',
                                                                                       'level': 'learn',
                                                                                       'focus': 'learn '
                                                                                                'how '
                                                                                                'to '
                                                                                                'play',
                                                                                       'exercises': [{'name': 'Ball '
                                                                                                              'Stop '
                                                                                                              'Practice',
                                                                                                      'prescription': '50 '
                                                                                                                      'reps',
                                                                                                      'notes': 'Roll '
                                                                                                               'ball '
                                                                                                               'forward. '
                                                                                                               'Stop '
                                                                                                               'it '
                                                                                                               'with '
                                                                                                               'stick. '
                                                                                                               'Repeat.'}]},
                                 'hockey_learn_how_to_play_alone_cone_dribbling_basics': {'key': 'hockey_learn_how_to_play_alone_cone_dribbling_basics',
                                                                                          'sport': 'Hockey',
                                                                                          'title': 'Cone '
                                                                                                   'Dribbling '
                                                                                                   'Basics',
                                                                                          'category': 'learn_how_to_play',
                                                                                          'training_mode': 'alone',
                                                                                          'level': 'learn',
                                                                                          'focus': 'learn '
                                                                                                   'how '
                                                                                                   'to '
                                                                                                   'play',
                                                                                          'exercises': [{'name': 'Cone '
                                                                                                                 'Dribbling '
                                                                                                                 'Basics',
                                                                                                         'prescription': '6 '
                                                                                                                         'rounds',
                                                                                                         'notes': 'Place '
                                                                                                                  '5 '
                                                                                                                  'cones. '
                                                                                                                  'Dribble '
                                                                                                                  'around '
                                                                                                                  'each '
                                                                                                                  'cone.'}]},
                                 'hockey_learn_how_to_play_alone_walking_ball_control': {'key': 'hockey_learn_how_to_play_alone_walking_ball_control',
                                                                                         'sport': 'Hockey',
                                                                                         'title': 'Walking '
                                                                                                  'Ball '
                                                                                                  'Control',
                                                                                         'category': 'learn_how_to_play',
                                                                                         'training_mode': 'alone',
                                                                                         'level': 'learn',
                                                                                         'focus': 'learn '
                                                                                                  'how '
                                                                                                  'to '
                                                                                                  'play',
                                                                                         'exercises': [{'name': 'Walking '
                                                                                                                'Ball '
                                                                                                                'Control',
                                                                                                        'prescription': '5 '
                                                                                                                        'minutes',
                                                                                                        'notes': 'Walk '
                                                                                                                 'continuously '
                                                                                                                 'while '
                                                                                                                 'dribbling.'}]},
                                 'hockey_learn_how_to_play_alone_jogging_ball_control': {'key': 'hockey_learn_how_to_play_alone_jogging_ball_control',
                                                                                         'sport': 'Hockey',
                                                                                         'title': 'Jogging '
                                                                                                  'Ball '
                                                                                                  'Control',
                                                                                         'category': 'learn_how_to_play',
                                                                                         'training_mode': 'alone',
                                                                                         'level': 'learn',
                                                                                         'focus': 'learn '
                                                                                                  'how '
                                                                                                  'to '
                                                                                                  'play',
                                                                                         'exercises': [{'name': 'Jogging '
                                                                                                                'Ball '
                                                                                                                'Control',
                                                                                                        'prescription': '5 '
                                                                                                                        'minutes',
                                                                                                        'notes': 'Jog '
                                                                                                                 'continuously '
                                                                                                                 'while '
                                                                                                                 'dribbling.'}]},
                                 'hockey_learn_how_to_play_alone_first_shot_practice': {'key': 'hockey_learn_how_to_play_alone_first_shot_practice',
                                                                                        'sport': 'Hockey',
                                                                                        'title': 'First '
                                                                                                 'Shot '
                                                                                                 'Practice',
                                                                                        'category': 'learn_how_to_play',
                                                                                        'training_mode': 'alone',
                                                                                        'level': 'learn',
                                                                                        'focus': 'learn '
                                                                                                 'how '
                                                                                                 'to '
                                                                                                 'play',
                                                                                        'exercises': [{'name': 'First '
                                                                                                               'Shot '
                                                                                                               'Practice',
                                                                                                       'prescription': '30 '
                                                                                                                       'shots',
                                                                                                       'notes': 'Stand '
                                                                                                                '5m '
                                                                                                                'from '
                                                                                                                'goal. '
                                                                                                                'Push '
                                                                                                                'ball '
                                                                                                                'toward '
                                                                                                                'goal.'}]},
                                 'hockey_learn_how_to_play_alone_receive_and_stop': {'key': 'hockey_learn_how_to_play_alone_receive_and_stop',
                                                                                     'sport': 'Hockey',
                                                                                     'title': 'Receive '
                                                                                              'and '
                                                                                              'Stop',
                                                                                     'category': 'learn_how_to_play',
                                                                                     'training_mode': 'alone',
                                                                                     'level': 'learn',
                                                                                     'focus': 'learn '
                                                                                              'how '
                                                                                              'to '
                                                                                              'play',
                                                                                     'exercises': [{'name': 'Receive '
                                                                                                            'and '
                                                                                                            'Stop',
                                                                                                    'prescription': '50 '
                                                                                                                    'reps',
                                                                                                    'notes': 'Pass '
                                                                                                             'against '
                                                                                                             'wall. '
                                                                                                             'Stop '
                                                                                                             'ball '
                                                                                                             'dead. '
                                                                                                             'Repeat.'}]},
                                 'hockey_learn_how_to_play_alone_mini_skills_circuit': {'key': 'hockey_learn_how_to_play_alone_mini_skills_circuit',
                                                                                        'sport': 'Hockey',
                                                                                        'title': 'Mini '
                                                                                                 'Skills '
                                                                                                 'Circuit',
                                                                                        'category': 'learn_how_to_play',
                                                                                        'training_mode': 'alone',
                                                                                        'level': 'learn',
                                                                                        'focus': 'learn '
                                                                                                 'how '
                                                                                                 'to '
                                                                                                 'play',
                                                                                        'exercises': [{'name': 'Mini '
                                                                                                               'Skills '
                                                                                                               'Circuit',
                                                                                                       'prescription': '10 '
                                                                                                                       'rounds',
                                                                                                       'notes': 'Dribble '
                                                                                                                '10m. '
                                                                                                                'Pass '
                                                                                                                'to '
                                                                                                                'wall. '
                                                                                                                'Receive. '
                                                                                                                'Shoot.'}]},
                                 'hockey_learn_how_to_play_alone_hockey_fundamentals_circuit': {'key': 'hockey_learn_how_to_play_alone_hockey_fundamentals_circuit',
                                                                                                'sport': 'Hockey',
                                                                                                'title': 'Hockey '
                                                                                                         'Fundamentals '
                                                                                                         'Circuit',
                                                                                                'category': 'learn_how_to_play',
                                                                                                'training_mode': 'alone',
                                                                                                'level': 'learn',
                                                                                                'focus': 'learn '
                                                                                                         'how '
                                                                                                         'to '
                                                                                                         'play',
                                                                                                'exercises': [{'name': 'Hockey '
                                                                                                                       'Fundamentals '
                                                                                                                       'Circuit',
                                                                                                               'prescription': '5 '
                                                                                                                               'rounds',
                                                                                                               'notes': '10 '
                                                                                                                        'push '
                                                                                                                        'passes. '
                                                                                                                        '10 '
                                                                                                                        'receptions. '
                                                                                                                        '20m '
                                                                                                                        'dribble. '
                                                                                                                        '1 '
                                                                                                                        'shot. '
                                                                                                                        'Repeat.'}]}},
                       'with_others': {'hockey_learn_how_to_play_with_others_partner_push_passing': {'key': 'hockey_learn_how_to_play_with_others_partner_push_passing',
                                                                                                     'sport': 'Hockey',
                                                                                                     'title': 'Partner '
                                                                                                              'Push '
                                                                                                              'Passing',
                                                                                                     'category': 'learn_how_to_play',
                                                                                                     'training_mode': 'with_others',
                                                                                                     'level': 'learn',
                                                                                                     'focus': 'learn '
                                                                                                              'how '
                                                                                                              'to '
                                                                                                              'play',
                                                                                                     'exercises': [{'name': 'Partner '
                                                                                                                            'Push '
                                                                                                                            'Passing',
                                                                                                                    'prescription': '100 '
                                                                                                                                    'passes',
                                                                                                                    'notes': 'Partners '
                                                                                                                             'stand '
                                                                                                                             '5m '
                                                                                                                             'apart. '
                                                                                                                             'Exchange '
                                                                                                                             'passes.'}]},
                                       'hockey_learn_how_to_play_with_others_partner_receiving': {'key': 'hockey_learn_how_to_play_with_others_partner_receiving',
                                                                                                  'sport': 'Hockey',
                                                                                                  'title': 'Partner '
                                                                                                           'Receiving',
                                                                                                  'category': 'learn_how_to_play',
                                                                                                  'training_mode': 'with_others',
                                                                                                  'level': 'learn',
                                                                                                  'focus': 'learn '
                                                                                                           'how '
                                                                                                           'to '
                                                                                                           'play',
                                                                                                  'exercises': [{'name': 'Partner '
                                                                                                                         'Receiving',
                                                                                                                 'prescription': '50 '
                                                                                                                                 'reps '
                                                                                                                                 'each',
                                                                                                                 'notes': 'One '
                                                                                                                          'player '
                                                                                                                          'passes. '
                                                                                                                          'Other '
                                                                                                                          'controls '
                                                                                                                          'and '
                                                                                                                          'stops '
                                                                                                                          'ball.'}]},
                                       'hockey_learn_how_to_play_with_others_follow_the_leader_dribbling': {'key': 'hockey_learn_how_to_play_with_others_follow_the_leader_dribbling',
                                                                                                            'sport': 'Hockey',
                                                                                                            'title': 'Follow '
                                                                                                                     'The '
                                                                                                                     'Leader '
                                                                                                                     'Dribbling',
                                                                                                            'category': 'learn_how_to_play',
                                                                                                            'training_mode': 'with_others',
                                                                                                            'level': 'learn',
                                                                                                            'focus': 'learn '
                                                                                                                     'how '
                                                                                                                     'to '
                                                                                                                     'play',
                                                                                                            'exercises': [{'name': 'Follow '
                                                                                                                                   'The '
                                                                                                                                   'Leader '
                                                                                                                                   'Dribbling',
                                                                                                                           'prescription': '5 '
                                                                                                                                           'minutes',
                                                                                                                           'notes': 'One '
                                                                                                                                    'player '
                                                                                                                                    'leads. '
                                                                                                                                    'Other '
                                                                                                                                    'copies '
                                                                                                                                    'movements.'}]},
                                       'hockey_learn_how_to_play_with_others_passing_while_walking': {'key': 'hockey_learn_how_to_play_with_others_passing_while_walking',
                                                                                                      'sport': 'Hockey',
                                                                                                      'title': 'Passing '
                                                                                                               'While '
                                                                                                               'Walking',
                                                                                                      'category': 'learn_how_to_play',
                                                                                                      'training_mode': 'with_others',
                                                                                                      'level': 'learn',
                                                                                                      'focus': 'learn '
                                                                                                               'how '
                                                                                                               'to '
                                                                                                               'play',
                                                                                                      'exercises': [{'name': 'Passing '
                                                                                                                             'While '
                                                                                                                             'Walking',
                                                                                                                     'prescription': '5 '
                                                                                                                                     'minutes',
                                                                                                                     'notes': 'Walk '
                                                                                                                              'continuously. '
                                                                                                                              'Exchange '
                                                                                                                              'passes.'}]},
                                       'hockey_learn_how_to_play_with_others_passing_while_jogging': {'key': 'hockey_learn_how_to_play_with_others_passing_while_jogging',
                                                                                                      'sport': 'Hockey',
                                                                                                      'title': 'Passing '
                                                                                                               'While '
                                                                                                               'Jogging',
                                                                                                      'category': 'learn_how_to_play',
                                                                                                      'training_mode': 'with_others',
                                                                                                      'level': 'learn',
                                                                                                      'focus': 'learn '
                                                                                                               'how '
                                                                                                               'to '
                                                                                                               'play',
                                                                                                      'exercises': [{'name': 'Passing '
                                                                                                                             'While '
                                                                                                                             'Jogging',
                                                                                                                     'prescription': '5 '
                                                                                                                                     'minutes',
                                                                                                                     'notes': 'Jog '
                                                                                                                              'side-by-side. '
                                                                                                                              'Exchange '
                                                                                                                              'passes.'}]},
                                       'hockey_learn_how_to_play_with_others_dribble_relay_race': {'key': 'hockey_learn_how_to_play_with_others_dribble_relay_race',
                                                                                                   'sport': 'Hockey',
                                                                                                   'title': 'Dribble '
                                                                                                            'Relay '
                                                                                                            'Race',
                                                                                                   'category': 'learn_how_to_play',
                                                                                                   'training_mode': 'with_others',
                                                                                                   'level': 'learn',
                                                                                                   'focus': 'learn '
                                                                                                            'how '
                                                                                                            'to '
                                                                                                            'play',
                                                                                                   'exercises': [{'name': 'Dribble '
                                                                                                                          'Relay '
                                                                                                                          'Race',
                                                                                                                  'prescription': '5 '
                                                                                                                                  'rounds',
                                                                                                                  'notes': 'Teams '
                                                                                                                           'race '
                                                                                                                           'through '
                                                                                                                           'cones.'}]},
                                       'hockey_learn_how_to_play_with_others_shoot_and_retrieve': {'key': 'hockey_learn_how_to_play_with_others_shoot_and_retrieve',
                                                                                                   'sport': 'Hockey',
                                                                                                   'title': 'Shoot '
                                                                                                            'and '
                                                                                                            'Retrieve',
                                                                                                   'category': 'learn_how_to_play',
                                                                                                   'training_mode': 'with_others',
                                                                                                   'level': 'learn',
                                                                                                   'focus': 'learn '
                                                                                                            'how '
                                                                                                            'to '
                                                                                                            'play',
                                                                                                   'exercises': [{'name': 'Shoot '
                                                                                                                          'and '
                                                                                                                          'Retrieve',
                                                                                                                  'prescription': '20 '
                                                                                                                                  'shots '
                                                                                                                                  'each',
                                                                                                                  'notes': 'One '
                                                                                                                           'player '
                                                                                                                           'shoots. '
                                                                                                                           'Other '
                                                                                                                           'retrieves. '
                                                                                                                           'Switch '
                                                                                                                           'roles.'}]},
                                       'hockey_learn_how_to_play_with_others_triangle_passing': {'key': 'hockey_learn_how_to_play_with_others_triangle_passing',
                                                                                                 'sport': 'Hockey',
                                                                                                 'title': 'Triangle '
                                                                                                          'Passing',
                                                                                                 'category': 'learn_how_to_play',
                                                                                                 'training_mode': 'with_others',
                                                                                                 'level': 'learn',
                                                                                                 'focus': 'learn '
                                                                                                          'how '
                                                                                                          'to '
                                                                                                          'play',
                                                                                                 'exercises': [{'name': 'Triangle '
                                                                                                                        'Passing',
                                                                                                                'prescription': '5 '
                                                                                                                                'minutes',
                                                                                                                'notes': 'Three '
                                                                                                                         'players. '
                                                                                                                         'Continuous '
                                                                                                                         'passing.'}]},
                                       'hockey_learn_how_to_play_with_others_basic_possession_game': {'key': 'hockey_learn_how_to_play_with_others_basic_possession_game',
                                                                                                      'sport': 'Hockey',
                                                                                                      'title': 'Basic '
                                                                                                               'Possession '
                                                                                                               'Game',
                                                                                                      'category': 'learn_how_to_play',
                                                                                                      'training_mode': 'with_others',
                                                                                                      'level': 'learn',
                                                                                                      'focus': 'learn '
                                                                                                               'how '
                                                                                                               'to '
                                                                                                               'play',
                                                                                                      'exercises': [{'name': 'Basic '
                                                                                                                             'Possession '
                                                                                                                             'Game',
                                                                                                                     'prescription': '5 '
                                                                                                                                     'x '
                                                                                                                                     '45 '
                                                                                                                                     'seconds',
                                                                                                                     'notes': 'Keep '
                                                                                                                              'possession '
                                                                                                                              'inside '
                                                                                                                              '10m '
                                                                                                                              'square.'}]},
                                       'hockey_learn_how_to_play_with_others_pass_and_follow': {'key': 'hockey_learn_how_to_play_with_others_pass_and_follow',
                                                                                                'sport': 'Hockey',
                                                                                                'title': 'Pass '
                                                                                                         'and '
                                                                                                         'Follow',
                                                                                                'category': 'learn_how_to_play',
                                                                                                'training_mode': 'with_others',
                                                                                                'level': 'learn',
                                                                                                'focus': 'learn '
                                                                                                         'how '
                                                                                                         'to '
                                                                                                         'play',
                                                                                                'exercises': [{'name': 'Pass '
                                                                                                                       'and '
                                                                                                                       'Follow',
                                                                                                               'prescription': '5 '
                                                                                                                               'minutes',
                                                                                                               'notes': 'Pass '
                                                                                                                        'ball. '
                                                                                                                        'Run '
                                                                                                                        'to '
                                                                                                                        "receiver's "
                                                                                                                        'position. '
                                                                                                                        'Continue.'}]},
                                       'hockey_learn_how_to_play_with_others_mini_hockey_circuit': {'key': 'hockey_learn_how_to_play_with_others_mini_hockey_circuit',
                                                                                                    'sport': 'Hockey',
                                                                                                    'title': 'Mini '
                                                                                                             'Hockey '
                                                                                                             'Circuit',
                                                                                                    'category': 'learn_how_to_play',
                                                                                                    'training_mode': 'with_others',
                                                                                                    'level': 'learn',
                                                                                                    'focus': 'learn '
                                                                                                             'how '
                                                                                                             'to '
                                                                                                             'play',
                                                                                                    'exercises': [{'name': 'Mini '
                                                                                                                           'Hockey '
                                                                                                                           'Circuit',
                                                                                                                   'prescription': '10 '
                                                                                                                                   'rounds',
                                                                                                                   'notes': 'Pass. '
                                                                                                                            'Receive. '
                                                                                                                            'Dribble. '
                                                                                                                            'Shoot. '
                                                                                                                            'Repeat.'}]},
                                       'hockey_learn_how_to_play_with_others_small_sided_match': {'key': 'hockey_learn_how_to_play_with_others_small_sided_match',
                                                                                                  'sport': 'Hockey',
                                                                                                  'title': 'Small-Sided '
                                                                                                           'Match',
                                                                                                  'category': 'learn_how_to_play',
                                                                                                  'training_mode': 'with_others',
                                                                                                  'level': 'learn',
                                                                                                  'focus': 'learn '
                                                                                                           'how '
                                                                                                           'to '
                                                                                                           'play',
                                                                                                  'exercises': [{'name': 'Small-Sided '
                                                                                                                         'Match',
                                                                                                                 'prescription': '10 '
                                                                                                                                 'minutes',
                                                                                                                 'notes': '2v2 '
                                                                                                                          'or '
                                                                                                                          '3v3.'}]}}},
 'beginner': {'alone': {'hockey_beginner_alone_zigzag_dribble_circuit': {'key': 'hockey_beginner_alone_zigzag_dribble_circuit',
                                                                         'sport': 'Hockey',
                                                                         'title': 'Zigzag Dribble '
                                                                                  'Circuit',
                                                                         'category': 'beginner',
                                                                         'training_mode': 'alone',
                                                                         'level': 'beginner',
                                                                         'focus': 'beginner',
                                                                         'exercises': [{'name': 'Zigzag '
                                                                                                'Dribble '
                                                                                                'Circuit',
                                                                                        'prescription': '10 '
                                                                                                        'rounds',
                                                                                        'notes': 'Place '
                                                                                                 '8 '
                                                                                                 'cones '
                                                                                                 '2m '
                                                                                                 'apart. '
                                                                                                 'Dribble '
                                                                                                 'through '
                                                                                                 'all '
                                                                                                 'cones.'}]},
                        'hockey_beginner_alone_pass_receive_continuous': {'key': 'hockey_beginner_alone_pass_receive_continuous',
                                                                          'sport': 'Hockey',
                                                                          'title': 'Pass-Receive '
                                                                                   'Continuous',
                                                                          'category': 'beginner',
                                                                          'training_mode': 'alone',
                                                                          'level': 'beginner',
                                                                          'focus': 'beginner',
                                                                          'exercises': [{'name': 'Pass-Receive '
                                                                                                 'Continuous',
                                                                                         'prescription': '100 '
                                                                                                         'passes',
                                                                                         'notes': 'Pass '
                                                                                                  'against '
                                                                                                  'wall. '
                                                                                                  'Receive '
                                                                                                  'with '
                                                                                                  'first '
                                                                                                  'touch. '
                                                                                                  'Continue '
                                                                                                  'without '
                                                                                                  'stopping.'}]},
                        'hockey_beginner_alone_dribble_and_turn': {'key': 'hockey_beginner_alone_dribble_and_turn',
                                                                   'sport': 'Hockey',
                                                                   'title': 'Dribble and Turn',
                                                                   'category': 'beginner',
                                                                   'training_mode': 'alone',
                                                                   'level': 'beginner',
                                                                   'focus': 'beginner',
                                                                   'exercises': [{'name': 'Dribble '
                                                                                          'and '
                                                                                          'Turn',
                                                                                  'prescription': '15 '
                                                                                                  'reps',
                                                                                  'notes': 'Dribble '
                                                                                           '15m. '
                                                                                           'Perform '
                                                                                           '180° '
                                                                                           'turn. '
                                                                                           'Return.'}]},
                        'hockey_beginner_alone_push_pass_accuracy': {'key': 'hockey_beginner_alone_push_pass_accuracy',
                                                                     'sport': 'Hockey',
                                                                     'title': 'Push Pass Accuracy',
                                                                     'category': 'beginner',
                                                                     'training_mode': 'alone',
                                                                     'level': 'beginner',
                                                                     'focus': 'beginner',
                                                                     'exercises': [{'name': 'Push '
                                                                                            'Pass '
                                                                                            'Accuracy',
                                                                                    'prescription': '50 '
                                                                                                    'passes',
                                                                                    'notes': 'Place '
                                                                                             'target '
                                                                                             'cone '
                                                                                             '10m '
                                                                                             'away. '
                                                                                             'Hit '
                                                                                             'target.'}]},
                        'hockey_beginner_alone_receive_move_pass': {'key': 'hockey_beginner_alone_receive_move_pass',
                                                                    'sport': 'Hockey',
                                                                    'title': 'Receive-Move-Pass',
                                                                    'category': 'beginner',
                                                                    'training_mode': 'alone',
                                                                    'level': 'beginner',
                                                                    'focus': 'beginner',
                                                                    'exercises': [{'name': 'Receive-Move-Pass',
                                                                                   'prescription': '50 '
                                                                                                   'reps',
                                                                                   'notes': 'Pass '
                                                                                            'against '
                                                                                            'wall. '
                                                                                            'Move '
                                                                                            '3 '
                                                                                            'steps '
                                                                                            'sideways. '
                                                                                            'Pass '
                                                                                            'again.'}]},
                        'hockey_beginner_alone_sprint_with_ball': {'key': 'hockey_beginner_alone_sprint_with_ball',
                                                                   'sport': 'Hockey',
                                                                   'title': 'Sprint With Ball',
                                                                   'category': 'beginner',
                                                                   'training_mode': 'alone',
                                                                   'level': 'beginner',
                                                                   'focus': 'beginner',
                                                                   'exercises': [{'name': 'Sprint '
                                                                                          'With '
                                                                                          'Ball',
                                                                                  'prescription': '10 '
                                                                                                  'reps',
                                                                                  'notes': 'Dribble '
                                                                                           '20m at '
                                                                                           'speed. '
                                                                                           'Return.'}]},
                        'hockey_beginner_alone_dribble_and_shoot': {'key': 'hockey_beginner_alone_dribble_and_shoot',
                                                                    'sport': 'Hockey',
                                                                    'title': 'Dribble and Shoot',
                                                                    'category': 'beginner',
                                                                    'training_mode': 'alone',
                                                                    'level': 'beginner',
                                                                    'focus': 'beginner',
                                                                    'exercises': [{'name': 'Dribble '
                                                                                           'and '
                                                                                           'Shoot',
                                                                                   'prescription': '20 '
                                                                                                   'reps',
                                                                                   'notes': 'Dribble '
                                                                                            '15m. '
                                                                                            'Shoot.'}]},
                        'hockey_beginner_alone_figure_8_ball_control': {'key': 'hockey_beginner_alone_figure_8_ball_control',
                                                                        'sport': 'Hockey',
                                                                        'title': 'Figure-8 Ball '
                                                                                 'Control',
                                                                        'category': 'beginner',
                                                                        'training_mode': 'alone',
                                                                        'level': 'beginner',
                                                                        'focus': 'beginner',
                                                                        'exercises': [{'name': 'Figure-8 '
                                                                                               'Ball '
                                                                                               'Control',
                                                                                       'prescription': '5 '
                                                                                                       'x '
                                                                                                       '60 '
                                                                                                       'seconds',
                                                                                       'notes': 'Two '
                                                                                                'cones '
                                                                                                '2m '
                                                                                                'apart. '
                                                                                                'Dribble '
                                                                                                'figure-8 '
                                                                                                'continuously.'}]},
                        'hockey_beginner_alone_shuttle_run_with_ball': {'key': 'hockey_beginner_alone_shuttle_run_with_ball',
                                                                        'sport': 'Hockey',
                                                                        'title': 'Shuttle Run With '
                                                                                 'Ball',
                                                                        'category': 'beginner',
                                                                        'training_mode': 'alone',
                                                                        'level': 'beginner',
                                                                        'focus': 'beginner',
                                                                        'exercises': [{'name': 'Shuttle '
                                                                                               'Run '
                                                                                               'With '
                                                                                               'Ball',
                                                                                       'prescription': '6 '
                                                                                                       'rounds',
                                                                                       'notes': 'Dribble '
                                                                                                '10m '
                                                                                                'and '
                                                                                                'back. '
                                                                                                '20m '
                                                                                                'and '
                                                                                                'back. '
                                                                                                '30m '
                                                                                                'and '
                                                                                                'back.'}]},
                        'hockey_beginner_alone_ball_protection_drill': {'key': 'hockey_beginner_alone_ball_protection_drill',
                                                                        'sport': 'Hockey',
                                                                        'title': 'Ball Protection '
                                                                                 'Drill',
                                                                        'category': 'beginner',
                                                                        'training_mode': 'alone',
                                                                        'level': 'beginner',
                                                                        'focus': 'beginner',
                                                                        'exercises': [{'name': 'Ball '
                                                                                               'Protection '
                                                                                               'Drill',
                                                                                       'prescription': '5 '
                                                                                                       'x '
                                                                                                       '45 '
                                                                                                       'seconds',
                                                                                       'notes': 'Stay '
                                                                                                'inside '
                                                                                                'a '
                                                                                                '5m '
                                                                                                'square. '
                                                                                                'Keep '
                                                                                                'ball '
                                                                                                'moving '
                                                                                                'continuously.'}]},
                        'hockey_beginner_alone_accuracy_shooting': {'key': 'hockey_beginner_alone_accuracy_shooting',
                                                                    'sport': 'Hockey',
                                                                    'title': 'Accuracy Shooting',
                                                                    'category': 'beginner',
                                                                    'training_mode': 'alone',
                                                                    'level': 'beginner',
                                                                    'focus': 'beginner',
                                                                    'exercises': [{'name': 'Accuracy '
                                                                                           'Shooting',
                                                                                   'prescription': '40 '
                                                                                                   'shots',
                                                                                   'notes': 'Shoot '
                                                                                            'at a '
                                                                                            '1m '
                                                                                            'target '
                                                                                            'area.'}]},
                        'hockey_beginner_alone_beginner_hockey_circuit': {'key': 'hockey_beginner_alone_beginner_hockey_circuit',
                                                                          'sport': 'Hockey',
                                                                          'title': 'Beginner '
                                                                                   'Hockey Circuit',
                                                                          'category': 'beginner',
                                                                          'training_mode': 'alone',
                                                                          'level': 'beginner',
                                                                          'focus': 'beginner',
                                                                          'exercises': [{'name': 'Beginner '
                                                                                                 'Hockey '
                                                                                                 'Circuit',
                                                                                         'prescription': '6 '
                                                                                                         'rounds',
                                                                                         'notes': 'Dribble '
                                                                                                  'through '
                                                                                                  '6 '
                                                                                                  'cones. '
                                                                                                  'Pass '
                                                                                                  'to '
                                                                                                  'wall. '
                                                                                                  'Receive. '
                                                                                                  'Sprint '
                                                                                                  '15m. '
                                                                                                  'Shoot. '
                                                                                                  'Repeat.'}]}},
              'with_others': {'hockey_beginner_with_others_passing_triangle': {'key': 'hockey_beginner_with_others_passing_triangle',
                                                                               'sport': 'Hockey',
                                                                               'title': 'Passing '
                                                                                        'Triangle',
                                                                               'category': 'beginner',
                                                                               'training_mode': 'with_others',
                                                                               'level': 'beginner',
                                                                               'focus': 'beginner',
                                                                               'exercises': [{'name': 'Passing '
                                                                                                      'Triangle',
                                                                                              'prescription': '100 '
                                                                                                              'passes',
                                                                                              'notes': 'Three '
                                                                                                       'players. '
                                                                                                       'One-touch '
                                                                                                       'passing.'}]},
                              'hockey_beginner_with_others_dribble_and_pass': {'key': 'hockey_beginner_with_others_dribble_and_pass',
                                                                               'sport': 'Hockey',
                                                                               'title': 'Dribble '
                                                                                        'and Pass',
                                                                               'category': 'beginner',
                                                                               'training_mode': 'with_others',
                                                                               'level': 'beginner',
                                                                               'focus': 'beginner',
                                                                               'exercises': [{'name': 'Dribble '
                                                                                                      'and '
                                                                                                      'Pass',
                                                                                              'prescription': '20 '
                                                                                                              'reps',
                                                                                              'notes': 'Dribble '
                                                                                                       '10m. '
                                                                                                       'Pass '
                                                                                                       'to '
                                                                                                       'teammate. '
                                                                                                       'Repeat.'}]},
                              'hockey_beginner_with_others_give_and_go_drill': {'key': 'hockey_beginner_with_others_give_and_go_drill',
                                                                                'sport': 'Hockey',
                                                                                'title': 'Give-and-Go '
                                                                                         'Drill',
                                                                                'category': 'beginner',
                                                                                'training_mode': 'with_others',
                                                                                'level': 'beginner',
                                                                                'focus': 'beginner',
                                                                                'exercises': [{'name': 'Give-and-Go '
                                                                                                       'Drill',
                                                                                               'prescription': '20 '
                                                                                                               'reps',
                                                                                               'notes': 'Pass. '
                                                                                                        'Sprint '
                                                                                                        'forward. '
                                                                                                        'Receive '
                                                                                                        'return '
                                                                                                        'pass.'}]},
                              'hockey_beginner_with_others_possession_box': {'key': 'hockey_beginner_with_others_possession_box',
                                                                             'sport': 'Hockey',
                                                                             'title': 'Possession '
                                                                                      'Box',
                                                                             'category': 'beginner',
                                                                             'training_mode': 'with_others',
                                                                             'level': 'beginner',
                                                                             'focus': 'beginner',
                                                                             'exercises': [{'name': 'Possession '
                                                                                                    'Box',
                                                                                            'prescription': '5 '
                                                                                                            'x '
                                                                                                            '60 '
                                                                                                            'seconds',
                                                                                            'notes': '3 '
                                                                                                     'attackers '
                                                                                                     'vs '
                                                                                                     '1 '
                                                                                                     'defender. '
                                                                                                     'Maintain '
                                                                                                     'possession.'}]},
                              'hockey_beginner_with_others_passing_square': {'key': 'hockey_beginner_with_others_passing_square',
                                                                             'sport': 'Hockey',
                                                                             'title': 'Passing '
                                                                                      'Square',
                                                                             'category': 'beginner',
                                                                             'training_mode': 'with_others',
                                                                             'level': 'beginner',
                                                                             'focus': 'beginner',
                                                                             'exercises': [{'name': 'Passing '
                                                                                                    'Square',
                                                                                            'prescription': '10 '
                                                                                                            'minutes',
                                                                                            'notes': 'Four '
                                                                                                     'players '
                                                                                                     'on '
                                                                                                     'corners. '
                                                                                                     'Pass '
                                                                                                     'and '
                                                                                                     'follow '
                                                                                                     'pass.'}]},
                              'hockey_beginner_with_others_through_ball_drill': {'key': 'hockey_beginner_with_others_through_ball_drill',
                                                                                 'sport': 'Hockey',
                                                                                 'title': 'Through '
                                                                                          'Ball '
                                                                                          'Drill',
                                                                                 'category': 'beginner',
                                                                                 'training_mode': 'with_others',
                                                                                 'level': 'beginner',
                                                                                 'focus': 'beginner',
                                                                                 'exercises': [{'name': 'Through '
                                                                                                        'Ball '
                                                                                                        'Drill',
                                                                                                'prescription': '20 '
                                                                                                                'reps',
                                                                                                'notes': 'Teammate '
                                                                                                         'runs '
                                                                                                         'into '
                                                                                                         'space. '
                                                                                                         'Deliver '
                                                                                                         'pass '
                                                                                                         'ahead.'}]},
                              'hockey_beginner_with_others_partner_shooting': {'key': 'hockey_beginner_with_others_partner_shooting',
                                                                               'sport': 'Hockey',
                                                                               'title': 'Partner '
                                                                                        'Shooting',
                                                                               'category': 'beginner',
                                                                               'training_mode': 'with_others',
                                                                               'level': 'beginner',
                                                                               'focus': 'beginner',
                                                                               'exercises': [{'name': 'Partner '
                                                                                                      'Shooting',
                                                                                              'prescription': '30 '
                                                                                                              'shots',
                                                                                              'notes': 'Teammate '
                                                                                                       'passes. '
                                                                                                       'Receive '
                                                                                                       'and '
                                                                                                       'shoot.'}]},
                              'hockey_beginner_with_others_transition_sprint': {'key': 'hockey_beginner_with_others_transition_sprint',
                                                                                'sport': 'Hockey',
                                                                                'title': 'Transition '
                                                                                         'Sprint',
                                                                                'category': 'beginner',
                                                                                'training_mode': 'with_others',
                                                                                'level': 'beginner',
                                                                                'focus': 'beginner',
                                                                                'exercises': [{'name': 'Transition '
                                                                                                       'Sprint',
                                                                                               'prescription': '20 '
                                                                                                               'reps',
                                                                                               'notes': 'Pass '
                                                                                                        'to '
                                                                                                        'teammate. '
                                                                                                        'Sprint '
                                                                                                        'to '
                                                                                                        'next '
                                                                                                        'position. '
                                                                                                        'Repeat.'}]},
                              'hockey_beginner_with_others_2v1_attack': {'key': 'hockey_beginner_with_others_2v1_attack',
                                                                         'sport': 'Hockey',
                                                                         'title': '2v1 Attack',
                                                                         'category': 'beginner',
                                                                         'training_mode': 'with_others',
                                                                         'level': 'beginner',
                                                                         'focus': 'beginner',
                                                                         'exercises': [{'name': '2v1 '
                                                                                                'Attack',
                                                                                        'prescription': '15 '
                                                                                                        'reps',
                                                                                        'notes': 'Two '
                                                                                                 'attackers '
                                                                                                 'versus '
                                                                                                 'one '
                                                                                                 'defender. '
                                                                                                 'Create '
                                                                                                 'shot.'}]},
                              'hockey_beginner_with_others_fast_break_drill': {'key': 'hockey_beginner_with_others_fast_break_drill',
                                                                               'sport': 'Hockey',
                                                                               'title': 'Fast '
                                                                                        'Break '
                                                                                        'Drill',
                                                                               'category': 'beginner',
                                                                               'training_mode': 'with_others',
                                                                               'level': 'beginner',
                                                                               'focus': 'beginner',
                                                                               'exercises': [{'name': 'Fast '
                                                                                                      'Break '
                                                                                                      'Drill',
                                                                                              'prescription': '15 '
                                                                                                              'reps',
                                                                                              'notes': 'Start '
                                                                                                       'from '
                                                                                                       'midfield. '
                                                                                                       'Attack '
                                                                                                       'goal '
                                                                                                       'quickly.'}]},
                              'hockey_beginner_with_others_small_possession_game': {'key': 'hockey_beginner_with_others_small_possession_game',
                                                                                    'sport': 'Hockey',
                                                                                    'title': 'Small '
                                                                                             'Possession '
                                                                                             'Game',
                                                                                    'category': 'beginner',
                                                                                    'training_mode': 'with_others',
                                                                                    'level': 'beginner',
                                                                                    'focus': 'beginner',
                                                                                    'exercises': [{'name': 'Small '
                                                                                                           'Possession '
                                                                                                           'Game',
                                                                                                   'prescription': '10 '
                                                                                                                   'minutes',
                                                                                                   'notes': '3v3. '
                                                                                                            'Maximum '
                                                                                                            'three '
                                                                                                            'touches.'}]},
                              'hockey_beginner_with_others_beginner_match_simulation': {'key': 'hockey_beginner_with_others_beginner_match_simulation',
                                                                                        'sport': 'Hockey',
                                                                                        'title': 'Beginner '
                                                                                                 'Match '
                                                                                                 'Simulation',
                                                                                        'category': 'beginner',
                                                                                        'training_mode': 'with_others',
                                                                                        'level': 'beginner',
                                                                                        'focus': 'beginner',
                                                                                        'exercises': [{'name': 'Beginner '
                                                                                                               'Match '
                                                                                                               'Simulation',
                                                                                                       'prescription': '15 '
                                                                                                                       'minutes',
                                                                                                       'notes': '4v4 '
                                                                                                                'or '
                                                                                                                '5v5. '
                                                                                                                'Continuous '
                                                                                                                'play.'}]}}}}


def get_hockey_catalog() -> SportCatalog:
    """Return a deep copy of the complete hockey catalog."""
    return deepcopy(HOCKEY_CATALOG)


def list_hockey_sessions(
    category: Optional[str] = None,
    training_mode: Optional[str] = None,
) -> List[SportSession]:
    """List hockey sessions, optionally filtered by category and training mode."""
    sessions: List[SportSession] = []
    categories = [category] if category else list(HOCKEY_CATALOG.keys())

    for category_key in categories:
        if category_key not in HOCKEY_CATALOG:
            continue
        modes = [training_mode] if training_mode else list(HOCKEY_CATALOG[category_key].keys())
        for mode_key in modes:
            sessions.extend(HOCKEY_CATALOG[category_key].get(mode_key, {}).values())

    return deepcopy(sessions)


def get_hockey_session(
    session_key: str,
    category: Optional[str] = None,
    training_mode: Optional[str] = None,
) -> Optional[SportSession]:
    """Fetch one hockey session by key."""
    categories = [category] if category else list(HOCKEY_CATALOG.keys())

    for category_key in categories:
        if category_key not in HOCKEY_CATALOG:
            continue
        modes = [training_mode] if training_mode else list(HOCKEY_CATALOG[category_key].keys())
        for mode_key in modes:
            session = HOCKEY_CATALOG[category_key].get(mode_key, {}).get(session_key)
            if session:
                return deepcopy(session)

    return None


ALL_HOCKEY_SESSIONS: List[SportSession] = list_hockey_sessions()


__all__ = [
    "SPORT",
    "HOCKEY_CATALOG",
    "ALL_HOCKEY_SESSIONS",
    "get_hockey_catalog",
    "list_hockey_sessions",
    "get_hockey_session",
]
