"""
Cultural Heritage Content & Interactive Experience Datasets.
Provides grounded historical chronicles, virtual walking tour waypoints,
oral folklore archives, anatomical Meetei Mayek cosmological maps,
and interactive educational quiz questions for low-resource heritage discovery.
"""
from typing import Dict, List, Any

# =============================================================================
# 1. VIRTUAL HERITAGE TOUR: KANGLA SACRED WALK & CULTURAL TRAIL
# =============================================================================
HERITAGE_WALKING_TOUR: List[Dict[str, Any]] = [
    {
        "id": "tour_01",
        "title": "Kangla Western Gate & Dragon Citadel",
        "title_mayek": "ꯀꯪꯂꯥ ꯊꯣꯡ ꯑꯃꯁꯨꯡ ꯀꯪꯂꯥ ꯁꯥ",
        "era": "Pre-Colonial (Rebuilt 2006)",
        "coordinates": "24.8080° N, 93.9392° E",
        "summary": "The grand western entrance to Kangla, guarded by twin colossal statues of the mythological dragon-lion Kangla Sha.",
        "details": (
            "The Kangla Sha is the supreme state emblem of ancient Manipur—a chimera featuring the body of a lion "
            "and the head of a horned dragon. The original brick and mortar statues built during King Chourajit's reign (1804) "
            "were dynamited by British occupational forces in 1891 following the Anglo-Manipur War. The magnificent 20-foot "
            "replicas standing today were sculpted by Mutum Tomba Singh and unveiled on 20 November 2004 when Kangla was formally "
            "handed back to the people of Manipur by the Assam Rifles."
        ),
        "oral_tradition": "According to priestly oral traditions, the Kangla Sha represents divine celestial sentinels guarding the navel of the earth (Kangla).",
        "dual_provenance_note": "Colonial military gazetteers recorded the destruction as 'clearing royal fortifications', whereas community memory mourned it as a desecration of the sacred embodiment of sovereign Meitei statehood.",
        "image_path": "data/images/Southern_gateway_to_the_citadel_of_the_Kangla_fort_in_Imphal.JPG",
        "audio_path": "data/audio/elder_kangla_testimony.wav",
        "audio_caption": "Elder M. Ningthouja testifying on the sacred spiritual borders of Kangla",
        "iconography_tags": ["Kangla Sha", "Dragon Lion", "State Citadel", "Triple Arch Gate", "Imperial Fortification"]
    },
    {
        "id": "tour_02",
        "title": "Sanggai Yumpham (Innermost Royal Citadel)",
        "title_mayek": "ꯁꯪꯒꯥꯏ ꯌꯨꯝꯐꯝ",
        "era": "Ancient to 1891 CE",
        "coordinates": "24.8092° N, 93.9405° E",
        "summary": "The sanctified residential quarter of the Ningthouja dynasty kings and ancestral coronation palace.",
        "details": (
            "Sanggai Yumpham was the royal citadel enclosed within three concentric fortified brick walls and moats. "
            "It was where kings sat upon the sacred sandalwood throne and where the Queen Dowager held council. "
            "The southern gateway features the classic Meitei brick archway adorned with traditional sun motifs."
        ),
        "oral_tradition": "Priestly chronicles in the Puya record that no sword could be unsheathed within Sanggai Yumpham under severe spiritual taboo (Lallup oath).",
        "dual_provenance_note": "1891 British siege plans labelled it 'The King's Inner Enclosure', while Meitei oral chronicles revere it as the cosmic hearth of the realm.",
        "image_path": "data/images/Southern_doorway_of_Sanggai_Yumpham_the_innermost_Meitei_Imperial_residence_inside_the_Kangla_Fort.JPG",
        "audio_path": "data/audio/elder_kangla_testimony.wav",
        "audio_caption": "Oral recitation of royal coronation vows inside Sanggai Yumpham",
        "iconography_tags": ["Royal Residence", "Brick Archway", "Sanggai Yumpham", "Ningthouja Dynasty", "Inner Sanctum"]
    },
    {
        "id": "tour_03",
        "title": "Nungjeng Pukhri (Sacred Lake of Pakhangba)",
        "title_mayek": "ꯅꯨꯡꯖꯦꯡ ꯄꯨꯈ꯭ꯔꯤ",
        "era": "33 CE Ancestral Origin",
        "coordinates": "24.8087° N, 93.9380° E",
        "summary": "The holiest water body of Sanamahism, believed to be the subterranean dwelling of the divine serpent deity Pakhangba.",
        "details": (
            "Nungjeng Pukhri is situated in the north-western quadrant of Kangla. For over two millennia, every Meitei king "
            "was required to bathe in its waters as an indispensable rite of coronation. The lake is revered as an entrance "
            "to the underworld realm of Pakhangba, from where celestial energy is channeled into the kingdom."
        ),
        "oral_tradition": "Maibi priestesses chant that the ripples on Nungjeng Pukhri foretell agricultural harvests and the health of the sovereign.",
        "dual_provenance_note": "Colonial surveys cataloged it simply as a 'rectangular palace reservoir', completely missing its supreme metaphysical role in Sanamahi cosmology.",
        "image_path": "data/images/Kangla_Fort_imphal.JPG",
        "audio_path": "data/audio/lai_haraoba_jagoi_chant.wav",
        "audio_caption": "Sacred water invocation chant by Maibi priestesses during Lai Haraoba",
        "iconography_tags": ["Nungjeng Pukhri", "Pakhangba Residence", "Coronation Pond", "Sanamahi Holy Water"]
    },
    {
        "id": "tour_04",
        "title": "Mapal Kangjeibung (Oldest Living Polo Ground)",
        "title_mayek": "ꯃꯄꯥꯟ ꯀꯪꯖꯩꯕꯨꯡ",
        "era": "Traditional Origin 33 CE / 160 CE",
        "coordinates": "24.8055° N, 93.9360° E",
        "summary": "The birthplace of modern polo, where Sagol Kangjei has been played continuously for thousands of years.",
        "details": (
            "Guinness World Records recognizes Mapal Kangjeibung as the oldest living polo ground in the world. "
            "Meiteis play Sagol Kangjei with seven players a side on indigenous Manipuri ponies using bamboo-root balls and cane sticks. "
            "In 1859, British Lieutenant Joseph Sherer witnessed a match here and founded the Silchar Polo Club, popularizing the sport globally."
        ),
        "oral_tradition": "Mythology attributes polo to Lord Marjing, the god of horses, who invented the game to delight primeval gods on the hillslopes of Heingang.",
        "dual_provenance_note": "Colonial officers claimed the British 'codified' polo into a modern sport, whereas Meitei manuscripts (Sagol Kangjei Puya) demonstrate rigid game rules and referee codes existed centuries before European contact.",
        "image_path": "data/images/A_traditional_Meitei_garden_Heikol_Leikol_or_Heikon_Leikon_in_Kakching_Manipur.jpg",
        "audio_path": "data/audio/elder_kangla_testimony.wav",
        "audio_caption": "Oral account of the legendary polo matches played between the seven clans",
        "iconography_tags": ["Mapal Kangjeibung", "Sagol Kangjei", "Polo Origin", "Manipuri Pony", "Lord Marjing"]
    },
    {
        "id": "tour_05",
        "title": "Shree Govindajee Temple & Sanamahi Kiyong",
        "title_mayek": "ꯁ꯭ꯔꯤ ꯒꯣꯕꯤꯟꯗꯖꯤ ꯑꯃꯁꯨꯡ ꯁꯅꯥꯃꯍꯤ ꯀꯤꯌꯣꯡ",
        "era": "1846 CE & Ancient Restoration",
        "coordinates": "24.8062° N, 93.9485° E",
        "summary": "The twin spiritual poles of Manipur, embodying the unique syncretic coexistence of Gaudiya Vaishnavism and indigenous Sanamahism.",
        "details": (
            "Built by Maharaja Nara Singh in 1846 and later restored by Chandrakirti Singh, Shree Govindajee Temple features "
            "twin gold-plated domes and a spacious Nat Mandap where classical Manipuri Raas Leela and Nat Sankirtana are performed. "
            "Nearby inside Kangla stands the Sanamahi Kiyong temple, dedicated to Lainingthou Sanamahi, the creator deity of the universe."
        ),
        "oral_tradition": "Meitei elders explain that their identity is dual: in the morning they honor Lord Sanamahi at the household hearth (Phunga Lairu), and in the evening they sing praises to Govinda.",
        "dual_provenance_note": "British missionaries mistakenly classified the population as having completely abandoned indigenous religion, overlooking the resilient continuity of Sanamahi rites in every home.",
        "image_path": "data/images/Silky_Oak_tree_known_as_Koubilla_in_Classical_Meitei_language_grown_in_Kakching_Manipur.jpg",
        "audio_path": "data/audio/sankirtana_khol_kartal.wav",
        "audio_caption": "Temple Sankirtana drumming (Khol) and cymbals (Kartal) at the Nat Mandap",
        "iconography_tags": ["Govindajee Temple", "Sanamahi Kiyong", "Twin Gold Domes", "Nat Mandap", "Syncretic Faith"]
    },
    {
        "id": "tour_06",
        "title": "Ima Keithel (The Mother's Market)",
        "title_mayek": "ꯏꯃꯥ ꯀꯩꯊꯦꯜ",
        "era": "16th Century to Present",
        "coordinates": "24.8035° N, 93.9358° E",
        "summary": "Asia's largest all-women market where over 5,000 licensed female traders hold supreme commercial and political sway.",
        "details": (
            "Ima Keithel (literally 'Mother's Market') is a 500-year-old institution established during the reign of King Mwamba. "
            "Only married women are permitted to own and operate stalls across three sprawling multi-story complexes: Leimarel Shidabi, "
            "Emoinu, and Phouoibi. Historically, when men were drafted into forced military labor (Lallup), women took over the economy "
            "and repeatedly spearheaded democratic uprisings, notably the Nupi Lan (Women's Wars) of 1904 and 1939."
        ),
        "oral_tradition": "Market elders state: 'Ima Keithel is not just where we sell spices and handloom phanek; it is where the conscience of Manipur gathers to defend justice.'",
        "dual_provenance_note": "Colonial administrators documented Ima Keithel as a 'bazaar and public nuisance prone to political agitations', failing to respect it as a supreme matriarchal civic assembly.",
        "image_path": "data/images/A_traditional_Meitei_garden_Heikol_Leikol_or_Heikon_Leikon_in_Kakching_Manipur_02.jpg",
        "audio_path": "data/audio/tǝpta_story.wav",
        "audio_caption": "Oral storyteller narrating the courage of mothers during the Nupi Lan uprisings",
        "iconography_tags": ["Ima Keithel", "Women's Market", "Matriarchal Commerce", "Nupi Lan", "Handloom & Spices"]
    },
    {
        "id": "tour_07",
        "title": "Khongjom War Memorial & Hero's Pillar",
        "title_mayek": "ꯈꯣꯡꯖꯣꯝ ꯂꯥꯟꯐꯝ",
        "era": "April 1891 CE",
        "coordinates": "24.5800° N, 93.9900° E",
        "summary": "The sacred battlefield where Major Paona Brajabasi and patriotic warriors made their legendary last stand against the British Empire.",
        "details": (
            "On 25 April 1891, heavily outnumbered Meitei troops clashed with the British army at the foot of Kheba Hill. "
            "Major Paona Brajabasi fought with superhuman valor, refusing offers of treason with the immortal declaration: "
            "'A Meitei warrior dies by his sword rather than live under an alien flag.' Every year on 23 April, Manipur observes "
            "Khongjom Day with state honors and tarpan water offerings to the martyred patriots."
        ),
        "oral_tradition": "Balladeers sing Khongjom Parva—a gripping oral musical ballad recounting the battle with the rhythm of the dholak drum.",
        "dual_provenance_note": "British dispatches claimed the Battle of Khongjom as a 'swift punitive pacification', while Meitei collective consciousness celebrates it as the supreme pinnacle of anti-colonial resistance and martyrdom.",
        "image_path": "data/images/Tomb_of_Meitei_King_Maharaja_Bodhachandra_the_last_sovereign_King_of_Manipur.jpg",
        "audio_path": "data/audio/elder_kangla_testimony.wav",
        "audio_caption": "Oral recitation of Paona Brajabasi's defiance before the British general",
        "iconography_tags": ["Khongjom Battlefield", "Paona Brajabasi", "Khongjom Day", "Hero's Pillar", "Anglo-Manipur War"]
    }
]

