import streamlit as st


# =============================================================================
# SPORTZE.AI EXPLORE SECTION
# =============================================================================
# Self-contained Explore module for Sportze.AI.
# Features:
# - Featured Discover area with Water Polo, Triathlon, and Mountain Biking
# - Full catalog with 20 difficult and picturesque sports
# - Photo card for each sport
# - Clickable sport buttons that open one detailed sport page
# - Official global organization/platform link for each sport
#
# Sidebar note:
# The uploaded file does not contain your app.py sidebar code or the old
# "only emoji mode" button. To remove that button, delete the st.checkbox /
# st.toggle / st.button line in app.py that controls emoji-only mode and render
# sidebar labels directly as text titles.
# =============================================================================


SPORTS = {
    "Water Polo": {
        "tagline": "Explosive swimming, contact, strategy, and tactical execution in deep water.",
        "image": "https://www.google.com/imgres?q=water%20polo&imgurl=https%3A%2F%2Fsrsport.com%2Fproduct_images%2Fuploaded_images%2Fman-playing-water-polo.jpg&imgrefurl=https%3A%2F%2Fsrsport.com%2Fblog%2Fwater-polo-suits-vs-swimsuits-key-differences-in-fit-fabric-performance%2F%3Fsrsltid%3DAfmBOoo2x9l4cpM57WvmmemctgvOoldlr39XomEDIu7koWO6zuSQ8deE&docid=yHjOsejDdnCZeM&tbnid=7NKfLaJF8Wgh0M&vet=12ahUKEwiQ7ubSvOiUAxW0G7kGHbWSPBMQnPAOegUIhwEQAQ..i&w=1000&h=573&hcb=2&ved=2ahUKEwiQ7ubSvOiUAxW0G7kGHbWSPBMQnPAOegUIhwEQAQ",
        "mini_definition": (
            "A high-intensity aquatic team sport where athletes swim, pass, wrestle for position, defend, "
            "and shoot while staying afloat the entire time."
        ),
        "definition": (
            "Water polo is one of the most physically complete team sports in the world. It is played in deep water, "
            "so athletes cannot stand or rest on the bottom. They must swim repeatedly, use eggbeater kicking to stay "
            "vertical, absorb contact, pass accurately, defend intelligently, and shoot under pressure. The game looks "
            "beautiful because it combines pool speed, aerial shooting, tactical movement, and constant physical battles "
            "around the center and perimeter. At high levels, water polo demands elite endurance, shoulder power, leg "
            "strength, reaction speed, communication, and the ability to make decisions while exhausted."
        ),
        "why_difficult": (
            "It is difficult because the athlete must perform every action while floating: sprinting, wrestling, shooting, "
            "blocking, changing direction, and reading tactics. The combination of swimming endurance, contact, skill, and "
            "game intelligence makes it extremely demanding."
        ),
        "main_body": "World Aquatics",
        "link": "https://www.worldaquatics.com/",
    },
    "Triathlon": {
        "tagline": "A complete endurance test combining swimming, cycling, running, pacing, and nutrition.",
        "image": "https://images.unsplash.com/photo-1530143584546-02191bc84eb5?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": (
            "An endurance race where athletes swim, cycle, and run in sequence, managing fatigue and transitions."
        ),
        "definition": (
            "Triathlon is a multisport endurance race made of swimming, cycling, and running, completed one after another. "
            "It is picturesque because races often happen in open water, coastal roads, mountains, and city courses, making "
            "the sport visually diverse. The challenge is not only being good at three sports, but also knowing how to pace "
            "each section, transition efficiently, fuel properly, hydrate, and keep strong technique while the body becomes "
            "progressively more fatigued. Distances range from sprint triathlons to long-distance formats such as IRONMAN."
        ),
        "why_difficult": (
            "It is difficult because athletes need huge aerobic capacity, muscular endurance, technical efficiency in three "
            "different disciplines, strong recovery habits, and race strategy. A mistake in pacing or nutrition can destroy "
            "the entire race."
        ),
        "main_body": "World Triathlon",
        "link": "https://www.triathlon.org/",
    },
    "Mountain Biking": {
        "tagline": "High-speed riding through rough terrain, steep descents, rocks, mud, forests, and mountains.",
        "image": "https://www.google.com/imgres?q=mountain%20biking&imgurl=https%3A%2F%2Fwww.exploresquamish.com%2Fsite%2Fassets%2Ffiles%2F22494%2Fslab_riding_squamish.2000x1163.webp&imgrefurl=https%3A%2F%2Fwww.exploresquamish.com%2Fthings-to-do%2Factivities-adventures%2Fmountain-biking%2F&docid=9EkbcPsG9A3hMM&tbnid=Ml5g28rw0FdJIM&vet=12ahUKEwjFro6CveiUAxVUGbkGHYI-H28QnPAOegQIGxAB..i&w=1440&h=838&hcb=2&ved=2ahUKEwjFro6CveiUAxVUGbkGHYI-H28QnPAOegQIGxAB",
        "mini_definition": (
            "An off-road cycling discipline where riders control bikes across trails, climbs, jumps, descents, and technical obstacles."
        ),
        "definition": (
            "Mountain biking is an off-road cycling sport performed on trails, forests, mountains, rocky paths, and technical descents. "
            "It can include cross-country, downhill, enduro, marathon, and freeride styles. The sport is visually powerful because riders "
            "move through natural landscapes at speed, often jumping, cornering, climbing, and descending through difficult terrain. "
            "It requires bike handling, balance, braking control, courage, endurance, leg power, and instant decision-making. Downhill "
            "and enduro versions are especially intense because a rider must read terrain in real time while managing high speed and risk."
        ),
        "why_difficult": (
            "It is difficult because terrain changes constantly. The athlete must combine endurance, strength, technical handling, reflexes, "
            "risk control, and equipment knowledge while moving fast over unpredictable surfaces."
        ),
        "main_body": "Union Cycliste Internationale (UCI)",
        "link": "https://www.uci.org/",
    },
    "Sport Climbing": {
        "tagline": "Vertical problem-solving with strength, technique, flexibility, and courage.",
        "image": "https://images.unsplash.com/photo-1522163182402-834f871fd851?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A climbing sport where athletes solve routes on walls using power, balance, grip, and body control.",
        "definition": (
            "Sport climbing is a competitive and recreational discipline where athletes climb artificial walls or natural rock routes. "
            "Competition formats include lead, boulder, and speed. It is picturesque because it transforms vertical movement into a mix "
            "of athleticism and puzzle-solving. Climbers must understand route sequences, conserve grip strength, coordinate feet and hands, "
            "and move with precision. The best climbers are not just strong; they are efficient, calm, flexible, and creative under pressure."
        ),
        "why_difficult": "It demands finger strength, core control, mobility, fear management, explosive power, and tactical route reading.",
        "main_body": "International Federation of Sport Climbing (IFSC)",
        "link": "https://www.ifsc-climbing.org/",
    },
    "Mountaineering / Ice Climbing": {
        "tagline": "Technical climbing in mountains, snow, ice, altitude, and severe weather.",
        "image": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A mountain sport involving ascent through rock, snow, glaciers, and ice with technical equipment.",
        "definition": (
            "Mountaineering and ice climbing combine adventure, endurance, technical skill, and environmental judgment. Athletes may cross "
            "glaciers, climb frozen waterfalls, ascend ridgelines, use ropes, crampons, ice axes, anchors, and survival systems. The sport is "
            "picturesque because it happens in some of the most dramatic landscapes on Earth: alpine walls, snow peaks, icy valleys, and remote "
            "mountain ranges. It is as much about decision-making and safety as it is about physical strength."
        ),
        "why_difficult": "Altitude, cold, falling risk, avalanches, navigation, fatigue, and technical climbing make it one of the hardest outdoor sports.",
        "main_body": "UIAA",
        "link": "https://www.theuiaa.org/",
    },
    "Alpine Skiing": {
        "tagline": "High-speed racing down steep snow slopes with precision and bravery.",
        "image": "https://images.unsplash.com/photo-1551524559-8af4e6624178?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A winter sport where skiers descend mountain courses at high speed through gates or open slopes.",
        "definition": (
            "Alpine skiing is a mountain racing sport where athletes descend snow-covered slopes in disciplines such as downhill, slalom, giant "
            "slalom, and super-G. It is visually spectacular because it combines snow, mountains, speed, carving turns, and dramatic courses. "
            "Elite skiers control their body at extreme speeds while reacting to terrain, ice, gates, bumps, and changing snow conditions."
        ),
        "why_difficult": "It requires balance, leg strength, edge control, courage, reflexes, and the ability to make decisions at very high speed.",
        "main_body": "International Ski and Snowboard Federation (FIS)",
        "link": "https://www.fis-ski.com/",
    },
    "Ski Mountaineering": {
        "tagline": "Climb mountains on skis, then descend through natural alpine terrain.",
        "image": "https://images.unsplash.com/photo-1605540436563-5bca919ae766?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A sport combining uphill ski travel, mountain endurance, transitions, and technical descents.",
        "definition": (
            "Ski mountaineering mixes endurance climbing with technical skiing. Athletes travel uphill using skins attached to skis, often across "
            "snowy mountain terrain, then remove them and ski down. It is picturesque because it takes place across open alpine landscapes, ridges, "
            "snowfields, and mountain passes. The sport combines aerobic endurance, skiing skill, climbing efficiency, gear management, and mountain safety."
        ),
        "why_difficult": "It demands endurance, altitude adaptation, ski control, fast transitions, weather judgment, and comfort in mountain terrain.",
        "main_body": "International Ski Mountaineering Federation (ISMF)",
        "link": "https://www.ismf-ski.org/",
    },
    "Surfing": {
        "tagline": "Reading the ocean and riding waves with timing, balance, and style.",
        "image": "https://images.unsplash.com/photo-1502680390469-be75c86b636f?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A wave-riding sport where surfers stand on boards and use ocean energy to move across the wave face.",
        "definition": (
            "Surfing is a board sport where athletes ride breaking waves using timing, balance, positioning, and ocean knowledge. The beauty of "
            "surfing comes from its setting: beaches, reefs, sunset sessions, tropical coastlines, and powerful waves. The surfer must paddle into "
            "the right wave, stand at the correct moment, control the board, generate speed, and perform maneuvers while the wave constantly changes."
        ),
        "why_difficult": "No two waves are identical, so surfers must read the ocean, react instantly, balance precisely, and handle wipeouts.",
        "main_body": "International Surfing Association (ISA)",
        "link": "https://www.isasurf.org/",
    },
    "Big Wave Surfing": {
        "tagline": "Surfing giant waves where courage and ocean knowledge become survival skills.",
        "image": "https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "An extreme surfing discipline focused on riding massive ocean waves that can reach life-threatening size.",
        "definition": (
            "Big wave surfing is one of the most extreme ocean sports. Athletes ride waves that can reach enormous heights, often at famous breaks "
            "such as Nazaré, Jaws, Teahupoʻo, and Mavericks. The sport is unforgettable visually because the athlete appears tiny compared with the "
            "moving wall of water. Big wave surfers need technical surfing skill, breath control, rescue systems, courage, and deep understanding of "
            "swells, currents, reefs, and wipeout survival."
        ),
        "why_difficult": "The forces are huge, wipeouts can hold athletes underwater, and success depends on timing, safety teams, courage, and ocean science.",
        "main_body": "World Surf League (WSL)",
        "link": "https://www.worldsurfleague.com/",
    },
    "Kitesurfing": {
        "tagline": "Wind-powered board riding with jumps, speed, and aerial control.",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A water sport where athletes use a kite and board to ride across water and perform jumps.",
        "definition": (
            "Kitesurfing, also called kiteboarding, uses a large controllable kite to pull an athlete across the water on a board. It is picturesque "
            "because riders skim across beaches and blue water, jump high into the air, and use the wind like an engine. The athlete must control kite "
            "power, board direction, wind angle, body position, and safety systems simultaneously."
        ),
        "why_difficult": "It requires wind reading, balance, coordination, power control, and the ability to manage risk when conditions change quickly.",
        "main_body": "International Kiteboarding Association (IKA)",
        "link": "https://www.internationalkiteboarding.org/",
    },
    "Whitewater Kayaking": {
        "tagline": "Navigating powerful river rapids with precision, courage, and reflexes.",
        "image": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A river sport where kayakers descend rapids, drops, waves, and technical whitewater channels.",
        "definition": (
            "Whitewater kayaking is performed on fast-moving rivers, rapids, waterfalls, and artificial courses. Athletes use a small kayak and paddle "
            "to navigate current, rocks, waves, holes, and drops. It is visually dramatic because the athlete is surrounded by moving water and must choose "
            "precise lines through chaotic river features. It combines strength, rhythm, boat control, river reading, and emergency skills."
        ),
        "why_difficult": "Water is constantly moving, so kayakers must react instantly, roll safely, control their boat, and understand river hydraulics.",
        "main_body": "International Canoe Federation (ICF)",
        "link": "https://www.canoeicf.com/",
    },
    "Rowing": {
        "tagline": "Synchronized power, endurance, rhythm, and technical precision on water.",
        "image": "https://images.unsplash.com/photo-1508519829430-40f7d6bfdb69?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A boat-racing sport where athletes use oars to move shells across water as fast and efficiently as possible.",
        "definition": (
            "Rowing is a water racing sport in which athletes propel narrow boats using oars. It can be performed in single sculls, pairs, fours, eights, "
            "and other categories. The sport looks elegant because the boat glides across the water when technique and rhythm are perfect. Under that elegance, "
            "however, rowing is extremely painful and demanding, requiring leg drive, back strength, aerobic capacity, timing, and synchronization."
        ),
        "why_difficult": "It combines maximum endurance with precise technique. In team boats, one mistimed stroke can disturb the entire crew.",
        "main_body": "World Rowing",
        "link": "https://worldrowing.com/",
    },
    "Sailing": {
        "tagline": "Racing with wind, water, tactics, weather, and boat handling.",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A wind-powered racing sport where sailors control boats using sails, tactics, and weather knowledge.",
        "definition": (
            "Sailing is a sport where athletes race boats using wind power. It can happen in small dinghies, Olympic classes, ocean yachts, and high-performance "
            "foiling boats. It is picturesque because it combines open water, sails, wind, waves, and strategy. Sailors must understand wind shifts, currents, "
            "course tactics, boat trim, rules, starts, and equipment. The sport rewards intelligence as much as physical ability."
        ),
        "why_difficult": "Conditions constantly change, so sailors must combine meteorology, tactics, boat mechanics, balance, and fast decision-making.",
        "main_body": "World Sailing",
        "link": "https://www.sailing.org/",
    },
    "Modern Pentathlon": {
        "tagline": "A multi-discipline Olympic-style challenge of speed, skill, precision, and adaptability.",
        "image": "https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A combined sport traditionally involving fencing, swimming, obstacle-style movement, running, and shooting.",
        "definition": (
            "Modern pentathlon is a multi-sport discipline designed to test a complete athlete. It includes fencing, swimming, running, shooting, and modern "
            "event formats that continue to evolve. The sport is interesting because no single ability is enough: athletes need speed, calmness, technical "
            "precision, endurance, and mental reset between very different events. It is a sport of adaptability."
        ),
        "why_difficult": "Athletes must train across several unrelated skills and perform under fatigue while changing mental modes quickly.",
        "main_body": "Union Internationale de Pentathlon Moderne (UIPM)",
        "link": "https://www.uipmworld.org/",
    },
    "Equestrian Eventing": {
        "tagline": "A horse-and-rider test combining dressage, cross-country, and show jumping.",
        "image": "https://images.unsplash.com/photo-1516467508483-a7212febe31a?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "An equestrian discipline where horse and rider compete in control, endurance, jumping, and cross-country courage.",
        "definition": (
            "Equestrian eventing is a demanding horse sport made of dressage, cross-country, and show jumping. It is picturesque because competitions often "
            "take place on open fields, natural obstacles, and elegant arenas. The rider must communicate with the horse through subtle aids, while the horse "
            "must show power, trust, rhythm, courage, and accuracy. Eventing is sometimes described as an equestrian triathlon."
        ),
        "why_difficult": "It requires technical riding, horse partnership, bravery, timing, endurance, and precision across three very different tests.",
        "main_body": "Fédération Equestre Internationale (FEI)",
        "link": "https://www.fei.org/",
    },
    "Freediving": {
        "tagline": "Diving deep underwater on a single breath with calm, control, and physiology.",
        "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "An underwater discipline where athletes dive without breathing equipment, relying on one breath.",
        "definition": (
            "Freediving is the art and sport of diving underwater on a single breath. It can involve depth, distance, or time-based disciplines. The sport is "
            "visually stunning because athletes descend into blue water with minimal equipment, moving calmly through an environment that is naturally hostile "
            "to humans. Freediving requires breath control, relaxation, equalization, fin technique, safety protocols, and understanding of human physiology."
        ),
        "why_difficult": "It is difficult because panic wastes oxygen. Success depends on calmness, technique, body awareness, safety, and training discipline.",
        "main_body": "AIDA International",
        "link": "https://www.aidainternational.org/",
    },
    "Paragliding": {
        "tagline": "Foot-launched flight using air currents, mountains, thermals, and judgment.",
        "image": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "An air sport where pilots fly lightweight gliders launched from hills, mountains, or cliffs.",
        "definition": (
            "Paragliding is a free-flight sport where pilots launch from slopes with a fabric wing and use air currents to stay aloft. It is picturesque because "
            "it offers views over mountains, valleys, coastlines, and landscapes from the air. The pilot must understand thermals, wind direction, turbulence, "
            "landing zones, weather changes, and emergency procedures. It looks peaceful, but it requires serious judgment."
        ),
        "why_difficult": "The main challenge is decision-making: pilots must read invisible air and weather while maintaining control and safety.",
        "main_body": "Fédération Aéronautique Internationale (FAI)",
        "link": "https://www.fai.org/",
    },
    "Aerobatic Flying": {
        "tagline": "Precision aircraft control through loops, rolls, spins, and high-G maneuvers.",
        "image": "https://images.unsplash.com/photo-1529074963764-98f45c47344b?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "An aviation sport where pilots perform controlled aerial maneuvers with extreme precision.",
        "definition": (
            "Aerobatic flying is a discipline where pilots perform complex maneuvers such as rolls, loops, hammerheads, spins, and sequences judged for precision. "
            "It is visually impressive because it turns aircraft into instruments of controlled movement in three-dimensional space. Pilots must manage speed, "
            "altitude, aircraft limits, orientation, G-forces, and sequence accuracy."
        ),
        "why_difficult": "It requires spatial awareness, technical precision, physical tolerance to G-forces, and strict safety discipline.",
        "main_body": "Fédération Aéronautique Internationale (FAI)",
        "link": "https://www.fai.org/",
    },
    "Orienteering": {
        "tagline": "Running through terrain while solving a navigation puzzle at speed.",
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A navigation race where athletes use a map and compass to find checkpoints across terrain.",
        "definition": (
            "Orienteering is a sport where athletes race through forests, parks, mountains, or urban terrain using a detailed map and compass. The winner is not "
            "just the fastest runner, but the person who chooses the smartest route and navigates cleanly under pressure. It is picturesque because it happens "
            "in natural landscapes and turns terrain into a strategic puzzle."
        ),
        "why_difficult": "Athletes must run hard while reading maps, choosing routes, avoiding mistakes, and staying mentally sharp under fatigue.",
        "main_body": "International Orienteering Federation (IOF)",
        "link": "https://orienteering.sport/",
    },
    "Ultra-Trail Running": {
        "tagline": "Long-distance mountain running through remote landscapes, altitude, and extreme fatigue.",
        "image": "https://images.unsplash.com/photo-1551632811-561732d1e306?auto=format&fit=crop&w=1200&q=80",
        "mini_definition": "A long-distance running discipline over trails, mountains, deserts, forests, or remote terrain.",
        "definition": (
            "Ultra-trail running is a long-distance running discipline that often takes athletes through mountains, forests, deserts, coastal paths, and remote "
            "terrain. Races can exceed marathon distance and sometimes pass 100 kilometers or more. The sport is picturesque because it blends endurance with "
            "wild landscapes, sunrise starts, mountain passes, and dramatic finish lines. Athletes must manage pace, climbing, descending, nutrition, sleep, "
            "weather, equipment, and mental resilience."
        ),
        "why_difficult": "The distances are brutal, terrain is uneven, weather can change, and the mental battle becomes as important as fitness.",
        "main_body": "International Trail Running Association (ITRA)",
        "link": "https://itra.run/",
    },
}


