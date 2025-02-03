from data.managers.shader_classes.shake import Shake
from data.constants import ShaderType

shader_pass_lookup = {
    ShaderType.SHAKE: Shake,
    ShaderType.BLOOM: Bloom,
    ShaderType.GRAYSCALE: Grayscale,
    ShaderType.CRT: CRT,
    ShaderType.RAYS: Rays,

    ShaderType._CALIBRATE: lambda *args: None,
    ShaderType.BASE: Base,
    ShaderType._BLUR: _Blur,
    ShaderType._HIGHLIGHT_BRIGHTNESS: _Highlight_Brightness,
    ShaderType._HIGHLIGHT_COLOUR: _Highlight_Colour,
    ShaderType._SHADOWMAP: _ShadowMap,
    ShaderType._OCCLUSION: _Occlusion,
    ShaderType._LIGHTMAP: _LightMap,
    ShaderType._BLEND: _Blend,
    ShaderType._CROP: _Crop,
}