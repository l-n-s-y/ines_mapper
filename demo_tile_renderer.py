import pygame

# NES palette hex codes from: https://lospec.com/palette-list/nintendo-entertainment-system


# TODO: Implement system palette

tile_scale = 8
max_tile_scale = 32


mario = [(184,184,248),(248,56,0),(252,160,4),(172,124,0)] # mario
eyebleed = [(255,0,0),(0,255,0),(0,0,255),(255,255,0)] # eyebleed
palettes = [mario,eyebleed]
palette_index = 0

def palette_lookup(p):
    return palettes[palette_index][p]

def render_tiles(tiles): # tiles -> 8x8x8192 array
    global palette_index
    global tile_scale
    global max_tile_scale

    pygame.display.init()
    size = (1024,1024)
    screen = pygame.display.set_mode(size)

    vertical_index = 0
    while True:
        #pygame.time.Clock().tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    palette_index = 0
                if event.key == pygame.K_2:
                    palette_index = 1

            if event.type == pygame.MOUSEWHEEL:
                tile_scale += event.y
                tile_scale = min(max(tile_scale,0),max_tile_scale)

        screen.fill((0,0,0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            vertical_index = min(vertical_index+(size[0]//tile_scale)//8,len(tiles))
            #print("GOING DOWN")

        if keys[pygame.K_UP]:
            vertical_index = max(vertical_index-(size[0]//tile_scale)//8,0)
            #print("GOING UP")

        x,y = 0,0
        #for tile in tiles:
        for i in range(vertical_index,len(tiles)):
            tile = tiles[i]

            l_y = 0
            for row in tile:
                l_x=8
                for pixel in row:
                    #old_x=x
                    #old_y=y
                    #y=x
                    #x=old_y
                    pygame.draw.rect(screen, palette_lookup(pixel), (((x+l_x))*tile_scale,(y+l_y)*tile_scale,tile_scale,tile_scale))
                    l_x -= 1
                    #x=old_x
                    #y=old_y
                l_y += 1
            x+=8
            #if x >= 256: 
            if (x*tile_scale) >= size[0]:
                y+=8
                x=0

            #if i/32>=size[1]:
            if (y*tile_scale) >= size[1]:
                break


        pygame.display.flip()

        # hang