FEATURED_SPORTS = ["Water Polo", "Triathlon", "Mountain Biking"]


def _slug(name: str) -> str:
    return (
        name.lower()
        .replace("/", "")
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "_")
    )


def _inject_explore_css() -> None:
    st.markdown(
        """
<style>
    .explore-hero {
        padding: 1.35rem 1.45rem;
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(91,92,255,0.18), rgba(110,231,255,0.08), rgba(255,255,255,0.035));
        margin-bottom: 1.25rem;
    }

    .explore-hero h1 {
        margin: 0 0 0.35rem 0;
        font-size: clamp(2.1rem, 4.8vw, 3.7rem);
        line-height: 0.95;
        letter-spacing: -0.055em;
        font-weight: 900;
    }

    .explore-hero p {
        margin: 0;
        font-size: 1.02rem;
        line-height: 1.58;
        color: rgba(255,255,255,0.80);
        max-width: 980px;
    }

    .explore-card {
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 24px;
        padding: 1.05rem 1.1rem;
        background: rgba(255,255,255,0.052);
        margin-bottom: 0.85rem;
    }

    .explore-card h3 {
        margin: 0 0 0.35rem 0;
        font-size: 1.05rem;
        font-weight: 850;
        letter-spacing: -0.02em;
    }

    .explore-card p, .explore-card li {
        color: rgba(255,255,255,0.78);
        line-height: 1.55;
    }

    .explore-section-title {
        margin-top: 0.3rem;
        font-size: 1.55rem;
        font-weight: 900;
        letter-spacing: -0.035em;
    }

    .explore-muted {
        color: rgba(255,255,255,0.70);
        line-height: 1.5;
    }

    .explore-sport-title {
        font-size: clamp(2.0rem, 4.2vw, 3.2rem);
        line-height: 1.0;
        letter-spacing: -0.052em;
        font-weight: 950;
        margin-bottom: 0.35rem;
    }

    .explore-tagline {
        color: rgba(255,255,255,0.78);
        font-size: 1.05rem;
        margin-bottom: 1rem;
    }

    .explore-link-box {
        border: 1px solid rgba(110,231,255,0.26);
        background: rgba(110,231,255,0.07);
        border-radius: 22px;
        padding: 1rem;
        margin-top: 0.7rem;
    }

    .mini-card-text {
        min-height: 118px;
    }

    div[data-testid="stImage"] img {
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.13);
    }

    .stButton button {
        border-radius: 999px;
        font-weight: 750;
    }
</style>
        """,
        unsafe_allow_html=True,
    )


