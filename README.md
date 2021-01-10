# subdivision
## Simple implementation of three most common subdivision algorithms *(and one more)*
### by [Michał Lampert](https://github.com/michlampert/) & [Wojciech Achtelik](https://github.com/WojtAcht/)

- [x] Doo–Sabin
- [x] Catmull–Clark
- [x] Loop
- [x] Peters-Reif


## 1. Step by step effect of Catmull-Clark algorithm
![suzanne](suzanne_CC.gif)


## 2. Statistics and results for Suzanne (Blender monkey)
below images: number of vertices | number of faces | time to compute
| Doo-Sabin | Catmull-Clark | Loop | Peters-Reif |
|---|---|---|---|
| ![gif](gifs/suzanne_DS.gif) | ![gif](gifs/suzanne_CC.gif) | ![gif](gifs/suzanne_LOOP.gif) | ![gif](gifs/suzanne_PR.gif) |
| ![img](photos/group_photo01_L06.png) <br/> 506 \| 500 \| 0 ms | ![img](photos/group_photo01_L00.png) <br/> 506 \| 500 \| 0 ms | ![img](photos/group_photo01_L12.png) <br/> 506 \| 966 \| 0 ms | ![img](photos/group_photo01_L18.png) <br/> 506 \| 500 \| 0 ms |
| ![img](photos/group_photo01_L07.png) <br/> 1966 \| 1926 \| 86.52 ms | ![img](photos/group_photo01_L01.png) <br/> 2010 \| 1966 \| 0.15 s | ![img](photos/group_photo01_L13.png) <br/> 1976 \| 3864 \| 0.18 s | ![img](photos/group_photo01_L19.png) <br/> 1004 \| 1006 \| 0.15 s |
| ![img](photos/group_photo01_L08.png) <br/> 7696 \| 7614 \| 0.4 s | ![img](photos/group_photo01_L02.png) <br/> 7950 \| 7864 \| 0.46 s | ![img](photos/group_photo01_L14.png) <br/> 7814 \| 15456 \| 0.59 s | ![img](photos/group_photo01_L20.png) <br/> 2008 \| 2010 \| 0.26 s |
| ![img](photos/group_photo01_L09.png) <br/> 30448 \| 30282 \| 2.78 s | ![img](photos/group_photo01_L03.png) <br/> 31626 \| 31456 \| 1.82 s | ![img](photos/group_photo01_L15.png) <br/> 31082 \| 61824 \| 2.32 s | ![img](photos/group_photo01_L21.png) <br/> 4016 \| 4018 \| 0.47 s |
| ![img](photos/group_photo01_L10.png) <br/> 121120 \| 120786 \| 38.28 s | ![img](photos/group_photo01_L04.png) <br/> 126162 \| 125824 \| 9.78 s | ![img](photos/group_photo01_L16.png) <br/> 123986 \| 247296 \| 14.47 s | ![img](photos/group_photo01_L22.png) <br/> 8032 \| 8034 \| 0.93 s |
| ![img](photos/group_photo01_L11.png) <br/> 483136 \| 482466 \| 721.48 s | ![img](photos/group_photo01_L05.png) <br/> 503970 \| 503296 \| 37.89 s | ![img](photos/group_photo01_L17.png) <br/> 495266 \| 989184 \| 51.01 s | ![img](photos/group_photo01_L23.png) <br/> 16064 \| 16066 \| 12.21 s |
|   |   |   | ![img](photos/group_photo01_L24.png) <br/> 32128 \| 32130 \| 14.05 s |
|   |   |   | ![img](photos/group_photo01_L25.png) <br/> 64256 \| 64258 \| 17.59 s |
|   |   |   | ![img](photos/group_photo01_L26.png) <br/> 128512 \| 128514 \| 24.39 s |
|   |   |   | ![img](photos/group_photo01_L27.png) <br/> 257024 \| 257026 \| 47.95 s |
|   |   |   | ![img](photos/group_photo01_L28.png) <br/> 514048 \| 514050 \| 85.45 s |

