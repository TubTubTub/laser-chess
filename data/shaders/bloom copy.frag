#version 330 core

in vec2 uvs;
out vec4 f_colour;
  

uniform sampler2D image;
uniform sampler2D blurredImage;
uniform float exposure = 1.0;

void main()
{             
    const float gamma = 2.2;
    vec3 hdrColor = texture(image, uvs).rgb;      
    vec3 bloomColor = texture(blurredImage, uvs).rgb;
    hdrColor += bloomColor; // additive blending
    // tone mapping
    vec3 result = vec3(1.0) - exp(-hdrColor * exposure);
    // also gamma correct while we're at it       
    result = pow(result, vec3(1.0 / gamma));
    f_colour = vec4(result, 1.0);
}  