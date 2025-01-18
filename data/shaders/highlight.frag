# version 330 core

uniform sampler2D image;
uniform float threshold = 1.0;
uniform float strength = 1.0;

in vec2 uvs;
out vec4 f_colour;

void main(){
    vec4 pixel = texture(image, uvs).rgba;
    float brightness = dot(pixel.rgb, vec3(0.2126, 0.7152, 0.0722));

    if (brightness > threshold) {
        f_colour = vec4(pixel.rgb * strength, pixel.a);
    } else {
        f_colour = vec4(0.0, 0.0, 0.0, 1.0);
    }
}