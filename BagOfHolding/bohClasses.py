import thumby
import math
import random

# TODO: Collision:
#       Have an external collision handler which runs in the main loop?
#       Calls a collision method in each entity?
#       Standard sprites can have circular colliders?
#       Terrain can use rectangular colliders?

# Obj which tracks/modifies position and velocity
class PhysObj():
    
    def __init__(self,
                 x=0.0,
                 y=0.0,
                 momentum=0.8,
                 gravity=0.5):
        
        # Position
        self.x = x
        self.y = y
        
        # Velocity
        self.vx = 0.0   # + : right
        self.vy = 0.0   # + : down
        
        # Properties
        self.momentum = momentum
        self.gravity = gravity

    # Push in a direction
    def impulse(self, x=0, y=0):
        self.vx += x
        self.vy += y
    
    # TODO: Use timedelta?
    def updatePosition(self, t):
        self.vy += self.gravity
        
        self.x += self.vx
        self.y += self.vy
        self.vx *= self.momentum
        self.vy *= self.momentum


# Obj which tracks the camera position
class CameraObj(PhysObj):
    
    def __init__(self, tracked_obj: PhysObj, pref_x=36, pref_y=32):
        super().__init__(x=tracked_obj.x,
                         y=tracked_obj.y,
                         momentum=0.2,
                         gravity=0.0)
        
        # Obj to track (player)
        self.tracked_obj = tracked_obj
        
        # Preferred position of tracked object (~center of screen)
        self.pref_x = pref_x - tracked_obj.sprite.width/2
        self.pref_y = pref_y - tracked_obj.sprite.height/2
        
        # Damping factor when pulling towards preferred position
        self.damping = 0.3

        # Axial response to tracked obj velocity
        self.tracked_factor_x = 2.0
        self.tracked_factor_y = 0.3
        
        # self.max_dist = 10
        # self.accel = 2
        
    def updatePosition(self, t):
        
        # Vector between tracked obj and preferred obj position
        target_x = self.tracked_obj.x - self.pref_x
        target_y = self.tracked_obj.y - self.pref_y
        
        # Velocity to put tracked obj in preffered pos, with damping
        self.vx = (target_x - self.x) * self.damping
        self.vy = (target_y - self.y) * self.damping
        
        # Add tracked obj velocity to camera, for lookahead
        self.vx += self.tracked_obj.vx * self.tracked_factor_x
        self.vy += self.tracked_obj.vy * self.tracked_factor_y
        
        # self.x = self.x + (target_x - self.x)*self.follow_ratio
        # self.y = self.y + (target_y - self.y)*self.follow_ratio
        
        super().updatePosition(t)


# Obj which attaches a sprite to a PhysObj
class SpriteObj(PhysObj):
    
    entities = []
    
    @staticmethod
    def updateEntities(t):
        for entity in SpriteObj.entities:
            entity.updatePosition(t)
            
    @staticmethod
    def drawEntities(camera: CameraObj):
        for entity in SpriteObj.entities:
            entity.draw(camera)
    
    @staticmethod
    def cleanupEntities():
        SpriteObj.entities = [e for e in SpriteObj.entities if not e.cleanup]

    def __init__(self, 
                 sprite: thumby.Sprite,
                 x=0.0,
                 y=0.0,
                 momentum=0.8,
                 gravity=0.5,
                 isEntity=True):
        
        super().__init__(x=x, y=y, momentum=momentum, gravity=gravity)
        self.sprite = sprite
        
        self.grounded = False   # Has collided with ground # TODO: Remove/improve
        self.collision = True   # Can collide with objects
        self.cleanup = False    # Flag for removal from entity list
        
        # TODO: Consider a defined max number of entities.
        # TODO: Consider an entity dict
        
        # self.isEntity = isEntity
        if isEntity:
            SpriteObj.entities.append(self)
            
            
    # TODO: Use timedelta
    def updatePosition(self, t):
        super().updatePosition(t)

        # TODO: Add support for terrain.
        # TODO: Add an external collision handler?
        if self.y >= thumby.display.height - self.sprite.height:
            self.y = thumby.display.height - self.sprite.height
            self.vy = 0
            self.grounded = True
        
    def updateSprite(self, camera: CameraObj):
        self.sprite.x = int(round(self.x - camera.x))
        self.sprite.y = int(round(self.y - camera.y))
        
    def draw(self, camera: CameraObj):
        self.updateSprite(camera)
        thumby.display.drawSpriteWithMask(self.sprite, self.sprite)
        
    def collision(self, other):
        pass


