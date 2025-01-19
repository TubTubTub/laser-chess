#version 330 core

uniform sampler2D image;
uniform vec2 center;

in vec2 uvs;
out vec4 f_colour;

vec2 resolution = textureSize(image, 0);
float radius = 100.0; // radius in pixel

float getDistance(vec2 pixelCoord, vec2 playerCoord) {
    return distance(pixelCoord*resolution, playerCoord);
}

void main() {
    float distance = getDistance(uvs, center);
    float a = 0;
    float b = 1;

    // if (distance < radius)


    if (distance < 10000) {
        float factor = 1.0 / (pow((distance / 100), 2) + 1);
        f_colour = vec4(texture(image, uvs).rgb + factor, 1.0);
    }
    else {
        f_colour = vec4(texture(image, uvs).rgb, 1.0);
    }
}