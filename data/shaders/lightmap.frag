# version 330 core

#define PI 3.14159265

//inputs from vertex shader
in vec2 uvs;
out vec4 f_colour;

//uniform values
uniform sampler2D image;
uniform sampler2D shadowMap;
uniform vec2 resolution;

//sample from the 1D distance map
float sample(vec2 coord, float r) {
	return step(r, texture(shadowMap, coord).r); // returns 1.0 if 2nd parameter greater than 1st, 0.0 if not
}

void main() {
	//rectangular to polar
	vec2 norm = uvs.xy * 2.0 - 1.0; // [0, 1] -> [-1, 1]
	float angle = atan(norm.y, norm.x);
	float r = length(norm);	
	float coord = (angle + PI) / (2.0 * PI); // uvs -> [0, 1]
	
	//the tex coord to sample our 1D lookup texture	
	//always 0.0 on y axis
	vec2 tc = vec2(coord, 0.0);
	
	//the center tex coord, which gives us hard shadows
	float center = sample(tc, r); // center = 1.0 -> in light, center = 0.0, -> in shadow
	
	//we multiply the blur amount by our distance from center
	//this leads to more blurriness as the shadow "fades away"
    // straight to cuved edges
	float blur = (1.0 / resolution.x) * smoothstep(0.0, 0.1, r); 
	
	//now we use a simple gaussian blur
	float sum = 0.0;
	
	sum += sample(vec2(tc.x - 4.0 * blur, tc.y), r) * 0.05;
	sum += sample(vec2(tc.x - 3.0 * blur, tc.y), r) * 0.09;
	sum += sample(vec2(tc.x - 2.0 * blur, tc.y), r) * 0.12;
	sum += sample(vec2(tc.x - 1.0 * blur, tc.y), r) * 0.15;
	
	sum += center * 0.16;
	
	sum += sample(vec2(tc.x + 1.0 * blur, tc.y), r) * 0.15;
	sum += sample(vec2(tc.x + 2.0 * blur, tc.y), r) * 0.12;
	sum += sample(vec2(tc.x + 3.0 * blur, tc.y), r) * 0.09;
	sum += sample(vec2(tc.x + 4.0 * blur, tc.y), r) * 0.05;
	
	//sum of 1.0 -> in light, 0.0 -> in shadow
 	
 	//multiply the summed amount by our distance, which gives us a radial falloff
 	// //then multiply by vertex (light) color
    // if (center == 1.0) {
        f_colour = texture(image, uvs).rgba * vec4(vec3(1.0), sum * smoothstep(1.0, 0.0, r));
    // } else {
    //     f_colour = vec4(0.0, 1.0, 0.0, 1.0);
    // }
}

// void main() {
//     f_colour = vec4(texture(image, uvs).rgb, 1.0);
// }