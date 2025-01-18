#version 330 core

in vec2 uvs;
out vec4 f_colour;

uniform sampler2D image;
uniform float bloom_spread = 0.1;
uniform float bloom_intensity = 0.5;

void main() {
	ivec2 size = textureSize(screenTexture, 0);

    float uv_x = uvs.x * size.x;
    float uv_y = uvs.y * size.y;

    vec4 sum = vec4(0.0);

    for (int n = 0; n < 9; ++n) {
        uv_y = (uvs.y * size.y) + (bloom_spread * float(n - 4));
        vec4 h_sum = vec4(0.0);
        h_sum += texelFetch(screenTexture, ivec2(uv_x - (4.0 * bloom_spread), uv_y), 0);
        h_sum += texelFetch(screenTexture, ivec2(uv_x - (3.0 * bloom_spread), uv_y), 0);
        h_sum += texelFetch(screenTexture, ivec2(uv_x - (2.0 * bloom_spread), uv_y), 0);
        h_sum += texelFetch(screenTexture, ivec2(uv_x - bloom_spread, uv_y), 0);
        h_sum += texelFetch(screenTexture, ivec2(uv_x, uv_y), 0);
        h_sum += texelFetch(screenTexture, ivec2(uv_x + bloom_spread, uv_y), 0);
        h_sum += texelFetch(screenTexture, ivec2(uv_x + (2.0 * bloom_spread), uv_y), 0);
        h_sum += texelFetch(screenTexture, ivec2(uv_x + (3.0 * bloom_spread), uv_y), 0);
        h_sum += texelFetch(screenTexture, ivec2(uv_x + (4.0 * bloom_spread), uv_y), 0);
        sum += h_sum / 9.0;
    }

    f_colour = texture(screenTexture, uvs) + ((sum / 9.0) * bloom_intensity);
}