# version 330 core

uniform sampler2D image;

uniform int size=1;
uniform int separation=1;

in vec2 uvs;
out vec4 f_colour;

vec2 textureSize = textureSize(image, 0);

void main() {
    if (size <= 0) {
        return;
    }
    
    float count = 0.0;

    for (int i = -size ; i <= size ; ++i) {
        for (int j = -size ; j <= size ; ++j) {
            f_colour += texture(image, uvs + (vec2(i, j) * separation) / textureSize).rgba;

            count += 1.0;
        }
    }

    f_colour.rgb /= count;
}