# =============================================================================
# 2. MEETEI MAYEK ANATOMICAL SCRIPT DATA & BIDIRECTIONAL CONVERTER
# =============================================================================
MEETEI_MAYEK_ANATOMY = [
    {"char": "ꯀ", "name": "Kok", "body_part": "Head", "ipa": "/k/", "meaning": "Seat of wisdom and supreme consciousness", "example": "ꯀꯪꯂꯩꯄꯥꯛ (Kangleipak)", "region": "Head & Face"},
    {"char": "ꯁ", "name": "Sam", "body_part": "Hair", "ipa": "/s/", "meaning": "Crown of life, antennae to cosmic energy", "example": "ꯁꯪꯒꯥꯏ (Sanggai)", "region": "Head & Face"},
    {"char": "ꯂ", "name": "Lai", "body_part": "Forehead", "ipa": "/l/", "meaning": "Destiny and spiritual vision", "example": "ꯂꯥꯏ (Lai - Deity)", "region": "Head & Face"},
    {"char": "ꯃ", "name": "Mit", "body_part": "Eye", "ipa": "/m/", "meaning": "Clarity, observation, and truth", "example": "ꯃꯤꯇꯩ (Meitei)", "region": "Head & Face"},
    {"char": "ꯄ", "name": "Pa", "body_part": "Eyelash / Lip", "ipa": "/p/", "meaning": "Sensory boundary and expression", "example": "ꯄꯥꯈꯪꯕꯥ (Pakhangba)", "region": "Head & Face"},
    {"char": "ꯅ", "name": "Na", "body_part": "Ear", "ipa": "/n/", "meaning": "Listening to ancestral oral chronicles", "example": "ꯅꯤꯡꯊꯧ (Ningthou - King)", "region": "Head & Face"},
    {"char": "ꯆ", "name": "Chil", "body_part": "Mouth / Lip", "ipa": "/tʃ/", "meaning": "Utterance of sacred words and songs", "example": "ꯆꯩꯊꯥꯔꯣꯜ (Cheitharol)", "region": "Head & Face"},
    {"char": "ꯇ", "name": "Til", "body_part": "Saliva", "ipa": "/t/", "meaning": "Life-giving fluid and sustenance", "example": "ꯇꯞꯇꯥ (Tapta)", "region": "Head & Face"},
    {"char": "ꯈ", "name": "Khou", "body_part": "Throat", "ipa": "/kʰ/", "meaning": "Voice and chant vibration", "example": "ꯈꯣꯡꯖꯣꯝ (Khongjom)", "region": "Throat & Chest"},
    {"char": "ꯉ", "name": "Ngou", "body_part": "Nape of Neck", "ipa": "/ŋ/", "meaning": "Support and steadfastness", "example": "ꯉꯥꯡꯂꯩ (Ngangna)", "region": "Throat & Chest"},
    {"char": "ꯊ", "name": "Thou", "body_part": "Chest / Breast", "ipa": "/tʰ/", "meaning": "Courage, valor, and deep breath", "example": "ꯊꯣꯏꯕꯤ (Thoibi)", "region": "Throat & Chest"},
    {"char": "ꯋ", "name": "Wai", "body_part": "Navel (Solar Plexus)", "ipa": "/w/", "meaning": "Umbilical connection to ancestral soil", "example": "ꯋꯥꯔꯤ (Wari - Story)", "region": "Torso & Spine"},
    {"char": "ꯌ", "name": "Yang", "body_part": "Spine / Backbone", "ipa": "/j/", "meaning": "Moral rectitude and tribal endurance", "example": "ꯌꯨꯝ (Yum - Home)", "region": "Torso & Spine"},
    {"char": "ꯍ", "name": "Huk", "body_part": "Armpit / Ribs", "ipa": "/h/", "meaning": "Protection of the internal organs", "example": "ꯍꯤꯌꯥꯡ (Hiyang)", "region": "Torso & Spine"},
    {"char": "ꯎ", "name": "Un", "body_part": "Skin", "ipa": "/u/", "meaning": "Armor against environmental elements", "example": "ꯎꯃꯪ (Umang - Sacred Forest)", "region": "Limbs & Surface"},
    {"char": "ꯏ", "name": "I", "body_part": "Blood", "ipa": "/i/", "meaning": "Hereditary lineage of the seven clans", "example": "ꯏꯃꯥ (Ima - Mother)", "region": "Internal & Spiritual"},
    {"char": "ꯐ", "name": "Pham", "body_part": "Seat / Pelvis", "ipa": "/pʰ/", "meaning": "Foundational stability and dignity", "example": "ꯐꯨꯡꯒꯥ (Phunga - Hearth)", "region": "Internal & Spiritual"},
    {"char": "ꯑ", "name": "Atiya", "body_part": "Crown / Sky (Aether)", "ipa": "/a/", "meaning": "Supreme vault of heaven and infinity", "example": "ꯑꯄꯣꯛꯄꯥ (Apokpa - Ancestor)", "region": "Internal & Spiritual"}
]

