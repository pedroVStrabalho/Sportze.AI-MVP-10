"""Martial Arts training catalog for Sportze.AI.

This module codifies karate, taekwondo, Muay Thai, judo, Brazilian jiu-jitsu,
and Krav Maga sessions into a clean, implementation-ready structure for the
Training Generator catalog.

Structure:
- MARTIAL_ARTS_CATALOG[category][training_mode][session_key]
- training_mode: "alone"
- each session contains: key, sport, martial_art, title, category, training_mode,
  level, focus, and exercises

Helper functions:
- get_martial_arts_catalog()
- list_martial_arts_sessions(category=None, training_mode=None, martial_art=None)
- get_martial_arts_session(session_key, category=None, training_mode=None)
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional

SportSession = Dict[str, Any]
SportCatalog = Dict[str, Dict[str, Dict[str, SportSession]]]

SPORT = "Martial Arts"


MARTIAL_ARTS_CATALOG: SportCatalog = {'karate_learn_how_to_play': {'alone': {'martial_arts_karate_learn_how_to_play': {'key': 'martial_arts_karate_learn_how_to_play',
                                                                                  'sport': 'Martial Arts',
                                                                                  'martial_art': 'Karate',
                                                                                  'title': 'Karate – Learn How To Play',
                                                                                  'category': 'karate_learn_how_to_play',
                                                                                  'training_mode': 'alone',
                                                                                  'level': 'learn_how_to_play',
                                                                                  'focus': 'learn how to play',
                                                                                  'exercises': [{'name': 'Fighting '
                                                                                                         'Stance '
                                                                                                         'Practice',
                                                                                                 'prescription': 'Assume '
                                                                                                                 'Karate '
                                                                                                                 'fighting '
                                                                                                                 'stance. '
                                                                                                                 'Hold '
                                                                                                                 'for '
                                                                                                                 '30 '
                                                                                                                 'seconds. '
                                                                                                                 'Repeat '
                                                                                                                 '10 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Forward and '
                                                                                                         'Backward '
                                                                                                         'Movement',
                                                                                                 'prescription': 'Move '
                                                                                                                 'forward '
                                                                                                                 '10 '
                                                                                                                 'steps. '
                                                                                                                 'Move '
                                                                                                                 'backward '
                                                                                                                 '10 '
                                                                                                                 'steps. '
                                                                                                                 'Repeat '
                                                                                                                 '10 '
                                                                                                                 'rounds.'},
                                                                                                {'name': 'Basic '
                                                                                                         'Straight '
                                                                                                         'Punch',
                                                                                                 'prescription': 'Perform '
                                                                                                                 '100 '
                                                                                                                 'straight '
                                                                                                                 'punches '
                                                                                                                 'with '
                                                                                                                 'the '
                                                                                                                 'right '
                                                                                                                 'arm. '
                                                                                                                 'Perform '
                                                                                                                 '100 '
                                                                                                                 'straight '
                                                                                                                 'punches '
                                                                                                                 'with '
                                                                                                                 'the '
                                                                                                                 'left '
                                                                                                                 'arm.'},
                                                                                                {'name': 'Reverse '
                                                                                                         'Punch '
                                                                                                         'Introduction',
                                                                                                 'prescription': 'Perform '
                                                                                                                 '50 '
                                                                                                                 'reverse '
                                                                                                                 'punches '
                                                                                                                 'from '
                                                                                                                 'fighting '
                                                                                                                 'stance '
                                                                                                                 'per '
                                                                                                                 'side.'},
                                                                                                {'name': 'Front Kick '
                                                                                                         'Introduction',
                                                                                                 'prescription': 'Perform '
                                                                                                                 '50 '
                                                                                                                 'front '
                                                                                                                 'kicks '
                                                                                                                 'with '
                                                                                                                 'the '
                                                                                                                 'right '
                                                                                                                 'leg. '
                                                                                                                 'Perform '
                                                                                                                 '50 '
                                                                                                                 'front '
                                                                                                                 'kicks '
                                                                                                                 'with '
                                                                                                                 'the '
                                                                                                                 'left '
                                                                                                                 'leg.'},
                                                                                                {'name': 'Low Block '
                                                                                                         'Practice',
                                                                                                 'prescription': 'Perform '
                                                                                                                 '100 '
                                                                                                                 'low '
                                                                                                                 'blocks '
                                                                                                                 'per '
                                                                                                                 'arm.'},
                                                                                                {'name': 'Middle Block '
                                                                                                         'Practice',
                                                                                                 'prescription': 'Perform '
                                                                                                                 '100 '
                                                                                                                 'middle '
                                                                                                                 'blocks '
                                                                                                                 'per '
                                                                                                                 'arm.'},
                                                                                                {'name': 'Rising Block '
                                                                                                         'Practice',
                                                                                                 'prescription': 'Perform '
                                                                                                                 '100 '
                                                                                                                 'rising '
                                                                                                                 'blocks '
                                                                                                                 'per '
                                                                                                                 'arm.'},
                                                                                                {'name': 'Punch-and-Step '
                                                                                                         'Drill',
                                                                                                 'prescription': 'Step '
                                                                                                                 'forward '
                                                                                                                 'and '
                                                                                                                 'throw '
                                                                                                                 'a '
                                                                                                                 'straight '
                                                                                                                 'punch. '
                                                                                                                 'Repeat '
                                                                                                                 '100 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Front Kick '
                                                                                                         'and Return',
                                                                                                 'prescription': 'Throw '
                                                                                                                 'a '
                                                                                                                 'front '
                                                                                                                 'kick. '
                                                                                                                 'Return '
                                                                                                                 'immediately '
                                                                                                                 'to '
                                                                                                                 'stance. '
                                                                                                                 'Repeat '
                                                                                                                 '50 '
                                                                                                                 'times '
                                                                                                                 'per '
                                                                                                                 'leg.'},
                                                                                                {'name': 'Shadow '
                                                                                                         'Karate Round',
                                                                                                 'prescription': 'Practice '
                                                                                                                 'punches, '
                                                                                                                 'kicks, '
                                                                                                                 'blocks, '
                                                                                                                 'and '
                                                                                                                 'movement '
                                                                                                                 'continuously '
                                                                                                                 'for '
                                                                                                                 '2 '
                                                                                                                 'minutes. '
                                                                                                                 'Complete '
                                                                                                                 '5 '
                                                                                                                 'rounds.'},
                                                                                                {'name': 'Karate '
                                                                                                         'Coordination '
                                                                                                         'Circuit',
                                                                                                 'prescription': '20 '
                                                                                                                 'punches '
                                                                                                                 '20 '
                                                                                                                 'blocks '
                                                                                                                 '20 '
                                                                                                                 'kicks '
                                                                                                                 'Repeat '
                                                                                                                 '5 '
                                                                                                                 'rounds.'}]}}},
 'karate_beginner': {'alone': {'martial_arts_karate_beginner': {'key': 'martial_arts_karate_beginner',
                                                                'sport': 'Martial Arts',
                                                                'martial_art': 'Karate',
                                                                'title': 'Karate – Beginner',
                                                                'category': 'karate_beginner',
                                                                'training_mode': 'alone',
                                                                'level': 'beginner',
                                                                'focus': 'beginner',
                                                                'exercises': [{'name': 'Stance Hold Circuit',
                                                                               'prescription': 'Front stance: 1 minute '
                                                                                               'Back stance: 1 minute '
                                                                                               'Horse stance: 1 minute '
                                                                                               'Repeat 3 rounds.'},
                                                                              {'name': 'Straight Punch Volume',
                                                                               'prescription': 'Perform 300 straight '
                                                                                               'punches.'},
                                                                              {'name': 'Reverse Punch Volume',
                                                                               'prescription': 'Perform 200 reverse '
                                                                                               'punches.'},
                                                                              {'name': 'Front Kick Volume',
                                                                               'prescription': 'Perform 100 front '
                                                                                               'kicks per leg.'},
                                                                              {'name': 'Roundhouse Kick Introduction',
                                                                               'prescription': 'Perform 100 roundhouse '
                                                                                               'kicks per leg.'},
                                                                              {'name': 'Side Kick Introduction',
                                                                               'prescription': 'Perform 50 side kicks '
                                                                                               'per leg.'},
                                                                              {'name': 'Block Combination Drill',
                                                                               'prescription': 'Low block → middle '
                                                                                               'block → rising block. '
                                                                                               'Repeat 100 sequences.'},
                                                                              {'name': 'Step-and-Punch Drill',
                                                                               'prescription': 'Step forward and '
                                                                                               'punch. Repeat 100 '
                                                                                               'times.'},
                                                                              {'name': 'Shadow Sparring',
                                                                               'prescription': '3-minute round. '
                                                                                               'Complete 5 rounds.'},
                                                                              {'name': 'Speed Punch Drill',
                                                                               'prescription': 'Throw as many punches '
                                                                                               'as possible in 30 '
                                                                                               'seconds. Complete 5 '
                                                                                               'rounds.'},
                                                                              {'name': 'Speed Kick Drill',
                                                                               'prescription': 'Throw as many front '
                                                                                               'kicks as possible in '
                                                                                               '30 seconds. Complete 5 '
                                                                                               'rounds.'},
                                                                              {'name': 'Beginner Conditioning Circuit',
                                                                               'prescription': '20 push-ups 30 squats '
                                                                                               '30 sit-ups Repeat 5 '
                                                                                               'rounds.'}]}}},
 'karate_kihon_fundamentals': {'alone': {'martial_arts_karate_kihon_fundamentals': {'key': 'martial_arts_karate_kihon_fundamentals',
                                                                                    'sport': 'Martial Arts',
                                                                                    'martial_art': 'Karate',
                                                                                    'title': 'Karate – Kihon '
                                                                                             '(Fundamentals)',
                                                                                    'category': 'karate_kihon_fundamentals',
                                                                                    'training_mode': 'alone',
                                                                                    'level': 'all_levels',
                                                                                    'focus': 'kihon (fundamentals)',
                                                                                    'exercises': [{'name': 'Front '
                                                                                                           'Stance '
                                                                                                           'Walk',
                                                                                                   'prescription': 'Walk '
                                                                                                                   '50 '
                                                                                                                   'meters '
                                                                                                                   'in '
                                                                                                                   'front '
                                                                                                                   'stance.'},
                                                                                                  {'name': 'Horse '
                                                                                                           'Stance '
                                                                                                           'Hold',
                                                                                                   'prescription': 'Hold '
                                                                                                                   'horse '
                                                                                                                   'stance '
                                                                                                                   'for '
                                                                                                                   '3 '
                                                                                                                   'minutes. '
                                                                                                                   'Repeat '
                                                                                                                   '3 '
                                                                                                                   'times.'},
                                                                                                  {'name': 'Reverse '
                                                                                                           'Punch '
                                                                                                           'Repetitions',
                                                                                                   'prescription': 'Perform '
                                                                                                                   '200 '
                                                                                                                   'reverse '
                                                                                                                   'punches.'},
                                                                                                  {'name': 'Front '
                                                                                                           'Punch '
                                                                                                           'Repetitions',
                                                                                                   'prescription': 'Perform '
                                                                                                                   '200 '
                                                                                                                   'front '
                                                                                                                   'punches.'},
                                                                                                  {'name': 'Low Block '
                                                                                                           'Repetitions',
                                                                                                   'prescription': 'Perform '
                                                                                                                   '200 '
                                                                                                                   'low '
                                                                                                                   'blocks.'},
                                                                                                  {'name': 'Middle '
                                                                                                           'Block '
                                                                                                           'Repetitions',
                                                                                                   'prescription': 'Perform '
                                                                                                                   '200 '
                                                                                                                   'middle '
                                                                                                                   'blocks.'},
                                                                                                  {'name': 'Rising '
                                                                                                           'Block '
                                                                                                           'Repetitions',
                                                                                                   'prescription': 'Perform '
                                                                                                                   '200 '
                                                                                                                   'rising '
                                                                                                                   'blocks.'},
                                                                                                  {'name': 'Knife-Hand '
                                                                                                           'Block',
                                                                                                   'prescription': 'Perform '
                                                                                                                   '100 '
                                                                                                                   'knife-hand '
                                                                                                                   'blocks '
                                                                                                                   'per '
                                                                                                                   'arm.'},
                                                                                                  {'name': 'Step-and-Block '
                                                                                                           'Drill',
                                                                                                   'prescription': 'Step '
                                                                                                                   'forward '
                                                                                                                   'and '
                                                                                                                   'block. '
                                                                                                                   'Repeat '
                                                                                                                   '100 '
                                                                                                                   'times.'},
                                                                                                  {'name': 'Step-and-Punch '
                                                                                                           'Drill',
                                                                                                   'prescription': 'Step '
                                                                                                                   'forward '
                                                                                                                   'and '
                                                                                                                   'punch. '
                                                                                                                   'Repeat '
                                                                                                                   '100 '
                                                                                                                   'times.'},
                                                                                                  {'name': 'Kihon '
                                                                                                           'Combination',
                                                                                                   'prescription': 'Block '
                                                                                                                   '→ '
                                                                                                                   'punch. '
                                                                                                                   'Repeat '
                                                                                                                   '200 '
                                                                                                                   'times.'},
                                                                                                  {'name': 'Full Kihon '
                                                                                                           'Sequence',
                                                                                                   'prescription': 'Execute '
                                                                                                                   '20 '
                                                                                                                   'different '
                                                                                                                   'techniques '
                                                                                                                   'in '
                                                                                                                   'sequence. '
                                                                                                                   'Repeat '
                                                                                                                   '10 '
                                                                                                                   'rounds.'}]}}},
 'karate_kata': {'alone': {'martial_arts_karate_kata': {'key': 'martial_arts_karate_kata',
                                                        'sport': 'Martial Arts',
                                                        'martial_art': 'Karate',
                                                        'title': 'Karate – Kata',
                                                        'category': 'karate_kata',
                                                        'training_mode': 'alone',
                                                        'level': 'all_levels',
                                                        'focus': 'kata',
                                                        'exercises': [{'name': 'Kata Walkthrough',
                                                                       'prescription': 'Perform chosen kata slowly 10 '
                                                                                       'times.'},
                                                                      {'name': 'Competition Kata',
                                                                       'prescription': 'Perform chosen kata at full '
                                                                                       'speed 10 times.'},
                                                                      {'name': 'Power Kata',
                                                                       'prescription': 'Execute kata emphasizing '
                                                                                       'maximum power. Repeat 5 '
                                                                                       'times.'},
                                                                      {'name': 'Balance Kata',
                                                                       'prescription': 'Hold each stance for 5 seconds '
                                                                                       'during kata. Repeat 5 times.'},
                                                                      {'name': 'Mirror Kata',
                                                                       'prescription': 'Perform kata while checking '
                                                                                       'technique in a mirror. Repeat '
                                                                                       '10 times.'},
                                                                      {'name': 'Stance Correction Drill',
                                                                       'prescription': 'Hold every kata stance for 30 '
                                                                                       'seconds. Complete all '
                                                                                       'stances.'},
                                                                      {'name': 'First Sequence Repetition',
                                                                       'prescription': 'Perform first sequence of kata '
                                                                                       '50 times.'},
                                                                      {'name': 'Middle Sequence Repetition',
                                                                       'prescription': 'Perform middle sequence 50 '
                                                                                       'times.'},
                                                                      {'name': 'Final Sequence Repetition',
                                                                       'prescription': 'Perform final sequence 50 '
                                                                                       'times.'},
                                                                      {'name': 'Slow Motion Kata',
                                                                       'prescription': 'Perform entire kata in 5 '
                                                                                       'minutes. Repeat 3 times.'},
                                                                      {'name': 'Explosive Kata',
                                                                       'prescription': 'Perform kata as fast as '
                                                                                       'possible. Repeat 10 times.'},
                                                                      {'name': 'Tournament Simulation',
                                                                       'prescription': 'Perform kata exactly as if '
                                                                                       'being judged. Complete 10 '
                                                                                       'attempts.'}]}}},
 'karate_punching': {'alone': {'martial_arts_karate_punching': {'key': 'martial_arts_karate_punching',
                                                                'sport': 'Martial Arts',
                                                                'martial_art': 'Karate',
                                                                'title': 'Karate – Punching',
                                                                'category': 'karate_punching',
                                                                'training_mode': 'alone',
                                                                'level': 'all_levels',
                                                                'focus': 'punching',
                                                                'exercises': [{'name': 'Straight Punch Volume',
                                                                               'prescription': 'Perform 500 straight '
                                                                                               'punches.'},
                                                                              {'name': 'Reverse Punch Volume',
                                                                               'prescription': 'Perform 300 reverse '
                                                                                               'punches.'},
                                                                              {'name': 'Jab-Reverse Combination',
                                                                               'prescription': 'Perform 200 '
                                                                                               'combinations.'},
                                                                              {'name': 'Triple Punch Combination',
                                                                               'prescription': 'Perform 100 '
                                                                                               'combinations.'},
                                                                              {'name': 'Punch While Advancing',
                                                                               'prescription': 'Advance while punching '
                                                                                               'for 50 meters. Repeat '
                                                                                               '5 rounds.'},
                                                                              {'name': 'Punch While Retreating',
                                                                               'prescription': 'Move backward while '
                                                                                               'punching. Repeat 100 '
                                                                                               'repetitions.'},
                                                                              {'name': 'Speed Punch Round',
                                                                               'prescription': 'Punch continuously for '
                                                                                               '1 minute. Complete 5 '
                                                                                               'rounds.'},
                                                                              {'name': 'Heavy Bag Punches',
                                                                               'prescription': 'Throw 200 powerful '
                                                                                               'punches.'},
                                                                              {'name': 'One-Step Attack Drill',
                                                                               'prescription': 'Step and reverse '
                                                                                               'punch. Repeat 200 '
                                                                                               'times.'},
                                                                              {'name': 'Counter Punch Drill',
                                                                               'prescription': 'Simulate opponent '
                                                                                               'attack. Execute '
                                                                                               'counter punch. Repeat '
                                                                                               '100 times.'},
                                                                              {'name': 'Shadow Punch Sparring',
                                                                               'prescription': '3-minute rounds. '
                                                                                               'Complete 5 rounds.'},
                                                                              {'name': 'Punch Endurance Challenge',
                                                                               'prescription': 'Perform 1,000 punches '
                                                                                               'without stopping.'}]}}},
 'karate_kicking': {'alone': {'martial_arts_karate_kicking': {'key': 'martial_arts_karate_kicking',
                                                              'sport': 'Martial Arts',
                                                              'martial_art': 'Karate',
                                                              'title': 'Karate – Kicking',
                                                              'category': 'karate_kicking',
                                                              'training_mode': 'alone',
                                                              'level': 'all_levels',
                                                              'focus': 'kicking',
                                                              'exercises': [{'name': 'Front Kick Volume',
                                                                             'prescription': 'Perform 200 front kicks '
                                                                                             'per leg.'},
                                                                            {'name': 'Roundhouse Kick Volume',
                                                                             'prescription': 'Perform 200 roundhouse '
                                                                                             'kicks per leg.'},
                                                                            {'name': 'Side Kick Volume',
                                                                             'prescription': 'Perform 100 side kicks '
                                                                                             'per leg.'},
                                                                            {'name': 'Back Kick Volume',
                                                                             'prescription': 'Perform 100 back kicks '
                                                                                             'per leg.'},
                                                                            {'name': 'High Kick Volume',
                                                                             'prescription': 'Perform 100 high kicks '
                                                                                             'per leg.'},
                                                                            {'name': 'Front Kick Speed Drill',
                                                                             'prescription': 'Perform maximum kicks in '
                                                                                             '30 seconds. Complete 10 '
                                                                                             'rounds.'},
                                                                            {'name': 'Roundhouse Speed Drill',
                                                                             'prescription': 'Perform maximum kicks in '
                                                                                             '30 seconds. Complete 10 '
                                                                                             'rounds.'},
                                                                            {'name': 'Kick-and-Step Drill',
                                                                             'prescription': 'Kick and immediately '
                                                                                             'move. Repeat 100 times.'},
                                                                            {'name': 'Jump Front Kick',
                                                                             'prescription': 'Perform 50 repetitions.'},
                                                                            {'name': 'Jump Roundhouse Kick',
                                                                             'prescription': 'Perform 50 repetitions.'},
                                                                            {'name': 'Shadow Kicking Round',
                                                                             'prescription': 'Kick continuously for 2 '
                                                                                             'minutes. Complete 5 '
                                                                                             'rounds.'},
                                                                            {'name': 'Kick Endurance Challenge',
                                                                             'prescription': 'Perform 500 total '
                                                                                             'kicks.'}]}}},
 'karate_kumite_sparring': {'alone': {'martial_arts_karate_kumite_sparring': {'key': 'martial_arts_karate_kumite_sparring',
                                                                              'sport': 'Martial Arts',
                                                                              'martial_art': 'Karate',
                                                                              'title': 'Karate – Kumite (Sparring)',
                                                                              'category': 'karate_kumite_sparring',
                                                                              'training_mode': 'alone',
                                                                              'level': 'all_levels',
                                                                              'focus': 'kumite (sparring)',
                                                                              'exercises': [{'name': 'Shadow Sparring',
                                                                                             'prescription': '3-minute '
                                                                                                             'round. '
                                                                                                             'Complete '
                                                                                                             '10 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Entry Drill',
                                                                                             'prescription': 'Simulate '
                                                                                                             'entering '
                                                                                                             'punching '
                                                                                                             'range. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Exit Drill',
                                                                                             'prescription': 'Enter '
                                                                                                             'and '
                                                                                                             'leave '
                                                                                                             'range. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Counterattack '
                                                                                                     'Drill',
                                                                                             'prescription': 'Simulate '
                                                                                                             'opponent '
                                                                                                             'attack. '
                                                                                                             'Counter '
                                                                                                             'immediately. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Angle Change '
                                                                                                     'Drill',
                                                                                             'prescription': 'Move '
                                                                                                             'left, '
                                                                                                             'attack. '
                                                                                                             'Move '
                                                                                                             'right, '
                                                                                                             'attack. '
                                                                                                             'Repeat '
                                                                                                             '100 '
                                                                                                             'times.'},
                                                                                            {'name': 'Distance '
                                                                                                     'Management Drill',
                                                                                             'prescription': 'Advance '
                                                                                                             'and '
                                                                                                             'retreat '
                                                                                                             'continuously. '
                                                                                                             '5 rounds '
                                                                                                             'of 2 '
                                                                                                             'minutes.'},
                                                                                            {'name': 'One-Technique '
                                                                                                     'Sparring',
                                                                                             'prescription': 'Use only '
                                                                                                             'reverse '
                                                                                                             'punches. '
                                                                                                             '5 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Kick-Only '
                                                                                                     'Sparring Shadow',
                                                                                             'prescription': 'Use only '
                                                                                                             'kicks. 5 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Punch-Only '
                                                                                                     'Sparring Shadow',
                                                                                             'prescription': 'Use only '
                                                                                                             'punches. '
                                                                                                             '5 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Speed Reaction '
                                                                                                     'Drill',
                                                                                             'prescription': 'Visualize '
                                                                                                             'attacks '
                                                                                                             'and '
                                                                                                             'react. '
                                                                                                             '100 '
                                                                                                             'repetitions.'},
                                                                                            {'name': 'Competition '
                                                                                                     'Round Simulation',
                                                                                             'prescription': '3-minute '
                                                                                                             'rounds. '
                                                                                                             'Complete '
                                                                                                             '5 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Tournament '
                                                                                                     'Simulation',
                                                                                             'prescription': 'Complete '
                                                                                                             '3 full '
                                                                                                             'match '
                                                                                                             'simulations.'}]}}},
 'karate_conditioning': {'alone': {'martial_arts_karate_conditioning': {'key': 'martial_arts_karate_conditioning',
                                                                        'sport': 'Martial Arts',
                                                                        'martial_art': 'Karate',
                                                                        'title': 'Karate – Conditioning',
                                                                        'category': 'karate_conditioning',
                                                                        'training_mode': 'alone',
                                                                        'level': 'all_levels',
                                                                        'focus': 'conditioning',
                                                                        'exercises': [{'name': 'Finger Push-Ups',
                                                                                       'prescription': '30 '
                                                                                                       'repetitions. '
                                                                                                       'Complete 5 '
                                                                                                       'sets.'},
                                                                                      {'name': 'Knuckle Push-Ups',
                                                                                       'prescription': '50 '
                                                                                                       'repetitions. '
                                                                                                       'Complete 5 '
                                                                                                       'sets.'},
                                                                                      {'name': 'Standard Push-Ups',
                                                                                       'prescription': '50 '
                                                                                                       'repetitions. '
                                                                                                       'Complete 5 '
                                                                                                       'sets.'},
                                                                                      {'name': 'Bodyweight Squats',
                                                                                       'prescription': '100 '
                                                                                                       'repetitions. '
                                                                                                       'Complete 5 '
                                                                                                       'sets.'},
                                                                                      {'name': 'Jump Squats',
                                                                                       'prescription': '50 '
                                                                                                       'repetitions. '
                                                                                                       'Complete 5 '
                                                                                                       'sets.'},
                                                                                      {'name': 'Sit-Ups',
                                                                                       'prescription': '100 '
                                                                                                       'repetitions. '
                                                                                                       'Complete 5 '
                                                                                                       'sets.'},
                                                                                      {'name': 'Leg Raises',
                                                                                       'prescription': '50 '
                                                                                                       'repetitions. '
                                                                                                       'Complete 5 '
                                                                                                       'sets.'},
                                                                                      {'name': 'Plank Hold',
                                                                                       'prescription': '2 minutes. '
                                                                                                       'Complete 5 '
                                                                                                       'rounds.'},
                                                                                      {'name': 'Horse Stance Hold',
                                                                                       'prescription': 'Hold 5 '
                                                                                                       'minutes. '
                                                                                                       'Complete 3 '
                                                                                                       'rounds.'},
                                                                                      {'name': 'Sprint Intervals',
                                                                                       'prescription': 'Sprint 100 '
                                                                                                       'meters. Repeat '
                                                                                                       '10 times.'},
                                                                                      {'name': 'Burpee Circuit',
                                                                                       'prescription': 'Perform 100 '
                                                                                                       'burpees.'},
                                                                                      {'name': 'Karate Warrior Circuit',
                                                                                       'prescription': '50 knuckle '
                                                                                                       'push-ups 100 '
                                                                                                       'squats 100 '
                                                                                                       'punches 50 '
                                                                                                       'kicks per leg '
                                                                                                       'Repeat 3 '
                                                                                                       'rounds.'}]}}},
 'taekwondo_learn_how_to_play': {'alone': {'martial_arts_taekwondo_learn_how_to_play': {'key': 'martial_arts_taekwondo_learn_how_to_play',
                                                                                        'sport': 'Martial Arts',
                                                                                        'martial_art': 'Taekwondo',
                                                                                        'title': 'Taekwondo – Learn '
                                                                                                 'How To Play',
                                                                                        'category': 'taekwondo_learn_how_to_play',
                                                                                        'training_mode': 'alone',
                                                                                        'level': 'learn_how_to_play',
                                                                                        'focus': 'learn how to play',
                                                                                        'exercises': [{'name': 'Fighting '
                                                                                                               'Stance '
                                                                                                               'Practice',
                                                                                                       'prescription': 'Assume '
                                                                                                                       'taekwondo '
                                                                                                                       'fighting '
                                                                                                                       'stance. '
                                                                                                                       'Hold '
                                                                                                                       'for '
                                                                                                                       '30 '
                                                                                                                       'seconds. '
                                                                                                                       'Repeat '
                                                                                                                       '10 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Basic '
                                                                                                               'Footwork '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Move '
                                                                                                                       'forward '
                                                                                                                       '10 '
                                                                                                                       'steps. '
                                                                                                                       'Move '
                                                                                                                       'backward '
                                                                                                                       '10 '
                                                                                                                       'steps. '
                                                                                                                       'Repeat '
                                                                                                                       '10 '
                                                                                                                       'rounds.'},
                                                                                                      {'name': 'Guard '
                                                                                                               'Position '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Hold '
                                                                                                                       'guard '
                                                                                                                       'position '
                                                                                                                       'for '
                                                                                                                       '1 '
                                                                                                                       'minute. '
                                                                                                                       'Repeat '
                                                                                                                       '5 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Front '
                                                                                                               'Kick '
                                                                                                               'Introduction',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '50 '
                                                                                                                       'front '
                                                                                                                       'kicks '
                                                                                                                       'per '
                                                                                                                       'leg.'},
                                                                                                      {'name': 'Roundhouse '
                                                                                                               'Kick '
                                                                                                               'Introduction',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '50 '
                                                                                                                       'roundhouse '
                                                                                                                       'kicks '
                                                                                                                       'per '
                                                                                                                       'leg.'},
                                                                                                      {'name': 'Side '
                                                                                                               'Kick '
                                                                                                               'Introduction',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '30 '
                                                                                                                       'side '
                                                                                                                       'kicks '
                                                                                                                       'per '
                                                                                                                       'leg.'},
                                                                                                      {'name': 'Basic '
                                                                                                               'Punch '
                                                                                                               'Practice',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '100 '
                                                                                                                       'straight '
                                                                                                                       'punches.'},
                                                                                                      {'name': 'Block '
                                                                                                               'Practice',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '50 '
                                                                                                                       'low '
                                                                                                                       'blocks. '
                                                                                                                       'Perform '
                                                                                                                       '50 '
                                                                                                                       'middle '
                                                                                                                       'blocks. '
                                                                                                                       'Perform '
                                                                                                                       '50 '
                                                                                                                       'high '
                                                                                                                       'blocks.'},
                                                                                                      {'name': 'Kick '
                                                                                                               'and '
                                                                                                               'Return '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Throw '
                                                                                                                       'a '
                                                                                                                       'kick '
                                                                                                                       'and '
                                                                                                                       'immediately '
                                                                                                                       'return '
                                                                                                                       'to '
                                                                                                                       'stance. '
                                                                                                                       'Repeat '
                                                                                                                       '100 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Balance '
                                                                                                               'Hold '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Raise '
                                                                                                                       'one '
                                                                                                                       'knee '
                                                                                                                       'into '
                                                                                                                       'kicking '
                                                                                                                       'position. '
                                                                                                                       'Hold '
                                                                                                                       'for '
                                                                                                                       '15 '
                                                                                                                       'seconds. '
                                                                                                                       'Repeat '
                                                                                                                       '20 '
                                                                                                                       'times '
                                                                                                                       'per '
                                                                                                                       'leg.'},
                                                                                                      {'name': 'Shadow '
                                                                                                               'Taekwondo '
                                                                                                               'Round',
                                                                                                       'prescription': 'Practice '
                                                                                                                       'kicks, '
                                                                                                                       'punches, '
                                                                                                                       'blocks, '
                                                                                                                       'and '
                                                                                                                       'movement '
                                                                                                                       'for '
                                                                                                                       '2 '
                                                                                                                       'minutes. '
                                                                                                                       'Complete '
                                                                                                                       '5 '
                                                                                                                       'rounds.'},
                                                                                                      {'name': 'Beginner '
                                                                                                               'Coordination '
                                                                                                               'Circuit',
                                                                                                       'prescription': '20 '
                                                                                                                       'punches '
                                                                                                                       '20 '
                                                                                                                       'front '
                                                                                                                       'kicks '
                                                                                                                       '20 '
                                                                                                                       'roundhouse '
                                                                                                                       'kicks '
                                                                                                                       'Repeat '
                                                                                                                       '5 '
                                                                                                                       'rounds.'}]}}},
 'taekwondo_beginner': {'alone': {'martial_arts_taekwondo_beginner': {'key': 'martial_arts_taekwondo_beginner',
                                                                      'sport': 'Martial Arts',
                                                                      'martial_art': 'Taekwondo',
                                                                      'title': 'Taekwondo – Beginner',
                                                                      'category': 'taekwondo_beginner',
                                                                      'training_mode': 'alone',
                                                                      'level': 'beginner',
                                                                      'focus': 'beginner',
                                                                      'exercises': [{'name': 'Fighting Stance Circuit',
                                                                                     'prescription': 'Hold fighting '
                                                                                                     'stance for 1 '
                                                                                                     'minute. Repeat 5 '
                                                                                                     'rounds.'},
                                                                                    {'name': 'Front Kick Volume',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'front kicks per '
                                                                                                     'leg.'},
                                                                                    {'name': 'Roundhouse Kick Volume',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'roundhouse kicks '
                                                                                                     'per leg.'},
                                                                                    {'name': 'Side Kick Volume',
                                                                                     'prescription': 'Perform 50 side '
                                                                                                     'kicks per leg.'},
                                                                                    {'name': 'Back Kick Introduction',
                                                                                     'prescription': 'Perform 50 back '
                                                                                                     'kicks per leg.'},
                                                                                    {'name': 'Punch and Kick '
                                                                                             'Combination',
                                                                                     'prescription': 'Throw 1 punch '
                                                                                                     'and 1 roundhouse '
                                                                                                     'kick. Repeat 100 '
                                                                                                     'times.'},
                                                                                    {'name': 'Footwork Circuit',
                                                                                     'prescription': 'Move forward, '
                                                                                                     'backward, left, '
                                                                                                     'and right. '
                                                                                                     'Repeat 50 '
                                                                                                     'rounds.'},
                                                                                    {'name': 'Speed Kick Drill',
                                                                                     'prescription': 'Perform maximum '
                                                                                                     'front kicks in '
                                                                                                     '30 seconds. '
                                                                                                     'Complete 5 '
                                                                                                     'rounds.'},
                                                                                    {'name': 'Shadow Sparring',
                                                                                     'prescription': '3-minute round. '
                                                                                                     'Complete 5 '
                                                                                                     'rounds.'},
                                                                                    {'name': 'Jumping Knee Raise',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'repetitions.'},
                                                                                    {'name': 'Balance Challenge',
                                                                                     'prescription': 'Stand on one leg '
                                                                                                     'for 1 minute. '
                                                                                                     'Repeat 5 times '
                                                                                                     'per side.'},
                                                                                    {'name': 'Beginner Conditioning '
                                                                                             'Circuit',
                                                                                     'prescription': '20 push-ups 30 '
                                                                                                     'squats 20 lunges '
                                                                                                     'per leg Repeat 5 '
                                                                                                     'rounds.'}]}}},
 'taekwondo_fundamentals': {'alone': {'martial_arts_taekwondo_fundamentals': {'key': 'martial_arts_taekwondo_fundamentals',
                                                                              'sport': 'Martial Arts',
                                                                              'martial_art': 'Taekwondo',
                                                                              'title': 'Taekwondo – Fundamentals',
                                                                              'category': 'taekwondo_fundamentals',
                                                                              'training_mode': 'alone',
                                                                              'level': 'all_levels',
                                                                              'focus': 'fundamentals',
                                                                              'exercises': [{'name': 'Fighting Stance '
                                                                                                     'Walk',
                                                                                             'prescription': 'Move '
                                                                                                             'continuously '
                                                                                                             'in '
                                                                                                             'fighting '
                                                                                                             'stance '
                                                                                                             'for 50 '
                                                                                                             'meters. '
                                                                                                             'Repeat 5 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Guard Recovery '
                                                                                                     'Drill',
                                                                                             'prescription': 'Drop '
                                                                                                             'guard '
                                                                                                             'and '
                                                                                                             'immediately '
                                                                                                             'recover. '
                                                                                                             'Repeat '
                                                                                                             '100 '
                                                                                                             'times.'},
                                                                                            {'name': 'Footwork Ladder',
                                                                                             'prescription': 'Forward '
                                                                                                             'and '
                                                                                                             'backward '
                                                                                                             'movement '
                                                                                                             'for 5 '
                                                                                                             'minutes.'},
                                                                                            {'name': 'Side Movement '
                                                                                                     'Drill',
                                                                                             'prescription': 'Move '
                                                                                                             'left and '
                                                                                                             'right '
                                                                                                             'continuously '
                                                                                                             'for 5 '
                                                                                                             'minutes.'},
                                                                                            {'name': 'Stance Switching '
                                                                                                     'Drill',
                                                                                             'prescription': 'Switch '
                                                                                                             'lead leg '
                                                                                                             'position. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Front Kick '
                                                                                                     'Chamber Hold',
                                                                                             'prescription': 'Hold '
                                                                                                             'chamber '
                                                                                                             'position '
                                                                                                             'for 10 '
                                                                                                             'seconds. '
                                                                                                             'Repeat '
                                                                                                             '30 times '
                                                                                                             'per '
                                                                                                             'leg.'},
                                                                                            {'name': 'Roundhouse '
                                                                                                     'Chamber Hold',
                                                                                             'prescription': 'Hold '
                                                                                                             'chamber '
                                                                                                             'position '
                                                                                                             'for 10 '
                                                                                                             'seconds. '
                                                                                                             'Repeat '
                                                                                                             '30 times '
                                                                                                             'per '
                                                                                                             'leg.'},
                                                                                            {'name': 'Balance Recovery '
                                                                                                     'Drill',
                                                                                             'prescription': 'Perform '
                                                                                                             'kick and '
                                                                                                             'freeze '
                                                                                                             'for 3 '
                                                                                                             'seconds. '
                                                                                                             'Repeat '
                                                                                                             '100 '
                                                                                                             'times.'},
                                                                                            {'name': 'Basic Punch '
                                                                                                     'Drill',
                                                                                             'prescription': 'Perform '
                                                                                                             '300 '
                                                                                                             'straight '
                                                                                                             'punches.'},
                                                                                            {'name': 'Basic Block '
                                                                                                     'Circuit',
                                                                                             'prescription': '100 low '
                                                                                                             'blocks '
                                                                                                             '100 '
                                                                                                             'middle '
                                                                                                             'blocks '
                                                                                                             '100 high '
                                                                                                             'blocks'},
                                                                                            {'name': 'Kick and Step '
                                                                                                     'Drill',
                                                                                             'prescription': 'Kick, '
                                                                                                             'land, '
                                                                                                             'move. '
                                                                                                             'Repeat '
                                                                                                             '100 '
                                                                                                             'times.'},
                                                                                            {'name': 'Full '
                                                                                                     'Fundamentals '
                                                                                                     'Sequence',
                                                                                             'prescription': 'Combine '
                                                                                                             'footwork, '
                                                                                                             'guard, '
                                                                                                             'punch, '
                                                                                                             'and '
                                                                                                             'kick. '
                                                                                                             'Repeat '
                                                                                                             '50 '
                                                                                                             'rounds.'}]}}},
 'taekwondo_poomsae': {'alone': {'martial_arts_taekwondo_poomsae': {'key': 'martial_arts_taekwondo_poomsae',
                                                                    'sport': 'Martial Arts',
                                                                    'martial_art': 'Taekwondo',
                                                                    'title': 'Taekwondo – Poomsae',
                                                                    'category': 'taekwondo_poomsae',
                                                                    'training_mode': 'alone',
                                                                    'level': 'all_levels',
                                                                    'focus': 'poomsae',
                                                                    'exercises': [{'name': 'Poomsae Walkthrough',
                                                                                   'prescription': 'Perform chosen '
                                                                                                   'poomsae slowly 10 '
                                                                                                   'times.'},
                                                                                  {'name': 'Competition Poomsae',
                                                                                   'prescription': 'Perform poomsae at '
                                                                                                   'full speed 10 '
                                                                                                   'times.'},
                                                                                  {'name': 'Power Poomsae',
                                                                                   'prescription': 'Emphasize maximum '
                                                                                                   'force. Repeat 5 '
                                                                                                   'times.'},
                                                                                  {'name': 'Precision Poomsae',
                                                                                   'prescription': 'Focus on exact '
                                                                                                   'technique. Repeat '
                                                                                                   '10 times.'},
                                                                                  {'name': 'Balance Poomsae',
                                                                                   'prescription': 'Hold each stance '
                                                                                                   'for 5 seconds. '
                                                                                                   'Repeat 5 times.'},
                                                                                  {'name': 'Mirror Poomsae',
                                                                                   'prescription': 'Perform poomsae '
                                                                                                   'while checking '
                                                                                                   'form. Repeat 10 '
                                                                                                   'times.'},
                                                                                  {'name': 'Opening Sequence '
                                                                                           'Repetition',
                                                                                   'prescription': 'Repeat opening '
                                                                                                   'sequence 50 '
                                                                                                   'times.'},
                                                                                  {'name': 'Middle Sequence Repetition',
                                                                                   'prescription': 'Repeat middle '
                                                                                                   'sequence 50 '
                                                                                                   'times.'},
                                                                                  {'name': 'Final Sequence Repetition',
                                                                                   'prescription': 'Repeat final '
                                                                                                   'sequence 50 '
                                                                                                   'times.'},
                                                                                  {'name': 'Slow Motion Poomsae',
                                                                                   'prescription': 'Complete poomsae '
                                                                                                   'in 5 minutes. '
                                                                                                   'Repeat 3 times.'},
                                                                                  {'name': 'Explosive Poomsae',
                                                                                   'prescription': 'Perform as quickly '
                                                                                                   'as possible. '
                                                                                                   'Repeat 10 times.'},
                                                                                  {'name': 'Tournament Simulation',
                                                                                   'prescription': 'Perform poomsae as '
                                                                                                   'if being judged. '
                                                                                                   'Complete 10 '
                                                                                                   'attempts.'}]}}},
 'taekwondo_speed_kicking': {'alone': {'martial_arts_taekwondo_speed_kicking': {'key': 'martial_arts_taekwondo_speed_kicking',
                                                                                'sport': 'Martial Arts',
                                                                                'martial_art': 'Taekwondo',
                                                                                'title': 'Taekwondo – Speed Kicking',
                                                                                'category': 'taekwondo_speed_kicking',
                                                                                'training_mode': 'alone',
                                                                                'level': 'all_levels',
                                                                                'focus': 'speed kicking',
                                                                                'exercises': [{'name': 'Front Kick '
                                                                                                       'Sprint',
                                                                                               'prescription': 'Maximum '
                                                                                                               'front '
                                                                                                               'kicks '
                                                                                                               'in 30 '
                                                                                                               'seconds. '
                                                                                                               'Complete '
                                                                                                               '10 '
                                                                                                               'rounds.'},
                                                                                              {'name': 'Roundhouse '
                                                                                                       'Kick Sprint',
                                                                                               'prescription': 'Maximum '
                                                                                                               'roundhouse '
                                                                                                               'kicks '
                                                                                                               'in 30 '
                                                                                                               'seconds. '
                                                                                                               'Complete '
                                                                                                               '10 '
                                                                                                               'rounds.'},
                                                                                              {'name': 'Double Kick '
                                                                                                       'Drill',
                                                                                               'prescription': 'Perform '
                                                                                                               '100 '
                                                                                                               'double '
                                                                                                               'roundhouse '
                                                                                                               'kicks.'},
                                                                                              {'name': 'Triple Kick '
                                                                                                       'Drill',
                                                                                               'prescription': 'Perform '
                                                                                                               '50 '
                                                                                                               'triple '
                                                                                                               'kick '
                                                                                                               'combinations.'},
                                                                                              {'name': 'Fast '
                                                                                                       'Alternating '
                                                                                                       'Kicks',
                                                                                               'prescription': 'Alternate '
                                                                                                               'legs '
                                                                                                               'continuously '
                                                                                                               'for 1 '
                                                                                                               'minute. '
                                                                                                               'Complete '
                                                                                                               '5 '
                                                                                                               'rounds.'},
                                                                                              {'name': 'Lead Leg '
                                                                                                       'Roundhouse '
                                                                                                       'Drill',
                                                                                               'prescription': 'Perform '
                                                                                                               '200 '
                                                                                                               'lead-leg '
                                                                                                               'roundhouse '
                                                                                                               'kicks.'},
                                                                                              {'name': 'Rear Leg '
                                                                                                       'Roundhouse '
                                                                                                       'Drill',
                                                                                               'prescription': 'Perform '
                                                                                                               '200 '
                                                                                                               'rear-leg '
                                                                                                               'roundhouse '
                                                                                                               'kicks.'},
                                                                                              {'name': 'Front Leg Push '
                                                                                                       'Kick',
                                                                                               'prescription': 'Perform '
                                                                                                               '150 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Kick Ladder '
                                                                                                       'Challenge',
                                                                                               'prescription': '10 '
                                                                                                               'kicks '
                                                                                                               '20 '
                                                                                                               'kicks '
                                                                                                               '30 '
                                                                                                               'kicks '
                                                                                                               'Continue '
                                                                                                               'to '
                                                                                                               '100.'},
                                                                                              {'name': 'Speed '
                                                                                                       'Combination '
                                                                                                       'Drill',
                                                                                               'prescription': 'Roundhouse '
                                                                                                               '→ '
                                                                                                               'roundhouse. '
                                                                                                               'Repeat '
                                                                                                               '200 '
                                                                                                               'times.'},
                                                                                              {'name': 'Shadow Speed '
                                                                                                       'Round',
                                                                                               'prescription': 'Kick '
                                                                                                               'continuously '
                                                                                                               'for 2 '
                                                                                                               'minutes. '
                                                                                                               'Complete '
                                                                                                               '5 '
                                                                                                               'rounds.'},
                                                                                              {'name': '500 Kick '
                                                                                                       'Challenge',
                                                                                               'prescription': 'Perform '
                                                                                                               '500 '
                                                                                                               'total '
                                                                                                               'kicks '
                                                                                                               'as '
                                                                                                               'quickly '
                                                                                                               'as '
                                                                                                               'possible.'}]}}},
 'taekwondo_power_kicking': {'alone': {'martial_arts_taekwondo_power_kicking': {'key': 'martial_arts_taekwondo_power_kicking',
                                                                                'sport': 'Martial Arts',
                                                                                'martial_art': 'Taekwondo',
                                                                                'title': 'Taekwondo – Power Kicking',
                                                                                'category': 'taekwondo_power_kicking',
                                                                                'training_mode': 'alone',
                                                                                'level': 'all_levels',
                                                                                'focus': 'power kicking',
                                                                                'exercises': [{'name': 'Power Front '
                                                                                                       'Kick',
                                                                                               'prescription': 'Perform '
                                                                                                               '100 '
                                                                                                               'maximum-power '
                                                                                                               'kicks '
                                                                                                               'per '
                                                                                                               'leg.'},
                                                                                              {'name': 'Power '
                                                                                                       'Roundhouse '
                                                                                                       'Kick',
                                                                                               'prescription': 'Perform '
                                                                                                               '100 '
                                                                                                               'maximum-power '
                                                                                                               'kicks '
                                                                                                               'per '
                                                                                                               'leg.'},
                                                                                              {'name': 'Power Side '
                                                                                                       'Kick',
                                                                                               'prescription': 'Perform '
                                                                                                               '100 '
                                                                                                               'maximum-power '
                                                                                                               'kicks '
                                                                                                               'per '
                                                                                                               'leg.'},
                                                                                              {'name': 'Power Back '
                                                                                                       'Kick',
                                                                                               'prescription': 'Perform '
                                                                                                               '100 '
                                                                                                               'maximum-power '
                                                                                                               'kicks '
                                                                                                               'per '
                                                                                                               'leg.'},
                                                                                              {'name': 'Jump Front '
                                                                                                       'Kick',
                                                                                               'prescription': 'Perform '
                                                                                                               '50 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Jump '
                                                                                                       'Roundhouse '
                                                                                                       'Kick',
                                                                                               'prescription': 'Perform '
                                                                                                               '50 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Jump Side Kick',
                                                                                               'prescription': 'Perform '
                                                                                                               '50 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Tornado Kick '
                                                                                                       'Drill',
                                                                                               'prescription': 'Perform '
                                                                                                               '50 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Spinning Hook '
                                                                                                       'Kick',
                                                                                               'prescription': 'Perform '
                                                                                                               '50 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Double Jump '
                                                                                                       'Kick',
                                                                                               'prescription': 'Perform '
                                                                                                               '30 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'High Kick '
                                                                                                       'Challenge',
                                                                                               'prescription': 'Perform '
                                                                                                               '100 '
                                                                                                               'head-height '
                                                                                                               'kicks '
                                                                                                               'per '
                                                                                                               'leg.'},
                                                                                              {'name': 'Power Kick '
                                                                                                       'Circuit',
                                                                                               'prescription': '20 '
                                                                                                               'front '
                                                                                                               'kicks '
                                                                                                               '20 '
                                                                                                               'roundhouse '
                                                                                                               'kicks '
                                                                                                               '20 '
                                                                                                               'side '
                                                                                                               'kicks '
                                                                                                               'Repeat '
                                                                                                               '5 '
                                                                                                               'rounds.'}]}}},
 'taekwondo_olympic_sparring': {'alone': {'martial_arts_taekwondo_olympic_sparring': {'key': 'martial_arts_taekwondo_olympic_sparring',
                                                                                      'sport': 'Martial Arts',
                                                                                      'martial_art': 'Taekwondo',
                                                                                      'title': 'Taekwondo – Olympic '
                                                                                               'Sparring',
                                                                                      'category': 'taekwondo_olympic_sparring',
                                                                                      'training_mode': 'alone',
                                                                                      'level': 'all_levels',
                                                                                      'focus': 'olympic sparring',
                                                                                      'exercises': [{'name': 'Shadow '
                                                                                                             'Sparring',
                                                                                                     'prescription': '3-minute '
                                                                                                                     'round. '
                                                                                                                     'Complete '
                                                                                                                     '10 '
                                                                                                                     'rounds.'},
                                                                                                    {'name': 'Entry '
                                                                                                             'Drill',
                                                                                                     'prescription': 'Simulate '
                                                                                                                     'entering '
                                                                                                                     'scoring '
                                                                                                                     'range. '
                                                                                                                     'Repeat '
                                                                                                                     '200 '
                                                                                                                     'times.'},
                                                                                                    {'name': 'Exit '
                                                                                                             'Drill',
                                                                                                     'prescription': 'Enter '
                                                                                                                     'and '
                                                                                                                     'leave '
                                                                                                                     'range. '
                                                                                                                     'Repeat '
                                                                                                                     '200 '
                                                                                                                     'times.'},
                                                                                                    {'name': 'Counter '
                                                                                                             'Kick '
                                                                                                             'Drill',
                                                                                                     'prescription': 'Simulate '
                                                                                                                     'opponent '
                                                                                                                     'attack. '
                                                                                                                     'Counter '
                                                                                                                     'with '
                                                                                                                     'roundhouse '
                                                                                                                     'kick. '
                                                                                                                     'Repeat '
                                                                                                                     '100 '
                                                                                                                     'times.'},
                                                                                                    {'name': 'Cut Kick '
                                                                                                             'Practice',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '200 '
                                                                                                                     'cut '
                                                                                                                     'kicks.'},
                                                                                                    {'name': 'Lead Leg '
                                                                                                             'Roundhouse '
                                                                                                             'Drill',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '200 '
                                                                                                                     'repetitions.'},
                                                                                                    {'name': 'Spin '
                                                                                                             'Counter '
                                                                                                             'Practice',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '100 '
                                                                                                                     'spinning '
                                                                                                                     'counters.'},
                                                                                                    {'name': 'Angle '
                                                                                                             'Change '
                                                                                                             'Drill',
                                                                                                     'prescription': 'Move '
                                                                                                                     'left, '
                                                                                                                     'attack. '
                                                                                                                     'Move '
                                                                                                                     'right, '
                                                                                                                     'attack. '
                                                                                                                     'Repeat '
                                                                                                                     '100 '
                                                                                                                     'times.'},
                                                                                                    {'name': 'Kick-Only '
                                                                                                             'Shadow '
                                                                                                             'Match',
                                                                                                     'prescription': '2-minute '
                                                                                                                     'rounds. '
                                                                                                                     'Complete '
                                                                                                                     '5 '
                                                                                                                     'rounds.'},
                                                                                                    {'name': 'Scoring '
                                                                                                             'Combination '
                                                                                                             'Drill',
                                                                                                     'prescription': 'Roundhouse '
                                                                                                                     '→ '
                                                                                                                     'back '
                                                                                                                     'kick. '
                                                                                                                     'Repeat '
                                                                                                                     '100 '
                                                                                                                     'times.'},
                                                                                                    {'name': 'Tournament '
                                                                                                             'Round '
                                                                                                             'Simulation',
                                                                                                     'prescription': '3 '
                                                                                                                     'rounds '
                                                                                                                     'of '
                                                                                                                     '2 '
                                                                                                                     'minutes. '
                                                                                                                     'Complete '
                                                                                                                     '5 '
                                                                                                                     'matches.'},
                                                                                                    {'name': 'Olympic '
                                                                                                             'Match '
                                                                                                             'Simulation',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '3 '
                                                                                                                     'complete '
                                                                                                                     'competition '
                                                                                                                     'simulations.'}]}}},
 'taekwondo_conditioning': {'alone': {'martial_arts_taekwondo_conditioning': {'key': 'martial_arts_taekwondo_conditioning',
                                                                              'sport': 'Martial Arts',
                                                                              'martial_art': 'Taekwondo',
                                                                              'title': 'Taekwondo – Conditioning',
                                                                              'category': 'taekwondo_conditioning',
                                                                              'training_mode': 'alone',
                                                                              'level': 'all_levels',
                                                                              'focus': 'conditioning',
                                                                              'exercises': [{'name': 'Push-Ups',
                                                                                             'prescription': 'Perform '
                                                                                                             '50 '
                                                                                                             'repetitions. '
                                                                                                             'Complete '
                                                                                                             '5 sets.'},
                                                                                            {'name': 'Jump Squats',
                                                                                             'prescription': 'Perform '
                                                                                                             '50 '
                                                                                                             'repetitions. '
                                                                                                             'Complete '
                                                                                                             '5 sets.'},
                                                                                            {'name': 'Bodyweight '
                                                                                                     'Squats',
                                                                                             'prescription': 'Perform '
                                                                                                             '100 '
                                                                                                             'repetitions. '
                                                                                                             'Complete '
                                                                                                             '5 sets.'},
                                                                                            {'name': 'Walking Lunges',
                                                                                             'prescription': 'Perform '
                                                                                                             '50 '
                                                                                                             'lunges '
                                                                                                             'per leg. '
                                                                                                             'Complete '
                                                                                                             '3 sets.'},
                                                                                            {'name': 'Sit-Ups',
                                                                                             'prescription': 'Perform '
                                                                                                             '100 '
                                                                                                             'repetitions. '
                                                                                                             'Complete '
                                                                                                             '5 sets.'},
                                                                                            {'name': 'Leg Raises',
                                                                                             'prescription': 'Perform '
                                                                                                             '50 '
                                                                                                             'repetitions. '
                                                                                                             'Complete '
                                                                                                             '5 sets.'},
                                                                                            {'name': 'Plank Hold',
                                                                                             'prescription': 'Hold for '
                                                                                                             '2 '
                                                                                                             'minutes. '
                                                                                                             'Complete '
                                                                                                             '5 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Wall Sit',
                                                                                             'prescription': 'Hold for '
                                                                                                             '2 '
                                                                                                             'minutes. '
                                                                                                             'Complete '
                                                                                                             '5 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Jump Rope',
                                                                                             'prescription': 'Skip '
                                                                                                             'continuously '
                                                                                                             'for 5 '
                                                                                                             'minutes. '
                                                                                                             'Complete '
                                                                                                             '5 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Sprint Intervals',
                                                                                             'prescription': 'Sprint '
                                                                                                             '100 '
                                                                                                             'meters. '
                                                                                                             'Repeat '
                                                                                                             '10 '
                                                                                                             'times.'},
                                                                                            {'name': 'Burpee Challenge',
                                                                                             'prescription': 'Perform '
                                                                                                             '100 '
                                                                                                             'burpees.'},
                                                                                            {'name': 'Taekwondo '
                                                                                                     'Warrior Circuit',
                                                                                             'prescription': '50 '
                                                                                                             'push-ups '
                                                                                                             '100 '
                                                                                                             'squats '
                                                                                                             '50 jump '
                                                                                                             'squats '
                                                                                                             '100 '
                                                                                                             'kicks '
                                                                                                             'per leg '
                                                                                                             'Repeat 3 '
                                                                                                             'rounds.'}]}}},
 'muay_thai_learn_how_to_play': {'alone': {'martial_arts_muay_thai_learn_how_to_play': {'key': 'martial_arts_muay_thai_learn_how_to_play',
                                                                                        'sport': 'Martial Arts',
                                                                                        'martial_art': 'Muay Thai',
                                                                                        'title': 'Muay Thai – Learn '
                                                                                                 'How To Play',
                                                                                        'category': 'muay_thai_learn_how_to_play',
                                                                                        'training_mode': 'alone',
                                                                                        'level': 'learn_how_to_play',
                                                                                        'focus': 'learn how to play',
                                                                                        'exercises': [{'name': 'Fighting '
                                                                                                               'Stance '
                                                                                                               'Practice',
                                                                                                       'prescription': 'Assume '
                                                                                                                       'Muay '
                                                                                                                       'Thai '
                                                                                                                       'stance. '
                                                                                                                       'Hold '
                                                                                                                       'for '
                                                                                                                       '30 '
                                                                                                                       'seconds. '
                                                                                                                       'Repeat '
                                                                                                                       '10 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Forward '
                                                                                                               'and '
                                                                                                               'Backward '
                                                                                                               'Footwork',
                                                                                                       'prescription': 'Move '
                                                                                                                       'forward '
                                                                                                                       '10 '
                                                                                                                       'steps. '
                                                                                                                       'Move '
                                                                                                                       'backward '
                                                                                                                       '10 '
                                                                                                                       'steps. '
                                                                                                                       'Repeat '
                                                                                                                       '10 '
                                                                                                                       'rounds.'},
                                                                                                      {'name': 'Basic '
                                                                                                               'Jab '
                                                                                                               'Practice',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '100 '
                                                                                                                       'jabs.'},
                                                                                                      {'name': 'Basic '
                                                                                                               'Cross '
                                                                                                               'Practice',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '100 '
                                                                                                                       'crosses.'},
                                                                                                      {'name': 'Front '
                                                                                                               'Teep '
                                                                                                               'Introduction',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '50 '
                                                                                                                       'teeps '
                                                                                                                       'per '
                                                                                                                       'leg.'},
                                                                                                      {'name': 'Roundhouse '
                                                                                                               'Kick '
                                                                                                               'Introduction',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '50 '
                                                                                                                       'roundhouse '
                                                                                                                       'kicks '
                                                                                                                       'per '
                                                                                                                       'leg.'},
                                                                                                      {'name': 'Basic '
                                                                                                               'Knee '
                                                                                                               'Strike',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '50 '
                                                                                                                       'knees '
                                                                                                                       'per '
                                                                                                                       'leg.'},
                                                                                                      {'name': 'Basic '
                                                                                                               'Elbow '
                                                                                                               'Strike',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '50 '
                                                                                                                       'horizontal '
                                                                                                                       'elbows '
                                                                                                                       'per '
                                                                                                                       'arm.'},
                                                                                                      {'name': 'Jab-Cross '
                                                                                                               'Combination',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '100 '
                                                                                                                       'combinations.'},
                                                                                                      {'name': 'Teep '
                                                                                                               'and '
                                                                                                               'Recover '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Throw '
                                                                                                                       'a '
                                                                                                                       'teep '
                                                                                                                       'and '
                                                                                                                       'immediately '
                                                                                                                       'return '
                                                                                                                       'to '
                                                                                                                       'stance. '
                                                                                                                       'Repeat '
                                                                                                                       '100 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Shadow '
                                                                                                               'Muay '
                                                                                                               'Thai '
                                                                                                               'Round',
                                                                                                       'prescription': 'Practice '
                                                                                                                       'punches, '
                                                                                                                       'kicks, '
                                                                                                                       'knees, '
                                                                                                                       'elbows, '
                                                                                                                       'and '
                                                                                                                       'movement '
                                                                                                                       'for '
                                                                                                                       '2 '
                                                                                                                       'minutes. '
                                                                                                                       'Complete '
                                                                                                                       '5 '
                                                                                                                       'rounds.'},
                                                                                                      {'name': 'Beginner '
                                                                                                               'Muay '
                                                                                                               'Thai '
                                                                                                               'Circuit',
                                                                                                       'prescription': '20 '
                                                                                                                       'punches '
                                                                                                                       '20 '
                                                                                                                       'kicks '
                                                                                                                       '20 '
                                                                                                                       'knees '
                                                                                                                       'Repeat '
                                                                                                                       '5 '
                                                                                                                       'rounds.'}]}}},
 'muay_thai_beginner': {'alone': {'martial_arts_muay_thai_beginner': {'key': 'martial_arts_muay_thai_beginner',
                                                                      'sport': 'Martial Arts',
                                                                      'martial_art': 'Muay Thai',
                                                                      'title': 'Muay Thai – Beginner',
                                                                      'category': 'muay_thai_beginner',
                                                                      'training_mode': 'alone',
                                                                      'level': 'beginner',
                                                                      'focus': 'beginner',
                                                                      'exercises': [{'name': 'Fighting Stance Hold',
                                                                                     'prescription': 'Hold stance for '
                                                                                                     '1 minute. Repeat '
                                                                                                     '5 rounds.'},
                                                                                    {'name': 'Jab Volume Drill',
                                                                                     'prescription': 'Perform 300 '
                                                                                                     'jabs.'},
                                                                                    {'name': 'Cross Volume Drill',
                                                                                     'prescription': 'Perform 300 '
                                                                                                     'crosses.'},
                                                                                    {'name': 'Roundhouse Kick Volume',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'kicks per leg.'},
                                                                                    {'name': 'Teep Volume Drill',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'teeps per leg.'},
                                                                                    {'name': 'Knee Volume Drill',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'knees per leg.'},
                                                                                    {'name': 'Elbow Volume Drill',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'elbows per arm.'},
                                                                                    {'name': 'Jab-Cross-Roundhouse '
                                                                                             'Combination',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'repetitions.'},
                                                                                    {'name': 'Shadow Sparring',
                                                                                     'prescription': '3-minute rounds. '
                                                                                                     'Complete 5 '
                                                                                                     'rounds.'},
                                                                                    {'name': 'Speed Punch Drill',
                                                                                     'prescription': 'Punch '
                                                                                                     'continuously for '
                                                                                                     '30 seconds. '
                                                                                                     'Complete 5 '
                                                                                                     'rounds.'},
                                                                                    {'name': 'Speed Kick Drill',
                                                                                     'prescription': 'Kick '
                                                                                                     'continuously for '
                                                                                                     '30 seconds. '
                                                                                                     'Complete 5 '
                                                                                                     'rounds.'},
                                                                                    {'name': 'Beginner Conditioning '
                                                                                             'Circuit',
                                                                                     'prescription': '20 push-ups 30 '
                                                                                                     'squats 20 '
                                                                                                     'burpees Repeat 5 '
                                                                                                     'rounds.'}]}}},
 'muay_thai_boxing': {'alone': {'martial_arts_muay_thai_boxing': {'key': 'martial_arts_muay_thai_boxing',
                                                                  'sport': 'Martial Arts',
                                                                  'martial_art': 'Muay Thai',
                                                                  'title': 'Muay Thai – Boxing',
                                                                  'category': 'muay_thai_boxing',
                                                                  'training_mode': 'alone',
                                                                  'level': 'all_levels',
                                                                  'focus': 'boxing',
                                                                  'exercises': [{'name': 'Jab Volume Challenge',
                                                                                 'prescription': 'Perform 500 jabs.'},
                                                                                {'name': 'Cross Volume Challenge',
                                                                                 'prescription': 'Perform 500 '
                                                                                                 'crosses.'},
                                                                                {'name': 'Hook Volume Drill',
                                                                                 'prescription': 'Perform 300 hooks '
                                                                                                 'per arm.'},
                                                                                {'name': 'Uppercut Volume Drill',
                                                                                 'prescription': 'Perform 300 '
                                                                                                 'uppercuts per arm.'},
                                                                                {'name': 'Jab-Cross Combination',
                                                                                 'prescription': 'Perform 300 '
                                                                                                 'repetitions.'},
                                                                                {'name': 'Jab-Cross-Hook Combination',
                                                                                 'prescription': 'Perform 200 '
                                                                                                 'repetitions.'},
                                                                                {'name': 'Four-Punch Combination',
                                                                                 'prescription': 'Jab → Cross → Hook → '
                                                                                                 'Cross. Repeat 150 '
                                                                                                 'times.'},
                                                                                {'name': 'Forward Pressure Boxing',
                                                                                 'prescription': 'Move forward while '
                                                                                                 'punching for 3 '
                                                                                                 'minutes. Complete 5 '
                                                                                                 'rounds.'},
                                                                                {'name': 'Defensive Shadow Boxing',
                                                                                 'prescription': 'Practice slips and '
                                                                                                 'counters for 3 '
                                                                                                 'minutes. Complete 5 '
                                                                                                 'rounds.'},
                                                                                {'name': 'Speed Punch Round',
                                                                                 'prescription': 'Throw punches '
                                                                                                 'continuously for 1 '
                                                                                                 'minute. Complete 5 '
                                                                                                 'rounds.'},
                                                                                {'name': 'Heavy Bag Punch Round',
                                                                                 'prescription': 'Throw maximum-power '
                                                                                                 'punches for 3 '
                                                                                                 'minutes. Complete 5 '
                                                                                                 'rounds.'},
                                                                                {'name': '1,000 Punch Challenge',
                                                                                 'prescription': 'Complete 1,000 '
                                                                                                 'punches without '
                                                                                                 'stopping.'}]}}},
 'muay_thai_kicks': {'alone': {'martial_arts_muay_thai_kicks': {'key': 'martial_arts_muay_thai_kicks',
                                                                'sport': 'Martial Arts',
                                                                'martial_art': 'Muay Thai',
                                                                'title': 'Muay Thai – Kicks',
                                                                'category': 'muay_thai_kicks',
                                                                'training_mode': 'alone',
                                                                'level': 'all_levels',
                                                                'focus': 'kicks',
                                                                'exercises': [{'name': 'Roundhouse Kick Volume',
                                                                               'prescription': 'Perform 200 kicks per '
                                                                                               'leg.'},
                                                                              {'name': 'Low Kick Volume',
                                                                               'prescription': 'Perform 200 low kicks '
                                                                                               'per leg.'},
                                                                              {'name': 'Body Kick Volume',
                                                                               'prescription': 'Perform 100 body kicks '
                                                                                               'per leg.'},
                                                                              {'name': 'High Kick Volume',
                                                                               'prescription': 'Perform 100 '
                                                                                               'head-height kicks per '
                                                                                               'leg.'},
                                                                              {'name': 'Switch Kick Drill',
                                                                               'prescription': 'Perform 100 switch '
                                                                                               'kicks per leg.'},
                                                                              {'name': 'Teep Volume Challenge',
                                                                               'prescription': 'Perform 200 teeps per '
                                                                                               'leg.'},
                                                                              {'name': 'Lead Leg Roundhouse',
                                                                               'prescription': 'Perform 150 kicks.'},
                                                                              {'name': 'Rear Leg Roundhouse',
                                                                               'prescription': 'Perform 150 kicks.'},
                                                                              {'name': 'Kick Speed Round',
                                                                               'prescription': 'Maximum kicks in 30 '
                                                                                               'seconds. Complete 10 '
                                                                                               'rounds.'},
                                                                              {'name': 'Double Kick Combination',
                                                                               'prescription': 'Perform 100 '
                                                                                               'double-kick '
                                                                                               'combinations.'},
                                                                              {'name': 'Shadow Kicking Round',
                                                                               'prescription': 'Kick continuously for '
                                                                                               '2 minutes. Complete 5 '
                                                                                               'rounds.'},
                                                                              {'name': '500 Kick Challenge',
                                                                               'prescription': 'Perform 500 total '
                                                                                               'kicks.'}]}}},
 'muay_thai_knees': {'alone': {'martial_arts_muay_thai_knees': {'key': 'martial_arts_muay_thai_knees',
                                                                'sport': 'Martial Arts',
                                                                'martial_art': 'Muay Thai',
                                                                'title': 'Muay Thai – Knees',
                                                                'category': 'muay_thai_knees',
                                                                'training_mode': 'alone',
                                                                'level': 'all_levels',
                                                                'focus': 'knees',
                                                                'exercises': [{'name': 'Straight Knee Volume',
                                                                               'prescription': 'Perform 300 straight '
                                                                                               'knees.'},
                                                                              {'name': 'Alternating Knee Drill',
                                                                               'prescription': 'Perform 200 '
                                                                                               'alternating knees.'},
                                                                              {'name': 'Jump Knee Drill',
                                                                               'prescription': 'Perform 100 jumping '
                                                                                               'knees.'},
                                                                              {'name': 'Running Knee Drill',
                                                                               'prescription': 'Sprint 5 meters. '
                                                                                               'Perform 1 knee strike. '
                                                                                               'Repeat 100 times.'},
                                                                              {'name': 'Double Knee Drill',
                                                                               'prescription': 'Perform 100 '
                                                                                               'double-knee '
                                                                                               'combinations.'},
                                                                              {'name': 'Triple Knee Drill',
                                                                               'prescription': 'Perform 50 triple-knee '
                                                                                               'combinations.'},
                                                                              {'name': 'Knee Endurance Round',
                                                                               'prescription': 'Throw knees '
                                                                                               'continuously for 1 '
                                                                                               'minute. Complete 5 '
                                                                                               'rounds.'},
                                                                              {'name': 'Explosive Knee Drill',
                                                                               'prescription': 'Perform 50 '
                                                                                               'maximum-power knees '
                                                                                               'per leg.'},
                                                                              {'name': 'Long Range Knee Entry',
                                                                               'prescription': 'Step in and throw a '
                                                                                               'knee. Repeat 100 '
                                                                                               'times.'},
                                                                              {'name': 'Clinch Knee Simulation',
                                                                               'prescription': "Pull opponent's head "
                                                                                               'position with '
                                                                                               'resistance band. '
                                                                                               'Perform 200 knees.'},
                                                                              {'name': 'Shadow Knee Round',
                                                                               'prescription': 'Throw knees '
                                                                                               'continuously for 2 '
                                                                                               'minutes. Complete 5 '
                                                                                               'rounds.'},
                                                                              {'name': '500 Knee Challenge',
                                                                               'prescription': 'Perform 500 total '
                                                                                               'knees.'}]}}},
 'muay_thai_elbows': {'alone': {'martial_arts_muay_thai_elbows': {'key': 'martial_arts_muay_thai_elbows',
                                                                  'sport': 'Martial Arts',
                                                                  'martial_art': 'Muay Thai',
                                                                  'title': 'Muay Thai – Elbows',
                                                                  'category': 'muay_thai_elbows',
                                                                  'training_mode': 'alone',
                                                                  'level': 'all_levels',
                                                                  'focus': 'elbows',
                                                                  'exercises': [{'name': 'Horizontal Elbow Volume',
                                                                                 'prescription': 'Perform 200 elbows '
                                                                                                 'per arm.'},
                                                                                {'name': 'Upward Elbow Drill',
                                                                                 'prescription': 'Perform 100 elbows '
                                                                                                 'per arm.'},
                                                                                {'name': 'Downward Elbow Drill',
                                                                                 'prescription': 'Perform 100 elbows '
                                                                                                 'per arm.'},
                                                                                {'name': 'Diagonal Elbow Drill',
                                                                                 'prescription': 'Perform 100 elbows '
                                                                                                 'per arm.'},
                                                                                {'name': 'Spinning Elbow Drill',
                                                                                 'prescription': 'Perform 50 '
                                                                                                 'repetitions per '
                                                                                                 'side.'},
                                                                                {'name': 'Double Elbow Combination',
                                                                                 'prescription': 'Perform 100 '
                                                                                                 'combinations.'},
                                                                                {'name': 'Triple Elbow Combination',
                                                                                 'prescription': 'Perform 50 '
                                                                                                 'combinations.'},
                                                                                {'name': 'Elbow Entry Drill',
                                                                                 'prescription': 'Step forward and '
                                                                                                 'throw elbow. Repeat '
                                                                                                 '100 times.'},
                                                                                {'name': 'Elbow Speed Round',
                                                                                 'prescription': 'Throw elbows '
                                                                                                 'continuously for 1 '
                                                                                                 'minute. Complete 5 '
                                                                                                 'rounds.'},
                                                                                {'name': 'Heavy Bag Elbow Round',
                                                                                 'prescription': '3-minute rounds. '
                                                                                                 'Complete 5 rounds.'},
                                                                                {'name': 'Shadow Elbow Round',
                                                                                 'prescription': 'Throw elbows '
                                                                                                 'continuously for 2 '
                                                                                                 'minutes. Complete 5 '
                                                                                                 'rounds.'},
                                                                                {'name': '500 Elbow Challenge',
                                                                                 'prescription': 'Perform 500 total '
                                                                                                 'elbows.'}]}}},
 'muay_thai_clinch': {'alone': {'martial_arts_muay_thai_clinch': {'key': 'martial_arts_muay_thai_clinch',
                                                                  'sport': 'Martial Arts',
                                                                  'martial_art': 'Muay Thai',
                                                                  'title': 'Muay Thai – Clinch',
                                                                  'category': 'muay_thai_clinch',
                                                                  'training_mode': 'alone',
                                                                  'level': 'all_levels',
                                                                  'focus': 'clinch',
                                                                  'exercises': [{'name': 'Neck Pull Drill',
                                                                                 'prescription': 'Pull resistance band '
                                                                                                 'toward chest. '
                                                                                                 'Perform 200 '
                                                                                                 'repetitions.'},
                                                                                {'name': 'Clinch Posture Hold',
                                                                                 'prescription': 'Hold clinch posture '
                                                                                                 'for 1 minute. Repeat '
                                                                                                 '10 rounds.'},
                                                                                {'name': 'Clinch Knee Combination',
                                                                                 'prescription': 'Pull and throw knee. '
                                                                                                 'Repeat 200 times.'},
                                                                                {'name': 'Alternating Clinch Knees',
                                                                                 'prescription': 'Perform 300 '
                                                                                                 'alternating knees.'},
                                                                                {'name': 'Clinch Walk Drill',
                                                                                 'prescription': 'Walk 20 meters while '
                                                                                                 'maintaining clinch '
                                                                                                 'posture. Repeat 10 '
                                                                                                 'rounds.'},
                                                                                {'name': 'Grip Endurance Hold',
                                                                                 'prescription': 'Hold towel grip for '
                                                                                                 '1 minute. Repeat 10 '
                                                                                                 'times.'},
                                                                                {'name': 'Clinch Pull-Ups',
                                                                                 'prescription': 'Perform 50 '
                                                                                                 'repetitions using '
                                                                                                 'towel grip.'},
                                                                                {'name': 'Resistance Band Clinch Pulls',
                                                                                 'prescription': 'Perform 200 '
                                                                                                 'repetitions.'},
                                                                                {'name': 'Balance Recovery Drill',
                                                                                 'prescription': 'Lift one knee and '
                                                                                                 'maintain balance for '
                                                                                                 '10 seconds. Repeat '
                                                                                                 '30 times per side.'},
                                                                                {'name': 'Clinch Shadow Round',
                                                                                 'prescription': 'Simulate clinch '
                                                                                                 'fighting for 2 '
                                                                                                 'minutes. Complete 5 '
                                                                                                 'rounds.'},
                                                                                {'name': 'Clinch Endurance Round',
                                                                                 'prescription': 'Continuous clinch '
                                                                                                 'movement for 3 '
                                                                                                 'minutes. Complete 5 '
                                                                                                 'rounds.'},
                                                                                {'name': 'Clinch Warrior Circuit',
                                                                                 'prescription': '50 pulls 50 knees 50 '
                                                                                                 'squats Repeat 5 '
                                                                                                 'rounds.'}]}}},
 'muay_thai_fight_conditioning': {'alone': {'martial_arts_muay_thai_fight_conditioning': {'key': 'martial_arts_muay_thai_fight_conditioning',
                                                                                          'sport': 'Martial Arts',
                                                                                          'martial_art': 'Muay Thai',
                                                                                          'title': 'Muay Thai – Fight '
                                                                                                   'Conditioning',
                                                                                          'category': 'muay_thai_fight_conditioning',
                                                                                          'training_mode': 'alone',
                                                                                          'level': 'all_levels',
                                                                                          'focus': 'fight conditioning',
                                                                                          'exercises': [{'name': 'Push-Ups',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '50 '
                                                                                                                         'repetitions. '
                                                                                                                         'Complete '
                                                                                                                         '5 '
                                                                                                                         'sets.'},
                                                                                                        {'name': 'Burpees',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '100 '
                                                                                                                         'repetitions.'},
                                                                                                        {'name': 'Bodyweight '
                                                                                                                 'Squats',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '100 '
                                                                                                                         'repetitions. '
                                                                                                                         'Complete '
                                                                                                                         '5 '
                                                                                                                         'sets.'},
                                                                                                        {'name': 'Jump '
                                                                                                                 'Squats',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '50 '
                                                                                                                         'repetitions. '
                                                                                                                         'Complete '
                                                                                                                         '5 '
                                                                                                                         'sets.'},
                                                                                                        {'name': 'Walking '
                                                                                                                 'Lunges',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '50 '
                                                                                                                         'lunges '
                                                                                                                         'per '
                                                                                                                         'leg. '
                                                                                                                         'Complete '
                                                                                                                         '3 '
                                                                                                                         'sets.'},
                                                                                                        {'name': 'Sit-Ups',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '100 '
                                                                                                                         'repetitions. '
                                                                                                                         'Complete '
                                                                                                                         '5 '
                                                                                                                         'sets.'},
                                                                                                        {'name': 'Leg '
                                                                                                                 'Raises',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '50 '
                                                                                                                         'repetitions. '
                                                                                                                         'Complete '
                                                                                                                         '5 '
                                                                                                                         'sets.'},
                                                                                                        {'name': 'Plank '
                                                                                                                 'Hold',
                                                                                                         'prescription': 'Hold '
                                                                                                                         'for '
                                                                                                                         '2 '
                                                                                                                         'minutes. '
                                                                                                                         'Complete '
                                                                                                                         '5 '
                                                                                                                         'rounds.'},
                                                                                                        {'name': 'Sprint '
                                                                                                                 'Intervals',
                                                                                                         'prescription': 'Sprint '
                                                                                                                         '100 '
                                                                                                                         'meters. '
                                                                                                                         'Repeat '
                                                                                                                         '10 '
                                                                                                                         'times.'},
                                                                                                        {'name': 'Jump '
                                                                                                                 'Rope '
                                                                                                                 'Endurance',
                                                                                                         'prescription': 'Skip '
                                                                                                                         'continuously '
                                                                                                                         'for '
                                                                                                                         '5 '
                                                                                                                         'minutes. '
                                                                                                                         'Complete '
                                                                                                                         '5 '
                                                                                                                         'rounds.'},
                                                                                                        {'name': 'Fight '
                                                                                                                 'Simulation '
                                                                                                                 'Circuit',
                                                                                                         'prescription': '3 '
                                                                                                                         'minutes '
                                                                                                                         'punching '
                                                                                                                         '3 '
                                                                                                                         'minutes '
                                                                                                                         'kicking '
                                                                                                                         '3 '
                                                                                                                         'minutes '
                                                                                                                         'knees '
                                                                                                                         'Repeat '
                                                                                                                         '3 '
                                                                                                                         'rounds.'},
                                                                                                        {'name': 'Muay '
                                                                                                                 'Thai '
                                                                                                                 'Warrior '
                                                                                                                 'Challenge',
                                                                                                         'prescription': '100 '
                                                                                                                         'punches '
                                                                                                                         '100 '
                                                                                                                         'kicks '
                                                                                                                         '100 '
                                                                                                                         'knees '
                                                                                                                         '50 '
                                                                                                                         'burpees '
                                                                                                                         'Repeat '
                                                                                                                         '3 '
                                                                                                                         'rounds.'}]}}},
 'judo_learn_how_to_play': {'alone': {'martial_arts_judo_learn_how_to_play': {'key': 'martial_arts_judo_learn_how_to_play',
                                                                              'sport': 'Martial Arts',
                                                                              'martial_art': 'Judo',
                                                                              'title': 'Judo – Learn How To Play',
                                                                              'category': 'judo_learn_how_to_play',
                                                                              'training_mode': 'alone',
                                                                              'level': 'learn_how_to_play',
                                                                              'focus': 'learn how to play',
                                                                              'exercises': [{'name': 'Judo Stance '
                                                                                                     'Practice',
                                                                                             'prescription': 'Assume '
                                                                                                             'basic '
                                                                                                             'judo '
                                                                                                             'stance. '
                                                                                                             'Hold for '
                                                                                                             '30 '
                                                                                                             'seconds. '
                                                                                                             'Repeat '
                                                                                                             '10 '
                                                                                                             'times.'},
                                                                                            {'name': 'Forward Movement '
                                                                                                     'Drill',
                                                                                             'prescription': 'Move '
                                                                                                             'forward '
                                                                                                             '10 '
                                                                                                             'meters '
                                                                                                             'using '
                                                                                                             'judo '
                                                                                                             'footwork. '
                                                                                                             'Repeat '
                                                                                                             '10 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Backward '
                                                                                                     'Movement Drill',
                                                                                             'prescription': 'Move '
                                                                                                             'backward '
                                                                                                             '10 '
                                                                                                             'meters '
                                                                                                             'using '
                                                                                                             'judo '
                                                                                                             'footwork. '
                                                                                                             'Repeat '
                                                                                                             '10 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Side Movement '
                                                                                                     'Drill',
                                                                                             'prescription': 'Shuffle '
                                                                                                             'left 10 '
                                                                                                             'meters. '
                                                                                                             'Shuffle '
                                                                                                             'right 10 '
                                                                                                             'meters. '
                                                                                                             'Repeat '
                                                                                                             '10 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Back Breakfall '
                                                                                                     'Introduction',
                                                                                             'prescription': 'Perform '
                                                                                                             '50 '
                                                                                                             'backward '
                                                                                                             'breakfalls.'},
                                                                                            {'name': 'Side Breakfall '
                                                                                                     'Introduction',
                                                                                             'prescription': 'Perform '
                                                                                                             '50 '
                                                                                                             'breakfalls '
                                                                                                             'per '
                                                                                                             'side.'},
                                                                                            {'name': 'Forward '
                                                                                                     'Breakfall '
                                                                                                     'Introduction',
                                                                                             'prescription': 'Perform '
                                                                                                             '50 '
                                                                                                             'forward '
                                                                                                             'breakfalls.'},
                                                                                            {'name': 'Technical '
                                                                                                     'Stand-Up',
                                                                                             'prescription': 'Stand up '
                                                                                                             'safely '
                                                                                                             'from the '
                                                                                                             'ground. '
                                                                                                             'Repeat '
                                                                                                             '100 '
                                                                                                             'times.'},
                                                                                            {'name': 'Hip Rotation '
                                                                                                     'Drill',
                                                                                             'prescription': 'Perform '
                                                                                                             '100 hip '
                                                                                                             'turns.'},
                                                                                            {'name': 'Entry Position '
                                                                                                     'Practice',
                                                                                             'prescription': 'Step '
                                                                                                             'into '
                                                                                                             'throwing '
                                                                                                             'position. '
                                                                                                             'Repeat '
                                                                                                             '100 '
                                                                                                             'times.'},
                                                                                            {'name': 'Shadow Throw '
                                                                                                     'Drill',
                                                                                             'prescription': 'Simulate '
                                                                                                             'a throw '
                                                                                                             'without '
                                                                                                             'a '
                                                                                                             'partner. '
                                                                                                             'Repeat '
                                                                                                             '100 '
                                                                                                             'times.'},
                                                                                            {'name': 'Beginner '
                                                                                                     'Coordination '
                                                                                                     'Circuit',
                                                                                             'prescription': '20 '
                                                                                                             'breakfalls '
                                                                                                             '20 hip '
                                                                                                             'turns 20 '
                                                                                                             'technical '
                                                                                                             'stand-ups '
                                                                                                             'Repeat 5 '
                                                                                                             'rounds.'}]}}},
 'judo_beginner': {'alone': {'martial_arts_judo_beginner': {'key': 'martial_arts_judo_beginner',
                                                            'sport': 'Martial Arts',
                                                            'martial_art': 'Judo',
                                                            'title': 'Judo – Beginner',
                                                            'category': 'judo_beginner',
                                                            'training_mode': 'alone',
                                                            'level': 'beginner',
                                                            'focus': 'beginner',
                                                            'exercises': [{'name': 'Footwork Circuit',
                                                                           'prescription': 'Move forward, backward, '
                                                                                           'left, and right. Continue '
                                                                                           'for 5 minutes.'},
                                                                          {'name': 'Backward Breakfall Volume',
                                                                           'prescription': 'Perform 100 repetitions.'},
                                                                          {'name': 'Side Breakfall Volume',
                                                                           'prescription': 'Perform 100 repetitions '
                                                                                           'per side.'},
                                                                          {'name': 'Forward Breakfall Volume',
                                                                           'prescription': 'Perform 100 repetitions.'},
                                                                          {'name': 'Hip Throw Entry',
                                                                           'prescription': 'Perform 100 entries.'},
                                                                          {'name': 'Shoulder Throw Entry',
                                                                           'prescription': 'Perform 100 entries.'},
                                                                          {'name': 'Foot Sweep Entry',
                                                                           'prescription': 'Perform 100 entries.'},
                                                                          {'name': 'Technical Stand-Up Drill',
                                                                           'prescription': 'Perform 200 repetitions.'},
                                                                          {'name': 'Grip Reach Practice',
                                                                           'prescription': 'Simulate obtaining sleeve '
                                                                                           'and lapel grips. Repeat '
                                                                                           '200 times.'},
                                                                          {'name': 'Shadow Judo Round',
                                                                           'prescription': 'Move and simulate throws '
                                                                                           'for 3 minutes. Complete 5 '
                                                                                           'rounds.'},
                                                                          {'name': 'Balance Challenge',
                                                                           'prescription': 'Stand on one leg for 1 '
                                                                                           'minute. Repeat 5 times per '
                                                                                           'side.'},
                                                                          {'name': 'Beginner Conditioning Circuit',
                                                                           'prescription': '20 push-ups 30 squats 20 '
                                                                                           'sit-ups Repeat 5 '
                                                                                           'rounds.'}]}}},
 'judo_ukemi_breakfalls': {'alone': {'martial_arts_judo_ukemi_breakfalls': {'key': 'martial_arts_judo_ukemi_breakfalls',
                                                                            'sport': 'Martial Arts',
                                                                            'martial_art': 'Judo',
                                                                            'title': 'Judo – Ukemi (Breakfalls)',
                                                                            'category': 'judo_ukemi_breakfalls',
                                                                            'training_mode': 'alone',
                                                                            'level': 'all_levels',
                                                                            'focus': 'ukemi (breakfalls)',
                                                                            'exercises': [{'name': 'Back Breakfalls',
                                                                                           'prescription': 'Perform '
                                                                                                           '200 '
                                                                                                           'repetitions.'},
                                                                                          {'name': 'Side Breakfalls '
                                                                                                   'Left',
                                                                                           'prescription': 'Perform '
                                                                                                           '100 '
                                                                                                           'repetitions.'},
                                                                                          {'name': 'Side Breakfalls '
                                                                                                   'Right',
                                                                                           'prescription': 'Perform '
                                                                                                           '100 '
                                                                                                           'repetitions.'},
                                                                                          {'name': 'Forward Breakfalls',
                                                                                           'prescription': 'Perform '
                                                                                                           '200 '
                                                                                                           'repetitions.'},
                                                                                          {'name': 'Rolling Breakfalls',
                                                                                           'prescription': 'Perform '
                                                                                                           '100 '
                                                                                                           'repetitions.'},
                                                                                          {'name': 'Standing '
                                                                                                   'Breakfalls',
                                                                                           'prescription': 'Start '
                                                                                                           'standing '
                                                                                                           'and '
                                                                                                           'perform '
                                                                                                           'breakfall. '
                                                                                                           'Repeat 100 '
                                                                                                           'times.'},
                                                                                          {'name': 'Jump Breakfalls',
                                                                                           'prescription': 'Jump and '
                                                                                                           'perform '
                                                                                                           'controlled '
                                                                                                           'breakfall. '
                                                                                                           'Repeat 50 '
                                                                                                           'times.'},
                                                                                          {'name': 'Forward Roll to '
                                                                                                   'Breakfall',
                                                                                           'prescription': 'Perform '
                                                                                                           '100 '
                                                                                                           'repetitions.'},
                                                                                          {'name': 'Backward Roll to '
                                                                                                   'Breakfall',
                                                                                           'prescription': 'Perform '
                                                                                                           '100 '
                                                                                                           'repetitions.'},
                                                                                          {'name': 'Continuous Ukemi '
                                                                                                   'Circuit',
                                                                                           'prescription': 'Perform '
                                                                                                           'breakfalls '
                                                                                                           'continuously '
                                                                                                           'for 2 '
                                                                                                           'minutes. '
                                                                                                           'Complete 5 '
                                                                                                           'rounds.'},
                                                                                          {'name': 'Reaction Ukemi '
                                                                                                   'Drill',
                                                                                           'prescription': 'Randomly '
                                                                                                           'alternate '
                                                                                                           'breakfall '
                                                                                                           'types. '
                                                                                                           'Perform '
                                                                                                           '200 '
                                                                                                           'repetitions.'},
                                                                                          {'name': 'Ukemi Endurance '
                                                                                                   'Challenge',
                                                                                           'prescription': 'Perform '
                                                                                                           '500 total '
                                                                                                           'breakfalls.'}]}}},
 'judo_throws_nage_waza': {'alone': {'martial_arts_judo_throws_nage_waza': {'key': 'martial_arts_judo_throws_nage_waza',
                                                                            'sport': 'Martial Arts',
                                                                            'martial_art': 'Judo',
                                                                            'title': 'Judo – Throws (Nage-Waza)',
                                                                            'category': 'judo_throws_nage_waza',
                                                                            'training_mode': 'alone',
                                                                            'level': 'all_levels',
                                                                            'focus': 'throws (nage-waza)',
                                                                            'exercises': [{'name': 'Hip Throw Entries '
                                                                                                   '(O Goshi)',
                                                                                           'prescription': 'Perform '
                                                                                                           '200 '
                                                                                                           'entries.'},
                                                                                          {'name': 'Shoulder Throw '
                                                                                                   'Entries (Seoi '
                                                                                                   'Nage)',
                                                                                           'prescription': 'Perform '
                                                                                                           '200 '
                                                                                                           'entries.'},
                                                                                          {'name': 'Foot Sweep Entries',
                                                                                           'prescription': 'Perform '
                                                                                                           '200 '
                                                                                                           'entries.'},
                                                                                          {'name': 'Inner Reap Entries '
                                                                                                   '(Ouchi Gari)',
                                                                                           'prescription': 'Perform '
                                                                                                           '200 '
                                                                                                           'entries.'},
                                                                                          {'name': 'Outer Reap Entries '
                                                                                                   '(Osoto Gari)',
                                                                                           'prescription': 'Perform '
                                                                                                           '200 '
                                                                                                           'entries.'},
                                                                                          {'name': 'Uchi Komi Circuit',
                                                                                           'prescription': 'Complete '
                                                                                                           '500 throw '
                                                                                                           'entries '
                                                                                                           'total.'},
                                                                                          {'name': 'Shadow Hip Throws',
                                                                                           'prescription': 'Simulate '
                                                                                                           '100 '
                                                                                                           'throws.'},
                                                                                          {'name': 'Shadow Shoulder '
                                                                                                   'Throws',
                                                                                           'prescription': 'Simulate '
                                                                                                           '100 '
                                                                                                           'throws.'},
                                                                                          {'name': 'Explosive Throw '
                                                                                                   'Entries',
                                                                                           'prescription': 'Perform 50 '
                                                                                                           'maximum-speed '
                                                                                                           'entries.'},
                                                                                          {'name': 'Throw Combination '
                                                                                                   'Drill',
                                                                                           'prescription': 'Transition '
                                                                                                           'between '
                                                                                                           'two '
                                                                                                           'throws. '
                                                                                                           'Repeat 100 '
                                                                                                           'times.'},
                                                                                          {'name': 'Footwork-to-Throw '
                                                                                                   'Drill',
                                                                                           'prescription': 'Move and '
                                                                                                           'enter '
                                                                                                           'throw '
                                                                                                           'position. '
                                                                                                           'Repeat 200 '
                                                                                                           'times.'},
                                                                                          {'name': 'Throw Endurance '
                                                                                                   'Challenge',
                                                                                           'prescription': 'Complete '
                                                                                                           '1,000 '
                                                                                                           'total '
                                                                                                           'entries.'}]}}},
 'judo_grip_fighting_kumi_kata': {'alone': {'martial_arts_judo_grip_fighting_kumi_kata': {'key': 'martial_arts_judo_grip_fighting_kumi_kata',
                                                                                          'sport': 'Martial Arts',
                                                                                          'martial_art': 'Judo',
                                                                                          'title': 'Judo – Grip '
                                                                                                   'Fighting '
                                                                                                   '(Kumi-Kata)',
                                                                                          'category': 'judo_grip_fighting_kumi_kata',
                                                                                          'training_mode': 'alone',
                                                                                          'level': 'all_levels',
                                                                                          'focus': 'grip fighting '
                                                                                                   '(kumi-kata)',
                                                                                          'exercises': [{'name': 'Towel '
                                                                                                                 'Grip '
                                                                                                                 'Hold',
                                                                                                         'prescription': 'Hold '
                                                                                                                         'towel '
                                                                                                                         'grip '
                                                                                                                         'for '
                                                                                                                         '1 '
                                                                                                                         'minute. '
                                                                                                                         'Repeat '
                                                                                                                         '10 '
                                                                                                                         'times.'},
                                                                                                        {'name': 'Gi '
                                                                                                                 'Sleeve '
                                                                                                                 'Hold',
                                                                                                         'prescription': 'Hold '
                                                                                                                         'sleeve '
                                                                                                                         'grip '
                                                                                                                         'for '
                                                                                                                         '1 '
                                                                                                                         'minute. '
                                                                                                                         'Repeat '
                                                                                                                         '10 '
                                                                                                                         'times.'},
                                                                                                        {'name': 'Gi '
                                                                                                                 'Lapel '
                                                                                                                 'Hold',
                                                                                                         'prescription': 'Hold '
                                                                                                                         'lapel '
                                                                                                                         'grip '
                                                                                                                         'for '
                                                                                                                         '1 '
                                                                                                                         'minute. '
                                                                                                                         'Repeat '
                                                                                                                         '10 '
                                                                                                                         'times.'},
                                                                                                        {'name': 'Towel '
                                                                                                                 'Pull-Ups',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '50 '
                                                                                                                         'repetitions.'},
                                                                                                        {'name': 'Gi '
                                                                                                                 'Pull-Ups',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '50 '
                                                                                                                         'repetitions.'},
                                                                                                        {'name': 'Farmer '
                                                                                                                 'Carry',
                                                                                                         'prescription': 'Carry '
                                                                                                                         'heavy '
                                                                                                                         'weights '
                                                                                                                         'for '
                                                                                                                         '50 '
                                                                                                                         'meters. '
                                                                                                                         'Repeat '
                                                                                                                         '10 '
                                                                                                                         'rounds.'},
                                                                                                        {'name': 'Dead '
                                                                                                                 'Hang',
                                                                                                         'prescription': 'Hang '
                                                                                                                         'from '
                                                                                                                         'pull-up '
                                                                                                                         'bar '
                                                                                                                         'for '
                                                                                                                         '1 '
                                                                                                                         'minute. '
                                                                                                                         'Repeat '
                                                                                                                         '10 '
                                                                                                                         'times.'},
                                                                                                        {'name': 'Grip '
                                                                                                                 'Squeeze '
                                                                                                                 'Drill',
                                                                                                         'prescription': 'Squeeze '
                                                                                                                         'grip '
                                                                                                                         'trainer '
                                                                                                                         '100 '
                                                                                                                         'times '
                                                                                                                         'per '
                                                                                                                         'hand.'},
                                                                                                        {'name': 'Wrist '
                                                                                                                 'Curl '
                                                                                                                 'Circuit',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '100 '
                                                                                                                         'repetitions '
                                                                                                                         'per '
                                                                                                                         'arm.'},
                                                                                                        {'name': 'Rope '
                                                                                                                 'Climb',
                                                                                                         'prescription': 'Complete '
                                                                                                                         '10 '
                                                                                                                         'climbs.'},
                                                                                                        {'name': 'Grip '
                                                                                                                 'Endurance '
                                                                                                                 'Circuit',
                                                                                                         'prescription': 'Hold '
                                                                                                                         'grip '
                                                                                                                         'continuously '
                                                                                                                         'for '
                                                                                                                         '5 '
                                                                                                                         'minutes.'},
                                                                                                        {'name': 'Judoka '
                                                                                                                 'Grip '
                                                                                                                 'Challenge',
                                                                                                         'prescription': '50 '
                                                                                                                         'pull-ups '
                                                                                                                         '5-minute '
                                                                                                                         'dead '
                                                                                                                         'hang '
                                                                                                                         '200 '
                                                                                                                         'grip '
                                                                                                                         'squeezes'}]}}},
 'judo_groundwork_ne_waza': {'alone': {'martial_arts_judo_groundwork_ne_waza': {'key': 'martial_arts_judo_groundwork_ne_waza',
                                                                                'sport': 'Martial Arts',
                                                                                'martial_art': 'Judo',
                                                                                'title': 'Judo – Groundwork (Ne-Waza)',
                                                                                'category': 'judo_groundwork_ne_waza',
                                                                                'training_mode': 'alone',
                                                                                'level': 'all_levels',
                                                                                'focus': 'groundwork (ne-waza)',
                                                                                'exercises': [{'name': 'Bridge Escapes',
                                                                                               'prescription': 'Perform '
                                                                                                               '200 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Shrimp Escapes',
                                                                                               'prescription': 'Perform '
                                                                                                               '200 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Technical '
                                                                                                       'Stand-Ups',
                                                                                               'prescription': 'Perform '
                                                                                                               '200 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Forward Rolls',
                                                                                               'prescription': 'Perform '
                                                                                                               '100 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Backward Rolls',
                                                                                               'prescription': 'Perform '
                                                                                                               '100 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Side Movement '
                                                                                                       'Drill',
                                                                                               'prescription': 'Move '
                                                                                                               'across '
                                                                                                               'mat '
                                                                                                               'using '
                                                                                                               'groundwork '
                                                                                                               'movement. '
                                                                                                               'Repeat '
                                                                                                               '20 '
                                                                                                               'lengths.'},
                                                                                              {'name': 'Hip Escape '
                                                                                                       'Circuit',
                                                                                               'prescription': 'Continue '
                                                                                                               'for 5 '
                                                                                                               'minutes.'},
                                                                                              {'name': 'Bridge and '
                                                                                                       'Turn Drill',
                                                                                               'prescription': 'Perform '
                                                                                                               '200 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Ground '
                                                                                                       'Transition '
                                                                                                       'Drill',
                                                                                               'prescription': 'Simulate '
                                                                                                               'moving '
                                                                                                               'between '
                                                                                                               'positions. '
                                                                                                               'Repeat '
                                                                                                               '100 '
                                                                                                               'times.'},
                                                                                              {'name': 'Turtle '
                                                                                                       'Position '
                                                                                                       'Escape',
                                                                                               'prescription': 'Perform '
                                                                                                               '100 '
                                                                                                               'repetitions.'},
                                                                                              {'name': 'Groundwork '
                                                                                                       'Shadow Round',
                                                                                               'prescription': 'Simulate '
                                                                                                               'grappling '
                                                                                                               'movement '
                                                                                                               'for 3 '
                                                                                                               'minutes. '
                                                                                                               'Complete '
                                                                                                               '5 '
                                                                                                               'rounds.'},
                                                                                              {'name': 'Ne-Waza '
                                                                                                       'Endurance '
                                                                                                       'Challenge',
                                                                                               'prescription': 'Complete '
                                                                                                               '1,000 '
                                                                                                               'total '
                                                                                                               'groundwork '
                                                                                                               'movements.'}]}}},
 'judo_randori_sparring_preparation': {'alone': {'martial_arts_judo_randori_sparring_preparation': {'key': 'martial_arts_judo_randori_sparring_preparation',
                                                                                                    'sport': 'Martial '
                                                                                                             'Arts',
                                                                                                    'martial_art': 'Judo',
                                                                                                    'title': 'Judo – '
                                                                                                             'Randori '
                                                                                                             '(Sparring '
                                                                                                             'Preparation)',
                                                                                                    'category': 'judo_randori_sparring_preparation',
                                                                                                    'training_mode': 'alone',
                                                                                                    'level': 'all_levels',
                                                                                                    'focus': 'randori '
                                                                                                             '(sparring '
                                                                                                             'preparation)',
                                                                                                    'exercises': [{'name': 'Shadow '
                                                                                                                           'Randori',
                                                                                                                   'prescription': 'Move '
                                                                                                                                   'and '
                                                                                                                                   'attack '
                                                                                                                                   'continuously '
                                                                                                                                   'for '
                                                                                                                                   '3 '
                                                                                                                                   'minutes. '
                                                                                                                                   'Complete '
                                                                                                                                   '10 '
                                                                                                                                   'rounds.'},
                                                                                                                  {'name': 'Entry '
                                                                                                                           'and '
                                                                                                                           'Retreat '
                                                                                                                           'Drill',
                                                                                                                   'prescription': 'Enter '
                                                                                                                                   'throwing '
                                                                                                                                   'range '
                                                                                                                                   'and '
                                                                                                                                   'exit. '
                                                                                                                                   'Repeat '
                                                                                                                                   '200 '
                                                                                                                                   'times.'},
                                                                                                                  {'name': 'Throw '
                                                                                                                           'Combination '
                                                                                                                           'Shadow '
                                                                                                                           'Drill',
                                                                                                                   'prescription': 'Perform '
                                                                                                                                   '100 '
                                                                                                                                   'combinations.'},
                                                                                                                  {'name': 'Counter '
                                                                                                                           'Throw '
                                                                                                                           'Simulation',
                                                                                                                   'prescription': 'Simulate '
                                                                                                                                   'counter '
                                                                                                                                   'attacks. '
                                                                                                                                   'Repeat '
                                                                                                                                   '100 '
                                                                                                                                   'times.'},
                                                                                                                  {'name': 'Direction '
                                                                                                                           'Change '
                                                                                                                           'Drill',
                                                                                                                   'prescription': 'Change '
                                                                                                                                   'direction '
                                                                                                                                   'and '
                                                                                                                                   'attack. '
                                                                                                                                   'Repeat '
                                                                                                                                   '200 '
                                                                                                                                   'times.'},
                                                                                                                  {'name': 'Foot '
                                                                                                                           'Sweep '
                                                                                                                           'Simulation',
                                                                                                                   'prescription': 'Perform '
                                                                                                                                   '200 '
                                                                                                                                   'foot '
                                                                                                                                   'sweep '
                                                                                                                                   'movements.'},
                                                                                                                  {'name': 'Attack '
                                                                                                                           'Chain '
                                                                                                                           'Drill',
                                                                                                                   'prescription': 'Simulate '
                                                                                                                                   'three '
                                                                                                                                   'consecutive '
                                                                                                                                   'attacks. '
                                                                                                                                   'Repeat '
                                                                                                                                   '100 '
                                                                                                                                   'times.'},
                                                                                                                  {'name': 'Continuous '
                                                                                                                           'Movement '
                                                                                                                           'Round',
                                                                                                                   'prescription': 'Move '
                                                                                                                                   'continuously '
                                                                                                                                   'for '
                                                                                                                                   '5 '
                                                                                                                                   'minutes. '
                                                                                                                                   'Complete '
                                                                                                                                   '5 '
                                                                                                                                   'rounds.'},
                                                                                                                  {'name': 'Balance '
                                                                                                                           'Recovery '
                                                                                                                           'Drill',
                                                                                                                   'prescription': 'Lose '
                                                                                                                                   'balance '
                                                                                                                                   'and '
                                                                                                                                   'recover. '
                                                                                                                                   'Repeat '
                                                                                                                                   '100 '
                                                                                                                                   'times.'},
                                                                                                                  {'name': 'Competition '
                                                                                                                           'Pace '
                                                                                                                           'Round',
                                                                                                                   'prescription': 'Simulate '
                                                                                                                                   'tournament '
                                                                                                                                   'pace '
                                                                                                                                   'for '
                                                                                                                                   '4 '
                                                                                                                                   'minutes. '
                                                                                                                                   'Complete '
                                                                                                                                   '5 '
                                                                                                                                   'rounds.'},
                                                                                                                  {'name': 'Golden '
                                                                                                                           'Score '
                                                                                                                           'Simulation',
                                                                                                                   'prescription': 'Continue '
                                                                                                                                   'attacking '
                                                                                                                                   'for '
                                                                                                                                   '6 '
                                                                                                                                   'minutes. '
                                                                                                                                   'Complete '
                                                                                                                                   '3 '
                                                                                                                                   'rounds.'},
                                                                                                                  {'name': 'Tournament '
                                                                                                                           'Simulation',
                                                                                                                   'prescription': 'Complete '
                                                                                                                                   '5 '
                                                                                                                                   'full '
                                                                                                                                   'match '
                                                                                                                                   'simulations.'}]}}},
 'judo_conditioning': {'alone': {'martial_arts_judo_conditioning': {'key': 'martial_arts_judo_conditioning',
                                                                    'sport': 'Martial Arts',
                                                                    'martial_art': 'Judo',
                                                                    'title': 'Judo – Conditioning',
                                                                    'category': 'judo_conditioning',
                                                                    'training_mode': 'alone',
                                                                    'level': 'all_levels',
                                                                    'focus': 'conditioning',
                                                                    'exercises': [{'name': 'Push-Ups',
                                                                                   'prescription': 'Perform 50 '
                                                                                                   'repetitions. '
                                                                                                   'Complete 5 sets.'},
                                                                                  {'name': 'Pull-Ups',
                                                                                   'prescription': 'Perform 20 '
                                                                                                   'repetitions. '
                                                                                                   'Complete 5 sets.'},
                                                                                  {'name': 'Squats',
                                                                                   'prescription': 'Perform 100 '
                                                                                                   'repetitions. '
                                                                                                   'Complete 5 sets.'},
                                                                                  {'name': 'Jump Squats',
                                                                                   'prescription': 'Perform 50 '
                                                                                                   'repetitions. '
                                                                                                   'Complete 5 sets.'},
                                                                                  {'name': 'Walking Lunges',
                                                                                   'prescription': 'Perform 50 lunges '
                                                                                                   'per leg. Complete '
                                                                                                   '3 sets.'},
                                                                                  {'name': 'Sit-Ups',
                                                                                   'prescription': 'Perform 100 '
                                                                                                   'repetitions. '
                                                                                                   'Complete 5 sets.'},
                                                                                  {'name': 'Leg Raises',
                                                                                   'prescription': 'Perform 50 '
                                                                                                   'repetitions. '
                                                                                                   'Complete 5 sets.'},
                                                                                  {'name': 'Plank Hold',
                                                                                   'prescription': 'Hold for 2 '
                                                                                                   'minutes. Complete '
                                                                                                   '5 rounds.'},
                                                                                  {'name': 'Sprint Intervals',
                                                                                   'prescription': 'Sprint 100 meters. '
                                                                                                   'Repeat 10 times.'},
                                                                                  {'name': 'Bear Crawl',
                                                                                   'prescription': 'Crawl 20 meters. '
                                                                                                   'Repeat 10 rounds.'},
                                                                                  {'name': 'Burpee Challenge',
                                                                                   'prescription': 'Perform 100 '
                                                                                                   'burpees.'},
                                                                                  {'name': 'Judoka Warrior Circuit',
                                                                                   'prescription': '50 push-ups 20 '
                                                                                                   'pull-ups 100 '
                                                                                                   'squats 100 shrimp '
                                                                                                   'escapes Repeat 3 '
                                                                                                   'rounds.'}]}}},
 'brazilian_jiu_jitsu_learn_how_to_play': {'alone': {'martial_arts_brazilian_jiu_jitsu_learn_how_to_play': {'key': 'martial_arts_brazilian_jiu_jitsu_learn_how_to_play',
                                                                                                            'sport': 'Martial '
                                                                                                                     'Arts',
                                                                                                            'martial_art': 'Brazilian '
                                                                                                                           'Jiu-Jitsu',
                                                                                                            'title': 'Brazilian '
                                                                                                                     'Jiu-Jitsu '
                                                                                                                     '– '
                                                                                                                     'Learn '
                                                                                                                     'How '
                                                                                                                     'To '
                                                                                                                     'Play',
                                                                                                            'category': 'brazilian_jiu_jitsu_learn_how_to_play',
                                                                                                            'training_mode': 'alone',
                                                                                                            'level': 'learn_how_to_play',
                                                                                                            'focus': 'learn '
                                                                                                                     'how '
                                                                                                                     'to '
                                                                                                                     'play',
                                                                                                            'exercises': [{'name': 'BJJ '
                                                                                                                                   'Fighting '
                                                                                                                                   'Stance '
                                                                                                                                   'Practice',
                                                                                                                           'prescription': 'Assume '
                                                                                                                                           'grappling '
                                                                                                                                           'stance. '
                                                                                                                                           'Hold '
                                                                                                                                           'for '
                                                                                                                                           '30 '
                                                                                                                                           'seconds. '
                                                                                                                                           'Repeat '
                                                                                                                                           '10 '
                                                                                                                                           'times.'},
                                                                                                                          {'name': 'Forward '
                                                                                                                                   'Movement '
                                                                                                                                   'Drill',
                                                                                                                           'prescription': 'Move '
                                                                                                                                           'forward '
                                                                                                                                           '10 '
                                                                                                                                           'meters '
                                                                                                                                           'in '
                                                                                                                                           'grappling '
                                                                                                                                           'stance. '
                                                                                                                                           'Repeat '
                                                                                                                                           '10 '
                                                                                                                                           'rounds.'},
                                                                                                                          {'name': 'Backward '
                                                                                                                                   'Movement '
                                                                                                                                   'Drill',
                                                                                                                           'prescription': 'Move '
                                                                                                                                           'backward '
                                                                                                                                           '10 '
                                                                                                                                           'meters '
                                                                                                                                           'in '
                                                                                                                                           'grappling '
                                                                                                                                           'stance. '
                                                                                                                                           'Repeat '
                                                                                                                                           '10 '
                                                                                                                                           'rounds.'},
                                                                                                                          {'name': 'Technical '
                                                                                                                                   'Stand-Up '
                                                                                                                                   'Introduction',
                                                                                                                           'prescription': 'Perform '
                                                                                                                                           '100 '
                                                                                                                                           'technical '
                                                                                                                                           'stand-ups.'},
                                                                                                                          {'name': 'Hip '
                                                                                                                                   'Escape '
                                                                                                                                   'Introduction',
                                                                                                                           'prescription': 'Perform '
                                                                                                                                           '100 '
                                                                                                                                           'shrimp '
                                                                                                                                           'escapes.'},
                                                                                                                          {'name': 'Bridge '
                                                                                                                                   'Introduction',
                                                                                                                           'prescription': 'Perform '
                                                                                                                                           '100 '
                                                                                                                                           'bridge '
                                                                                                                                           'movements.'},
                                                                                                                          {'name': 'Forward '
                                                                                                                                   'Roll '
                                                                                                                                   'Drill',
                                                                                                                           'prescription': 'Perform '
                                                                                                                                           '50 '
                                                                                                                                           'forward '
                                                                                                                                           'rolls.'},
                                                                                                                          {'name': 'Backward '
                                                                                                                                   'Roll '
                                                                                                                                   'Drill',
                                                                                                                           'prescription': 'Perform '
                                                                                                                                           '50 '
                                                                                                                                           'backward '
                                                                                                                                           'rolls.'},
                                                                                                                          {'name': 'Sit-Out '
                                                                                                                                   'Introduction',
                                                                                                                           'prescription': 'Perform '
                                                                                                                                           '50 '
                                                                                                                                           'sit-outs '
                                                                                                                                           'per '
                                                                                                                                           'side.'},
                                                                                                                          {'name': 'Ground '
                                                                                                                                   'Movement '
                                                                                                                                   'Circuit',
                                                                                                                           'prescription': 'Shrimp '
                                                                                                                                           '10 '
                                                                                                                                           'meters. '
                                                                                                                                           'Forward '
                                                                                                                                           'roll '
                                                                                                                                           'back. '
                                                                                                                                           'Repeat '
                                                                                                                                           '10 '
                                                                                                                                           'rounds.'},
                                                                                                                          {'name': 'Shadow '
                                                                                                                                   'Grappling '
                                                                                                                                   'Round',
                                                                                                                           'prescription': 'Simulate '
                                                                                                                                           'BJJ '
                                                                                                                                           'movement '
                                                                                                                                           'for '
                                                                                                                                           '2 '
                                                                                                                                           'minutes. '
                                                                                                                                           'Complete '
                                                                                                                                           '5 '
                                                                                                                                           'rounds.'},
                                                                                                                          {'name': 'Beginner '
                                                                                                                                   'Coordination '
                                                                                                                                   'Circuit',
                                                                                                                           'prescription': '20 '
                                                                                                                                           'bridges '
                                                                                                                                           '20 '
                                                                                                                                           'shrimp '
                                                                                                                                           'escapes '
                                                                                                                                           '20 '
                                                                                                                                           'technical '
                                                                                                                                           'stand-ups '
                                                                                                                                           'Repeat '
                                                                                                                                           '5 '
                                                                                                                                           'rounds.'}]}}},
 'brazilian_jiu_jitsu_beginner': {'alone': {'martial_arts_brazilian_jiu_jitsu_beginner': {'key': 'martial_arts_brazilian_jiu_jitsu_beginner',
                                                                                          'sport': 'Martial Arts',
                                                                                          'martial_art': 'Brazilian '
                                                                                                         'Jiu-Jitsu',
                                                                                          'title': 'Brazilian '
                                                                                                   'Jiu-Jitsu – '
                                                                                                   'Beginner',
                                                                                          'category': 'brazilian_jiu_jitsu_beginner',
                                                                                          'training_mode': 'alone',
                                                                                          'level': 'beginner',
                                                                                          'focus': 'beginner',
                                                                                          'exercises': [{'name': 'Technical '
                                                                                                                 'Stand-Up '
                                                                                                                 'Volume',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '200 '
                                                                                                                         'repetitions.'},
                                                                                                        {'name': 'Shrimp '
                                                                                                                 'Escape '
                                                                                                                 'Volume',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '200 '
                                                                                                                         'repetitions.'},
                                                                                                        {'name': 'Reverse '
                                                                                                                 'Shrimp '
                                                                                                                 'Volume',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '200 '
                                                                                                                         'repetitions.'},
                                                                                                        {'name': 'Bridge '
                                                                                                                 'Volume',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '200 '
                                                                                                                         'repetitions.'},
                                                                                                        {'name': 'Sit-Out '
                                                                                                                 'Volume',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '100 '
                                                                                                                         'repetitions '
                                                                                                                         'per '
                                                                                                                         'side.'},
                                                                                                        {'name': 'Forward '
                                                                                                                 'Roll '
                                                                                                                 'Volume',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '100 '
                                                                                                                         'repetitions.'},
                                                                                                        {'name': 'Backward '
                                                                                                                 'Roll '
                                                                                                                 'Volume',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '100 '
                                                                                                                         'repetitions.'},
                                                                                                        {'name': 'Granby '
                                                                                                                 'Roll '
                                                                                                                 'Introduction',
                                                                                                         'prescription': 'Perform '
                                                                                                                         '50 '
                                                                                                                         'repetitions '
                                                                                                                         'per '
                                                                                                                         'side.'},
                                                                                                        {'name': 'Ground '
                                                                                                                 'Movement '
                                                                                                                 'Round',
                                                                                                         'prescription': 'Move '
                                                                                                                         'continuously '
                                                                                                                         'for '
                                                                                                                         '3 '
                                                                                                                         'minutes. '
                                                                                                                         'Complete '
                                                                                                                         '5 '
                                                                                                                         'rounds.'},
                                                                                                        {'name': 'Balance '
                                                                                                                 'Challenge',
                                                                                                         'prescription': 'Stand '
                                                                                                                         'on '
                                                                                                                         'one '
                                                                                                                         'leg '
                                                                                                                         'for '
                                                                                                                         '1 '
                                                                                                                         'minute. '
                                                                                                                         'Repeat '
                                                                                                                         '5 '
                                                                                                                         'times '
                                                                                                                         'per '
                                                                                                                         'side.'},
                                                                                                        {'name': 'Shadow '
                                                                                                                 'Grappling',
                                                                                                         'prescription': '3-minute '
                                                                                                                         'rounds. '
                                                                                                                         'Complete '
                                                                                                                         '5 '
                                                                                                                         'rounds.'},
                                                                                                        {'name': 'Beginner '
                                                                                                                 'Conditioning '
                                                                                                                 'Circuit',
                                                                                                         'prescription': '20 '
                                                                                                                         'push-ups '
                                                                                                                         '30 '
                                                                                                                         'squats '
                                                                                                                         '20 '
                                                                                                                         'sit-ups '
                                                                                                                         'Repeat '
                                                                                                                         '5 '
                                                                                                                         'rounds.'}]}}},
 'brazilian_jiu_jitsu_guard': {'alone': {'martial_arts_brazilian_jiu_jitsu_guard': {'key': 'martial_arts_brazilian_jiu_jitsu_guard',
                                                                                    'sport': 'Martial Arts',
                                                                                    'martial_art': 'Brazilian '
                                                                                                   'Jiu-Jitsu',
                                                                                    'title': 'Brazilian Jiu-Jitsu – '
                                                                                             'Guard',
                                                                                    'category': 'brazilian_jiu_jitsu_guard',
                                                                                    'training_mode': 'alone',
                                                                                    'level': 'all_levels',
                                                                                    'focus': 'guard',
                                                                                    'exercises': [{'name': 'Hip Escape '
                                                                                                           'Circuit',
                                                                                                   'prescription': 'Perform '
                                                                                                                   '300 '
                                                                                                                   'shrimp '
                                                                                                                   'escapes.'},
                                                                                                  {'name': 'Reverse '
                                                                                                           'Shrimp '
                                                                                                           'Circuit',
                                                                                                   'prescription': 'Perform '
                                                                                                                   '300 '
                                                                                                                   'reverse '
                                                                                                                   'shrimp '
                                                                                                                   'escapes.'},
                                                                                                  {'name': 'Closed '
                                                                                                           'Guard Leg '
                                                                                                           'Lift',
                                                                                                   'prescription': 'Raise '
                                                                                                                   'hips '
                                                                                                                   'and '
                                                                                                                   'squeeze '
                                                                                                                   'knees '
                                                                                                                   'together. '
                                                                                                                   'Repeat '
                                                                                                                   '200 '
                                                                                                                   'times.'},
                                                                                                  {'name': 'Guard '
                                                                                                           'Retention '
                                                                                                           'Movement',
                                                                                                   'prescription': 'Move '
                                                                                                                   'hips '
                                                                                                                   'side '
                                                                                                                   'to '
                                                                                                                   'side '
                                                                                                                   'continuously '
                                                                                                                   'for '
                                                                                                                   '3 '
                                                                                                                   'minutes. '
                                                                                                                   'Complete '
                                                                                                                   '5 '
                                                                                                                   'rounds.'},
                                                                                                  {'name': 'Knee-to-Chest '
                                                                                                           'Drill',
                                                                                                   'prescription': 'Pull '
                                                                                                                   'knees '
                                                                                                                   'to '
                                                                                                                   'chest. '
                                                                                                                   'Repeat '
                                                                                                                   '200 '
                                                                                                                   'times.'},
                                                                                                  {'name': 'Leg '
                                                                                                           'Pummeling '
                                                                                                           'Drill',
                                                                                                   'prescription': 'Alternate '
                                                                                                                   'leg '
                                                                                                                   'positions. '
                                                                                                                   'Repeat '
                                                                                                                   '200 '
                                                                                                                   'times.'},
                                                                                                  {'name': 'Inversion '
                                                                                                           'Drill',
                                                                                                   'prescription': 'Perform '
                                                                                                                   '100 '
                                                                                                                   'inversions.'},
                                                                                                  {'name': 'Granby '
                                                                                                           'Roll Drill',
                                                                                                   'prescription': 'Perform '
                                                                                                                   '100 '
                                                                                                                   'granby '
                                                                                                                   'rolls.'},
                                                                                                  {'name': 'Guard '
                                                                                                           'Recovery '
                                                                                                           'Drill',
                                                                                                   'prescription': 'Simulate '
                                                                                                                   'recovering '
                                                                                                                   'guard. '
                                                                                                                   'Repeat '
                                                                                                                   '200 '
                                                                                                                   'times.'},
                                                                                                  {'name': 'Butterfly '
                                                                                                           'Lift '
                                                                                                           'Motion',
                                                                                                   'prescription': 'Simulate '
                                                                                                                   'butterfly '
                                                                                                                   'sweep '
                                                                                                                   'motion. '
                                                                                                                   'Repeat '
                                                                                                                   '200 '
                                                                                                                   'times.'},
                                                                                                  {'name': 'Guard '
                                                                                                           'Endurance '
                                                                                                           'Round',
                                                                                                   'prescription': 'Maintain '
                                                                                                                   'active '
                                                                                                                   'guard '
                                                                                                                   'movement '
                                                                                                                   'for '
                                                                                                                   '5 '
                                                                                                                   'minutes. '
                                                                                                                   'Complete '
                                                                                                                   '3 '
                                                                                                                   'rounds.'},
                                                                                                  {'name': 'Guard '
                                                                                                           'Warrior '
                                                                                                           'Challenge',
                                                                                                   'prescription': '100 '
                                                                                                                   'shrimps '
                                                                                                                   '100 '
                                                                                                                   'reverse '
                                                                                                                   'shrimps '
                                                                                                                   '50 '
                                                                                                                   'inversions '
                                                                                                                   'Repeat '
                                                                                                                   '3 '
                                                                                                                   'rounds.'}]}}},
 'brazilian_jiu_jitsu_passing': {'alone': {'martial_arts_brazilian_jiu_jitsu_passing': {'key': 'martial_arts_brazilian_jiu_jitsu_passing',
                                                                                        'sport': 'Martial Arts',
                                                                                        'martial_art': 'Brazilian '
                                                                                                       'Jiu-Jitsu',
                                                                                        'title': 'Brazilian Jiu-Jitsu '
                                                                                                 '– Passing',
                                                                                        'category': 'brazilian_jiu_jitsu_passing',
                                                                                        'training_mode': 'alone',
                                                                                        'level': 'all_levels',
                                                                                        'focus': 'passing',
                                                                                        'exercises': [{'name': 'Combat '
                                                                                                               'Base '
                                                                                                               'Movement',
                                                                                                       'prescription': 'Move '
                                                                                                                       'forward '
                                                                                                                       'and '
                                                                                                                       'backward '
                                                                                                                       'in '
                                                                                                                       'combat '
                                                                                                                       'base. '
                                                                                                                       'Continue '
                                                                                                                       'for '
                                                                                                                       '5 '
                                                                                                                       'minutes.'},
                                                                                                      {'name': 'Side-to-Side '
                                                                                                               'Passing '
                                                                                                               'Motion',
                                                                                                       'prescription': 'Simulate '
                                                                                                                       'guard '
                                                                                                                       'passing '
                                                                                                                       'footwork. '
                                                                                                                       'Repeat '
                                                                                                                       '200 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Knee '
                                                                                                               'Slice '
                                                                                                               'Motion',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '200 '
                                                                                                                       'knee '
                                                                                                                       'slice '
                                                                                                                       'movements.'},
                                                                                                      {'name': 'Toreando '
                                                                                                               'Motion',
                                                                                                       'prescription': 'Simulate '
                                                                                                                       'toreando '
                                                                                                                       'pass. '
                                                                                                                       'Repeat '
                                                                                                                       '200 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Long '
                                                                                                               'Step '
                                                                                                               'Motion',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '100 '
                                                                                                                       'long-step '
                                                                                                                       'passes.'},
                                                                                                      {'name': 'Sprawl '
                                                                                                               'and '
                                                                                                               'Pass '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '100 '
                                                                                                                       'sprawls '
                                                                                                                       'followed '
                                                                                                                       'by '
                                                                                                                       'passing '
                                                                                                                       'motion.'},
                                                                                                      {'name': 'Pressure '
                                                                                                               'Walk '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Walk '
                                                                                                                       'forward '
                                                                                                                       'maintaining '
                                                                                                                       'low '
                                                                                                                       'pressure '
                                                                                                                       'position. '
                                                                                                                       'Continue '
                                                                                                                       'for '
                                                                                                                       '10 '
                                                                                                                       'minutes.'},
                                                                                                      {'name': 'Side '
                                                                                                               'Control '
                                                                                                               'Entry',
                                                                                                       'prescription': 'Simulate '
                                                                                                                       'entering '
                                                                                                                       'side '
                                                                                                                       'control. '
                                                                                                                       'Repeat '
                                                                                                                       '200 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Back '
                                                                                                               'Step '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '200 '
                                                                                                                       'back-step '
                                                                                                                       'movements.'},
                                                                                                      {'name': 'Passing '
                                                                                                               'Flow '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Chain '
                                                                                                                       'three '
                                                                                                                       'pass '
                                                                                                                       'movements '
                                                                                                                       'together. '
                                                                                                                       'Repeat '
                                                                                                                       '100 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Continuous '
                                                                                                               'Passing '
                                                                                                               'Round',
                                                                                                       'prescription': 'Simulate '
                                                                                                                       'passing '
                                                                                                                       'for '
                                                                                                                       '3 '
                                                                                                                       'minutes. '
                                                                                                                       'Complete '
                                                                                                                       '5 '
                                                                                                                       'rounds.'},
                                                                                                      {'name': 'Passing '
                                                                                                               'Endurance '
                                                                                                               'Challenge',
                                                                                                       'prescription': 'Complete '
                                                                                                                       '1,000 '
                                                                                                                       'total '
                                                                                                                       'passing '
                                                                                                                       'movements.'}]}}},
 'brazilian_jiu_jitsu_sweeps': {'alone': {'martial_arts_brazilian_jiu_jitsu_sweeps': {'key': 'martial_arts_brazilian_jiu_jitsu_sweeps',
                                                                                      'sport': 'Martial Arts',
                                                                                      'martial_art': 'Brazilian '
                                                                                                     'Jiu-Jitsu',
                                                                                      'title': 'Brazilian Jiu-Jitsu – '
                                                                                               'Sweeps',
                                                                                      'category': 'brazilian_jiu_jitsu_sweeps',
                                                                                      'training_mode': 'alone',
                                                                                      'level': 'all_levels',
                                                                                      'focus': 'sweeps',
                                                                                      'exercises': [{'name': 'Bridge '
                                                                                                             'Sweep '
                                                                                                             'Motion',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '200 '
                                                                                                                     'repetitions.'},
                                                                                                    {'name': 'Scissor '
                                                                                                             'Sweep '
                                                                                                             'Motion',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '200 '
                                                                                                                     'repetitions.'},
                                                                                                    {'name': 'Hip Bump '
                                                                                                             'Sweep '
                                                                                                             'Motion',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '200 '
                                                                                                                     'repetitions.'},
                                                                                                    {'name': 'Pendulum '
                                                                                                             'Sweep '
                                                                                                             'Motion',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '100 '
                                                                                                                     'repetitions.'},
                                                                                                    {'name': 'Butterfly '
                                                                                                             'Sweep '
                                                                                                             'Motion',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '200 '
                                                                                                                     'repetitions.'},
                                                                                                    {'name': 'Tripod '
                                                                                                             'Sweep '
                                                                                                             'Motion',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '200 '
                                                                                                                     'repetitions.'},
                                                                                                    {'name': 'Technical '
                                                                                                             'Stand-Up '
                                                                                                             'Sweep '
                                                                                                             'Finish',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '100 '
                                                                                                                     'repetitions.'},
                                                                                                    {'name': 'Explosive '
                                                                                                             'Hip Lift',
                                                                                                     'prescription': 'Perform '
                                                                                                                     '100 '
                                                                                                                     'explosive '
                                                                                                                     'bridges.'},
                                                                                                    {'name': 'Sweep '
                                                                                                             'Chain '
                                                                                                             'Drill',
                                                                                                     'prescription': 'Link '
                                                                                                                     'three '
                                                                                                                     'sweep '
                                                                                                                     'motions. '
                                                                                                                     'Repeat '
                                                                                                                     '100 '
                                                                                                                     'times.'},
                                                                                                    {'name': 'Sweep '
                                                                                                             'Balance '
                                                                                                             'Drill',
                                                                                                     'prescription': 'Shift '
                                                                                                                     'body '
                                                                                                                     'weight '
                                                                                                                     'side '
                                                                                                                     'to '
                                                                                                                     'side. '
                                                                                                                     'Repeat '
                                                                                                                     '200 '
                                                                                                                     'times.'},
                                                                                                    {'name': 'Continuous '
                                                                                                             'Sweep '
                                                                                                             'Round',
                                                                                                     'prescription': 'Simulate '
                                                                                                                     'sweeps '
                                                                                                                     'continuously '
                                                                                                                     'for '
                                                                                                                     '3 '
                                                                                                                     'minutes. '
                                                                                                                     'Complete '
                                                                                                                     '5 '
                                                                                                                     'rounds.'},
                                                                                                    {'name': 'Sweep '
                                                                                                             'Warrior '
                                                                                                             'Circuit',
                                                                                                     'prescription': '50 '
                                                                                                                     'bridges '
                                                                                                                     '50 '
                                                                                                                     'scissor '
                                                                                                                     'sweeps '
                                                                                                                     '50 '
                                                                                                                     'hip '
                                                                                                                     'bumps '
                                                                                                                     'Repeat '
                                                                                                                     '3 '
                                                                                                                     'rounds.'}]}}},
 'brazilian_jiu_jitsu_submissions': {'alone': {'martial_arts_brazilian_jiu_jitsu_submissions': {'key': 'martial_arts_brazilian_jiu_jitsu_submissions',
                                                                                                'sport': 'Martial Arts',
                                                                                                'martial_art': 'Brazilian '
                                                                                                               'Jiu-Jitsu',
                                                                                                'title': 'Brazilian '
                                                                                                         'Jiu-Jitsu – '
                                                                                                         'Submissions',
                                                                                                'category': 'brazilian_jiu_jitsu_submissions',
                                                                                                'training_mode': 'alone',
                                                                                                'level': 'all_levels',
                                                                                                'focus': 'submissions',
                                                                                                'exercises': [{'name': 'Armbar '
                                                                                                                       'Hip '
                                                                                                                       'Lift '
                                                                                                                       'Motion',
                                                                                                               'prescription': 'Perform '
                                                                                                                               '200 '
                                                                                                                               'repetitions.'},
                                                                                                              {'name': 'Triangle '
                                                                                                                       'Leg '
                                                                                                                       'Lock '
                                                                                                                       'Motion',
                                                                                                               'prescription': 'Perform '
                                                                                                                               '200 '
                                                                                                                               'repetitions.'},
                                                                                                              {'name': 'Kimura '
                                                                                                                       'Grip '
                                                                                                                       'Motion',
                                                                                                               'prescription': 'Perform '
                                                                                                                               '200 '
                                                                                                                               'repetitions.'},
                                                                                                              {'name': 'Guillotine '
                                                                                                                       'Grip '
                                                                                                                       'Motion',
                                                                                                               'prescription': 'Perform '
                                                                                                                               '200 '
                                                                                                                               'repetitions.'},
                                                                                                              {'name': 'Rear '
                                                                                                                       'Naked '
                                                                                                                       'Choke '
                                                                                                                       'Motion',
                                                                                                               'prescription': 'Perform '
                                                                                                                               '200 '
                                                                                                                               'repetitions.'},
                                                                                                              {'name': 'Omoplata '
                                                                                                                       'Motion',
                                                                                                               'prescription': 'Perform '
                                                                                                                               '100 '
                                                                                                                               'repetitions.'},
                                                                                                              {'name': 'Armbar '
                                                                                                                       'Swing '
                                                                                                                       'Drill',
                                                                                                               'prescription': 'Swing '
                                                                                                                               'leg '
                                                                                                                               'over '
                                                                                                                               'imaginary '
                                                                                                                               'opponent. '
                                                                                                                               'Repeat '
                                                                                                                               '200 '
                                                                                                                               'times.'},
                                                                                                              {'name': 'Triangle '
                                                                                                                       'Angle '
                                                                                                                       'Creation',
                                                                                                               'prescription': 'Rotate '
                                                                                                                               'hips '
                                                                                                                               'into '
                                                                                                                               'triangle '
                                                                                                                               'position. '
                                                                                                                               'Repeat '
                                                                                                                               '200 '
                                                                                                                               'times.'},
                                                                                                              {'name': 'Submission '
                                                                                                                       'Chain '
                                                                                                                       'Drill',
                                                                                                               'prescription': 'Armbar '
                                                                                                                               '→ '
                                                                                                                               'Triangle '
                                                                                                                               '→ '
                                                                                                                               'Omoplata. '
                                                                                                                               'Repeat '
                                                                                                                               '100 '
                                                                                                                               'times.'},
                                                                                                              {'name': 'Fast '
                                                                                                                       'Submission '
                                                                                                                       'Drill',
                                                                                                               'prescription': 'Perform '
                                                                                                                               'maximum '
                                                                                                                               'submission '
                                                                                                                               'entries '
                                                                                                                               'in '
                                                                                                                               '1 '
                                                                                                                               'minute. '
                                                                                                                               'Complete '
                                                                                                                               '5 '
                                                                                                                               'rounds.'},
                                                                                                              {'name': 'Submission '
                                                                                                                       'Flow '
                                                                                                                       'Round',
                                                                                                               'prescription': 'Chain '
                                                                                                                               'submissions '
                                                                                                                               'continuously '
                                                                                                                               'for '
                                                                                                                               '3 '
                                                                                                                               'minutes. '
                                                                                                                               'Complete '
                                                                                                                               '5 '
                                                                                                                               'rounds.'},
                                                                                                              {'name': 'Submission '
                                                                                                                       'Challenge',
                                                                                                               'prescription': 'Complete '
                                                                                                                               '1,000 '
                                                                                                                               'total '
                                                                                                                               'submission '
                                                                                                                               'movements.'}]}}},
 'brazilian_jiu_jitsu_escapes': {'alone': {'martial_arts_brazilian_jiu_jitsu_escapes': {'key': 'martial_arts_brazilian_jiu_jitsu_escapes',
                                                                                        'sport': 'Martial Arts',
                                                                                        'martial_art': 'Brazilian '
                                                                                                       'Jiu-Jitsu',
                                                                                        'title': 'Brazilian Jiu-Jitsu '
                                                                                                 '– Escapes',
                                                                                        'category': 'brazilian_jiu_jitsu_escapes',
                                                                                        'training_mode': 'alone',
                                                                                        'level': 'all_levels',
                                                                                        'focus': 'escapes',
                                                                                        'exercises': [{'name': 'Mount '
                                                                                                               'Escape '
                                                                                                               'Bridge',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '200 '
                                                                                                                       'repetitions.'},
                                                                                                      {'name': 'Elbow '
                                                                                                               'Escape '
                                                                                                               'Motion',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '200 '
                                                                                                                       'repetitions.'},
                                                                                                      {'name': 'Side '
                                                                                                               'Control '
                                                                                                               'Shrimp '
                                                                                                               'Escape',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '200 '
                                                                                                                       'repetitions.'},
                                                                                                      {'name': 'Technical '
                                                                                                               'Stand-Up '
                                                                                                               'Escape',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '200 '
                                                                                                                       'repetitions.'},
                                                                                                      {'name': 'Back '
                                                                                                               'Escape '
                                                                                                               'Hip '
                                                                                                               'Rotation',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '200 '
                                                                                                                       'repetitions.'},
                                                                                                      {'name': 'Turtle '
                                                                                                               'Escape '
                                                                                                               'Motion',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '100 '
                                                                                                                       'repetitions.'},
                                                                                                      {'name': 'Frame '
                                                                                                               'Creation '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Build '
                                                                                                                       'defensive '
                                                                                                                       'frames. '
                                                                                                                       'Repeat '
                                                                                                                       '200 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Bridge-to-Shrimp '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Combine '
                                                                                                                       'bridge '
                                                                                                                       'and '
                                                                                                                       'shrimp. '
                                                                                                                       'Repeat '
                                                                                                                       '200 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Escape '
                                                                                                               'Chain '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Link '
                                                                                                                       'three '
                                                                                                                       'escapes. '
                                                                                                                       'Repeat '
                                                                                                                       '100 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Fast '
                                                                                                               'Escape '
                                                                                                               'Challenge',
                                                                                                       'prescription': 'Perform '
                                                                                                                       'maximum '
                                                                                                                       'escapes '
                                                                                                                       'in '
                                                                                                                       '1 '
                                                                                                                       'minute. '
                                                                                                                       'Complete '
                                                                                                                       '5 '
                                                                                                                       'rounds.'},
                                                                                                      {'name': 'Continuous '
                                                                                                               'Escape '
                                                                                                               'Round',
                                                                                                       'prescription': 'Simulate '
                                                                                                                       'escapes '
                                                                                                                       'for '
                                                                                                                       '3 '
                                                                                                                       'minutes. '
                                                                                                                       'Complete '
                                                                                                                       '5 '
                                                                                                                       'rounds.'},
                                                                                                      {'name': 'Escape '
                                                                                                               'Warrior '
                                                                                                               'Circuit',
                                                                                                       'prescription': '100 '
                                                                                                                       'bridges '
                                                                                                                       '100 '
                                                                                                                       'shrimps '
                                                                                                                       '50 '
                                                                                                                       'stand-ups '
                                                                                                                       'Repeat '
                                                                                                                       '3 '
                                                                                                                       'rounds.'}]}}},
 'brazilian_jiu_jitsu_rolling_sparring_preparation': {'alone': {'martial_arts_brazilian_jiu_jitsu_rolling_sparring_preparation': {'key': 'martial_arts_brazilian_jiu_jitsu_rolling_sparring_preparation',
                                                                                                                                  'sport': 'Martial '
                                                                                                                                           'Arts',
                                                                                                                                  'martial_art': 'Brazilian '
                                                                                                                                                 'Jiu-Jitsu',
                                                                                                                                  'title': 'Brazilian '
                                                                                                                                           'Jiu-Jitsu '
                                                                                                                                           '– '
                                                                                                                                           'Rolling '
                                                                                                                                           '(Sparring '
                                                                                                                                           'Preparation)',
                                                                                                                                  'category': 'brazilian_jiu_jitsu_rolling_sparring_preparation',
                                                                                                                                  'training_mode': 'alone',
                                                                                                                                  'level': 'all_levels',
                                                                                                                                  'focus': 'rolling '
                                                                                                                                           '(sparring '
                                                                                                                                           'preparation)',
                                                                                                                                  'exercises': [{'name': 'Shadow '
                                                                                                                                                         'Rolling',
                                                                                                                                                 'prescription': 'Simulate '
                                                                                                                                                                 'grappling '
                                                                                                                                                                 'exchanges '
                                                                                                                                                                 'for '
                                                                                                                                                                 '3 '
                                                                                                                                                                 'minutes. '
                                                                                                                                                                 'Complete '
                                                                                                                                                                 '10 '
                                                                                                                                                                 'rounds.'},
                                                                                                                                                {'name': 'Position '
                                                                                                                                                         'Transition '
                                                                                                                                                         'Drill',
                                                                                                                                                 'prescription': 'Move '
                                                                                                                                                                 'between '
                                                                                                                                                                 'mount, '
                                                                                                                                                                 'side '
                                                                                                                                                                 'control, '
                                                                                                                                                                 'guard, '
                                                                                                                                                                 'and '
                                                                                                                                                                 'back '
                                                                                                                                                                 'control. '
                                                                                                                                                                 'Repeat '
                                                                                                                                                                 '200 '
                                                                                                                                                                 'times.'},
                                                                                                                                                {'name': 'Technical '
                                                                                                                                                         'Stand-Up '
                                                                                                                                                         'Recovery',
                                                                                                                                                 'prescription': 'Stand '
                                                                                                                                                                 'and '
                                                                                                                                                                 'return '
                                                                                                                                                                 'to '
                                                                                                                                                                 'grappling '
                                                                                                                                                                 'stance. '
                                                                                                                                                                 'Repeat '
                                                                                                                                                                 '200 '
                                                                                                                                                                 'times.'},
                                                                                                                                                {'name': 'Attack '
                                                                                                                                                         'Chain '
                                                                                                                                                         'Drill',
                                                                                                                                                 'prescription': 'Simulate '
                                                                                                                                                                 'three '
                                                                                                                                                                 'attacks '
                                                                                                                                                                 'in '
                                                                                                                                                                 'sequence. '
                                                                                                                                                                 'Repeat '
                                                                                                                                                                 '100 '
                                                                                                                                                                 'times.'},
                                                                                                                                                {'name': 'Escape-to-Attack '
                                                                                                                                                         'Drill',
                                                                                                                                                 'prescription': 'Simulate '
                                                                                                                                                                 'escape '
                                                                                                                                                                 'then '
                                                                                                                                                                 'submission. '
                                                                                                                                                                 'Repeat '
                                                                                                                                                                 '100 '
                                                                                                                                                                 'times.'},
                                                                                                                                                {'name': 'Guard-to-Sweep '
                                                                                                                                                         'Drill',
                                                                                                                                                 'prescription': 'Simulate '
                                                                                                                                                                 'sweep '
                                                                                                                                                                 'sequence. '
                                                                                                                                                                 'Repeat '
                                                                                                                                                                 '100 '
                                                                                                                                                                 'times.'},
                                                                                                                                                {'name': 'Passing-to-Control '
                                                                                                                                                         'Drill',
                                                                                                                                                 'prescription': 'Simulate '
                                                                                                                                                                 'pass '
                                                                                                                                                                 'then '
                                                                                                                                                                 'control '
                                                                                                                                                                 'position. '
                                                                                                                                                                 'Repeat '
                                                                                                                                                                 '100 '
                                                                                                                                                                 'times.'},
                                                                                                                                                {'name': 'Submission-to-Control '
                                                                                                                                                         'Drill',
                                                                                                                                                 'prescription': 'Transition '
                                                                                                                                                                 'between '
                                                                                                                                                                 'attacks. '
                                                                                                                                                                 'Repeat '
                                                                                                                                                                 '100 '
                                                                                                                                                                 'times.'},
                                                                                                                                                {'name': 'Continuous '
                                                                                                                                                         'Movement '
                                                                                                                                                         'Round',
                                                                                                                                                 'prescription': 'Move '
                                                                                                                                                                 'non-stop '
                                                                                                                                                                 'for '
                                                                                                                                                                 '5 '
                                                                                                                                                                 'minutes. '
                                                                                                                                                                 'Complete '
                                                                                                                                                                 '5 '
                                                                                                                                                                 'rounds.'},
                                                                                                                                                {'name': 'Competition '
                                                                                                                                                         'Pace '
                                                                                                                                                         'Round',
                                                                                                                                                 'prescription': 'Simulate '
                                                                                                                                                                 'tournament '
                                                                                                                                                                 'intensity '
                                                                                                                                                                 'for '
                                                                                                                                                                 '6 '
                                                                                                                                                                 'minutes. '
                                                                                                                                                                 'Complete '
                                                                                                                                                                 '5 '
                                                                                                                                                                 'rounds.'},
                                                                                                                                                {'name': 'Match '
                                                                                                                                                         'Simulation',
                                                                                                                                                 'prescription': 'Perform '
                                                                                                                                                                 '5 '
                                                                                                                                                                 'complete '
                                                                                                                                                                 'BJJ '
                                                                                                                                                                 'match '
                                                                                                                                                                 'simulations.'},
                                                                                                                                                {'name': 'Tournament '
                                                                                                                                                         'Endurance '
                                                                                                                                                         'Challenge',
                                                                                                                                                 'prescription': 'Complete '
                                                                                                                                                                 '30 '
                                                                                                                                                                 'minutes '
                                                                                                                                                                 'of '
                                                                                                                                                                 'continuous '
                                                                                                                                                                 'grappling '
                                                                                                                                                                 'movement.'}]}}},
 'brazilian_jiu_jitsu_conditioning': {'alone': {'martial_arts_brazilian_jiu_jitsu_conditioning': {'key': 'martial_arts_brazilian_jiu_jitsu_conditioning',
                                                                                                  'sport': 'Martial '
                                                                                                           'Arts',
                                                                                                  'martial_art': 'Brazilian '
                                                                                                                 'Jiu-Jitsu',
                                                                                                  'title': 'Brazilian '
                                                                                                           'Jiu-Jitsu '
                                                                                                           '– '
                                                                                                           'Conditioning',
                                                                                                  'category': 'brazilian_jiu_jitsu_conditioning',
                                                                                                  'training_mode': 'alone',
                                                                                                  'level': 'all_levels',
                                                                                                  'focus': 'conditioning',
                                                                                                  'exercises': [{'name': 'Push-Ups',
                                                                                                                 'prescription': 'Perform '
                                                                                                                                 '50 '
                                                                                                                                 'repetitions. '
                                                                                                                                 'Complete '
                                                                                                                                 '5 '
                                                                                                                                 'sets.'},
                                                                                                                {'name': 'Pull-Ups',
                                                                                                                 'prescription': 'Perform '
                                                                                                                                 '20 '
                                                                                                                                 'repetitions. '
                                                                                                                                 'Complete '
                                                                                                                                 '5 '
                                                                                                                                 'sets.'},
                                                                                                                {'name': 'Squats',
                                                                                                                 'prescription': 'Perform '
                                                                                                                                 '100 '
                                                                                                                                 'repetitions. '
                                                                                                                                 'Complete '
                                                                                                                                 '5 '
                                                                                                                                 'sets.'},
                                                                                                                {'name': 'Jump '
                                                                                                                         'Squats',
                                                                                                                 'prescription': 'Perform '
                                                                                                                                 '50 '
                                                                                                                                 'repetitions. '
                                                                                                                                 'Complete '
                                                                                                                                 '5 '
                                                                                                                                 'sets.'},
                                                                                                                {'name': 'Walking '
                                                                                                                         'Lunges',
                                                                                                                 'prescription': 'Perform '
                                                                                                                                 '50 '
                                                                                                                                 'lunges '
                                                                                                                                 'per '
                                                                                                                                 'leg. '
                                                                                                                                 'Complete '
                                                                                                                                 '3 '
                                                                                                                                 'sets.'},
                                                                                                                {'name': 'Sit-Ups',
                                                                                                                 'prescription': 'Perform '
                                                                                                                                 '100 '
                                                                                                                                 'repetitions. '
                                                                                                                                 'Complete '
                                                                                                                                 '5 '
                                                                                                                                 'sets.'},
                                                                                                                {'name': 'Leg '
                                                                                                                         'Raises',
                                                                                                                 'prescription': 'Perform '
                                                                                                                                 '50 '
                                                                                                                                 'repetitions. '
                                                                                                                                 'Complete '
                                                                                                                                 '5 '
                                                                                                                                 'sets.'},
                                                                                                                {'name': 'Plank '
                                                                                                                         'Hold',
                                                                                                                 'prescription': 'Hold '
                                                                                                                                 'for '
                                                                                                                                 '2 '
                                                                                                                                 'minutes. '
                                                                                                                                 'Complete '
                                                                                                                                 '5 '
                                                                                                                                 'rounds.'},
                                                                                                                {'name': 'Bear '
                                                                                                                         'Crawl',
                                                                                                                 'prescription': 'Crawl '
                                                                                                                                 '20 '
                                                                                                                                 'meters. '
                                                                                                                                 'Repeat '
                                                                                                                                 '10 '
                                                                                                                                 'rounds.'},
                                                                                                                {'name': 'Sprint '
                                                                                                                         'Intervals',
                                                                                                                 'prescription': 'Sprint '
                                                                                                                                 '100 '
                                                                                                                                 'meters. '
                                                                                                                                 'Repeat '
                                                                                                                                 '10 '
                                                                                                                                 'times.'},
                                                                                                                {'name': 'Burpee '
                                                                                                                         'Challenge',
                                                                                                                 'prescription': 'Perform '
                                                                                                                                 '100 '
                                                                                                                                 'burpees.'},
                                                                                                                {'name': 'BJJ '
                                                                                                                         'Warrior '
                                                                                                                         'Circuit',
                                                                                                                 'prescription': '50 '
                                                                                                                                 'push-ups '
                                                                                                                                 '20 '
                                                                                                                                 'pull-ups '
                                                                                                                                 '100 '
                                                                                                                                 'shrimps '
                                                                                                                                 '100 '
                                                                                                                                 'bridges '
                                                                                                                                 'Repeat '
                                                                                                                                 '3 '
                                                                                                                                 'rounds.'}]}}},
 'krav_maga_learn_how_to_play': {'alone': {'martial_arts_krav_maga_learn_how_to_play': {'key': 'martial_arts_krav_maga_learn_how_to_play',
                                                                                        'sport': 'Martial Arts',
                                                                                        'martial_art': 'Krav Maga',
                                                                                        'title': 'Krav Maga – Learn '
                                                                                                 'How To Play',
                                                                                        'category': 'krav_maga_learn_how_to_play',
                                                                                        'training_mode': 'alone',
                                                                                        'level': 'learn_how_to_play',
                                                                                        'focus': 'learn how to play',
                                                                                        'exercises': [{'name': 'Fighting '
                                                                                                               'Stance '
                                                                                                               'Practice',
                                                                                                       'prescription': 'Assume '
                                                                                                                       'Krav '
                                                                                                                       'Maga '
                                                                                                                       'fighting '
                                                                                                                       'stance. '
                                                                                                                       'Hold '
                                                                                                                       'for '
                                                                                                                       '30 '
                                                                                                                       'seconds. '
                                                                                                                       'Repeat '
                                                                                                                       '10 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Forward '
                                                                                                               'and '
                                                                                                               'Backward '
                                                                                                               'Movement',
                                                                                                       'prescription': 'Move '
                                                                                                                       'forward '
                                                                                                                       '10 '
                                                                                                                       'steps. '
                                                                                                                       'Move '
                                                                                                                       'backward '
                                                                                                                       '10 '
                                                                                                                       'steps. '
                                                                                                                       'Repeat '
                                                                                                                       '10 '
                                                                                                                       'rounds.'},
                                                                                                      {'name': 'Basic '
                                                                                                               'Palm '
                                                                                                               'Strike',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '100 '
                                                                                                                       'palm '
                                                                                                                       'strikes '
                                                                                                                       'per '
                                                                                                                       'arm.'},
                                                                                                      {'name': 'Basic '
                                                                                                               'Hammer '
                                                                                                               'Fist',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '100 '
                                                                                                                       'hammer '
                                                                                                                       'fists '
                                                                                                                       'per '
                                                                                                                       'arm.'},
                                                                                                      {'name': 'Front '
                                                                                                               'Kick '
                                                                                                               'Introduction',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '50 '
                                                                                                                       'front '
                                                                                                                       'kicks '
                                                                                                                       'per '
                                                                                                                       'leg.'},
                                                                                                      {'name': 'Knee '
                                                                                                               'Strike '
                                                                                                               'Introduction',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '50 '
                                                                                                                       'knees '
                                                                                                                       'per '
                                                                                                                       'leg.'},
                                                                                                      {'name': 'Elbow '
                                                                                                               'Strike '
                                                                                                               'Introduction',
                                                                                                       'prescription': 'Perform '
                                                                                                                       '50 '
                                                                                                                       'elbows '
                                                                                                                       'per '
                                                                                                                       'arm.'},
                                                                                                      {'name': 'Defensive '
                                                                                                               'Cover '
                                                                                                               'Position',
                                                                                                       'prescription': 'Raise '
                                                                                                                       'defensive '
                                                                                                                       'cover '
                                                                                                                       'and '
                                                                                                                       'hold '
                                                                                                                       'for '
                                                                                                                       '10 '
                                                                                                                       'seconds. '
                                                                                                                       'Repeat '
                                                                                                                       '50 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Strike-and-Move '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Throw '
                                                                                                                       'a '
                                                                                                                       'strike '
                                                                                                                       'and '
                                                                                                                       'move '
                                                                                                                       'away. '
                                                                                                                       'Repeat '
                                                                                                                       '100 '
                                                                                                                       'times.'},
                                                                                                      {'name': 'Awareness '
                                                                                                               'Drill',
                                                                                                       'prescription': 'Walk '
                                                                                                                       'for '
                                                                                                                       '5 '
                                                                                                                       'minutes '
                                                                                                                       'while '
                                                                                                                       'scanning '
                                                                                                                       'left, '
                                                                                                                       'right, '
                                                                                                                       'and '
                                                                                                                       'behind '
                                                                                                                       'every '
                                                                                                                       '5 '
                                                                                                                       'seconds.'},
                                                                                                      {'name': 'Shadow '
                                                                                                               'Self-Defense '
                                                                                                               'Round',
                                                                                                       'prescription': 'Practice '
                                                                                                                       'strikes, '
                                                                                                                       'movement, '
                                                                                                                       'and '
                                                                                                                       'defensive '
                                                                                                                       'reactions '
                                                                                                                       'for '
                                                                                                                       '2 '
                                                                                                                       'minutes. '
                                                                                                                       'Complete '
                                                                                                                       '5 '
                                                                                                                       'rounds.'},
                                                                                                      {'name': 'Beginner '
                                                                                                               'Coordination '
                                                                                                               'Circuit',
                                                                                                       'prescription': '20 '
                                                                                                                       'palm '
                                                                                                                       'strikes '
                                                                                                                       '20 '
                                                                                                                       'knees '
                                                                                                                       '20 '
                                                                                                                       'front '
                                                                                                                       'kicks '
                                                                                                                       'Repeat '
                                                                                                                       '5 '
                                                                                                                       'rounds.'}]}}},
 'krav_maga_beginner': {'alone': {'martial_arts_krav_maga_beginner': {'key': 'martial_arts_krav_maga_beginner',
                                                                      'sport': 'Martial Arts',
                                                                      'martial_art': 'Krav Maga',
                                                                      'title': 'Krav Maga – Beginner',
                                                                      'category': 'krav_maga_beginner',
                                                                      'training_mode': 'alone',
                                                                      'level': 'beginner',
                                                                      'focus': 'beginner',
                                                                      'exercises': [{'name': 'Fighting Stance Hold',
                                                                                     'prescription': 'Hold stance for '
                                                                                                     '1 minute. Repeat '
                                                                                                     '5 rounds.'},
                                                                                    {'name': 'Palm Strike Volume',
                                                                                     'prescription': 'Perform 300 palm '
                                                                                                     'strikes.'},
                                                                                    {'name': 'Hammer Fist Volume',
                                                                                     'prescription': 'Perform 300 '
                                                                                                     'hammer fists.'},
                                                                                    {'name': 'Front Kick Volume',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'front kicks per '
                                                                                                     'leg.'},
                                                                                    {'name': 'Knee Strike Volume',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'knees per leg.'},
                                                                                    {'name': 'Elbow Strike Volume',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'elbows per arm.'},
                                                                                    {'name': 'Palm Strike-Knee '
                                                                                             'Combination',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'combinations.'},
                                                                                    {'name': 'Defensive Cover Drill',
                                                                                     'prescription': 'Cover and '
                                                                                                     'counterattack. '
                                                                                                     'Repeat 100 '
                                                                                                     'times.'},
                                                                                    {'name': 'Movement Circuit',
                                                                                     'prescription': 'Move forward, '
                                                                                                     'backward, left, '
                                                                                                     'and right '
                                                                                                     'continuously for '
                                                                                                     '5 minutes.'},
                                                                                    {'name': 'Shadow Self-Defense',
                                                                                     'prescription': '3-minute rounds. '
                                                                                                     'Complete 5 '
                                                                                                     'rounds.'},
                                                                                    {'name': 'Awareness Walk',
                                                                                     'prescription': 'Walk while '
                                                                                                     'continuously '
                                                                                                     'scanning '
                                                                                                     'surroundings for '
                                                                                                     '10 minutes.'},
                                                                                    {'name': 'Beginner Conditioning '
                                                                                             'Circuit',
                                                                                     'prescription': '20 push-ups 30 '
                                                                                                     'squats 20 '
                                                                                                     'burpees Repeat 5 '
                                                                                                     'rounds.'}]}}},
 'krav_maga_striking': {'alone': {'martial_arts_krav_maga_striking': {'key': 'martial_arts_krav_maga_striking',
                                                                      'sport': 'Martial Arts',
                                                                      'martial_art': 'Krav Maga',
                                                                      'title': 'Krav Maga – Striking',
                                                                      'category': 'krav_maga_striking',
                                                                      'training_mode': 'alone',
                                                                      'level': 'all_levels',
                                                                      'focus': 'striking',
                                                                      'exercises': [{'name': 'Palm Strike Volume',
                                                                                     'prescription': 'Perform 500 palm '
                                                                                                     'strikes.'},
                                                                                    {'name': 'Hammer Fist Volume',
                                                                                     'prescription': 'Perform 500 '
                                                                                                     'hammer fists.'},
                                                                                    {'name': 'Straight Punch Volume',
                                                                                     'prescription': 'Perform 300 '
                                                                                                     'straight '
                                                                                                     'punches.'},
                                                                                    {'name': 'Elbow Strike Volume',
                                                                                     'prescription': 'Perform 300 '
                                                                                                     'elbows.'},
                                                                                    {'name': 'Knee Strike Volume',
                                                                                     'prescription': 'Perform 300 '
                                                                                                     'knees.'},
                                                                                    {'name': 'Front Kick Volume',
                                                                                     'prescription': 'Perform 200 '
                                                                                                     'front kicks per '
                                                                                                     'leg.'},
                                                                                    {'name': 'Palm-Knee Combination',
                                                                                     'prescription': 'Perform 200 '
                                                                                                     'combinations.'},
                                                                                    {'name': 'Palm-Elbow Combination',
                                                                                     'prescription': 'Perform 200 '
                                                                                                     'combinations.'},
                                                                                    {'name': 'Palm-Knee-Elbow '
                                                                                             'Combination',
                                                                                     'prescription': 'Perform 100 '
                                                                                                     'combinations.'},
                                                                                    {'name': 'Speed Striking Round',
                                                                                     'prescription': 'Strike '
                                                                                                     'continuously for '
                                                                                                     '1 minute. '
                                                                                                     'Complete 5 '
                                                                                                     'rounds.'},
                                                                                    {'name': 'Heavy Bag Striking Round',
                                                                                     'prescription': 'Strike at '
                                                                                                     'maximum power '
                                                                                                     'for 3 minutes. '
                                                                                                     'Complete 5 '
                                                                                                     'rounds.'},
                                                                                    {'name': '1,000 Strike Challenge',
                                                                                     'prescription': 'Complete 1,000 '
                                                                                                     'total '
                                                                                                     'strikes.'}]}}},
 'krav_maga_self_defense': {'alone': {'martial_arts_krav_maga_self_defense': {'key': 'martial_arts_krav_maga_self_defense',
                                                                              'sport': 'Martial Arts',
                                                                              'martial_art': 'Krav Maga',
                                                                              'title': 'Krav Maga – Self-Defense',
                                                                              'category': 'krav_maga_self_defense',
                                                                              'training_mode': 'alone',
                                                                              'level': 'all_levels',
                                                                              'focus': 'self-defense',
                                                                              'exercises': [{'name': 'Wrist Grab '
                                                                                                     'Escape Motion',
                                                                                             'prescription': 'Practice '
                                                                                                             'escape '
                                                                                                             'movement. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Double Wrist '
                                                                                                     'Grab Escape',
                                                                                             'prescription': 'Practice '
                                                                                                             'escape '
                                                                                                             'movement. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Front Choke '
                                                                                                     'Escape Motion',
                                                                                             'prescription': 'Practice '
                                                                                                             'escape '
                                                                                                             'movement. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Side Choke '
                                                                                                     'Escape Motion',
                                                                                             'prescription': 'Practice '
                                                                                                             'escape '
                                                                                                             'movement. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Rear Choke '
                                                                                                     'Escape Motion',
                                                                                             'prescription': 'Practice '
                                                                                                             'escape '
                                                                                                             'movement. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Bear Hug Escape '
                                                                                                     'Motion',
                                                                                             'prescription': 'Practice '
                                                                                                             'escape '
                                                                                                             'movement. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Shirt Grab '
                                                                                                     'Release',
                                                                                             'prescription': 'Practice '
                                                                                                             'release '
                                                                                                             'movement. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Push Defense '
                                                                                                     'Drill',
                                                                                             'prescription': 'Simulate '
                                                                                                             'defending '
                                                                                                             'against '
                                                                                                             'a push. '
                                                                                                             'Repeat '
                                                                                                             '200 '
                                                                                                             'times.'},
                                                                                            {'name': 'Immediate '
                                                                                                     'Counterattack '
                                                                                                     'Drill',
                                                                                             'prescription': 'Escape '
                                                                                                             'and '
                                                                                                             'throw 3 '
                                                                                                             'strikes. '
                                                                                                             'Repeat '
                                                                                                             '100 '
                                                                                                             'times.'},
                                                                                            {'name': 'Escape-and-Run '
                                                                                                     'Drill',
                                                                                             'prescription': 'Escape '
                                                                                                             'position '
                                                                                                             'and '
                                                                                                             'sprint '
                                                                                                             '20 '
                                                                                                             'meters. '
                                                                                                             'Repeat '
                                                                                                             '50 '
                                                                                                             'times.'},
                                                                                            {'name': 'Scenario '
                                                                                                     'Visualization '
                                                                                                     'Round',
                                                                                             'prescription': 'Visualize '
                                                                                                             'self-defense '
                                                                                                             'situations '
                                                                                                             'for 3 '
                                                                                                             'minutes. '
                                                                                                             'Complete '
                                                                                                             '5 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Self-Defense '
                                                                                                     'Circuit',
                                                                                             'prescription': '20 wrist '
                                                                                                             'escapes '
                                                                                                             '20 choke '
                                                                                                             'escapes '
                                                                                                             '20 push '
                                                                                                             'defenses '
                                                                                                             'Repeat 5 '
                                                                                                             'rounds.'}]}}},
 'krav_maga_weapon_defense': {'alone': {'martial_arts_krav_maga_weapon_defense': {'key': 'martial_arts_krav_maga_weapon_defense',
                                                                                  'sport': 'Martial Arts',
                                                                                  'martial_art': 'Krav Maga',
                                                                                  'title': 'Krav Maga – Weapon Defense',
                                                                                  'category': 'krav_maga_weapon_defense',
                                                                                  'training_mode': 'alone',
                                                                                  'level': 'all_levels',
                                                                                  'focus': 'weapon defense',
                                                                                  'exercises': [{'name': 'Knife '
                                                                                                         'Defense '
                                                                                                         'Footwork',
                                                                                                 'prescription': 'Practice '
                                                                                                                 'offline '
                                                                                                                 'movement. '
                                                                                                                 'Repeat '
                                                                                                                 '200 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Defensive '
                                                                                                         'Redirection '
                                                                                                         'Motion',
                                                                                                 'prescription': 'Simulate '
                                                                                                                 'redirecting '
                                                                                                                 'a '
                                                                                                                 'weapon '
                                                                                                                 'attack. '
                                                                                                                 'Repeat '
                                                                                                                 '200 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Control '
                                                                                                         'Position '
                                                                                                         'Entry',
                                                                                                 'prescription': 'Practice '
                                                                                                                 'entering '
                                                                                                                 'control '
                                                                                                                 'position. '
                                                                                                                 'Repeat '
                                                                                                                 '200 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Disarm '
                                                                                                         'Motion',
                                                                                                 'prescription': 'Practice '
                                                                                                                 'disarm '
                                                                                                                 'mechanics. '
                                                                                                                 'Repeat '
                                                                                                                 '200 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Stick '
                                                                                                         'Defense '
                                                                                                         'Motion',
                                                                                                 'prescription': 'Simulate '
                                                                                                                 'stick '
                                                                                                                 'defense. '
                                                                                                                 'Repeat '
                                                                                                                 '200 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Overhead '
                                                                                                         'Attack '
                                                                                                         'Defense',
                                                                                                 'prescription': 'Practice '
                                                                                                                 'defensive '
                                                                                                                 'movement. '
                                                                                                                 'Repeat '
                                                                                                                 '200 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Side Attack '
                                                                                                         'Defense',
                                                                                                 'prescription': 'Practice '
                                                                                                                 'defensive '
                                                                                                                 'movement. '
                                                                                                                 'Repeat '
                                                                                                                 '200 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Threat '
                                                                                                         'Response '
                                                                                                         'Drill',
                                                                                                 'prescription': 'Practice '
                                                                                                                 'immediate '
                                                                                                                 'movement '
                                                                                                                 'and '
                                                                                                                 'control. '
                                                                                                                 'Repeat '
                                                                                                                 '100 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Multiple '
                                                                                                         'Angle '
                                                                                                         'Defense',
                                                                                                 'prescription': 'Alternate '
                                                                                                                 'attack '
                                                                                                                 'angles. '
                                                                                                                 'Repeat '
                                                                                                                 '200 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Defense-to-Escape '
                                                                                                         'Drill',
                                                                                                 'prescription': 'Defend '
                                                                                                                 'and '
                                                                                                                 'sprint '
                                                                                                                 '20 '
                                                                                                                 'meters. '
                                                                                                                 'Repeat '
                                                                                                                 '50 '
                                                                                                                 'times.'},
                                                                                                {'name': 'Weapon '
                                                                                                         'Awareness '
                                                                                                         'Walk',
                                                                                                 'prescription': 'Walk '
                                                                                                                 'and '
                                                                                                                 'identify '
                                                                                                                 'potential '
                                                                                                                 'threats '
                                                                                                                 'for '
                                                                                                                 '10 '
                                                                                                                 'minutes.'},
                                                                                                {'name': 'Weapon '
                                                                                                         'Defense '
                                                                                                         'Circuit',
                                                                                                 'prescription': '20 '
                                                                                                                 'redirections '
                                                                                                                 '20 '
                                                                                                                 'controls '
                                                                                                                 '20 '
                                                                                                                 'escapes '
                                                                                                                 'Repeat '
                                                                                                                 '5 '
                                                                                                                 'rounds.'}]}}},
 'krav_maga_multiple_attackers': {'alone': {'martial_arts_krav_maga_multiple_attackers': {'key': 'martial_arts_krav_maga_multiple_attackers',
                                                                                          'sport': 'Martial Arts',
                                                                                          'martial_art': 'Krav Maga',
                                                                                          'title': 'Krav Maga – '
                                                                                                   'Multiple Attackers',
                                                                                          'category': 'krav_maga_multiple_attackers',
                                                                                          'training_mode': 'alone',
                                                                                          'level': 'all_levels',
                                                                                          'focus': 'multiple attackers',
                                                                                          'exercises': [{'name': 'Circular '
                                                                                                                 'Footwork '
                                                                                                                 'Drill',
                                                                                                         'prescription': 'Move '
                                                                                                                         'around '
                                                                                                                         'an '
                                                                                                                         'imaginary '
                                                                                                                         'group. '
                                                                                                                         'Continue '
                                                                                                                         'for '
                                                                                                                         '5 '
                                                                                                                         'minutes.'},
                                                                                                        {'name': 'Strike-and-Move '
                                                                                                                 'Drill',
                                                                                                         'prescription': 'Throw '
                                                                                                                         '3 '
                                                                                                                         'strikes '
                                                                                                                         'and '
                                                                                                                         'change '
                                                                                                                         'direction. '
                                                                                                                         'Repeat '
                                                                                                                         '200 '
                                                                                                                         'times.'},
                                                                                                        {'name': 'Escape '
                                                                                                                 'Lane '
                                                                                                                 'Drill',
                                                                                                         'prescription': 'Identify '
                                                                                                                         'escape '
                                                                                                                         'path '
                                                                                                                         'and '
                                                                                                                         'sprint '
                                                                                                                         '20 '
                                                                                                                         'meters. '
                                                                                                                         'Repeat '
                                                                                                                         '50 '
                                                                                                                         'times.'},
                                                                                                        {'name': 'Continuous '
                                                                                                                 'Scanning '
                                                                                                                 'Drill',
                                                                                                         'prescription': 'Turn '
                                                                                                                         'and '
                                                                                                                         'check '
                                                                                                                         'surroundings '
                                                                                                                         'every '
                                                                                                                         '3 '
                                                                                                                         'seconds. '
                                                                                                                         'Continue '
                                                                                                                         'for '
                                                                                                                         '10 '
                                                                                                                         'minutes.'},
                                                                                                        {'name': '360° '
                                                                                                                 'Defense '
                                                                                                                 'Movement',
                                                                                                         'prescription': 'Rotate '
                                                                                                                         'and '
                                                                                                                         'defend '
                                                                                                                         'in '
                                                                                                                         'all '
                                                                                                                         'directions. '
                                                                                                                         'Repeat '
                                                                                                                         '200 '
                                                                                                                         'times.'},
                                                                                                        {'name': 'Front-Rear '
                                                                                                                 'Reaction '
                                                                                                                 'Drill',
                                                                                                         'prescription': 'Alternate '
                                                                                                                         'responses '
                                                                                                                         'to '
                                                                                                                         'front '
                                                                                                                         'and '
                                                                                                                         'rear '
                                                                                                                         'threats. '
                                                                                                                         'Repeat '
                                                                                                                         '200 '
                                                                                                                         'times.'},
                                                                                                        {'name': 'Direction '
                                                                                                                 'Change '
                                                                                                                 'Sprint',
                                                                                                         'prescription': 'Sprint '
                                                                                                                         '10 '
                                                                                                                         'meters '
                                                                                                                         'and '
                                                                                                                         'change '
                                                                                                                         'direction. '
                                                                                                                         'Repeat '
                                                                                                                         '50 '
                                                                                                                         'times.'},
                                                                                                        {'name': 'Burst '
                                                                                                                 'Striking '
                                                                                                                 'Drill',
                                                                                                         'prescription': 'Throw '
                                                                                                                         '10 '
                                                                                                                         'strikes '
                                                                                                                         'and '
                                                                                                                         'move '
                                                                                                                         'away. '
                                                                                                                         'Repeat '
                                                                                                                         '50 '
                                                                                                                         'times.'},
                                                                                                        {'name': 'Defensive '
                                                                                                                 'Circle '
                                                                                                                 'Round',
                                                                                                         'prescription': 'Move '
                                                                                                                         'continuously '
                                                                                                                         'for '
                                                                                                                         '3 '
                                                                                                                         'minutes. '
                                                                                                                         'Complete '
                                                                                                                         '5 '
                                                                                                                         'rounds.'},
                                                                                                        {'name': 'Awareness '
                                                                                                                 'Sprint '
                                                                                                                 'Circuit',
                                                                                                         'prescription': 'Sprint, '
                                                                                                                         'scan, '
                                                                                                                         'recover. '
                                                                                                                         'Repeat '
                                                                                                                         '20 '
                                                                                                                         'rounds.'},
                                                                                                        {'name': 'Escape '
                                                                                                                 'Simulation '
                                                                                                                 'Round',
                                                                                                         'prescription': 'Practice '
                                                                                                                         'escape-focused '
                                                                                                                         'movement '
                                                                                                                         'for '
                                                                                                                         '5 '
                                                                                                                         'minutes. '
                                                                                                                         'Complete '
                                                                                                                         '3 '
                                                                                                                         'rounds.'},
                                                                                                        {'name': 'Multiple '
                                                                                                                 'Attacker '
                                                                                                                 'Circuit',
                                                                                                         'prescription': '20 '
                                                                                                                         'strikes '
                                                                                                                         '20 '
                                                                                                                         'direction '
                                                                                                                         'changes '
                                                                                                                         '20 '
                                                                                                                         'sprints '
                                                                                                                         'Repeat '
                                                                                                                         '5 '
                                                                                                                         'rounds.'}]}}},
 'krav_maga_situational_awareness': {'alone': {'martial_arts_krav_maga_situational_awareness': {'key': 'martial_arts_krav_maga_situational_awareness',
                                                                                                'sport': 'Martial Arts',
                                                                                                'martial_art': 'Krav '
                                                                                                               'Maga',
                                                                                                'title': 'Krav Maga – '
                                                                                                         'Situational '
                                                                                                         'Awareness',
                                                                                                'category': 'krav_maga_situational_awareness',
                                                                                                'training_mode': 'alone',
                                                                                                'level': 'all_levels',
                                                                                                'focus': 'situational '
                                                                                                         'awareness',
                                                                                                'exercises': [{'name': 'Observation '
                                                                                                                       'Walk',
                                                                                                               'prescription': 'Walk '
                                                                                                                               'for '
                                                                                                                               '10 '
                                                                                                                               'minutes. '
                                                                                                                               'Memorize '
                                                                                                                               'details '
                                                                                                                               'of '
                                                                                                                               'surroundings.'},
                                                                                                              {'name': 'Threat '
                                                                                                                       'Identification '
                                                                                                                       'Drill',
                                                                                                               'prescription': 'Identify '
                                                                                                                               '20 '
                                                                                                                               'possible '
                                                                                                                               'exits '
                                                                                                                               'in '
                                                                                                                               'public '
                                                                                                                               'areas.'},
                                                                                                              {'name': 'Awareness '
                                                                                                                       'Scan '
                                                                                                                       'Drill',
                                                                                                               'prescription': 'Check '
                                                                                                                               'surroundings '
                                                                                                                               'every '
                                                                                                                               '5 '
                                                                                                                               'seconds '
                                                                                                                               'for '
                                                                                                                               '10 '
                                                                                                                               'minutes.'},
                                                                                                              {'name': 'Exit '
                                                                                                                       'Location '
                                                                                                                       'Exercise',
                                                                                                               'prescription': 'Enter '
                                                                                                                               'a '
                                                                                                                               'building '
                                                                                                                               'and '
                                                                                                                               'immediately '
                                                                                                                               'identify '
                                                                                                                               'all '
                                                                                                                               'exits. '
                                                                                                                               'Repeat '
                                                                                                                               'in '
                                                                                                                               '10 '
                                                                                                                               'different '
                                                                                                                               'locations.'},
                                                                                                              {'name': 'Vehicle '
                                                                                                                       'Awareness '
                                                                                                                       'Drill',
                                                                                                               'prescription': 'Observe '
                                                                                                                               'parking '
                                                                                                                               'areas '
                                                                                                                               'and '
                                                                                                                               'identify '
                                                                                                                               'safe '
                                                                                                                               'routes. '
                                                                                                                               'Continue '
                                                                                                                               'for '
                                                                                                                               '10 '
                                                                                                                               'minutes.'},
                                                                                                              {'name': 'Reaction '
                                                                                                                       'Time '
                                                                                                                       'Drill',
                                                                                                               'prescription': 'Toss '
                                                                                                                               'a '
                                                                                                                               'tennis '
                                                                                                                               'ball '
                                                                                                                               'and '
                                                                                                                               'catch '
                                                                                                                               'it '
                                                                                                                               'after '
                                                                                                                               'one '
                                                                                                                               'bounce. '
                                                                                                                               'Repeat '
                                                                                                                               '100 '
                                                                                                                               'times.'},
                                                                                                              {'name': 'Peripheral '
                                                                                                                       'Vision '
                                                                                                                       'Drill',
                                                                                                               'prescription': 'Focus '
                                                                                                                               'forward '
                                                                                                                               'while '
                                                                                                                               'identifying '
                                                                                                                               'objects '
                                                                                                                               'to '
                                                                                                                               'the '
                                                                                                                               'sides. '
                                                                                                                               'Continue '
                                                                                                                               'for '
                                                                                                                               '10 '
                                                                                                                               'minutes.'},
                                                                                                              {'name': 'Distance '
                                                                                                                       'Assessment '
                                                                                                                       'Drill',
                                                                                                               'prescription': 'Estimate '
                                                                                                                               'distances '
                                                                                                                               'to '
                                                                                                                               'nearby '
                                                                                                                               'objects. '
                                                                                                                               'Check '
                                                                                                                               'accuracy '
                                                                                                                               '50 '
                                                                                                                               'times.'},
                                                                                                              {'name': 'Environment '
                                                                                                                       'Mapping '
                                                                                                                       'Drill',
                                                                                                               'prescription': 'Spend '
                                                                                                                               '2 '
                                                                                                                               'minutes '
                                                                                                                               'observing '
                                                                                                                               'an '
                                                                                                                               'area. '
                                                                                                                               'Recreate '
                                                                                                                               'the '
                                                                                                                               'layout '
                                                                                                                               'from '
                                                                                                                               'memory.'},
                                                                                                              {'name': 'Escape '
                                                                                                                       'Route '
                                                                                                                       'Planning',
                                                                                                               'prescription': 'Create '
                                                                                                                               'an '
                                                                                                                               'exit '
                                                                                                                               'plan '
                                                                                                                               'for '
                                                                                                                               '10 '
                                                                                                                               'locations.'},
                                                                                                              {'name': 'Awareness '
                                                                                                                       'Challenge',
                                                                                                               'prescription': 'Spend '
                                                                                                                               '15 '
                                                                                                                               'minutes '
                                                                                                                               'in '
                                                                                                                               'public. '
                                                                                                                               'Record '
                                                                                                                               'every '
                                                                                                                               'person '
                                                                                                                               'entering '
                                                                                                                               'and '
                                                                                                                               'leaving '
                                                                                                                               'the '
                                                                                                                               'area.'},
                                                                                                              {'name': 'Situational '
                                                                                                                       'Awareness '
                                                                                                                       'Circuit',
                                                                                                               'prescription': 'Observation '
                                                                                                                               'Exit '
                                                                                                                               'identification '
                                                                                                                               'Threat '
                                                                                                                               'identification '
                                                                                                                               'Repeat '
                                                                                                                               '5 '
                                                                                                                               'rounds.'}]}}},
 'krav_maga_conditioning': {'alone': {'martial_arts_krav_maga_conditioning': {'key': 'martial_arts_krav_maga_conditioning',
                                                                              'sport': 'Martial Arts',
                                                                              'martial_art': 'Krav Maga',
                                                                              'title': 'Krav Maga – Conditioning',
                                                                              'category': 'krav_maga_conditioning',
                                                                              'training_mode': 'alone',
                                                                              'level': 'all_levels',
                                                                              'focus': 'conditioning',
                                                                              'exercises': [{'name': 'Push-Ups',
                                                                                             'prescription': 'Perform '
                                                                                                             '50 '
                                                                                                             'repetitions. '
                                                                                                             'Complete '
                                                                                                             '5 sets.'},
                                                                                            {'name': 'Burpees',
                                                                                             'prescription': 'Perform '
                                                                                                             '100 '
                                                                                                             'repetitions.'},
                                                                                            {'name': 'Squats',
                                                                                             'prescription': 'Perform '
                                                                                                             '100 '
                                                                                                             'repetitions. '
                                                                                                             'Complete '
                                                                                                             '5 sets.'},
                                                                                            {'name': 'Jump Squats',
                                                                                             'prescription': 'Perform '
                                                                                                             '50 '
                                                                                                             'repetitions. '
                                                                                                             'Complete '
                                                                                                             '5 sets.'},
                                                                                            {'name': 'Walking Lunges',
                                                                                             'prescription': 'Perform '
                                                                                                             '50 '
                                                                                                             'lunges '
                                                                                                             'per leg. '
                                                                                                             'Complete '
                                                                                                             '3 sets.'},
                                                                                            {'name': 'Sit-Ups',
                                                                                             'prescription': 'Perform '
                                                                                                             '100 '
                                                                                                             'repetitions. '
                                                                                                             'Complete '
                                                                                                             '5 sets.'},
                                                                                            {'name': 'Leg Raises',
                                                                                             'prescription': 'Perform '
                                                                                                             '50 '
                                                                                                             'repetitions. '
                                                                                                             'Complete '
                                                                                                             '5 sets.'},
                                                                                            {'name': 'Plank Hold',
                                                                                             'prescription': 'Hold for '
                                                                                                             '2 '
                                                                                                             'minutes. '
                                                                                                             'Complete '
                                                                                                             '5 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Sprint Intervals',
                                                                                             'prescription': 'Sprint '
                                                                                                             '100 '
                                                                                                             'meters. '
                                                                                                             'Repeat '
                                                                                                             '10 '
                                                                                                             'times.'},
                                                                                            {'name': 'Bear Crawl',
                                                                                             'prescription': 'Crawl 20 '
                                                                                                             'meters. '
                                                                                                             'Repeat '
                                                                                                             '10 '
                                                                                                             'rounds.'},
                                                                                            {'name': 'Shuttle Runs',
                                                                                             'prescription': 'Sprint '
                                                                                                             '10 '
                                                                                                             'meters '
                                                                                                             'and '
                                                                                                             'back. '
                                                                                                             'Repeat '
                                                                                                             '20 '
                                                                                                             'times.'},
                                                                                            {'name': 'Krav Maga '
                                                                                                     'Warrior Circuit',
                                                                                             'prescription': '50 '
                                                                                                             'push-ups '
                                                                                                             '100 '
                                                                                                             'squats '
                                                                                                             '50 '
                                                                                                             'burpees '
                                                                                                             '100 palm '
                                                                                                             'strikes '
                                                                                                             'Repeat 3 '
                                                                                                             'rounds.'}]}}}}


def get_martial_arts_catalog() -> SportCatalog:
    """Return a deep copy of the full martial arts catalog."""
    return deepcopy(MARTIAL_ARTS_CATALOG)


def list_martial_arts_sessions(
    category: Optional[str] = None,
    training_mode: Optional[str] = None,
    martial_art: Optional[str] = None,
) -> List[SportSession]:
    """List martial arts sessions, optionally filtered by category, mode, or martial art."""
    sessions: List[SportSession] = []
    martial_art_filter = martial_art.lower() if martial_art else None

    for category_key, mode_map in MARTIAL_ARTS_CATALOG.items():
        if category and category_key != category:
            continue

        for mode_key, session_map in mode_map.items():
            if training_mode and mode_key != training_mode:
                continue

            for session_data in session_map.values():
                if martial_art_filter and session_data.get("martial_art", "").lower() != martial_art_filter:
                    continue
                sessions.append(deepcopy(session_data))

    return sessions


def get_martial_arts_session(
    session_key: str,
    category: Optional[str] = None,
    training_mode: Optional[str] = None,
) -> Optional[SportSession]:
    """Return one session by key, or None if it is not found."""
    for session_data in list_martial_arts_sessions(category=category, training_mode=training_mode):
        if session_data["key"] == session_key:
            return session_data
    return None


__all__ = [
    "SPORT",
    "MARTIAL_ARTS_CATALOG",
    "get_martial_arts_catalog",
    "list_martial_arts_sessions",
    "get_martial_arts_session",
]
