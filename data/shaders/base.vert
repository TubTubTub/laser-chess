#version 330 core

in vec2 vert;
in vec2 texCoords;
out vec2 uvs;

void main() {
    uvs = texCoords;
    gl_Position = vec4(vert, 0.0, 1.0);
}