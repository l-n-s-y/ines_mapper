import pygame



# TODO: Implement system palette

tile_scale = 2


palette = [(255,0,0),(0,255,0),(0,0,255),(255,255,0)]
def palette_lookup(p):
    return palette[p]


def render_tiles(tiles): # tiles -> 8x8x8192 array
    size = (512,512)
    screen = pygame.display.set_mode(size)

    x,y = 0,0
    for tile in tiles:

        l_y = 0
        for row in tile:
            l_x=8
            for pixel in row:
                pygame.draw.rect(screen, palette_lookup(pixel), (((x+l_x))*tile_scale,(y+l_y)*tile_scale,tile_scale,tile_scale))
                l_x -= 1
            l_y += 1
        x+=8
        if x >= 256: 
            y+=8
            x=0


    pygame.display.flip()

    # hang
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                exit()
