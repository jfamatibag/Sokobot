from collections import deque

class SokoBot:
    def solveSokobanPuzzle(self, width, height, mapData, itemsData):
        walls = set()
        goals = set()
        empty_floors = set()
        initial_boxes = set()
        initial_player = None

        for y, row in enumerate(mapData):
            for x, tile in enumerate(row):
                if tile == "#":
                    walls.add((y, x))
                elif tile == ".":
                    goals.add((y, x))
                else:
                    empty_floors.add((y,x))
                
        for y, row in enumerate(itemsData):
            for x, tile in enumerate(row):
                if tile == "$":
                    initial_boxes.add((y, x))
                elif tile == "@":
                    initial_player = (y, x)

        if not initial_player or not goals:
            return None

        # print(walls)
        # print(goals)
        # print(boxes)
        # print(player)

        directions = {
            "u": (-1, 0),
            "d": (1, 0),
            "l": (0, -1),
            "r": (0, 1)
        }

        dead_tiles = set()
    
        for (y,x) in empty_floors:
            if (y,x) in goals:
                continue
                    
            wall_up = (y - 1, x) in walls
            wall_down = (y + 1, x) in walls
            wall_left = (y, x - 1) in walls
            wall_right = (y, x + 1) in walls
                
            if (wall_up and wall_left) or (wall_up and wall_right) or \
            (wall_down and wall_left) or (wall_down and wall_right):
                dead_tiles.add((y,x))

        
        for cy, cx in list(dead_tiles):
            for direction in [-1, 1]: 
                step = 1
                line_coords = []
                while True:
                    nx = cx + (direction * step)
                    target = (cy, nx)
                    if target in walls:
                        break
                    if target in goals:
                        line_coords = []
                        break
                    
                    has_wall = ((cy - 1, nx) in walls) or ((cy + 1, nx) in walls)
                    if not has_wall:
                        line_coords = []
                        break
                        
                    if target in dead_tiles:
                        for lc in line_coords:
                            dead_tiles.add(lc)
                        break
                        
                    line_coords.append(target)
                    step += 1
                    
            for direction in [-1, 1]: 
                step = 1
                line_coords = []
                while True:
                    ny = cy + (direction * step)
                    target = (ny, cx)
                    if target in walls:
                        break
                    if target in goals:
                        line_coords = []
                        break
                        
                    has_wall = ((ny, cx - 1) in walls) or ((ny, cx + 1) in walls)
                    if not has_wall:
                        line_coords = []
                        break
                        
                    if target in dead_tiles:
                        for lc in line_coords:
                            dead_tiles.add(lc)
                        break
                        
                    line_coords.append(target)
                    step += 1

        def is_deadlock(box_coord, boxes_set):
            return box_coord in dead_tiles

        start_state = (initial_player, tuple(sorted(initial_boxes)))
        queue = deque([(start_state, [])])
        visited = {start_state}

        while queue:
            (current_player, current_boxes_tuple), path = queue.popleft()
            current_boxes_set = set(current_boxes_tuple)

            if current_boxes_set == goals:
                return path

            player_y, player_x = current_player  
            # valid_moves = []
            # valid_pushes = []

            for direction_name, (dy, dx) in directions.items():
                next_y = player_y + dy
                next_x = player_x + dx
                next_tile = (next_y, next_x)
                
                if next_tile in walls:
                    continue 
                    
                if next_tile in current_boxes_set:
                    behind_box_y = next_y + dy
                    behind_box_x = next_x + dx
                    behind_box_tile = (behind_box_y, behind_box_x)

                    if behind_box_tile not in walls and behind_box_tile not in current_boxes_set:
                        new_boxes_set = current_boxes_set.copy()
                        new_boxes_set.remove(next_tile)
                        new_boxes_set.add(behind_box_tile)
                        
                        if is_deadlock(behind_box_tile, new_boxes_set):
                            continue
                            
                        next_state = (next_tile, tuple(sorted(new_boxes_set)))
                        
                        if next_state not in visited:
                            visited.add(next_state)
                            queue.append((next_state, path + [direction_name]))

                else:
                    next_state = (next_tile, current_boxes_tuple)
                    
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append((next_state, path + [direction_name]))

        return None