#version 330 core

in vec2 uvs;
out vec4 f_colour;

uniform sampler2D image;

uniform bool enabled;
uniform vec2 mouseFocusPoint;
uniform float intensity;

void main() {
	if (!enabled) {
		f_colour = texture(image, uvs);
		return;
	}

	float redOffset = 0.009 * intensity;
	float greenOffset = 0.006 * intensity;
	float blueOffset = -0.006 * intensity;

	vec2 texSize = textureSize(image, 0).xy;
	vec2 direction = uvs - mouseFocusPoint;

	f_colour = texture(image, uvs);

	f_colour.r = texture(image, uvs + (direction * vec2(redOffset))).r;
	f_colour.g = texture(image, uvs + (direction * vec2(greenOffset))).g;
	f_colour.b = texture(image, uvs + (direction * vec2(blueOffset))).b;
}