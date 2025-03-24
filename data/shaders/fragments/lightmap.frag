# version 330 core

#define PI 3.14159265

in vec2 uvs;
out vec4 f_colour;

uniform float softShadow;
uniform float resolution;
uniform float falloff;
uniform vec3 lightColour;
uniform vec2 angleClamp;
uniform sampler2D occlusionMap;
uniform sampler2D image;

vec3 normLightColour = lightColour / 255;
vec2 radiansClamp = angleClamp * (PI / 180);

float sample(vec2 coord, float r) {
	/*
	Sample from the 1D distance map.

	Returns:
		float: 1.0 if sampled radius is greater than the passed radius, 0.0 if not.
	*/
	return step(r, texture(image, coord).r);
}

void main() {
	// Cartesian to polar transformation
	// Range from [0, 1] -> [-1, 1]
	vec2 norm = uvs.xy * 2.0 - 1.0;
	float angle = atan(norm.y, norm.x);
	float r = length(norm);

	// The texture coordinates to sample our 1D lookup texture
	// Always 0.0 on y-axis, as the texture is 1D
	float x = (angle + PI) / (2.0 * PI); // Normalise angle to [0, 1]
	vec2 tc = vec2(x, 0.0);

	// Sample the 1D lookup texture to check if pixel is in light or in shadow
	// Gives us hard shadows
	// 1.0 -> in light, 0.0, -> in shadow
	float inLight = sample(tc, r);
	// Clamp angle so that only pixels within the range are in light
	inLight = inLight * step(angle, radiansClamp.y) * step(radiansClamp.x, angle);

	// Multiply the blur amount by the distance from the center
	// So that the blurring increases as distance increases
	float blur = (1.0 / resolution) * smoothstep(0.0, 0.1, r);

	// Use gaussian blur to apply blur effect
	float sum = 0.0;

	sum += sample(vec2(tc.x - blur * 4.0, tc.y), r) * 0.05;
	sum += sample(vec2(tc.x - blur * 3.0, tc.y), r) * 0.09;
	sum += sample(vec2(tc.x - blur * 2.0, tc.y), r) * 0.12;
	sum += sample(vec2(tc.x - blur * 1.0, tc.y), r) * 0.15;

	sum += inLight * 0.16;

	sum += sample(vec2(tc.x + blur * 1.0, tc.y), r) * 0.15;
	sum += sample(vec2(tc.x + blur * 2.0, tc.y), r) * 0.12;
	sum += sample(vec2(tc.x + blur * 3.0, tc.y), r) * 0.09;
	sum += sample(vec2(tc.x + blur * 4.0, tc.y), r) * 0.05;

	// Mix with the softShadow uniform to toggle degree of softShadows
	float finalLight = mix(inLight, sum, softShadow);

 	// Multiply the final light value with the distance, to give a radial falloff
	// Use as the alpha value, with the light colour being the RGB values
	f_colour = vec4(normLightColour, finalLight * smoothstep(1.0, falloff, r));
}