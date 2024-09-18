def coords_to_screen_pos(coords, anchor_position, square_size):
    x = coords[0] * square_size + anchor_position[0]
    y = (7 - coords[1]) * square_size + anchor_position[1]

    return (x, y)