## 3. Statistics and results for cube
below images: number of vertices | number of faces | time to compute
| Doo-Sabin | Catmull-Clark | Loop | Peters-Reif |
|---|---|---|---|
| ![gif](gifs/cube_DS1.gif) | ![gif](gifs/cube_CC1.gif) | ![gif](gifs/cube_LOOP1.gif) | ![gif](gifs/cube_PR1.gif) |
| ![img](photos/group_photo00_L08.png) <br/> 8 \| 6 \| 0 ms | ![img](photos/group_photo00_L00.png) <br/> 8 \| 6 \| 0 ms | ![img](photos/group_photo00_L16.png) <br/> 8 \| 12 \| 0 ms | ![img](photos/group_photo00_L24.png) <br/> 8 \| 6 \| 0 ms |
| ![img](photos/group_photo00_L09.png) <br/> 24 \| 26 \| 1.2 ms | ![img](photos/group_photo00_L01.png) <br/> 26 \| 24 \| 1.03 ms | ![img](photos/group_photo00_L17.png) <br/> 26 \| 48 \| 1.28 ms | ![img](photos/group_photo00_L25.png) <br/> 12 \| 14 \| 0.49114 ms |
| ![img](photos/group_photo00_L10.png) <br/> 96 \| 98 \| 4.24 ms | ![img](photos/group_photo00_L02.png) <br/> 98 \| 96 \| 4.41 ms | ![img](photos/group_photo00_L18.png) <br/> 98 \| 192 \| 9.73 ms | ![img](photos/group_photo00_L26.png) <br/> 24 \| 26 \| 1.44 ms |
| ![img](photos/group_photo00_L11.png) <br/> 384 \| 386 \| 18.25 ms | ![img](photos/group_photo00_L03.png) <br/> 386 \| 384 \| 19.62 ms | ![img](photos/group_photo00_L19.png) <br/> 386 \| 768 \| 31.93 ms | ![img](photos/group_photo00_L27.png) <br/> 48 \| 50 \| 7.23 ms |
| ![img](photos/group_photo00_L12.png) <br/> 1536 \| 1538 \| 72.14 ms | ![img](photos/group_photo00_L04.png) <br/> 1538 \| 1536 \| 79.23 ms | ![img](photos/group_photo00_L20.png) <br/> 1538 \| 3072 \| 0.1 s | ![img](photos/group_photo00_L28.png) <br/> 96 \| 98 \| 10.88 ms |
| ![img](photos/group_photo00_L13.png) <br/> 6144 \| 6146 \| 0.33 s | ![img](photos/group_photo00_L05.png) <br/> 6146 \| 6144 \| 0.35 s | ![img](photos/group_photo00_L21.png) <br/> 6146 \| 12288 \| 0.37 s | ![img](photos/group_photo00_L29.png) <br/> 192 \| 194 \| 20.9 ms |
| ![img](photos/group_photo00_L14.png) <br/> 24576 \| 24578 \| 2.57 s | ![img](photos/group_photo00_L06.png) <br/> 24578 \| 24576 \| 2.02 s | ![img](photos/group_photo00_L22.png) <br/> 24578 \| 49152 \| 2.54 s | ![img](photos/group_photo00_L30.png) <br/> 384 \| 386 \| 42.9 ms |
| ![img](photos/group_photo00_L15.png) <br/> 98304 \| 98306 \| 27.11 s | ![img](photos/group_photo00_L07.png) <br/> 98306 \| 98304 \| 7.83 s | ![img](photos/group_photo00_L23.png) <br/> 98306 \| 196608 \| 10.69 s | ![img](photos/group_photo00_L31.png) <br/> 768 \| 770 \| 84.71 ms |
|   |   |   | ![img](photos/group_photo00_L32.png) <br/> 1536 \| 1538 \| 0.17 s |
|   |   |   | ![img](photos/group_photo00_L33.png) <br/> 3072 \| 3074 \| 0.31 s |
|   |   |   | ![img](photos/group_photo00_L34.png) <br/> 6144 \| 6146 \| 0.54 s |
|   |   |   | ![img](photos/group_photo00_L35.png) <br/> 12288 \| 12290 \| 0.99 s |
|   |   |   | ![img](photos/group_photo00_L36.png) <br/> 24576 \| 24578 \| 1.86 s |
|   |   |   | ![img](photos/group_photo00_L37.png) <br/> 49152 \| 49154 \| 5.86 s |
|   |   |   | ![img](photos/group_photo00_L38.png) <br/> 98304 \| 98306 \| 11.65 s |