# Common vocabulary transliteration dictionary (English / Romanized -> Meetei Mayek & Bengali script)
TRANSLITERATION_LEXICON = {
    "kangleipak": {"mayek": "ꯀꯪꯂꯩꯄꯥꯛ", "bengali": "কাংলেইপাক", "ipa": "/kaŋ.ləi.pak/", "meaning": "Ancient name of Manipur (Dry Land / Resplendent Realm)"},
    "kangla": {"mayek": "ꯀꯪꯂꯥ", "bengali": "কাংলা", "ipa": "/kaŋ.la/", "meaning": "Ancient sacred citadel; dry elevated ground"},
    "meitei": {"mayek": "ꯃꯤꯇꯩ", "bengali": "মৈতৈ", "ipa": "/məi.təi/", "meaning": "The predominant indigenous ethnic group of Manipur"},
    "manipuri": {"mayek": "ꯃꯅꯤꯄꯨꯔꯤ", "bengali": "মণিপুরী", "ipa": "/ma.ni.pu.ri/", "meaning": "Language and people of Manipur"},
    "pakhangba": {"mayek": "ꯄꯥꯈꯪꯕꯥ", "bengali": "পাখংবা", "ipa": "/pa.kʰaŋ.ba/", "meaning": "Divine dragon-serpent ancestor & first historical king (33 CE)"},
    "ima keithel": {"mayek": "ꯏꯃꯥ ꯀꯩꯊꯦꯜ", "bengali": "ইমা কৈত্থেল", "ipa": "/i.ma kəi.tʰel/", "meaning": "The Mother's Market (Asia's largest all-women market)"},
    "sankirtana": {"mayek": "ꯁꯪꯀꯤꯔꯇꯟ", "bengali": "সংকীর্তন", "ipa": "/saŋ.kir.tan/", "meaning": "UNESCO-inscribed ritual song, drumming (Khol) and dancing"},
    "lai haraoba": {"mayek": "ꯂꯥꯏ ꯍꯔꯥꯎꯕꯥ", "bengali": "লাই হরাওবা", "ipa": "/lai ha.rau.ba/", "meaning": "Merrymaking of the Forest Gods (Primeval creation festival)"},
    "sagol kangjei": {"mayek": "ꯁꯒꯣꯜ ꯀꯪꯖꯩ", "bengali": "সগোল কাংজৈ", "ipa": "/sa.gol kaŋ.dʒəi/", "meaning": "Traditional Meitei horse-polo on Manipuri ponies"},
    "puya meithaba": {"mayek": "ꯄꯨꯌꯥ ꯃꯩ ꯊꯥꯕꯥ", "bengali": "পুয়া মৈ থাবা", "ipa": "/pu.ja məi tʰa.ba/", "meaning": "Historical burning of sacred Meitei manuscripts in 1729/1732"},
    "cheitharol kumbaba": {"mayek": "ꯆꯩꯊꯥꯔꯣꯜ ꯀꯨꯝꯕꯥꯕꯥ", "bengali": "চৈথারোল কুম্বাবা", "ipa": "/tʃəi.tʰa.rol kum.ba.ba/", "meaning": "Royal Court Chronicle of the Kings of Manipur"},
    "khamba thoibi": {"mayek": "ꯈꯝꯕ ꯊꯣꯏꯕꯤ", "bengali": "খম্বা থোইবী", "ipa": "/kʰam.ba tʰoi.bi/", "meaning": "Legendary romantic epic of Moirang"},
    "keibu keioiba": {"mayek": "ꯀꯩꯕꯨ ꯀꯩꯑꯣꯏꯕꯥ", "bengali": "কেইবু কেইওইবা", "ipa": "/kəi.bu kəi.oi.ba/", "meaning": "Mythological shapeshifting Tiger-Man"},
    "tapta": {"mayek": "ꯇꯞꯇꯥ", "bengali": "তপ্তা", "ipa": "/tap.ta/", "meaning": "Monsoon rain-drip monster in traditional Meitei folklore"},
    "salai taret": {"mayek": "ꯁꯂꯥꯏ ꯇꯔꯦꯠ", "bengali": "সালাই তরেত", "ipa": "/sa.lai ta.ret/", "meaning": "The Seven Ancestral Clans of the Meitei nation"},
    "nupi lan": {"mayek": "ꯅꯨꯄꯤ ꯂꯥꯟ", "bengali": "নুপী লান", "ipa": "/nu.pi lan/", "meaning": "The Great Women's Wars of 1904 and 1939"},
    "subika": {"mayek": "ꯁꯨꯕꯤꯀꯥ", "bengali": "সুধিকা", "ipa": "/su.bi.ka/", "meaning": "16th-century illustrated cosmological and astrological manuscript"},
    "chainarol": {"mayek": "ꯆꯥꯏꯅꯥꯔꯣꯜ", "bengali": "চাইনারোল", "ipa": "/tʃai.na.rol/", "meaning": "Ancient ethical code of gladiatorial duels and combat honor"},
    "sanaleibak": {"mayek": "ꯁꯅꯥꯂꯩꯕꯥꯛ", "bengali": "সানালৈবাক", "ipa": "/sa.na.ləi.bak/", "meaning": "Golden Land (Poetic honorific for Manipur)"}
}

