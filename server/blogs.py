from __future__ import annotations


#  Deferred translations!
def _(message):
    return message


BLOG_TAGS = {
    "Announcement": _("Announcement"),
    "Tournament": _("Tournament"),
    "Blog": _("Blog"),
}

del _

BLOGS = [
    {
        "_id": "S-chess_endings_2",
        "date": "2024-01-01",
        "image": "/images/hawk.jpg",
        "title": "S-Chess Endings 2",
        "subtitle": "The Hawk",
        "author": "yasser-seirawan",
        "tags": ["Blog"],
    },
    {
        "_id": "Merry_Christmas",
        "date": "2023-12-24",
        "image": "/images/board/ataxx.png",
        "title": "Merry Christmas!",
        "subtitle": "Ataxx",
        "author": "gbtami",
        "tags": ["Announcement"],
    },
    {
        "_id": "S-chess_endings_1",
        "date": "2023-12-01",
        "image": "/images/elephant.jpg",
        "title": "S-chess endings 1",
        "subtitle": "The Elephant",
        "author": "yasser-seirawan",
        "tags": ["Blog"],
    },
    {
        "_id": "Correspondence_Chess",
        "date": "2023-11-10",
        "image": "/images/Postcard-for-correspondence-chess.png",
        "title": "Correspondence Chess",
        "subtitle": "You have time now",
        "author": "gbtami",
        "tags": ["Announcement"],
    },
    {
        "_id": "S-chess_ramblings",
        "date": "2023-11-03",
        "image": "/images/Hawk-Elephant.jpeg",
        "title": "S-chess ramblings",
        "subtitle": "S-chess ramblings",
        "author": "catask",
        "tags": ["Blog"],
    },
    {
        "_id": "More_variants",
        "date": "2023-10-19",
        "image": "/images/Mansindam.jpg",
        "title": "Autumn Update",
        "subtitle": "A slew of new variants!",
        "author": "CouchTomato87",
        "tags": ["Announcement"],
    },
    {
        "_id": "Summer_Update",
        "date": "2023-06-06",
        "image": "/images/puzzles.jpg",
        "title": "Summer Update",
        "subtitle": "New features and bug fixes",
        "author": "CouchTomato87",
        "tags": ["Announcement"],
    },
    {
        "_id": "Spartan_Chess",
        "date": "2023-04-01",
        "image": "/images/spartan-kick.jpg",
        "title": "Madness? This. Is. SPARTAN CHESS!",
        "subtitle": "Spartan chess has arrived",
        "author": "CouchTomato87",
        "tags": ["Announcement"],
    },
    {
        "_id": "Duck_Chess",
        "date": "2022-12-26",
        "image": "/images/Duck.jpg",
        "title": "A Christmas Present From Pychess",
        "subtitle": "Duck chess has arrived",
        "author": "e-pluszak",
        "tags": ["Announcement"],
    },
    {
        "_id": "Ouk_Chaktrang_Friendship_Between_Four_Countries_Tournament",
        "date": "2022-12-01",
        "image": "/images/four-countries.jpg",
        "title": "Ouk Chaktrang Friendship Between Four Countries Tournament",
        "subtitle": "Promoting Our Southeast Asian Brethren",
        "author": "furumin999",
        "tags": ["Tournament"],
    },
    {
        "_id": "Crazyhouse960_Tournament_Spring_Invitational_2022",
        "date": "2022-10-02",
        "image": "/images/one-flew-over-the-cuckoos-nest.jpg",
        "title": "Crazyhouse960 Tournament Spring Invitational 2022",
        "subtitle": "Final Standings",
        "author": "visualdennis",
        "tags": ["Tournament"],
    },
    {
        "_id": "NNUE_Everywhere",
        "date": "2022-08-04",
        "image": "/images/Weights-nn-62ef826d1a6d.png",
        "title": "Fairy-Stockfish on PyChess",
        "subtitle": "NNUE Everywhere",
        "author": "gbtami",
        "tags": ["Announcement"],
    },
    {
        "_id": "Serving_a_New_Variant",
        "date": "2022-02-01",
        "image": "/images/ChessTennis.jpg",
        "title": "Tennis and chess",
        "subtitle": "Serving a New Variant",
        "author": "CouchTomato87",
        "tags": ["Announcement"],
    },
    {
        "_id": "Merry_Chakmas",
        "date": "2021-12-24",
        "image": "/images/QuetzalinTikal.png",
        "title": "Christmas gift from PyChess",
        "subtitle": "Merry Chak-mas!",
        "author": "CouchTomato87",
        "tags": ["Announcement"],
    },
    {
        "_id": "Cold_Winter",
        "date": "2021-12-21",
        "image": "/images/board/ChakArt.jpg",
        "title": "Summary of latest changes",
        "subtitle": "Cold winter",
        "author": "CouchTomato87",
        "tags": ["Announcement"],
    },
    {
        "_id": "Hot_Summer",
        "date": "2021-09-02",
        "image": "/images/AngryBirds.png",
        "title": "New variant, new engine and more",
        "subtitle": "Hot summer",
        "author": "CouchTomato87",
        "tags": ["Announcement"],
    },
    {
        "_id": "Empire_Chess_and_Orda_Mirror_Have_Arrived",
        "date": "2021-07-30",
        "image": "/images/Darth-Vader-Comic.jpg",
        "title": "Empire Chess and Orda Mirror Have Arrived!",
        "subtitle": "New variants",
        "author": "CouchTomato87",
        "tags": ["Announcement"],
    },
    {
        "_id": "Shinobi_Arrives_in_Time_For_the_Sakura_Blossoms",
        "date": "2021-04-21",
        "image": "/icons/shinobi.svg",
        "title": "Shinobi Arrives in Time For the Sakura Blossoms",
        "subtitle": "Shinobi Chess has arrived!",
        "author": "CouchTomato87",
        "tags": ["Announcement"],
    },
    {
        "_id": "The_Winner_Is_Tasshaq",
        "date": "2021-03-28",
        "image": "/icons/Dobutsu.svg",
        "title": "And the winner is Tasshaq",
        "subtitle": "Subjective report on 1st Dōbutsu Tournament",
        "author": "gbtami",
        "tags": ["Tournament"],
    },
    {
        "_id": "New_Weapons_Arrived",
        "date": "2021-03-03",
        "image": "/images/RS-24.jpg",
        "title": "Atomic chess and Atomic960 are here",
        "subtitle": "New Weapons Arrived",
        "author": "gbtami",
        "tags": ["Announcement"],
    },
    {
        "_id": "Short_History_Of_Pychess",
        "date": "2021-02-27",
        "image": "/images/TomatoPlasticSet.svg",
        "title": "And Now for Something Completely Different",
        "subtitle": "Short History Of Pychess",
        "author": "gbtami",
        "tags": ["Blog"],
},
    {
        "_id": "Dobutsu_Tournament",
        "date": "2021-02-04",
        "image": "/icons/Dobutsu.svg",
        "title": "PyChess tournament announcement",
        "subtitle": "The 1st Dōbutsu Tournament on PyChess",
        "author": "Tasshaq",
        "tags": ["Tournament"],
    },
]