def _text_card(title: str, body: str) -> None:
    st.markdown(
        f"""
<div class="explore-card">
    <h3>{title}</h3>
    <p>{body}</p>
</div>
        """,
        unsafe_allow_html=True,
    )


def _set_mode(mode: str, sport_name: str | None = None) -> None:
    st.session_state.explore_mode = mode
    if sport_name:
        st.session_state.explore_selected_sport = sport_name


def _sport_card(sport_name: str, featured: bool = False) -> None:
    sport = SPORTS[sport_name]
    st.image(sport["image"], use_container_width=True)
    st.markdown(f"### {sport_name}")
    st.markdown(
        f"<div class='mini-card-text explore-muted'>{sport['mini_definition']}</div>",
        unsafe_allow_html=True,
    )
    button_label = "Open sport" if not featured else f"Open {sport_name}"
    if st.button(button_label, key=f"open_{_slug(sport_name)}_{'featured' if featured else 'catalog'}", use_container_width=True):
        _set_mode("detail", sport_name)
        st.rerun()


def _render_featured_discover() -> None:
    st.markdown("<div class='explore-section-title'>Discover</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='explore-muted'>Start with three Sportze.AI highlight sports, or open the full global catalog.</div>",
        unsafe_allow_html=True,
    )

    if st.button("Discover all 20 sports", type="primary", use_container_width=True):
        _set_mode("catalog")
        st.rerun()

    st.markdown("### Main sports")
    cols = st.columns(3, gap="large")
    for col, sport_name in zip(cols, FEATURED_SPORTS):
        with col:
            _sport_card(sport_name, featured=True)