def transliterate_text(query: str) -> Dict[str, Any]:
    """
    Translates or transliterates an input word into Meetei Mayek, Bengali script,
    and returns phonetic IPA and cultural meaning.
    """
    clean = query.lower().strip()
    if clean in TRANSLITERATION_LEXICON:
        res = TRANSLITERATION_LEXICON[clean].copy()
        res["found"] = True
        res["query"] = query
        return res
    
    # Substring / partial match
    for k, v in TRANSLITERATION_LEXICON.items():
        if k in clean or clean in k:
            res = v.copy()
            res["found"] = True
            res["query"] = query
            res["matched_key"] = k
            return res
            
    # Algorithmic phonetic transliteration fallback using letter mapping
    char_map = {
        "k": "ꯀ", "s": "ꯁ", "l": "ꯂ", "m": "ꯃ", "p": "ꯄ",
        "n": "ꯅ", "ch": "ꯆ", "t": "ꯇ", "kh": "ꯈ", "ng": "ꯉ",
        "th": "ꯊ", "w": "ꯋ", "y": "ꯌ", "h": "ꯍ", "u": "ꯎ",
        "i": "ꯏ", "ph": "ꯐ", "a": "ꯑ", "g": "ꯒ", "r": "ꯔ",
        "b": "ꯕ", "j": "ꯖ", "d": "ꯗ"
    }
    
    mayek_chars = []
    i = 0
    q_str = clean
    while i < len(q_str):
        if i + 1 < len(q_str) and q_str[i:i+2] in char_map:
            mayek_chars.append(char_map[q_str[i:i+2]])
            i += 2
        elif q_str[i] in char_map:
            mayek_chars.append(char_map[q_str[i]])
            i += 1
        elif q_str[i] == ' ':
            mayek_chars.append(' ')
            i += 1
        else:
            i += 1
            
    generated_mayek = "".join(mayek_chars) if mayek_chars else "ꯀꯪꯂꯩꯄꯥꯛ"
    return {
        "found": False,
        "query": query,
        "mayek": generated_mayek,
        "bengali": "স্বতঃস্ফূর্ত লিপি",
        "ipa": f"/{clean}/",
        "meaning": "Phonetically aligned candidate representation in Meetei Mayek script."
    }

