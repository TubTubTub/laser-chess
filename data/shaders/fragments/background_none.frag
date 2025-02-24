# version 330 core

in vec2 uvs;
out vec4 f_colour;

void main() {
    f_colour = vec4(vec3(0.0 + uvs.x * 0.001), 1.0);
}