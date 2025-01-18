#version 330 core

in vec2 uvs;
out vec4 f_colour;

uniform sampler2D image;
uniform float bloom_spread = 0.8;
uniform float bloom_intensity = 1;

uniform bool horizontal = 1;

texture blur(texture image) {             
    vec2 tex_offset = 1.0 / textureSize(image, 0); // gets size of single texel
    vec3 result = texture(image, TexCoords).rgb * weight[0]; // current fragment's contribution
    if(horizontal)
    {
        for(int i = 1; i < 5; ++i)
        {
            result += texture(image, TexCoords + vec2(tex_offset.x * i, 0.0)).rgb * weight[i];
            result += texture(image, TexCoords - vec2(tex_offset.x * i, 0.0)).rgb * weight[i];
        }
    }
    else
    {
        for(int i = 1; i < 5; ++i)
        {
            result += texture(image, TexCoords + vec2(0.0, tex_offset.y * i)).rgb * weight[i];
            result += texture(image, TexCoords - vec2(0.0, tex_offset.y * i)).rgb * weight[i];
        }
    }

    return result;
}

void main() {
    vec4 pixel_colour = vec4(texture(screenTexture, uvs).rgb, 1.0);

    float brightness = dot(pixel_colour.rgb, vec3(0.2126, 0.7152, 0.0722));
    
    if (brightness > 0.5) {
        f_colour = vec4(pixel_colour.rgb, 1.0);
    } else {
        f_colour = vec4(0.0, 0.0, 0.0, 0.0);
    }
}