# Obj which handles player input
class PlayerObj(SpriteObj):
    
    def __init__(self,
                 sprite: thumby.Sprite,     # Player sprite
                 ifSprite: thumby.Sprite,   # Item frame sprite
                 itemGenerators: list,      # List of item sprite generators
                 arrowSprites: dict,        # Angle deg -> Arrow sprites
                 x=0.0,
                 y=0.0,
                 momentum=0.8,
                 gravity=0.5):
        
        super().__init__(sprite=sprite,
                         x=x,
                         y=y,
                         momentum=momentum,
                         gravity=gravity)
        
        # Held item
        self.ifSprite = ifSprite
        self.itemGenerators = itemGenerators
        self.item = None
        
        # Directional arrow
        self.arrowAng = 0       # Current arrow angle
        self.arrowDelta = 45    # Change in arrow angle
        self.arrowOffset = 7    # Offset from player sprite
        self.arrowSprites = arrowSprites
        self.arrow = self.arrowSprites[self.arrowAng]
        
        # Properties
        self.hp = 10
        self.accel = 1.0
        self.jumpY = -5
        self.grounded = False
        
        # DEBUG
        self.reset_timer = 0
        
    def handle_input(self, entities: list, t: int):
        
        # DEBUG: Reload game if A is held.
        if thumby.buttonA.pressed():
            self.reset_timer += 1
            if self.reset_timer > 30:
                thumby.reset()
        else:
            self.reset_timer = 0
        
        # Get random item if A is pressed
        if thumby.buttonA.justPressed():
            self.roll_item()
            
        # Throw items if B is pressed
        if thumby.buttonB.justPressed() and self.item is not None:
            entities.append(self.throw())
            
        # Walking L/R
        horizontal = int(thumby.buttonR.pressed()) - int(thumby.buttonL.pressed())
        self.sprite.mirrorX = horizontal
        self.vx += horizontal * self.accel
        
        # Jump on U press
        # vertical = int(thumby.buttonD.pressed()) - int(thumby.buttonU.pressed())
        if thumby.buttonU.justPressed():
            self.jump()
        
    # Randomly generate a held item
    # TODO: Replace with a scrolling selection animation
    def roll_item(self):
        self.item = random.choice(self.itemGenerators)()
        
    # TODO: REMOVEME?
    def jump(self):
        if self.grounded:
            self.impulse(x=0, y=self.jumpY)
            self.grounded = False
        
    def updatePosition(self, t):
        super().updatePosition(t)
        
        # 1800 = millis per cycle
        # 225 = millis per increment
        # 45 = degrees per increment
        # 180 = shift to -180 ~ 180 range
        self.arrowAng = abs(180-((t%1800)//225)*45)
        
    def draw(self,
             camera: CameraObj,
             draw_item=True):
        super().draw(camera)
        
        # Update  # TODO: Can technically use 3 sprites and flip them.
        rad = math.radians(self.arrowAng)
        self.arrow = self.arrowSprites[self.arrowAng]
        self.arrow.x = self.sprite.x + math.cos(rad) * self.arrowOffset
        self.arrow.y = self.sprite.y - math.sin(rad) * self.arrowOffset
        
        # thumby.display.drawSpriteWithMask(self.sprite, self.sprite)
        thumby.display.drawSpriteWithMask(self.arrow, self.arrow)
        
        # Draw item if it exists
        if draw_item and self.item is not None:
            thumby.display.drawSprite(self.ifSprite)     # Item frame
            self.item.draw(camera)
            # thumby.display.drawSprite(self.item)    # Current item
        
    def throw(self, force=10, dx=0, dy=0): # TODO: Manually override with dx and dy? Alternate func?
        
        t_item = self.item
        self.item = None
        
        t_item.x = self.x
        t_item.y = self.y
        
        rad = math.radians(self.arrowAng)
        t_item.impulse(math.cos(rad)*force, -math.sin(rad)*force)
        
        t_item.on_throw()

        return t_item
        
    def use(self):
        if self.item is not None:
            self.item.use()
            self.item = None



# bobRate = 250 # Set arbitrary bob rate (higher is slower)
# bobRange = 5  # How many pixels to move the sprite up/down (-5px ~ 5px)

# # Calculate number of pixels to offset sprite for bob animation
# bobOffset = math.sin(t0 / bobRate) * bobRange

# # Center the sprite using screen and bitmap dimensions and apply bob offset
# player.sprite.x = int((thumby.display.width/2) - (8/2))
# player.sprite.y = int(round((thumby.display.height/2) - (8/2) + bobOffset))
