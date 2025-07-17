# Procedural Lighting System for Blender 4.1

A comprehensive Blender addon for creating and managing procedural lighting systems with advanced rendering effects.

## Features

### Core Features
- **Procedural Light Generation**: Create lights in mathematical patterns (Circle, Grid, Random, Spiral, Wave)
- **Advanced Light Management**: Easy controls for multiple lights with grouping and parenting
- **Rendering Effects**: Built-in volumetric lighting and bloom effects
- **Animation System**: Animate lights with customizable patterns and speeds
- **Preset System**: Save, load, and share lighting configurations
- **Performance Optimization**: Tools to optimize light setups for better performance

### Light Patterns
- **Circle**: Perfect for rim lighting and product shots
- **Grid**: Ideal for studio setups and even illumination
- **Random**: Creates organic, natural lighting feel
- **Spiral**: Adds dramatic, dynamic lighting
- **Wave**: Creates movement and flow in your lighting

### Light Properties
- **Energy Control**: Base energy with randomization
- **Color Variation**: Base color with controllable variation
- **Automatic Parenting**: Group lights under empty objects for easy manipulation
- **Smart Naming**: Organized naming system for easy identification

### Rendering Effects
- **Volumetric Lighting**: Automatic volumetric setup with density control
- **Bloom Effects**: Compositor-based bloom with customizable intensity
- **Light Baking**: Bake lighting to lightmaps for performance
- **Cycles Integration**: Optimized for Cycles rendering engine

## Installation

### Method 1: Manual Installation
1. Download or clone this repository
2. Open Blender 4.1
3. Go to `Edit` > `Preferences` > `Add-ons`
4. Click `Install...` and select the addon folder
5. Enable "Procedural Lighting System" in the addon list

### Method 2: Development Installation
1. Clone this repository to your Blender addons directory:
   ```
   # Windows
   %APPDATA%\Blender Foundation\Blender\4.1\scripts\addons\

   # macOS
   ~/Library/Application Support/Blender/4.1/scripts/addons/

   # Linux
   ~/.config/blender/4.1/scripts/addons/
   ```
2. Restart Blender
3. Enable the addon in preferences

## Usage Guide

### Basic Setup
1. Open Blender 4.1
2. In the 3D Viewport, open the sidebar (N key)
3. Navigate to the "Lighting" tab
4. Find the "Procedural Lighting" panel

### Creating Your First Light Setup
1. **Choose a Pattern**: Select from Circle, Grid, Random, Spiral, or Wave
2. **Set Parameters**:
   - Light Count: Number of lights to generate
   - Radius: Size of the pattern
   - Height: Vertical position of lights
3. **Configure Light Properties**:
   - Base Energy: Starting light intensity
   - Energy Variation: Random variation in intensity
   - Base Color: Starting light color
   - Color Variation: Random variation in color
4. **Click "Generate Lights"**

### Advanced Features

#### Volumetric Lighting
1. Enable "Use Volumetrics" in the Rendering Effects panel
2. Adjust "Volumetric Density" to control fog thickness
3. Click "Setup Volumetrics" to automatically configure materials
4. Ensure you're using Cycles render engine

#### Bloom Effects
1. Enable "Use Bloom" in the Rendering Effects panel
2. Set "Bloom Intensity" to desired level
3. Click "Setup Bloom" to configure compositor nodes
4. Render to see the bloom effect

#### Animation
1. Enable "Animate Lights" in the Animation panel
2. Set animation speed
3. Click "Animate Lights" to create keyframes
4. Play the timeline to see animated lighting

#### Presets
1. **Save Preset**: Click "+" in the Presets panel to save current settings
2. **Load Preset**: Select from list and click "Load Preset"
3. **Built-in Presets**: Use "Load Built-in Presets" for professional setups
4. **Export/Import**: Share presets with other users

### Tips for Best Results

#### Performance Optimization
- Use fewer lights (8-16) for real-time viewport
- Enable "Optimize Lights" for better performance
- Use light baking for static scenes
- Lower volumetric density for faster renders

#### Artistic Tips
- **Circle Pattern**: Great for product photography and rim lighting
- **Grid Pattern**: Perfect for studio lighting setups
- **Random Pattern**: Creates natural, organic lighting
- **Spiral Pattern**: Adds drama and movement
- **Wave Pattern**: Creates flowing, dynamic lighting

#### Technical Considerations
- Volumetric effects require Cycles rendering engine
- Bloom effects need compositor enabled
- Animation works best with 24-120 frame ranges
- Baking requires UV-mapped geometry

## Workflow Examples

### Studio Portrait Setup
1. Pattern: Grid (3x3, 9 lights)
2. Energy: 50W with 0.1 variation
3. Color: Warm white (1.0, 0.9, 0.8)
4. Add volumetrics for atmosphere
5. Enable bloom for professional look

### Product Photography
1. Pattern: Circle (8 lights)
2. Large radius for even coverage
3. Cool white color temperature
4. Low energy variation for consistency
5. Bake lighting for final renders

### Cinematic Lighting
1. Pattern: Random or Spiral
2. High energy variation (0.3-0.5)
3. Warm color with variation
4. Enable animation for dynamic feel
5. Strong bloom for dramatic effect

## API Reference

### Main Properties
- `pattern_type`: Light arrangement pattern
- `light_count`: Number of lights to generate
- `radius`: Pattern size
- `height`: Vertical position
- `base_energy`: Starting light intensity
- `base_color`: Starting light color
- `energy_variation`: Random intensity variation
- `color_variation`: Random color variation

### Operators
- `procedural_lighting.generate_lights`: Create light pattern
- `procedural_lighting.clear_lights`: Remove all lights
- `procedural_lighting.setup_volumetrics`: Configure volumetric lighting
- `procedural_lighting.setup_bloom`: Configure bloom effects
- `procedural_lighting.animate_lights`: Create light animation
- `procedural_lighting.optimize_lights`: Optimize for performance

## Troubleshooting

### Common Issues
1. **Lights not visible**: Check if lights are outside camera view
2. **Volumetrics not working**: Ensure Cycles render engine is selected
3. **Bloom not appearing**: Check compositor is enabled
4. **Performance issues**: Reduce light count or use optimization tools
5. **Animation not smooth**: Adjust animation speed and frame range

### Requirements
- Blender 4.1 or higher
- Cycles render engine (for volumetrics)
- Compositor enabled (for bloom effects)

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Sharing lighting presets

## License

This addon is released under the MIT License. See LICENSE file for details.

## Support

For support, feature requests, or bug reports, please create an issue on the project repository.

## Version History

### v1.0.0
- Initial release
- Basic procedural light generation
- Volumetric and bloom effects
- Animation system
- Preset management
- Performance optimization tools

---
