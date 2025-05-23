def height_to_font_size(font, target_height):
    test_size = 1
    while True:
        glyph_metrics = font.get_metrics('j', size=test_size)
        descender = font.get_sized_descender(test_size)
        test_height = abs(glyph_metrics[0][3] - glyph_metrics[0][2]) - descender
        if test_height > target_height:
            return test_size - 1

        test_size += 1

def width_to_font_size(font, target_width):
    test_size = 1
    while True:
        glyph_metrics = font.get_metrics(' ', size=test_size)
        
        if (glyph_metrics[0][4] * 8) > target_width:
            return (test_size - 1)

        test_size += 1

def text_width_to_font_size(text, font, target_width):
    test_size = 1
    if len(text) == 0:
        # print('(text_width_to_font_size) Text must have length greater than 1!')
        text = " "
    
    while True:
        text_rect = font.get_rect(text, size=test_size)
        
        if text_rect.width > target_width:
            return (test_size - 1)

        test_size += 1

def text_height_to_font_size(text, font, target_height):
    test_size = 1

    if ('(' in text) or (')' in text):
        text = text.replace('(', 'j') # Pygame freetype thinks '(' or ')' is taller for some reason
        text = text.replace(')', 'j')

    if len(text) == 0:
        # print('(text_height_to_font_size) Text must have length greater than 1!')
        text = "j"
    
    while True:
        text_rect = font.get_rect(text, size=test_size)
        
        if text_rect.height > target_height:
            return (test_size - 1)

        test_size += 1

def get_font_height(font, font_size):
    glyph_metrics = font.get_metrics('j', size=font_size)
    descender = font.get_sized_descender(font_size)
    return abs(glyph_metrics[0][3] - glyph_metrics[0][2]) - descender