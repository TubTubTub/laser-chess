# version 330 core

uniform float wave_amp=1.0;
uniform float wave_size=4.0;
uniform float wave_time_mul=0.2;

uniform int total_phases=20;

uniform vec4 bottom_color=vec4(0.38, 0.04, 0.71, 1.0);
uniform vec4 top_color=vec4(0.15, 0.02, 0.49, 1.0);

uniform float time;

in vec2 uvs;
out vec4 f_colour;

#define PI 3.14159

float rand (float n) {
    return fract(sin(n) * 43758.5453123);
}
float noise (float p){
	float fl = floor(p);
    float fc = fract(p);
	return mix(rand(fl), rand(fl + 1.0), fc);
}
float fmod(float x, float y) {
	return x - floor(x / y) * y;
}
vec4 lerp(vec4 a, vec4 b, float w) {
	return a + w * (b - a);
}

void main() {
	float t = float(total_phases);
	float effective_wave_amp = min(wave_amp, 0.5 / t);
	float d = fmod(uvs.y, 1.0 / t);
	float i = floor(uvs.y * t);
	float vi = floor(uvs.y * t + t * effective_wave_amp);
	float s = effective_wave_amp * sin((uvs.x + time * max(1.0 / t, noise(vi)) * wave_time_mul * vi / t) * 2.0 * PI * wave_size);
	
	if (d < s) i--;
	if (d > s + 1.0 / t) i++;
	i = clamp(i, 0.0, t - 1.0);
	
	f_colour = lerp(top_color, bottom_color, i / (t - 1.0));
}