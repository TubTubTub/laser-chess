from data.shaders.classes.highlight_brightness import _HighlightBrightness
from data.shaders.classes.highlight_colour import _Highlight_Colour
from data.shaders.classes.shadowmap import _Shadowmap
from data.shaders.classes.occlusion import _Occlusion
from data.shaders.classes.grayscale import Grayscale
from data.shaders.classes.lightmap import _Lightmap
from data.shaders.classes.blend import _Blend
from data.shaders.classes.shake import Shake
from data.shaders.classes.bloom import Bloom
from data.shaders.classes.blur import _Blur
from data.shaders.classes.crop import _Crop
from data.shaders.classes.rays import Rays
from data.shaders.classes.base import Base
from data.shaders.classes.crt import CRT
from data.constants import ShaderType

shader_pass_lookup = {
    ShaderType.GRAYSCALE: Grayscale,
    ShaderType.SHAKE: Shake,
    ShaderType.BLOOM: Bloom,
    ShaderType.BASE: Base,
    ShaderType.RAYS: Rays,
    ShaderType.CRT: CRT,

    ShaderType._HIGHLIGHT_BRIGHTNESS: _HighlightBrightness,
    ShaderType._HIGHLIGHT_COLOUR: _Highlight_Colour,
    ShaderType._CALIBRATE: lambda *args: None,
    ShaderType._SHADOWMAP: _Shadowmap,
    ShaderType._OCCLUSION: _Occlusion,
    ShaderType._LIGHTMAP: _Lightmap,
    ShaderType._BLEND: _Blend,
    ShaderType._BLUR: _Blur,
    ShaderType._CROP: _Crop,
}