# version 330 core

uniform sampler2D image;
uniform vec3 checkColour;

in vec2 uvs;
out vec4 f_colour;

void main() {
    vec4 pixel = texture(image, uvs);

    if (pixel.rgb == checkColour) {
        f_colour = vec4(checkColour, 1.0);
    } else {
        f_colour = vec4(vec3(0.0), 1.0);
    }
}