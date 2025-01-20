# version 330 core

uniform sampler2D image;
uniform float threshold;
uniform float intensity;

in vec2 uvs;
out vec4 f_colour;

void main(){
    vec4 pixel = texture(image, uvs);
    float brightness = dot(pixel.rgb, vec3(0.2126, 0.7152, 0.0722));
    float isBright = step(threshold, brightness);

    f_colour = vec4(vec3(pixel.rgb * intensity) * isBright, 1.0);

    // if (brightness > threshold) {
    //     f_colour = vec4(vec3(pixel.rgb * intensity), pixel.a);
    // } else {
    //     f_colour = vec4(0.0, 0.0, 0.0, 1.0);
    // }
}