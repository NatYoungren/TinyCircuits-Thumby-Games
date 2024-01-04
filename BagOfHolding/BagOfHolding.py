# Copyright © 2023 Nathaniel Youngren <natahyoungren@gmain.com>
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# See https://github.com/___/____ for full source repository


#       add item throwing
#       add directional arrow
#       camera lock on player
#       reset w/ button hold
#       item subclasses?
#       item usage (bomb jump)
#           better explosion animation
# TODO: 2 more items
#           potion
#               break on collision, heal on use
#           sword/axe
#               damage on collision, dash attack on use
#               'in-use' sprite locked to player
#       item scroll-select (rummaging)
#           Slows down movement
#           Select item w/ tap OR *hold to rummage*
#       enemy subclass
#           enemy behavior
#       bigger explosion on bomb!
#       collision
#           terrain
#       greyscale integration?



if __name__ == "__main__":
    from sys import path
    path.append("/Games/BagOfHolding")
    
    import thumby
    thumby.display.setFPS(30)
    
    from bohMain import main
    main()
