import thumby

# Make a sprite object using bytearray (a path to binary file from 'IMPORT SPRITE' is also valid)

# # #
# PLAYER: width: 8, height: 8
# playerBM = bytearray([38,211,151,117,63,117,146,200])
playerSprite = thumby.Sprite(8, 8, 
    bytearray([6,211,167,117,63,117,162,208]))


# TODO: Convert into a set of dots which travel smoothly.

#         .
#           .
# .   .   .   .
#           .
#         .

# ARROW: width: 7, height: 7
# Left
arrowSpriteL = thumby.Sprite(7, 7,
    bytearray([8,20,34,8,0,8,0]))
# Up left
arrowSpriteUL = thumby.Sprite(7, 7,
    bytearray([15,1,5,1,16,0,0]))
# Up
arrowSpriteU = thumby.Sprite(7, 7,
    bytearray([0,4,2,41,2,4,0]))
# Up right
arrowSpriteUR = thumby.Sprite(7, 7,
    bytearray([0,0,16,1,5,1,15]))
# Right
arrowSpriteR = thumby.Sprite(7, 7,
    bytearray([0,8,0,8,34,20,8]))

# Dict of angle -> Sprite
arrowSprites = {180: arrowSpriteL,
                135: arrowSpriteUL,
                90:  arrowSpriteU,
                45:  arrowSpriteUR,
                0:   arrowSpriteR}

# # #
# BAT: width: 8, height: 8
batSprite = thumby.Sprite(8, 8,
    bytearray([8,24,178,124,124,178,24,8]))


# EXPLOSION: width: 7, height: 7
def explosionSprite():
    return thumby.Sprite(7, 7, bytearray([0,0,8,0,20,0,0]) + bytearray([0,4,8,34,20,0,0]) + bytearray([0,20,8,66,36,10,0]) + bytearray([0,18,44,82,36,18,4]))


# # #
# ITEMFRAME: width: 10, height: 10
ifSprite = thumby.Sprite(10, 10, 
    # bytearray([0,0,0,0,0,0,0,0,0,255,2,2,2,2,2,2,2,2,2,3]))
    bytearray([1,1,1,1,1,1,1,1,1,255,0,0,0,0,0,0,0,0,0,3]))
ifSprite.y = thumby.display.height - ifSprite.height

# # # # #
# ITEMS #
# # # # #

# # #
# ITEMSWORD: width: 9, height: 9
# itemswordSprite = thumby.Sprite(9, 9, 
#     bytearray([0,144,80,32,216,28,14,6,0,0,0,0,0,0,0,0,0,0]))
# itemswordSprite.y = thumby.display.height - itemswordSprite.height

def itemswordSprite():
    i = thumby.Sprite(9, 9, bytearray([0,144,80,32,216,28,14,6,0,0,0,0,0,0,0,0,0,0]))
    i.y = thumby.display.height - i.height
    return i
    
# # BITMAP: width: 7, height: 7
# bitmap27 = bytearray([55,87,111,19,113,120,124])

# ITEMAXE: width: 9, height: 9
# itemaxeSprite = thumby.Sprite(9, 9,
#     bytearray([0,128,64,44,22,42,52,24,0,0,0,0,0,0,0,0,0,0]))
# itemaxeSprite.y = thumby.display.height - itemaxeSprite.height

def itemaxeSprite():
    i = thumby.Sprite(9, 9, bytearray([0,128,64,44,22,42,52,24,0,0,0,0,0,0,0,0,0,0]))
    i.y = thumby.display.height - i.height
    return i

# # BITMAP: width: 7, height: 7
# bitmap25 = bytearray([63,95,111,116,122,117,115])

# ITEMBOMB: width: 9, height: 9
# itembombSprite = thumby.Sprite(9, 9,
#     bytearray([0,48,72,188,254,121,49,6,0,0,0,0,0,0,0,0,0,0]))
# itembombSprite.y = thumby.display.height - itembombSprite.height

def itembombSprite():
    i = thumby.Sprite(9, 9, bytearray([0,48,72,188,254,121,49,6,0,0,0,0,0,0,0,0,0,0]))
    i.y = thumby.display.height - i.height
    return i
    
# # BITMAP: width: 7, height: 7
# bitmap28 = bytearray([24,36,94,126,61,25,2])    

# ITEMPOTION: width: 9, height: 9
# itempotionSprite = thumby.Sprite(9, 9,
#     # bytearray([0,48,120,250,254,186,72,48,0,0,0,0,0,0,0,0,0,0]))
#     bytearray([0,48,90,190,182,238,122,48,0,0,0,0,0,0,0,0,0,0]))
# itempotionSprite.y = thumby.display.height - itempotionSprite.height

def itempotionSprite():
    i = thumby.Sprite(9, 9, bytearray([0,48,90,190,182,238,122,48,0,0,0,0,0,0,0,0,0,0]))
    i.y = thumby.display.height - i.height
    return i
    
# # BITMAP: width: 7, height: 7
# bitmap30 = bytearray([24,60,125,127,93,36,24])

# ITEMROCK: width: 9, height: 9
# itemrockSprite = thumby.Sprite(9, 9,
#     bytearray([0,112,184,248,248,112,240,96,0,0,0,0,0,0,0,0,0,0]))
# itemrockSprite.y = thumby.display.height - itemrockSprite.height

def itemrockSprite():
    i = thumby.Sprite(9, 9, bytearray([0,112,184,248,248,112,240,96,0,0,0,0,0,0,0,0,0,0]))
    i.y = thumby.display.height - i.height
    return i
    
# # BITMAP: width: 7, height: 7
# bitmap31 = bytearray([56,116,126,126,62,58,28])

# ITEMBOOT: width: 8, height: 8
itembootSprite = thumby.Sprite(9, 9,
    bytearray([0,252,130,162,158,160,160,192,0,0,0,0,0,0,0,0,0,0]))
itembootSprite.y = thumby.display.height - itembootSprite.height

def itembootSprite():
    i = thumby.Sprite(9, 9, bytearray([0,252,130,162,158,160,160,192,0,0,0,0,0,0,0,0,0,0]))
    i.y = thumby.display.height - i.height
    return i
    
# TODO: Make item objects?
# def get_item():
    
itemSprites = [itemswordSprite,
               itemaxeSprite,
               itembombSprite,
               itempotionSprite,
               itemrockSprite,
               itembootSprite]



