TILE_DIMENSIONS = [8,8]

import demo_tile_renderer

class chr_parser:
    def __init__(self):
        #self.tiles = [[0 for x in TILE_DIMENSIONS[0]] for y in TILE_DIMENSIONS[1]]
        pass


    def parse_tiles(self,chr_rom):
        # tiles are split into 16 byte chunks
        
        tiles = [] # 8192x8x8 multidimensional array
        for i in range(0,len(chr_rom)-8,8):
            tile = []

            # iterate rows
            for j in range(0,8):
                row = []

                plane_0_byte = chr_rom[i+j]     # LSB
                plane_1_byte = chr_rom[(i+j)+8] # MSB
                #print("PLANE BYTES: ",bin(plane_0_byte),bin(plane_1_byte))

                # iterate pixels
                for h in range(0,8):

                    p0_bit = (plane_0_byte&(0b1<<h))>>h
                    p1_bit = (plane_1_byte&(0b1<<h))>>h
                    #print("PLANE BITS: ",p0_bit,p1_bit)

                    pixel = ((p0_bit) | (p1_bit<<1)) & 0b11
                    #print("TOTAL: ",bin(plane_0_byte&0b1<<h),bin(plane_1_byte&0b1<<h),p0_bit,p1_bit,pixel)


                    row.append(pixel)
                
                tile.append(row)


            tiles.append(tile)
        self.tiles = tiles

        demo_tile_renderer.render_tiles(self.tiles)
