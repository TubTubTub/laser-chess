#version 330 core

uniform sampler2D image;

in vec2 uvs;
out vec4 f_colour;

void main() {
    f_colour = vec4(texture(screenTexture, uvs).rgb, 1.0);
}