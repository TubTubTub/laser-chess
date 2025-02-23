# version 330 core

in vec2 uvs;
out vec4 f_colour;

uniform sampler2D image;
uniform vec3 checkColour;

void main() {
    vec4 pixel = texture(image, uvs);

    // If pixel is occluding colour, set pixel to white
    if (pixel.rgb == checkColour) {
        f_colour = vec4(1.0, 1.0, 1.0, 1.0);
    // Else, set pixel to black
    } else {
        f_colour = vec4(vec3(0.0), 1.0);
    }
}