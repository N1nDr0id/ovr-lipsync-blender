# ovr-lipsync-blender
A Blender 4.0.2 addon to automate lipsync for characters that follow the Oculus Viseme standard (i.e. VRChat avatars, etc).
This can be used either as the final result for your project, or as a starting point for further animation.

To use this addon, you must select a model that has shapekeys on it. Ideally, your model should have the shapekeys listed in the [Oculus Viseme Reference](https://developer.oculus.com/documentation/native/audio-ovrlipsync-viseme-reference/).

After selecting the desired mesh, audio file, viseme shapekeys, and starting point for the animation, keyframes will be inserted onto the selected shapekeys that match with the given audio.

In addition, this program only works with mono .wav files. Attempting to load a stereo .wav file will make the program fail to execute.

<img src="https://github.com/N1nDr0id/ovr-lipsync-blender/blob/main/docs/addon_preview.png?raw=true" alt="An example image of the lipsync addon, showing off the various features">

## Known issues
<ul>
  <li>This addon only works on Windows machines, as it uses an .exe file to process audio. Linux and MacOS versions may be made available in the future, but I can't guarantee this.</li>
  <li>The addon only works with mono .wav files, and does not handle stereo .wav files.</li>
  <li>The ProcessWAV.exe and OVRLipSync.dll files must be located alongside the __init__.py file, otherwise the addon will fail to apply the shapekeys.</li>
  <li>This program has not been extensively tested and should only be used at your own risk. It only modifies the selected viseme shaapekeys, so it <em>should</em> be safe to use alongside other animations, but this has not been tested in full.</li>
</ul>

## License
The OVRLipSync.dll plugin is the property of [Meta](https://about.meta.com/) and is provided under the Oculus SDK License, which allows for personal and commercial use of the plugin. By using this plugin, you agree to the terms of the Oculus SDK License.
