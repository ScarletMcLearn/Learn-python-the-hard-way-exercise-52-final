from nose.tools import *
from bin.map import *

def test_room():
    gold=Room("GoldRoom",
            """This room has gold you can grab""")
    assert_equal(gold.name,"GoldRoom")
    assert_equal(gold.paths,{})


def test_room_paths():
    center=Room("Center","Test room in the center.")
    north=Room("North","Test room in the north")
    south=Room("South","Test room in the south")
    end=Room('The End',"This is the end")

    center.add_paths({'north': north,'south':south,'*':end})
    assert_equal(center.go('north'),north)
    assert_equal(center.go('south'),south)


def test_map():
    start=Room("start","You can go west and down a hole.")
    west=Room("Trees","There are trees here, you can do east")
    down=Room("Dungeon","It's dark down there, you can go up")
    end=Room('The End',"This is the end")

    start.add_paths({'west':west,'down':down,'*':end})
    west.add_paths({'east':start})
    down.add_paths({'up':start})

    assert_equal(start.go('west'),west)
    assert_equal(start.go('west').go('east'),start)
    assert_equal(start.go('down').go('up'),start)

def test_gothon_game_map():
    #This is the worst code ever
    assert_equal(START.go('shoot!'),generic_death)
    assert_equal(START.go('dodge!'),generic_death)
    assert_equal(START.go("tell a joke"),laser_weapon_armory)
    assert_equal(laser_weapon_armory.go(laser_weapon_armory.rand),the_bridge)
    for x in range(10):
        assert_equal(laser_weapon_armory.go('*'),laser_weapon_armory)

    assert_equal(laser_weapon_armory.go('*'),generic_death)
    assert_equal(the_bridge.go('throw the bomb'),generic_death)
    assert_equal(the_bridge.go('slowly place the bomb'),escape_pod)
    assert_equal(escape_pod.go(escape_pod.rand),the_end_winner)
    assert_equal(escape_pod.go('*'),the_end_loser)