# =============================================================================
# 3. ORAL FOLKLORE ARCHIVES ("FUNGA WARI & KHUNUNG ESHEI")
# =============================================================================
ORAL_FOLKLORE_STORIES: List[Dict[str, Any]] = [
    {
        "id": "story_01",
        "title": "Keibu Keioiba (The Tiger-Man of Meitei Lore)",
        "title_mayek": "ꯀꯩꯕꯨ ꯀꯩꯑꯣꯏꯕꯥ",
        "genre": "Mythological Legend / Shamanic Transformation",
        "teller": "Oja Tombi Singh (Imphal West Oral Circle)",
        "audio_path": "data/audio/elder_kangla_testimony.wav",
        "synopsis": (
            "Once a skilled sorcerer and priest named Kabui Keioiba, he possessed the arcane power to transform "
            "into a ferocious tiger at night. However, when his half-human, half-beast nature alienated him from both "
            "man and wild beasts, he roamed the dense forests between the valley and the hills. He kidnapped the maiden "
            "Thabaton, but her seven clever brothers rescued her using indigenous engineering tricks, burning down his lair."
        ),
        "mayek_snippet": "ꯀꯩꯕꯨ ꯀꯩꯑꯣꯏꯕꯥ ꯑꯁꯤ ꯃꯤ ꯑꯃꯁꯨꯡ ꯁꯥꯒꯤ ꯃꯔꯛꯇꯥ ꯂꯩꯕꯥ ꯊꯥꯏꯅꯒꯤ ꯋꯥꯔꯤ ꯑꯃꯅꯤ...",
        "translit_snippet": "Keibu Keioiba asi mee amasung sa-gi marakta leiba thainagi wari amani...",
        "cultural_moral": (
            "Human arrogance in exploiting forbidden knowledge leads to spiritual exile. The tale emphasizes respecting "
            "the boundary between the civilized settlement (Yumpham) and the wild forest sanctuary (Umang)."
        ),
        "kg_entity": "E028",
        "tags": ["Keibu Keioiba", "Thabaton", "Shapeshifter", "Tiger Cult", "Oral Legend"]
    },
    {
        "id": "story_02",
        "title": "Tapta (The Monsoon Hearth Monster)",
        "title_mayek": "ꯇꯞꯇꯥ",
        "genre": "Children's Fable / Comic Wisdom",
        "teller": "Ima Shanti Devi (Heingang Village)",
        "audio_path": "data/audio/tǝpta_story.wav",
        "synopsis": (
            "On a tempestuous monsoon night, a mother attempted to soothe her crying child. Outside, a prowling tiger and a thief "
            "both hid under the eaves. The mother tried to quiet the infant saying: 'Hush, an elephant is coming!' but the baby cried. "
            "'A tiger is coming!' but the baby still wept. Finally she sighed: 'Look, Tap-Ta is falling!' (referring to the leaky roof drip). "
            "Instantly the baby stopped. The listening tiger trembled, thinking 'Tapta' was an invincible monster greater than an elephant or tiger. "
            "When the thief accidentally jumped onto the tiger's back in the dark, sheer comic mayhem ensued."
        ),
        "mayek_snippet": "ꯃꯇꯝ ꯑꯃꯗꯥ ꯅꯣꯡ ꯀꯟꯅꯥ ꯆꯨꯕꯥ ꯑꯍꯤꯡ ꯑꯃꯗꯥ ꯇꯞꯇꯥ ꯀꯧꯕꯥ ꯑꯀꯤꯕꯥ ꯄꯣꯠꯁꯛ ꯑꯃꯥ ꯂꯩꯔꯝꯃꯤ...",
        "translit_snippet": "Matam amada nong kanna chuba ahing amada Tapta kouba akiba potsak ama leirammi...",
        "cultural_moral": (
            "Fear born of ignorance magnifies harmless shadows into terrifying demons. A lighthearted household fable beloved "
            "across generations of Meitei families huddled by the Phunga hearth."
        ),
        "kg_entity": "E028",
        "tags": ["Tapta", "Folk Tale", "Phunga Wari", "Oral Storytelling", "Monsoon Tale"]
    },
    {
        "id": "story_03",
        "title": "Khamba Thoibi of Moirang (The National Romantic Epic)",
        "title_mayek": "ꯈꯝꯕ ꯊꯣꯏꯕꯤ",
        "genre": "Heroic Epic / Intangible Performing Arts",
        "teller": "Guru M. Sanajaoba (Moirang Cultural Troupe)",
        "audio_path": "data/audio/lai_haraoba_jagoi_chant.wav",
        "synopsis": (
            "Set during the reign of King Chingkhu Telheiba of the Moirang kingdom, this monumental epic of 34,000 verses "
            "chronicles the trials of the impoverished orphan Khamba of the Khuman clan and Princess Thoibi. Khamba proves "
            "his royal worth by wrestling the dreaded man-eating tiger of Khoirentak and capturing the wild bull of the forest. "
            "Their sacred duet dance at the altar of Lord Thangjing remains the supreme spiritual model for Lai Haraoba dance today."
        ),
        "mayek_snippet": "ꯃꯣꯏꯔꯥꯡ ꯀꯪꯂꯩꯔꯣꯜꯒꯤ ꯈ꯭ꯕꯥꯏꯗꯒꯤ ꯆꯥꯎꯕꯥ ꯄꯨꯋꯥꯔꯤ ꯑꯃꯁꯨꯡ ꯅꯨꯡꯁꯤꯕꯒꯤ ꯋꯥꯔꯤ...",
        "translit_snippet": "Moirang Kangleirolgi khwaidagi chaoba puwari amasung nungsibagi wari...",
        "cultural_moral": (
            "True nobility is forged through courage, devotion to deity Thangjing, and steadfast love that triumphs over "
            "clan rivalry and court intrigue."
        ),
        "kg_entity": "E014",
        "tags": ["Khamba Thoibi", "Moirang", "Lord Thangjing", "Lai Haraoba Dance", "National Epic"]
    },
    {
        "id": "story_04",
        "title": "Pakhangba & the Seven Clans (Salai Taret)",
        "title_mayek": "ꯄꯥꯈꯪꯕꯥ ꯑꯃꯁꯨꯡ ꯁꯂꯥꯏ ꯇꯔꯦꯠ",
        "genre": "Cosmological Genesis / Clan Creation",
        "teller": "Maiba K. Ibochouba (Sanamahi Council)",
        "audio_path": "data/audio/sankirtana_khol_kartal.wav",
        "synopsis": (
            "In the beginning, supreme creator father Yaibirel Sidaba instructed his twin sons Sanamahi and Pakhangba "
            "to race around the cosmos, promising the earthly throne to the victor. While Sanamahi set out across the universe, "
            "Pakhangba obeyed his mother Leimarel Shidabi's counsel to circumambulate his father's throne seven times. "
            "Granted the sovereign coronation at Kangla, Pakhangba established the Ningthouja dynasty and unified the seven "
            "indigenous clans (Ningthouja, Angom, Luwang, Khuman, Moirang, Chenglei, Khaba-Nganba)."
        ),
        "mayek_snippet": "ꯇꯥꯏꯕꯪ ꯁꯦꯝꯕꯥ ꯃꯇꯃꯗꯥ ꯁꯂꯥꯏ ꯇꯔꯦꯠ ꯄꯨꯟꯁꯤꯟꯗꯨꯅꯥ ꯄꯥꯈꯪꯕꯥꯅꯥ ꯀꯪꯂꯥꯗꯥ ꯐꯝꯕꯥꯜ ꯀꯥꯈꯤ...",
        "translit_snippet": "Taibang semba matamda Salai Taret punsinduna Pakhangbana Kanglada fambal kakhi...",
        "cultural_moral": (
            "The cosmic duty of filial piety, maternal wisdom, and peaceful unity among the seven clans under shared ancestral laws."
        ),
        "kg_entity": "E001",
        "tags": ["Pakhangba", "Salai Taret", "Sanamahi", "Seven Clans", "Genesis Myth"]
    }
]

