import thumby
import math
import random

class PhysObj:
    def __init__(self, sprite: thumby.Sprite):
        self.sprite = sprite

        self.loss = 0.8
        self.gravity = 0.5
        self.grounded = False

        # Velocity
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0 # + : right
        self.vy = 0.0 # + : down
        
    def impulse(self, x=0, y=0):
        self.vx += x
        self.vy += y
    
    # TODO: Use timedelta
    def updatePosition(self, t):
        self.vy += self.gravity
        
        self.x += self.vx
        self.y += self.vy
        self.vx *= self.loss
        self.vy *= self.loss

        # TODO: Add support for terrain.
        # TODO: Add an external collision handler?
        if self.y >= thumby.display.height - self.sprite.height:
            self.y = thumby.display.height - self.sprite.height
            self.vy = 0
            self.grounded = False

        # Separate updatesprite into separate function
        self.updateSprite(t)
    
    def updateSprite(self, t):
        self.sprite.x = int(round(self.x))
        self.sprite.y = int(round(self.y))
    
    def draw(self):
        thumby.display.drawSpriteWithMask(self.sprite, self.sprite)
        
        
# Inherit from PhysObj?
class Player(PhysObj):
    
    def __init__(self,
                 sprite: thumby.Sprite,     # Player sprite
                 ifSprite: thumby.Sprite,   # Item frame sprite
                 itemGenerators: list,      # List of item sprite generators
                 arrowSpriteDict: dict):    # Angle deg -> Arrow sprites
        
        super().__init__(sprite=sprite)
        self.ifSprite = ifSprite
        
        self.itemGenerators = itemGenerators
        self.item = None

        self.arrowSprites = arrowSpriteDict
        self.arrowDelta = 45    # Change in arrow angle
        self.arrowAng = 0       # Current arrow angle
        self.arrowOffset = 7    # Offset from player sprite
        self.arrow = self.arrowSprites[self.arrowAng]
        
        # {180: arrowSpriteL,
        #  135: arrowSpriteUL,
        #  90:  arrowSpriteU,
        #  45:  arrowSpriteUR,
        #  0:   arrowSpriteR}
        
        self.accel = 1.0 # Acceleration
        self.hp = 10
        self.grounded = False

    def roll_item(self):
        self.item = random.choice(self.itemGenerators)()
    
    # TODO: May not include in final version
    def jump(self):
        if self.grounded:
            self.impulse(x=0, y=-10)
            self.grounded = False
    
    # def updatePosition(self, t): # Add timedelta as well as time absolute
        
    #     self.vy += self.gravity
        
    #     self.x += self.vx
    #     self.y += self.vy
    #     self.vx *= self.loss
    #     self.vy *= self.loss

    #     # TODO: Add support for terrain.
    #     if self.y >= thumby.display.height - self.sprite.height:
    #         self.y = thumby.display.height - self.sprite.height
    #         self.vy = 0
    #         self.grounded = True

    def updateSprite(self, t):
        super().updateSprite(t)
        
        self.arrowAng = abs(180-((t%1800)//225)*45)
        self.arrow = self.arrowSprites[self.arrowAng]
        rad = math.radians(self.arrowAng)
        
        self.arrow.x = self.sprite.x + math.cos(rad) * self.arrowOffset
        self.arrow.y = self.sprite.y - math.sin(rad) * self.arrowOffset
    
    def draw(self, draw_item=True):
        super().draw()
        # thumby.display.drawSpriteWithMask(self.sprite, self.sprite)

        thumby.display.drawSpriteWithMask(self.arrow, self.arrow)
        
        # Move externally?
        if draw_item and self.item is not None:
            thumby.display.drawSprite(self.ifSprite)     # Item frame
            thumby.display.drawSprite(self.item)    # Current item
            
    def throw(self, force=10, dx=0, dy=0): # TODO: Allow override of force?
        t_item = PhysObj(self.item)
        self.item = None
        
        t_item.x = self.x
        t_item.y = self.y
        rad = math.radians(self.arrowAng)
        t_item.impulse(math.cos(rad)*force, -math.sin(rad)*force)
        
        return t_item
    
    def use(self):
        if self.item is not None:
            self.item.use()
            self.item = None
