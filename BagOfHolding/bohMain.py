import time
import thumby

from bohClasses import PlayerObj, CameraObj

# TODO: Rename itemsprites
from bohSprites import playerSprite, ifSprite, itemSprites, arrowSprites

from bohItems import all_items

from bohSprites import batSprite

def main():
    
    player = PlayerObj(sprite=playerSprite,
                       ifSprite=ifSprite,
                       itemGenerators=all_items,
                       arrowSprites=arrowSprites)

    camera = CameraObj(tracked_obj=player)

    # Could make entities a static class property?
    #   Would allow for a 'global' entity list.
    #   Would also allow for entities to be added to the list in their constructor.
    #   Would also allow for entities to be removed from the list in their destructor.
    #   Seems necessary for entities to check collisions.
    entities = []
    
    # # #
    # MAIN LOOP
    while(True):
        t0 = time.ticks_ms()   # Get time (ms)

        # Input acts upon the player
        player.handle_input(entities, t=t0)
        
        # Update all entity positions
        for entity in entities:
            entity.updatePosition(t0)
        player.updatePosition(t0)
        camera.updatePosition(t0)
        
        # Remove dead entities
        entities = [e for e in entities if not e.cleanup]
        
        # TODO: Check for collisions?
        #       Could also do this in the updatePosition() method of each entity?
        
        # Draw current frame.
        thumby.display.fill(0)
        for entity in entities:
            entity.draw(camera=camera)
        player.draw(camera=camera)
        
        thumby.display.update()
        
        # Consider updating camera after all other updates, adding 1 frame delay

        