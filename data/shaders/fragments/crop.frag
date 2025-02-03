#version 330 core

uniform sampler2D image;
uniform vec2 relativeSize;
uniform vec2 relativePos;

in vec2 uvs;
out vec4 f_colour;

void main() {
    vec2 sampleCoords = relativeSize.xy * uvs.xy + relativePos.xy;

    float withinBounds = step(0.0, sampleCoords.x) * step(sampleCoords.x, 1.0) * step(0.0, sampleCoords.y) * step(sampleCoords.y, 1.0);

    vec3 colour = texture(image, sampleCoords).rgb * withinBounds;
    colour.r += (1 - withinBounds);

    f_colour = vec4(colour, 1.0);
}