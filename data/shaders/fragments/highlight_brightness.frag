# version 330 core

in vec2 uvs;
out vec4 f_colour;

uniform sampler2D image;
uniform float threshold;
uniform float intensity;

void main() {
    vec4 pixel = texture(image, uvs);
    // Dot product used to calculate brightness of a pixel from its RGB values
    // Values taken from https://en.wikipedia.org/wiki/Relative_luminance
    float brightness = dot(pixel.rgb, vec3(0.2126, 0.7152, 0.0722));
    float isBright = step(threshold, brightness);

    f_colour = vec4(vec3(pixel.rgb * intensity) * isBright, 1.0);
}