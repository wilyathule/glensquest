# Kyle's Quest Game Parser

from palmdb import PalmDB

class Sprite:
    def __init__(self, record):
        self.xsize = int.from_bytes(record[0x0:0x2], "big")
        self.ysize = int.from_bytes(record[0x2:0x4], "big")
        self.rowbytes = int.from_bytes(record[0x4:0x6], "big")
        self.image = list(record[0x10:0x10+self.ysize*self.rowbytes])

def kqstr(record):
    return str(record.partition(b'\0')[0], encoding="ascii")
    
def kqint(record):
    return int.from_bytes(record, "big")
    
def kqbool(record):
    return bool(kqint(record))
    
class Tile:
    def __init__(self, record):
        self.id = int(record[0])
        self.sprite = Sprite(record[1:49])
        self.walk = bool(record[49])

class KQGame:
    """Class for converting .pdb files"""

    def __init__(self, filename):
        gamePDB = PalmDB(filename)
        
        #########################
        # Record 0 - Level Info #
        #########################
        
        self.levelinfo = {}
        
        self.levelinfo['name'] = gamePDB.header["name"]
        
        # Intro Text
        self.levelinfo['intro'] = [None] * 10
        self.levelinfo['intro'][0] = kqstr(gamePDB.record[0][0x00:0x26])
        self.levelinfo['intro'][1] = kqstr(gamePDB.record[0][0x26:0x4c])
        self.levelinfo['intro'][2] = kqstr(gamePDB.record[0][0x4c:0x72])
        self.levelinfo['intro'][3] = kqstr(gamePDB.record[0][0x72:0x98])
        self.levelinfo['intro'][4] = kqstr(gamePDB.record[0][0x98:0xbe])
        self.levelinfo['intro'][5] = kqstr(gamePDB.record[0][0xbe:0xe4])
        self.levelinfo['intro'][6] = kqstr(gamePDB.record[0][0xe4:0x10a])
        self.levelinfo['intro'][7] = kqstr(gamePDB.record[0][0x10a:0x130])
        self.levelinfo['intro'][8] = kqstr(gamePDB.record[0][0x130:0x156])
        self.levelinfo['intro'][9] = kqstr(gamePDB.record[0][0x156:0x17c])

        # End Graphic
        self.levelinfo['end1graphic'] = Sprite(gamePDB.record[0][0x17c:0x2f4])

        # TODO Unknown content between 0x2f5 and 0x5e3
        
        # Ending Text
        self.levelinfo['ending1'] = [None] * 6
        self.levelinfo['ending2'] = [None] * 6
        self.levelinfo['ending3'] = [None] * 6

        self.levelinfo['ending1'][0] = kqstr(gamePDB.record[0][0x5e4:0x60a])
        self.levelinfo['ending1'][1] = kqstr(gamePDB.record[0][0x60a:0x630])
        self.levelinfo['ending1'][2] = kqstr(gamePDB.record[0][0x630:0x656])
        self.levelinfo['ending1'][3] = kqstr(gamePDB.record[0][0x656:0x67c])
        self.levelinfo['ending1'][4] = kqstr(gamePDB.record[0][0x67c:0x6a2])
        self.levelinfo['ending1'][5] = kqstr(gamePDB.record[0][0x6a2:0x6c8])
        
        self.levelinfo['ending2'][0] = kqstr(gamePDB.record[0][0x6c8:0x6ee])
        self.levelinfo['ending2'][1] = kqstr(gamePDB.record[0][0x6ee:0x714])
        self.levelinfo['ending2'][2] = kqstr(gamePDB.record[0][0x714:0x73a])
        self.levelinfo['ending2'][3] = kqstr(gamePDB.record[0][0x73a:0x760])
        self.levelinfo['ending2'][4] = kqstr(gamePDB.record[0][0x760:0x786])
        self.levelinfo['ending2'][5] = kqstr(gamePDB.record[0][0x786:0x7ac])

        self.levelinfo['ending3'][0] = kqstr(gamePDB.record[0][0x7ac:0x7d2])
        self.levelinfo['ending3'][1] = kqstr(gamePDB.record[0][0x7d2:0x7f8])
        self.levelinfo['ending3'][2] = kqstr(gamePDB.record[0][0x7f8:0x81e])
        self.levelinfo['ending3'][3] = kqstr(gamePDB.record[0][0x81e:0x844])
        self.levelinfo['ending3'][4] = kqstr(gamePDB.record[0][0x844:0x86a])
        self.levelinfo['ending3'][5] = kqstr(gamePDB.record[0][0x86a:0x88f])

        # Ending Flags 0x890 through 0xb89
        self.levelinfo['ending1flags'] = [None] * 256
        self.levelinfo['ending2flags'] = [None] * 256
        self.levelinfo['ending3flags'] = [None] * 256
        
        i = 0
        for j in gamePDB.record[0][0x890:0x990]:
            self.levelinfo['ending1flags'][i] = bool(j)
            i += 1
            
        i = 0
        for j in gamePDB.record[0][0x990:0xa90]:
            self.levelinfo['ending2flags'][i] = bool(j)
            i += 1
            
        i = 0
        for j in gamePDB.record[0][0xa90:0xb90]:
            self.levelinfo['ending3flags'][i] = bool(j)
            i += 1

        # Start X
        self.levelinfo['startx'] = int.from_bytes(gamePDB.record[0][0xb90:0xb92], "big")

        # Start Y
        self.levelinfo['starty'] = int.from_bytes(gamePDB.record[0][0xb92:0xb94], "big")
        
        # Start Map - 0xFFFF is the main map, 0x0000 through 0x00C7 are sub maps, and 0x00C8 and up are room maps
        self.levelinfo['startmap'] = int.from_bytes(gamePDB.record[0][0xb94:0xb96], "big")
        
        # Start Direction
        self.levelinfo['startdirection'] = kqint(gamePDB.record[0xb96:0xb98])
        
        # Start HP
        self.levelinfo['starthp'] = int.from_bytes(gamePDB.record[0][0xb98:0xb99], "big")
        self.levelinfo['starthpdice'] = int.from_bytes(gamePDB.record[0][0xb99:0xb9a], "big")
        
        # Start Agility
        self.levelinfo['startagi'] = int.from_bytes(gamePDB.record[0][0xb9a:0xb9b], "big")
        self.levelinfo['startagidice'] = int.from_bytes(gamePDB.record[0][0xb9b:0xb9c], "big")
        
        # Start Strength
        self.levelinfo['startstr'] = int.from_bytes(gamePDB.record[0][0xb9c:0xb9d], "big")
        self.levelinfo['startstrdice'] = int.from_bytes(gamePDB.record[0][0xb9d:0xb9e], "big")
        
        # Start Intelligence
        self.levelinfo['startint'] = int.from_bytes(gamePDB.record[0][0xb9e:0xb9f], "big")
        self.levelinfo['startintdice'] = int.from_bytes(gamePDB.record[0][0xb9f:0xba0], "big")
        
        # Start Money
        self.levelinfo['startmoney'] = int.from_bytes(gamePDB.record[0][0xba0:0xba1], "big")
        self.levelinfo['startmoneydice'] = int.from_bytes(gamePDB.record[0][0xba1:0xba2], "big")
        
        # Start Items
        self.levelinfo['startitem1'] = int.from_bytes(gamePDB.record[0][0xba2:0xba4], "big")
        self.levelinfo['startitem2'] = int.from_bytes(gamePDB.record[0][0xba4:0xba6], "big")
        
        # Custom Character Graphics
        self.levelinfo['customgraphics'] = kqbool(gamePDB.record[0][0xba6:0xba7])
        
        if self.levelinfo['customgraphics']:
            self.levelinfo['customgraphicsu1'] = Sprite(gamePDB.record[0][0xba7:0xbd7])
            self.levelinfo['customgraphicsu2'] = Sprite(gamePDB.record[0][0xbd7:0xc07])
            
            self.levelinfo['customgraphicsd1'] = Sprite(gamePDB.record[0][0xc07:0xc37])
            self.levelinfo['customgraphicsd2'] = Sprite(gamePDB.record[0][0xc37:0xc67])

            self.levelinfo['customgraphicsl1'] = Sprite(gamePDB.record[0][0xc67:0xc97])
            self.levelinfo['customgraphicsl2'] = Sprite(gamePDB.record[0][0xc97:0xcc7])

            self.levelinfo['customgraphicsr1'] = Sprite(gamePDB.record[0][0xcc7:0xcf7])
            self.levelinfo['customgraphicsr2'] = Sprite(gamePDB.record[0][0xcf7:0xd27])
            
        else:
            self.levelinfo['customgraphicsu1'] = Sprite(b'\x00\x10\x00\x10\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xa0\x03\xf0\x07\xf8\x07\xf8\x07\xf8\x07\xf8\x0f\xfc\x12\x12$\x024\x0b\\\rw\xfb\x04\xd8\x07\x88\x02\x88\x03p')
            self.levelinfo['customgraphicsu2'] = Sprite(b'\x00\x10\x00\x10\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xa0\x07\xe0\x0f\xf0\x0f\xf0\x0f\xf0\x0f\xf0\x1f\xf8$$ \x12h\x16X\x1do\xf7\r\x90\x08\xf0\x08\xa0\x07`')
            
            self.levelinfo['customgraphicsd1'] = Sprite(b'\x00\x10\x00\x10\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01P\x03\xf0\x07\xf8\x06\xd8\x05(\x05(\x0c\x0c\x12\x125\xe5\\\x05w\xfb\x04\xd8\x07\x88\x02\x88\x03p\x03\xf0')
            self.levelinfo['customgraphicsd2'] = Sprite(b'\x00\x10\x00\x10\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05@\x07\xe0\x0f\xf0\r\xb0\nP\nP\x18\x18$$S\xd6P\x1do\xf7\r\x90\x08\xf0\x08\xa0\x07`\x07\xe0')

            self.levelinfo['customgraphicsl1'] = Sprite(b"\x00\x10\x00\x10\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05@\x07\xf0\x1f\xf8\r\xf8\n\xb8\n8\x080\x04p\x07\x90\x05H\n(\x1ep'\xc8\x11\x18\x0fp\x01\xc0")
            self.levelinfo['customgraphicsl2'] = Sprite(b'\x00\x10\x00\x10\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xa0\x07\xf0\x1f\xf8\r\xf8\n\xb8\n8\x080\x04p\x07\x90\x0c\x08\x12H\x11\x88\x0f\xf0\x06\xf0\x04 \x07\xe0')

            self.levelinfo['customgraphicsr1'] = Sprite(b'\x00\x10\x00\x10\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xa0\x0f\xe0\x1f\xf8\x1f\xb0\x1dP\x1cP\x0c\x10\x0e \t\xe0\x12\xa0\x14P\x0ex\x13\xe4\x18\x88\x0e\xf0\x03\x80')
            self.levelinfo['customgraphicsr2'] = Sprite(b'\x00\x10\x00\x10\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05@\x0f\xe0\x1f\xf8\x1f\xb0\x1dP\x1cP\x0c\x10\x0e \t\xe0\x100\x12H\x11\x88\x0f\xf0\x0f`\x04 \x07\xe0')

        # TODO Unknown content between 0xd27 and 0xd37
        
        
        
        #######################
        # Record 2 - Monsters #
        #######################
        
        
        ###############################
        # Record 3 - Special Monsters #
        ###############################
        
        
        ####################
        # Record 4 - Tiles #
        ####################
        
        tilecount = int(len(gamePDB.record[4])/50)
        self.tiles = {}
        
        for k in range(1, tilecount):
            tile = Tile(gamePDB.record[4][((k-1)*50):(k*50)])
            self.tiles[tile.id] = tile
        
        
        ###############################
        # Record 5 - Map Changes      #
        ###############################
        
        
        #####################
        # Record 6 - Events #
        #####################
        
        
        ###############################
        # Record 7 - ??? - No discernible text #
        ###############################
        
        
        #############################
        # Record 8 - Talking Events #
        #############################
        
        
        ###############################
        # Record 9 - ??? - No discernible text #
        ###############################
        
        
        #########################
        # Record 10 - Questions #
        #########################
        
        
        #####################
        # Record 11 - Items #
        #####################
        
        
        ###########################
        # Record 12 - Warp Points #
        ###########################
        
        
        ######################
        # Record 13 - Guilds #
        ######################
        
        
        ######################
        # Record 14 - Spells #
        ######################
        
        
        #########################
        # Record 15 - Room Maps? #
        #########################
        
        
        #########################
        # Record 16 - Sub Maps? #
        #########################
        
        
        ########################
        # Record 17 - Main Map #
        ########################
        self.mainmap = [[None] * 100 for i in range(100)]
        
        x = 0
        y = 0
        for tileid in gamePDB.record[17]:
            self.mainmap[x][y] = int(tileid)
            if x < 99:
                x += 1
            else:
                y += 1
                x = 0
