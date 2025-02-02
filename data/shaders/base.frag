#version 330 core

uniform sampler2D image;
uniform sampler2D background;

in vec2 uvs;
out vec4 f_colour;

void main() {
    vec4 colour = texture(image, uvs);

	if (colour.a == 1.0) {
		f_colour = colour;
	} else {
		f_colour = texture(background, uvs);
	}
}