# =============================================================================
# 4. CHRONICLE OF KANGLEIPAK (HISTORICAL TIMELINE FROM 33 CE TO 2013)
# =============================================================================
HISTORICAL_TIMELINE: List[Dict[str, Any]] = [
    {
        "year": "33 CE",
        "year_display": "33 CE",
        "era": "Antiquity / Foundation",
        "title": "Ascension of Nongda Lairen Pakhangba",
        "title_mayek": "ꯅꯣꯡꯗꯥ ꯂꯥꯏꯔꯦꯟ ꯄꯥꯈꯪꯕꯥꯒꯤ ꯐꯝꯕꯥꯜ ꯀꯥꯕꯥ",
        "description": "Coronation of Pakhangba at Kangla, unifying the warring clans and establishing the continuous Ningthouja dynasty.",
        "divergence": "D01: Colonial British surveys argued Kangla dates only to 16th c. fortifications, whereas royal chronicles (Cheitharol Kumbaba) record continuous rule from 33 CE.",
        "divergence_grade": "hard",
        "category": "Monarchy & Statehood",
        "key_figures": ["Nongda Lairen Pakhangba", "Queen Laisana"]
    },
    {
        "year": "1467 - 1508 CE",
        "year_display": "1467 - 1508 CE",
        "era": "Medieval Renaissance",
        "title": "Reign of King Kiyamba & Lamangdong Vishnu Temple",
        "title_mayek": "ꯅꯤꯡꯊꯧ ꯀꯤꯌꯥꯝꯕꯥꯒꯤ ꯃꯇꯝ",
        "description": "Joint military victory with King Khekhomba of Pong (Upper Burma). First recorded brick Vishnu temple built in Lamangdong (Bishnupur); Chainarol martial code codified.",
        "divergence": "D07: Archival colonial records disputed whether King Kiyamba ruled over Shan territory or solely Manipur valley.",
        "divergence_grade": "hard",
        "category": "Monuments & Architecture",
        "key_figures": ["King Kiyamba", "King of Pong"]
    },
    {
        "year": "1709 - 1748 CE",
        "year_display": "1709 - 1748 CE",
        "era": "18th Century",
        "title": "Reign of King Pamheiba (Garib Niwaz)",
        "title_mayek": "ꯃꯤꯡꯁ꯭ꯔꯣꯜ ꯄꯥꯝꯍꯩꯕꯥ",
        "description": "Great military expansions into Burma (Ava). Adoption of Ramanandi / Gaudiya Vaishnavism under guru Shantidas Goswami, causing profound religious shifts.",
        "divergence": "D04: Disagreement on whether Puya Meithaba occurred in 1729 CE or 1732 CE.",
        "divergence_grade": "hard",
        "category": "Religious Transition",
        "key_figures": ["King Pamheiba", "Guru Shantidas Goswami"]
    },
    {
        "year": "1729 / 1732 CE",
        "year_display": "1729 or 1732 CE",
        "era": "18th Century",
        "title": "Puya Meithaba (The Burning of Sacred Puyas)",
        "title_mayek": "ꯄꯨꯌꯥ ꯃꯩ ꯊꯥꯕꯥ",
        "description": "Mass burning of traditional Meitei religious and historical manuscripts in front of Kangla Uttra, and replacement of Meetei Mayek with the Bengali script.",
        "divergence": "D04 & D04b: Community memory grieves it as a cataclysmic destruction of ancestral scripture; some British colonial sources downplayed the event as minor.",
        "divergence_grade": "hard",
        "category": "Manuscripts & Cultural Memory",
        "key_figures": ["King Pamheiba", "Maibas (Traditional Priests)"]
    },
    {
        "year": "1763 - 1798 CE",
        "year_display": "1763 - 1798 CE",
        "era": "Golden Age of Classical Arts",
        "title": "Rajarshi Bhagyachandra & Genesis of Raas Leela",
        "title_mayek": "ꯔꯥꯖꯔꯁꯤ ꯚꯥꯒ꯭ꯌꯆꯟꯗ꯭ꯔ",
        "description": "Composer-king Bhagyachandra sees a divine dream of Lord Krishna and designs the ethereal Kumil costume, creating the classical Manipuri Raas Leela dance and Nat Sankirtana.",
        "divergence": "A02: Both oral memory and British surveys agree Bhagyachandra created the Maha Raas at Langthabal in 1779.",
        "divergence_grade": "none",
        "category": "Performing Arts",
        "key_figures": ["Maharaja Bhagyachandra", "Princess Bimbabati"]
    },
    {
        "year": "1819 - 1826 CE",
        "year_display": "1819 - 1826 CE",
        "era": "National Trauma",
        "title": "Chahi Taret Khuntakpa (The Seven Years' Devastation)",
        "title_mayek": "ꯆꯍꯤ ꯇꯔꯦꯠ ꯈꯨꯟꯇꯥꯛꯄꯥ",
        "description": "Brutal Burmese invasion and occupation of Manipur. Two-thirds of the population perished or were forced into exile until Prince Gambhir Singh liberated the state with the Manipur Levy.",
        "divergence": "Historical censuses show population plummeted from ~600,000 to under 10,000 in the central valley.",
        "divergence_grade": "soft",
        "category": "War & Survival",
        "key_figures": ["Maharaja Gambhir Singh", "Nara Singh"]
    },
    {
        "year": "1891 CE",
        "year_display": "25 April 1891",
        "era": "Colonial Conflict",
        "title": "Battle of Khongjom & Fall of Kangla",
        "title_mayek": "ꯈꯣꯡꯖꯣꯝ ꯂꯥꯟ ꯑꯃꯁꯨꯡ ꯀꯪꯂꯥ ꯊꯨꯒꯥꯏꯕꯥ",
        "description": "Paona Brajabasi dies fighting the British at Kheba Hill. British troops occupy Kangla, dynamite the Kangla Sha statues, and establish colonial suzerainty.",
        "divergence": "D12 & D13: British records assert direct military annexation; Meitei legal and oral accounts emphasize the preserve of princely status.",
        "divergence_grade": "hard",
        "category": "Anti-Colonial Resistance",
        "key_figures": ["Major Paona Brajabasi", "Bir Tikendrajit", "General Collett"]
    },
    {
        "year": "1891 (13 August)",
        "year_display": "13 August 1891",
        "era": "Martyrs' Sacrifice",
        "title": "Execution of Bir Tikendrajit & Thangal General",
        "title_mayek": "ꯕꯤꯔ ꯇꯤꯀꯦꯟꯗ꯭ꯔꯖꯤꯠ ꯑꯃꯁꯨꯡ ꯊꯥꯡꯒꯥꯜ ꯖꯦꯅꯔꯦꯜ ꯐꯥꯁꯤ",
        "description": "Public execution of crown prince Tikendrajit and General Thangal at Pheida Pung (now Bir Tikendrajit Park). Commemorated annually as Patriots' Day.",
        "divergence": "A03: Unanimously documented across both colonial trial records and Meitei chronicles.",
        "divergence_grade": "none",
        "category": "National Martyrs",
        "key_figures": ["Bir Tikendrajit", "Thangal General"]
    },
    {
        "year": "1904 & 1939 CE",
        "year_display": "1904 & 1939 CE",
        "era": "Women's Liberation",
        "title": "The Great Nupi Lan (Women's Wars)",
        "title_mayek": "ꯅꯨꯄꯤ ꯂꯥꯟ",
        "description": "Heroic women of Ima Keithel mobilize en masse against British forced labor (1904) and artificial rice export famine (1939), reshaping modern political consciousness.",
        "divergence": "Colonial police reports treated it as a market food riot; oral archives celebrate it as the earliest organized feminist anti-imperial struggle in Asia.",
        "divergence_grade": "soft",
        "category": "Women's Movements",
        "key_figures": ["Ima Rajani", "Ima Keithel Mothers"]
    },
    {
        "year": "1980 CE",
        "year_display": "1980 CE",
        "era": "Script Revival",
        "title": "Official Reinstatement of Meetei Mayek",
        "title_mayek": "ꯃꯤꯇꯩ ꯃꯌꯦꯛ ꯑꯃꯨꯛ ꯍꯟꯅꯥ ꯍꯧꯗꯣꯛꯄꯥ",
        "description": "Government of Manipur officially adopts the 27-letter Meetei Mayek alphabet, initiating its gradual reintroduction in schools, signs, and official gazettes.",
        "divergence": "D05: Historic dispute between the 18-letter conservative school vs the official 27-letter standard.",
        "divergence_grade": "hard",
        "category": "Language Sovereignty",
        "key_figures": ["Meetei Mayek Experts Council", "MEELAL"]
    },
    {
        "year": "2004 (20 Nov)",
        "year_display": "20 Nov 2004",
        "era": "Contemporary Rebirth",
        "title": "Kangla Returned to the People of Manipur",
        "title_mayek": "ꯀꯪꯂꯥ ꯃꯤꯌꯥꯃꯗꯥ ꯈꯨꯠꯁꯤꯟꯅꯕꯥ",
        "description": "After 113 years of military occupation (British army 1891-1947, Assam Rifles 1947-2004), the sacred fort is formally handed back and declared a protected heritage sanctuary.",
        "divergence": "None: Celebrated as a landmark victory for regional cultural self-determination.",
        "divergence_grade": "none",
        "category": "Heritage Reclamation",
        "key_figures": ["People of Manipur", "Kangla Fort Board"]
    },
    {
        "year": "2013 CE",
        "year_display": "December 2013",
        "era": "Global Recognition",
        "title": "UNESCO Inscribes Manipuri Sankirtana",
        "title_mayek": "ꯌꯨꯅꯦꯁ꯭ꯀꯣꯅꯥ ꯁꯪꯀꯤꯔꯇꯟ  শকꯈꯪꯕꯥ",
        "description": "UNESCO inscribes 'Sankirtana: ritual singing, drumming and dancing of Manipur' on the Representative List of the Intangible Cultural Heritage of Humanity.",
        "divergence": "A02: Globally documented under UNESCO ICH Decision 8.COM 8.14.",
        "divergence_grade": "none",
        "category": "Global Heritage",
        "key_figures": ["Sankirtana Gurus", "UNESCO Committee"]
    }
]

