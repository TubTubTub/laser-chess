#version 330 core

in vec2 uvs;
out vec4 f_colour;

uniform sampler2D image;
uniform sampler2D blurredImage;
uniform float intensity;

void main() {             
    vec3 baseColour = texture(image, uvs).rgb;      
    vec3 bloomColor = texture(blurredImage, uvs).rgb;

    baseColour += bloomColor * intensity;
    f_colour = vec4(baseColour, 1.0);
}  