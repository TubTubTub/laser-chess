# version 330 core

#define PI 3.1415926536;

in vec2 uvs;
out vec4 f_colour;

uniform sampler2D image;
uniform float resolution;
uniform float THRESHOLD=0.99;

void main() {
	float maxDistance = 1.0;

    for (float y = 0.0 ; y < resolution ; y += 1.0) {
        //rectangular to polar filter
        float currDistance = y / resolution;

        vec2 norm = vec2(uvs.x, currDistance) * 2.0 - 1.0; // Range from [0, 1] -> [-1, 1]
        float angle = (1.5 - norm.x) * PI; // Range from [-1, 1] -> [0.5PI, 2.5PI]
        float radius = (1.0 + norm.y) * 0.5; // Range from [-1, 1] -> [0, 1]
        
        //coord which we will sample from occlude map
        vec2 coords = vec2(radius * -sin(angle), radius * -cos(angle)) / 2.0 + 0.5;
        
        // Sample occlusion map
        vec4 occluding = texture(image, coords);
        
        // If pixel is not occluding (Red channel value below threshold), set maxDistance to current distance
		// If pixel is occluding, don't change distance
		// maxDistance therefore is the distance from the center to the nearest occluding pixel
        maxDistance = max(maxDistance * step(occluding.r, THRESHOLD), min(maxDistance, currDistance));
    }

    f_colour = vec4(vec3(maxDistance), 1.0);
}