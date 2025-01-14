#version 330 core

in vec2 uvs;

out vec4 f_colour;

uniform sampler2D screenTexture;

uniform bool horizontal = 1;
uniform float weight[5] = float[] (0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);

void main() {
    vec2 tex_offset = 1.0 / textureSize(screenTexture, 0); // gets size of single texel
    vec3 result = texture(screenTexture, uvs).rgb * weight[0]; // current fragment's contribution

    if (horizontal) {
        for (int i = 1; i < 5; ++i) {
            result += texture(screenTexture, uvs + vec2(tex_offset.x * i, 0.0)).rgb * weight[i];
            result += texture(screenTexture, uvs - vec2(tex_offset.x * i, 0.0)).rgb * weight[i];
        }
    }
    else {
        for (int i = 1; i < 5; ++i) {
            result += texture(screenTexture, uvs + vec2(0.0, tex_offset.y * i)).rgb * weight[i];
            result += texture(screenTexture, uvs - vec2(0.0, tex_offset.y * i)).rgb * weight[i];
        }
    }
    f_colour = vec4(result, 1.0);
}