#version 330 core

precision mediump float;
uniform sampler2D image;

in vec2 uvs;
out vec4 f_colour;
uniform int mode = 1;

void main() {
  if (mode == 0){
    f_colour = vec4(texture(image, uvs).rgb, 1.0);
  }
  else {
    float flatness = 1.0;

    if (mode == 1) flatness = 5.0;
    else if(mode == 2) flatness = 10.0;

    vec2 center = vec2(0.5, 0.5);
    vec2 off_center = uvs - center;

    off_center *= 1.0 + 0.8 * pow(abs(off_center.yx), vec2(flatness));
    // 1.0 -> 1.5 make distance to screen
    // vec 2 -> screen flatness

    vec2 uvs_2 = center+off_center;

    if (uvs_2.x > 1.0 || uvs_2.x < 0.0 || uvs_2.y > 1.0 || uvs_2.y < 0.0) {
      f_colour=vec4(0.0, 0.0, 0.0, 1.0);
      
    } else {
      f_colour = vec4(texture(image, uvs_2).rgb, 1.0);
      float fv = fract(uvs_2.y * float(textureSize(image,0).y));
      fv = min(1.0, 0.8+0.5*min(fv, 1.0-fv));
      f_colour.rgb *= fv;
    }
  }
}