# =============================================================================
# 5. GAMIFIED CULTURAL HERITAGE QUEST (QUIZ & TRIVIA CHALLENGE)
# =============================================================================
HERITAGE_QUIZ_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "q1",
        "tier": "Beginner",
        "question": "Which sport played worldwide originated in Manipur as 'Sagol Kangjei'?",
        "options": ["Cricket", "Modern Polo", "Field Hockey", "Badminton"],
        "answer_index": 1,
        "explanation": "Modern Polo originated from Sagol Kangjei. Guinness World Records recognizes Mapal Kangjeibung in Imphal as the oldest living polo ground in the world.",
        "entity_id": "E005"
    },
    {
        "id": "q2",
        "tier": "Beginner",
        "question": "What is unique about the famous 'Ima Keithel' market in Imphal?",
        "options": [
            "It is open only during the full moon",
            "It is operated exclusively by over 5,000 married women",
            "It only accepts barter trade",
            "It is floating on Loktak Lake"
        ],
        "answer_index": 1,
        "explanation": "Ima Keithel ('Mother's Market') is a 500-year-old commercial institution in Imphal run exclusively by women traders, holding immense economic and social power.",
        "entity_id": "E021"
    },
    {
        "id": "q3",
        "tier": "Beginner",
        "question": "In Meetei Mayek script philosophy, what anatomical part does the very first letter 'Kok' (ꯀ) represent?",
        "options": ["The Eye", "The Heart", "The Head", "The Throat"],
        "answer_index": 2,
        "explanation": "In the indigenous Iyek 27 system, 'Kok' (ꯀ) represents the Head, reflecting the seat of supreme consciousness in Meitei cosmological thought.",
        "entity_id": "E007"
    },
    {
        "id": "q4",
        "tier": "Intermediate",
        "question": "In which year was Sankirtana of Manipur inscribed on the UNESCO Intangible Cultural Heritage list?",
        "options": ["2008", "2010", "2013", "2018"],
        "answer_index": 2,
        "explanation": "Sankirtana ritual singing, drumming, and dancing was officially inscribed on the UNESCO Representative List of Intangible Cultural Heritage of Humanity in December 2013 (8.COM).",
        "entity_id": "E012"
    },
    {
        "id": "q5",
        "tier": "Intermediate",
        "question": "What mythological creature is depicted by the grand state emblem 'Kangla Sha'?",
        "options": [
            "A winged elephant",
            "A dragon-lion chimera",
            "A sacred peacock",
            "A golden deer"
        ],
        "answer_index": 1,
        "explanation": "The Kangla Sha is a mythical composite creature with the muscular body of a lion and the horned head of a dragon, acting as celestial guardians of the Ningthouja royalty.",
        "entity_id": "E033"
    },
    {
        "id": "q6",
        "tier": "Intermediate",
        "question": "Who composed the celestial Raas Leela dance and designed the Kumil bell-shaped skirt?",
        "options": ["Maharaja Gambhir Singh", "Rajarshi Bhagyachandra", "King Kiyamba", "Paona Brajabasi"],
        "answer_index": 1,
        "explanation": "Rajarshi Bhagyachandra (reigned 1763–1798) experienced a divine dream in which he envisioned the Maha Raas Leela and designed the unique cylindrical Kumil attire.",
        "entity_id": "E016"
    },
    {
        "id": "q7",
        "tier": "Divergence Master",
        "question": "Why does our Knowledge Graph flag the founding date of Kangla Fort as a 'Hard Divergence'?",
        "options": [
            "Because the fort was completely fictional",
            "Colonial British records claim 16th c. fortifications, while royal chronicles date rule from 33 CE",
            "Carbon dating gave conflicting results of 200 BCE and 5000 BCE",
            "The fort was moved across three different rivers"
        ],
        "answer_index": 1,
        "explanation": "Under the Divergence-Flag Protocol, case D01 highlights that colonial archival surveys cataloged Kangla only from 16th c. brickwork, whereas royal chronicles (Cheitharol Kumbaba) preserve continuous coronation history from King Pakhangba in 33 CE.",
        "entity_id": "E001"
    },
    {
        "id": "q8",
        "tier": "Divergence Master",
        "question": "What tragic historical event is known as 'Puya Meithaba'?",
        "options": [
            "The Great Flood of Imphal valley",
            "The burning of sacred ancestral Meitei manuscripts under King Pamheiba",
            "The collapse of the royal palace citadel",
            "The exile of the seven Meitei clans"
        ],
        "answer_index": 1,
        "explanation": "Puya Meithaba refers to the catastrophic burning of traditional religious, astrological, and philosophical manuscripts (Puyas) in 1729/1732 CE following the court's conversion to Ramanandi Vaishnavism.",
        "entity_id": "E009"
    },
    {
        "id": "q9",
        "tier": "Divergence Master",
        "question": "How many letters are in the modern officially recognized standard Meetei Mayek alphabet?",
        "options": ["18 letters", "27 letters", "35 letters", "42 letters"],
        "answer_index": 1,
        "explanation": "The official standard adopted by the Government of Manipur in 1980 consists of 27 letters (the traditional 18 letters plus 9 extended letters to represent loan phonemes).",
        "entity_id": "E007"
    }
]
