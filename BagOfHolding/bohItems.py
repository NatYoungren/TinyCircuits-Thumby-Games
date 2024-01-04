import thumby
import time
import random

import bohSprites
from bohClasses import SpriteObj

class ItemObj(SpriteObj):
        
    def __init__(self,
                 sprite: thumby.Sprite,
                 throw_speed=10.0,
                 lifespan=5000, # Millis
                 x=0,
                 y=0,
                 momentum=0.8,
                 gravity=0.5,
                 held=True):
        
        super().__init__(sprite=sprite,
                         x=x,
                         y=y,
                         momentum=momentum,
                         gravity=gravity)

        self.throw_speed = throw_speed
        self.lifespan = lifespan
        self.held = held # FIXME: This could be the same as birth=None.
        self.birth = None # time.ticks_ms() # NOTE: Currently set in on_throw.
    
    def updatePosition(self, t):
        super().updatePosition(t)
        
        if not self.held and t - self.birth > self.lifespan:
            self.on_timeout()
        
    def updateSprite(self, camera):
        if self.held:
            self.sprite.y = thumby.display.height - self.sprite.height
            self.sprite.x = 0
        else:
            super().updateSprite(camera)
    
    def on_collision(self, other):
        pass
    
    def on_throw(self):
        self.birth = time.ticks_ms()
        self.held = False
    
    def on_use(self):
        pass
    
    # def on_pickup(self):
    #     pass
    
    # TODO: Remove from entities on destroy?
    #       Add a 'destroyed' tag to entities, and cull them from the list.
    #       This would allow for a 'destroyed' animation.
    
    def on_timeout(self):
        pass


class BombItemObj(ItemObj):
        
    def __init__(self,
                #  sprite: thumby.Sprite,
                 throw_speed=6.0,
                 lifespan=3000,
                 x=0,
                 y=0,
                 momentum=0.8,
                 gravity=0.5):
        
        super().__init__(sprite=bohSprites.itembombSprite(),
                            throw_speed=throw_speed,
                            lifespan=lifespan,
                            x=x,
                            y=y,
                            momentum=momentum,
                            gravity=gravity)
        
        self.launch_speed = 8.0
        self.exploded = False
    
    def updatePosition(self, t):
        super().updatePosition(t)
        
        if t - self.birth > self.lifespan:
            self.on_timeout()
            
        if self.exploded: # Randomly set state of explosion sprite
            self.sprite.setFrame(t%2)
            r = random.randint(0, 3)
            self.sprite.mirrorX = r // 2
            self.sprite.mirrorY = r % 2
    
    def on_collision(self, other):
        print(f'Bomb collided with {other}!')
        
        # if not self.exploded:
        #     self.exploded = True
        #     self.sprite = thumby.Sprite(8, 8,
        #         bytearray([0,0,0,0,0,0,0,0]))
        #     self.birth = time.ticks_ms()
    
    def on_timeout(self):
        if not self.exploded:
            print('Bomb exploded!')
            self.sprite = bohSprites.explosionSprite()
            self.lifespan += 2000
            self.collision = False
            self.exploded = True
        else:
            print('Bomb removed!')
            self.cleanup = True

        
all_items = [BombItemObj]