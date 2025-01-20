# version 330 core

uniform sampler2D image;

in vec2 uvs;
out vec4 f_colour;

// void main() {
//     f_colour = vec4(texture(image, uvs).rgb, 1.0);
// }

void main() {
    vec4 pixel = texture(image, uvs);
    float isOccluding = step(0.8, pixel.r);
    f_colour = vec4(isOccluding, 0.0, 0.0, 1.0);
    // if (pixel.r > 0.8) {
    //     f_colour = vec4(1.0, 0.0, 0.0, 1.0);
    // } else {
    //     f_colour = vec4(0.0, 0.0, 0.0, 1.0);
    // }
}