def _render_catalog() -> None:
    top_left, top_right = st.columns([1, 1])
    with top_left:
        if st.button("Back to main Discover", use_container_width=True):
            _set_mode("home")
            st.rerun()
    with top_right:
        st.markdown(
            "<div class='explore-muted' style='text-align:right;'>Full catalog: 20 difficult and picturesque sports</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='explore-section-title'>All 20 Sports</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='explore-muted'>Each sport has a quick photo card. Open any sport to see the bigger definition, difficulty explanation, and global organization link.</div>",
        unsafe_allow_html=True,
    )

    sport_names = list(SPORTS.keys())
    for i in range(0, len(sport_names), 3):
        cols = st.columns(3, gap="large")
        for col, sport_name in zip(cols, sport_names[i : i + 3]):
            with col:
                _sport_card(sport_name)


def _render_detail() -> None:
    sport_name = st.session_state.get("explore_selected_sport", "Water Polo")
    sport = SPORTS.get(sport_name, SPORTS["Water Polo"])

    nav1, nav2 = st.columns([1, 1])
    with nav1:
        if st.button("Back to Discover", use_container_width=True):
            _set_mode("home")
            st.rerun()
    with nav2:
        if st.button("View all 20 sports", use_container_width=True):
            _set_mode("catalog")
            st.rerun()

    st.image(sport["image"], use_container_width=True)
    st.markdown(f"<div class='explore-sport-title'>{sport_name}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='explore-tagline'>{sport['tagline']}</div>", unsafe_allow_html=True)

    _text_card("Full definition", sport["definition"])
    _text_card("Why it is difficult", sport["why_difficult"])

    st.markdown(
        f"""
<div class="explore-link-box">
    <strong>Main global platform:</strong> {sport["main_body"]}<br>
    <span style="color: rgba(255,255,255,0.76);">
        Use this as the official reference point for rules, competitions, events, rankings, development, and international structure.
    </span>
</div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button(f"Open {sport['main_body']}", sport["link"], use_container_width=True)


def render_explore_section() -> None:
    """Render the Explore page for Sportze.AI."""
    _inject_explore_css()

    st.markdown(
        """
<div class="explore-hero">
    <h1>Explore Sportze.AI</h1>
    <p>
        Sportze.AI is an intelligent sports performance platform designed to help athletes excel in their abilities,
        stay fit, and understand their development with better structure. It connects training generation, sport knowledge,
        recovery logic, video review, counselling, and physical preparation so athletes can explore sports, compare demands,
        and train with more purpose.
    </p>
</div>
        """,
        unsafe_allow_html=True,
    )

    if "explore_mode" not in st.session_state:
        st.session_state.explore_mode = "home"
    if "explore_selected_sport" not in st.session_state:
        st.session_state.explore_selected_sport = "Water Polo"

    mode = st.session_state.explore_mode

    if mode == "catalog":
        _render_catalog()
    elif mode == "detail":
        _render_detail()
    else:
        _render_featured_discover()

    st.divider()
    st.markdown("### What Explore can become next")
    c1, c2, c3 = st.columns(3)
    with c1:
        _text_card("Sport libraries", "Rules, demands, athlete profiles, equipment, main competitions, and official bodies for every sport.")
    with c2:
        _text_card("Smart discovery", "Recommend sports based on goals, schedule, body type, injury history, personality, and available facilities.")
    with c3:
        _text_card("Athlete pathways", "Show beginner-to-elite routes, training milestones, competitions, costs, rankings, and scouting opportunities.")
