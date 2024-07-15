# Sonic Mania

%game_overview%

## Installation

This port has been repacked to work out of the box with the Smart Pro (libtheora removed, settings modified for full widescreen)

1. Download the repacked port [here](https://github.com/cobaltgit/TrimUI-Ports/raw/main/ports/SonicManiaTSP.zip) and unzip into the root of your console's SD card
2. Add your Sonic Mania `Data.rsdk` file to `Data/ports/sonicmania`
3. Launch and enjoy!

### Sonic Mania Plus

To play Sonic Mania Plus, including the Encore DLC, you'll need to compile your own RSDKv5 binary as the one shipped with the port was compiled with DLC disabled.  
This assumes you already have the Sonic Mania port installed on your device, and you have an arm64 environment for compilation:

1. Follow the instructions [here](https://github.com/romadu/RSDKv5-Decompilation/blob/master/README.md#building-on-device-with-arkos) to compile RSDK v5.
2. Copy your new `RSDKv5` and `Game.so` files to `Data/ports/sonicmania`, overwriting the old ones
3. Launch the game: you should now be in Sonic Mania Plus!