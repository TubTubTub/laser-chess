# version 330 core

in vec2 uvs;
out vec4 f_colour;

uniform sampler2D image;
uniform float resolution;

#define PI 3.1415926536;
const float THRESHOLD = 0.99;

// void main() {
//     f_colour = vec4(texture(image, uvs).rgba);
// }

// float get_colour(float angle, float radius) {
//     for (float currentRadius=0 ; currentRadius < radius ; currentRadius += 0.01) {
//         vec2 coords = vec2(-currentRadius * sin(angle), -currentRadius * cos(angle)) / 2.0 + 0.5;
//         vec4 colour = texture(image, coords);

//         if (colour.r == 1.0) {
//             // return 1.0;
//             return 0.9;
//         }
//     }

//     return 0.5;
// }

// void main() {
//     float distance = 1.0;

//         // rectangular to polar filter
//     vec2 norm = uvs.xy * 2.0 - 1.0; // [0, 1] -> [-1, 1]
//     float angle = atan(norm.y, norm.x); // range [pi, -pi]      [1, 0] = 0, [-1, 0] = pi or -pi
//     float radius = length(norm);

//     // 0.5, 1 -> 0, 0.5
//     // 1, 0.5 -> 0.5, 0

    
//     // coord which we will sample from occlude map
//     vec2 polar_coords = vec2(-radius * sin(angle), -radius * cos(angle)) / 2.0 + 0.5; // .s == .x, .t == .y
    
//     // for (float y = 0.0; y < resolution.y; y++) {
//         //sample the occlusion map
//         // float norm_distance = y / resolution.y;
//         // vec4 data = texture(image, polar_coords).rgba;
        
//         //the current distance is how far from the top we've come
        
//         //if we've hit an opaque fragment (occluder), then get new distance
//         //if the new distance is below the current, then we'll use that for our ray

//         // if (data.a == 1.0) {
//         //     distance = min(distance, polar_coords.y);
//             // distance = norm_distance;
//             // break;
//         // } // if using return, does not set frag colour so just returns normal image
//     // }

//     // float brightness = get_colour(angle, radius);
//     // f_colour = vec4(vec3(brightness), 1.0);

//     f_colour = texture(image, polar_coords).rgba;
// }


// void main() {
//   float distance = 0.5;
//   float resolution = 256;
  
//     for (float y=0.0; y< resolution; y+=1.0) { // putting y < resolution.y doesn't work for some reason
//         //rectangular to polar filter
//         vec2 norm = vec2(uvs.s, y/resolution) * 2.0 - 1.0;
//         float theta = PI*1.5 + norm.x * PI; 
//         float r = (1.0 + norm.y) * 0.5;
        
//         //coord which we will sample from occlude map
//         vec2 coord = vec2(-r * sin(theta), -r * cos(theta))/2.0 + 0.5;
        
//         //sample the occlusion map
//         vec4 data = texture(image, coord);
        
//         //the current distance is how far from the top we've come
//         float dst = y/resolution;
        
//         //if we've hit an opaque fragment (occluder), then get new distance
//         //if the new distance is below the current, then we'll use that for our ray
//         float caster = data.r;
//         if (caster > THRESHOLD) {
//             distance = 1.0;
//             // distance = min(distance, dst);
//             break;
//             //NOTE: we could probably use "break" or "return" here
//         }
//         distance = min(distance, dst);
//     }

//     f_colour = vec4(vec3(distance), 1.0);
// }


void main() {
  float distance = 1.0;
  
    for (float y=0.0; y < resolution; y += 1.0) {
        //rectangular to polar filter
        float dst = y / resolution;

        vec2 norm = vec2(uvs.x, dst) * 2.0 - 1.0; // [0, 1] -> [-1, 1]
        float angle = (1.5 - norm.x) * PI; // [-1, 1] -> [0.5PI, 2.5PI]
        float radius = (1.0 + norm.y) * 0.5;

        // float radius = length(norm);
        
        //coord which we will sample from occlude map
        vec2 coords = vec2(-radius * sin(angle), -radius * cos(angle)) / 2.0 + 0.5;
        
        //sample the occlusion map
        vec4 data = texture(image, coords);
        
        //the current distance is how far from the top we've come
        
        //if we've hit an opaque fragment (occluder), then get new distance
        //if the new distance is below the current, then we'll use that for our ray
        // float caster = data.r;
        // if (caster >= THRESHOLD) {
        //     distance = min(distance, dst);
        //     break;
        // }
        distance = max(distance * step(data.r, THRESHOLD), min(distance, dst));
    }

    f_colour = vec4(vec3(distance), 1.0);
}



// void main() {
//     vec2 norm = vec2(uvs.x, uvs.y) * 2.0 - 1.0;
//     float angle = (1.5 + norm.x) * PI;
//     float radius = (1.0 + norm.y) * 0.5;
//     vec2 coords = vec2(-radius * sin(angle), -radius * cos(angle)) / 2.0 + 0.5;

//     vec4 data = texture(image, coords);
    
//     f_colour = vec4(data.rgb, 1.0);
// }