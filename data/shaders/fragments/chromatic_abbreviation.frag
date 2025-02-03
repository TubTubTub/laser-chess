#version 330 core

in vec2 uvs;
out vec4 f_colour;

uniform sampler2D image;
uniform float time;

void main() {
	float amount = (1.0 + sin(time*6.0)) * 0.5;
	amount *= 1.0 + sin(time*16.0) * 0.5;
	amount *= 1.0 + sin(time*19.0) * 0.5;
	amount *= 1.0 + sin(time*27.0) * 0.5;
	amount = pow(amount, 3.0);

	amount *= 0.05;
	
    vec3 col;
    col.r = texture(image, vec2(uvs.x+amount,uvs.y) ).r;
    col.g = texture(image, uvs ).g;
    col.b = texture(image, vec2(uvs.x-amount,uvs.y) ).b;

	col *= (1.0 - amount * 0.5);
	
    f_colour = vec4(col,1.0);
}