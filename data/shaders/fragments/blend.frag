#version 330 core

uniform sampler2D image;
uniform sampler2D image2;
uniform vec2 relativeSize;
uniform vec2 image2Pos;

in vec2 uvs;
out vec4 f_colour;

void main() {
    vec3 colour = texture(image, uvs).rgb;

    vec2 image2Coords = vec2((uvs.x - image2Pos.x) / relativeSize.x, (uvs.y - image2Pos.y) / relativeSize.y);

    float withinBounds = step(image2Pos.x, uvs.x) * step(uvs.x, (image2Pos.x + relativeSize.x)) * step(image2Pos.y, uvs.y) * step(uvs.y, (image2Pos.y + relativeSize.y));

    f_colour = vec4(colour + (texture(image2, image2Coords).rgb * withinBounds), 1.0);
}