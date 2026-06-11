# MMD to MToon Connector

A Blender add-on that easily converts MMD (MikuMikuDance) materials to MToon materials with proper texture connections.

**Author:** Arfyuri  
**Version:** 1.31  
**Blender Compatibility:** 3.6.0 and above  

## Features

- **Automated Conversion:** Seamlessly replaces `MMDShaderDev` nodes with MToon nodes.
- **Smart Texture Routing:** Automatically maps and connects textures to their proper MToon counterparts:
  - `Base Tex` ➔ `MainTexture` (Color), `ShadeColor` (Color), `MainTextureAlpha` (Alpha)
  - `Toon Tex` ➔ `ShadeTexture` (Color), `ReceiveShadow_Texture_alpha` (Alpha)
  - `Sphere Tex` ➔ `SphereAddTexture` (Color)
- **Automatic Parameter Tuning:** Sets optimal default MToon parameters (`ShadeShift`: 1.0, `ShadeToony`: 1.0).
- **Cleanup:** Automatically removes the old MMD nodes and wires the new MToon node directly to the Material Output.

## Prerequisites

- **VRM Add-on for Blender**: This plugin requires the `MToon_unversioned` node group, which is provided by the VRM add-on. Make sure the VRM add-on is installed and enabled in Blender before running the conversion.

## Installation

1. Download the `mmd_to_mtoon.py` file.
2. In Blender, open **Edit > Preferences > Add-ons**.
3. Click **Install...**, locate your downloaded `mmd_to_mtoon.py` file, and install it.
4. Check the box next to **Material: MMD to MToon Connector** to enable the add-on.

## Usage

1. Select the mesh object(s) containing the MMD materials you wish to convert.
2. Open the 3D Viewport sidebar (press `N`).
3. Navigate to the **Arfyuri Tools** tab.
4. Expand the **MMD to MToon** panel.
5. Click **Convert to MToon**.
6. Check the System Console (`Window > Toggle System Console`) to view detailed logs and verify that all textures were successfully connected.

## Support

If you find this tool helpful, consider supporting my work!
- [Support Me on Carrd](https://arfyuri.carrd.co)
