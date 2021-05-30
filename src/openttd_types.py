#!/usr/bin/python3

"""
Various types used in the game. Most of these are not used in the save file parser.
"""

TILE_ZONES = [
    'normal',
    'desert',
    'rainforest'
]

TILE_BRIDGES = [
    'NONE',
    'NE',
    'SW'
]

TILE_TYPES = [
    'ground',
    'railway_tracks',
    'road',
    'town_building',
    'trees',
    'station_tiles',
    'water',
    'void',
    'industries',
    'tunnel_or_bridge',
    'objects'
]

WATER_TYPES = [
    'sea',
    'canal',
    'river',
    'invalid'
]

GROUND_TYPES = [
    'grass',
    'rough land',
    'rocks',
    'fields',
    'snow',
    'desert'
]

DEPOT_EXITS = [
    'NE',
    'SE',
    'SW',
    'NW'
]

SIGNAL_TYPES = [
    'normal signals',
    'pre-signals',
    'exit-signals',
    'combo-signals',
    'pbs signals',
    'no-entry signals'
]

SIGNAL_ERAS = [
    'semaphore signals',
    'light signals'
]

RAILWAY_GROUND_TYPES = [
    'bare land',
    'grass',
    'fence NW',
    'fence SE',
    'fence NW SE',
    'fence NE',
    'fence SW',
    'fence NE SW',
    'fence E',
    'fence W',
    'fence S',
    'fence N',
    'snow or desert',
    'fence and water',
    'foundation with snow'
]

TRACK_TYPES = [
    'conventional railway',
    'electrified railway',
    'monorail',
    'maglev'
]

INDUSTRY_TYPES = [
    # 00
    'COAL_MINE',
    'COAL_MINE',
    'COAL_MINE',
    'COAL_MINE',
    'COAL_MINE',
    'COAL_MINE',
    'COAL_MINE',

    'POWER_STATION',
    'POWER_STATION',
    'POWER_STATION',
    'POWER_STATION',

    'SAWMILL',
    'SAWMILL',
    'SAWMILL',
    'SAWMILL',
    'SAWMILL',

    # 10
    'FOREST',
    'FOREST',

    'OIL_REFINERY',
    'OIL_REFINERY',
    'OIL_REFINERY',
    'OIL_REFINERY',
    'OIL_REFINERY',
    'OIL_REFINERY',

    'OIL_RIG',
    'OIL_RIG',
    'OIL_RIG',
    'OIL_RIG',
    'OIL_RIG',

    'OIL_WELLS',
    'OIL_WELLS',
    'OIL_WELLS',
    # 20
    'OIL_WELLS',

    'FARM',
    'FARM',
    'FARM',
    'FARM',
    'FARM',
    'FARM',

    'FACTORY',
    'FACTORY',
    'FACTORY',
    'FACTORY',

    'PRINTING_WORKS',
    'PRINTING_WORKS',
    'PRINTING_WORKS',
    'PRINTING_WORKS',

    'COPPER_ORE_MINE',
    # 30
    'COPPER_ORE_MINE',
    'COPPER_ORE_MINE',
    'COPPER_ORE_MINE',
    'COPPER_ORE_MINE',

    'STEEL_MILL',
    'STEEL_MILL',
    'STEEL_MILL',
    'STEEL_MILL',
    'STEEL_MILL',
    'STEEL_MILL',

    'BANK',
    'BANK',

    'FOOD_PROCESSING_PLANT',
    'FOOD_PROCESSING_PLANT',
    'FOOD_PROCESSING_PLANT',
    'FOOD_PROCESSING_PLANT',

    # 40
    'PAPER_MILL',
    'PAPER_MILL',
    'PAPER_MILL',
    'PAPER_MILL',
    'PAPER_MILL',
    'PAPER_MILL',
    'PAPER_MILL',
    'PAPER_MILL',

    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    # 50
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',
    'GOLD_MINE',

    'BANK2',
    'BANK2',

    'DIAMOND_MINE',
    'DIAMOND_MINE',
    'DIAMOND_MINE',
    'DIAMOND_MINE',
    'DIAMOND_MINE',
    # 60
    'DIAMOND_MINE',
    'DIAMOND_MINE',
    'DIAMOND_MINE',
    'DIAMOND_MINE',

    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    # 70
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',
    'IRON_ORE_MINE',

    'FRUIT_PLANTATION',

    'RUBBER_PLANTATION',

    'WATER_SUPPLY',
    'WATER_SUPPLY',

    'WATER_TOWER',

    'FACTORY2',
    'FACTORY2',
    'FACTORY2',
    'FACTORY2',

    'LUMBER_MILL',
    'LUMBER_MILL',
    'LUMBER_MILL',
    # 80
    'LUMBER_MILL',

    'CANDYFLOSS_FOREST',
    'CANDYFLOSS_FOREST',

    'SWEET_FACTORY',
    'SWEET_FACTORY',
    'SWEET_FACTORY',
    'SWEET_FACTORY',

    'BATTERY_FARM',
    'BATTERY_FARM',

    'COLA_WELLS',

    'TOY_SHOP',
    'TOY_SHOP',
    'TOY_SHOP',
    'TOY_SHOP',

    'TOY_FACTORY',
    'TOY_FACTORY',
    # 90
    'TOY_FACTORY',
    'TOY_FACTORY',
    'TOY_FACTORY',
    'TOY_FACTORY',

    'PLASTIC_FOUNTAINS',
    'PLASTIC_FOUNTAINS',
    'PLASTIC_FOUNTAINS',
    'PLASTIC_FOUNTAINS',
    'PLASTIC_FOUNTAINS',
    'PLASTIC_FOUNTAINS',
    'PLASTIC_FOUNTAINS',
    'PLASTIC_FOUNTAINS',

    'FIZZY_DRINK_FACTORY',
    'FIZZY_DRINK_FACTORY',
    'FIZZY_DRINK_FACTORY',
    'FIZZY_DRINK_FACTORY',

    # A0
    'BUBBLE_GENERATOR',
    'BUBBLE_GENERATOR',
    'BUBBLE_GENERATOR',
    'BUBBLE_GENERATOR',

    'TOFFEE_QUARRY',
    'TOFFEE_QUARRY',
    'TOFFEE_QUARRY',

    'SUGAR_MINE',
    'SUGAR_MINE',
    'SUGAR_MINE',
    'SUGAR_MINE',
    'SUGAR_MINE',
    'SUGAR_MINE',
    'SUGAR_MINE',
    'SUGAR_MINE',
]

