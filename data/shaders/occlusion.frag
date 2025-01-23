# version 330 core

uniform sampler2D image;
uniform vec3 checkColour;

vec3 normColour = checkColour / 255;

in vec2 uvs;
out vec4 f_colour;

void main() {
    vec4 pixel = texture(image, uvs);

    if (pixel.rgb == normColour) {
        f_colour = vec4(normColour, 1.0);
    } else {
        f_colour = vec4(0.0, 0.0, 0.0, 1.0);
    }
}