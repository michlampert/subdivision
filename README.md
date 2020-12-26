# subdivision
## Simple implementation of three most common subdivision algorithms
### by [Michał Lampert](https://github.com/michlampert/) & [Wojciech Achtelik](https://github.com/WojtAcht/)

- [x] Doo–Sabin
- [x] Catmull–Clark
- [x] Loop

## 1. Step by step effect of Catmull-Clark algorithm
![suzanne](suzanne_CC.gif)


## 2. Statistics and results for Suzanne (Blender monkey)
below images: number of vertices | number of faces | time to compute
| Doo-Sabin | Catmull-Clark | Loop |
|---|---|---|
| ![img](photos/group_photo01_L06.png) <br/> 507 \| 500 \| 0 ms | ![img](photos/group_photo01_L00.png) <br/> 507 \| 500 \| 0 ms | ![img](photos/group_photo01_L12.png) <br/> 507 \| 968 \| 0 ms |
| ![img](photos/group_photo01_L07.png) <br/> 1968 \| 1927 \| 27.16 ms | ![img](photos/group_photo01_L01.png) <br/> 2012 \| 1968 \| 37.93 ms | ![img](photos/group_photo01_L13.png) <br/> 1980 \| 3872 \| 0.13 s |
| ![img](photos/group_photo01_L08.png) <br/> 7702 \| 7620 \| 0.15 s | ![img](photos/group_photo01_L02.png) <br/> 7958 \| 7872 \| 0.18 s | ![img](photos/group_photo01_L14.png) <br/> 7830 \| 15488 \| 0.47 s |
| ![img](photos/group_photo01_L09.png) <br/> 30472 \| 30306 \| 1.12 s | ![img](photos/group_photo01_L03.png) <br/> 31658 \| 31488 \| 2.71 s | ![img](photos/group_photo01_L15.png) <br/> 31146 \| 61952 \| 1.98 s |
| ![img](photos/group_photo01_L10.png) <br/> 121216 \| 120882 \| 27.22 s | ![img](photos/group_photo01_L04.png) <br/> 126290 \| 125952 \| 6.4 s | ![img](photos/group_photo01_L16.png) <br/> 124242 \| 247808 \| 9.78 s |
| ![img](photos/group_photo01_L11.png) <br/> 483520 \| 482850 \| 638.77 s | ![img](photos/group_photo01_L05.png) <br/> 504482 \| 503808 \| 26.93 s | ![img](photos/group_photo01_L17.png) <br/> 496290 \| 991232 \| 34.1 s |
|![suzanne](suzanne_DS.gif)|![suzanne](suzanne_CC.gif)|![suzanne](suzanne_LOOP.gif)|

## 3. Statistics and results for cube
below images: number of vertices | number of faces | time to compute
| Doo-Sabin | Catmull-Clark | Loop |
|---|---|---|
| ![img](photos/group_photo00_L08.png) <br/> 8 \| 6 \| 0 ms | ![img](photos/group_photo00_L00.png) <br/> 8 \| 6 \| 0 ms | ![img](photos/group_photo00_L16.png) <br/> 8 \| 12 \| 0 ms |
| ![img](photos/group_photo00_L09.png) <br/> 24 \| 26 \| 0.4127 ms | ![img](photos/group_photo00_L01.png) <br/> 26 \| 24 \| 0.65184 ms | ![img](photos/group_photo00_L17.png) <br/> 26 \| 48 \| 0.76866 ms |
| ![img](photos/group_photo00_L10.png) <br/> 96 \| 98 \| 1.73 ms | ![img](photos/group_photo00_L02.png) <br/> 98 \| 96 \| 3.87 ms | ![img](photos/group_photo00_L18.png) <br/> 98 \| 192 \| 5.18 ms |
| ![img](photos/group_photo00_L11.png) <br/> 384 \| 386 \| 8.28 ms | ![img](photos/group_photo00_L03.png) <br/> 386 \| 384 \| 11.22 ms | ![img](photos/group_photo00_L19.png) <br/> 386 \| 768 \| 15.26 ms |
| ![img](photos/group_photo00_L12.png) <br/> 1536 \| 1538 \| 27.7 ms | ![img](photos/group_photo00_L04.png) <br/> 1538 \| 1536 \| 36.12 ms | ![img](photos/group_photo00_L20.png) <br/> 1538 \| 3072 \| 45.71 ms |
| ![img](photos/group_photo00_L13.png) <br/> 6144 \| 6146 \| 0.11 s | ![img](photos/group_photo00_L05.png) <br/> 6146 \| 6144 \| 0.13 s | ![img](photos/group_photo00_L21.png) <br/> 6146 \| 12288 \| 0.85 s |
| ![img](photos/group_photo00_L14.png) <br/> 24576 \| 24578 \| 0.73 s | ![img](photos/group_photo00_L06.png) <br/> 24578 \| 24576 \| 0.92 s | ![img](photos/group_photo00_L22.png) <br/> 24578 \| 49152 \| 2.0 s |
| ![img](photos/group_photo00_L15.png) <br/> 98304 \| 98306 \| 16.61 s | ![img](photos/group_photo00_L07.png) <br/> 98306 \| 98304 \| 3.24 s | ![img](photos/group_photo00_L23.png) <br/> 98306 \| 196608 \| 5.52 s |
|![cube](cube_DS.gif)|![cube](cube_CC.gif)|![cube](cube_LOOP.gif)|
