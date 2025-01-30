# version 330 core

in sampler2D image;
in vec2 uvs;

out vec4 f_colour;

uniform float size=1;
uniform float separation=1;

vec2 textureSize = textureSize(image, 0);

void main() {
    if (size <= 0) {
        return;
    }
    
    float count = 0.0;

    for (int i = -size ; i <= size ; ++i) {
        for (int j = -size ; j <= size ; ++j) {
            f_colour += texture(image, uvs + (vec2(i, j) * separation) / textureSize).rgb;

            count += 1.0;
        }
    }

    f_colour.rgb /= count;
}