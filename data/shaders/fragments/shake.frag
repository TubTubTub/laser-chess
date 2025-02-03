#version 330 core

uniform sampler2D image;
uniform vec2 displacement;

in vec2 uvs;
out vec4 f_colour;

void main() {
    f_colour = vec4(texture(image, uvs + displacement).rgb, 1.0);
}