CHUNK_NAMES = [
    [
        b'GLOG'
    ],
    [
        b'MAPS',
        b'MAPT',
        b'MAPO',
        b'MAP2',
        b'M3LO',
        b'M3HI',
        b'MAP5',
        b'MAPE',
        b'MAP7',
        b'MAP8'
    ],
    [
        b'DATE',
        b'VIEW'
    ],
    [
        b'CHTS'
    ],
    [
        b'VEHS'
    ],
    [
        b'CHKP'
    ],
    [
        b'DEPT'
    ],
    [
        b'BKOR'
    ],
    [
        b'ORDR',
        b'ORDL'
    ],
    [
        b'INDY',
        b'IIDS',
        b'TIDS',
        b'IBLD',
        b'ITBL'
    ],
    [
        b'CAPY',
        b'PRIC',
        b'CAPR',
        b'ECMY'
    ],
    [
        b'SUBS'
    ],
    [
        b'CMDL',
        b'CMPU'
    ],
    [
        b'GOAL'
    ],
    [
        b'STPE',
        b'STPA'
    ],
    [
        b'EIDS',
        b'ENGN',
        b'ENGS'
    ],
    [
        b'HIDS',
        b'CITY'
    ],
    [
        b'SIGN'
    ],
    [
        b'STNS',
        b'STNN',
        b'ROAD'
    ],
    [
        b'PLYR'
    ],
    [
        b'AIPL'
    ],
    [
        b'GSTR',
        b'GSDT'
    ],
    [
        b'ANIT'
    ],
    [
        b'NGRF'
    ],
    [
        b'GRPS'
    ],
    [
        b'CAPA'
    ],
    [
        b'ERNW'
    ],
    [
        b'RAIL'
    ],
    [
        b'LGRP',
        b'LGRJ',
        b'LGRS'
    ],
    [
        b'ATID',
        b'APID'
    ],
    [
        b'OBID',
        b'OBJS'
    ],
    [
        b'PSAC'
    ]
]
