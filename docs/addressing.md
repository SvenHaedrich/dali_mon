# Representations

## Short Addresses

For control gear addressing check IEC 62368-102 7.2.1 \
For control device addressing check IEC 62368-103 7.2.1
| Description                          | Representation |
|--------------------------------------|----------------|
| Control gear short address           | G*s*           |
| Control gear group address           | GG*g*          |
| Control gear broadcast               | BC GEAR        |
| Control gear broadcast unaddressed   | BC GEAR UN     |
| Control device short address         | D*s*           |
| Control device group address         | DG*g*          |
| Control device broadcast             | BC DEV         |
| Control device broadcast unaddressed | BC DEV UN      |

## Event Schemes

See also IEC 62386-103:2022 9.7.3
| eventScheme | Description                                                                      | Representation |
|-------------|----------------------------------------------------------------------------------|----------------|
| 0 (default) | Instance addressing, using instance type *t* and number *i*.                     | T*t*, I*i*     |
| 1           | Device addressing, using short address *s* and instance type *t*.                | D*s*, T*t*     |
| 2           | Device and instance addressing, using short address *s* and instance number *i*. | D*s*, I*i*     |
| 3           | Device group addressing, using device group *g* and instance type *t*.           | DG*g*, T*t*    |
| 4           | Instance group addressing, using instance group *n* and type *t*.                | IG*n*, T*t*    |

## Instance Types

See also IEC 62386-103:2022 Table 4
| instance type | IEC 62386 | Description                                           |
|---------------|-----------|-------------------------------------------------------|
| 0             | 103       | Generic devices that do not implement a specific type |
| 1             | 301       | Input devices - Push buttons                          |
| 2             | 302       | Absolute input devices                                |
| 3             | 303       | Occupancy sensors                                     |
| 4             | 304       | Light sensors                                         |

## Addressing Modes

See also IEC 62386-103:2022 Table 2
| Addressing                          | Representation |
|-------------------------------------|----------------|
| Instance Number                     | I*n*           |
| Instance Group                      | IG*g*          |
| Instance Type                       | T*t*           |
| Feature on instance number level    | FI*n*          |
| Feature on instance group level     | FG*g*          |
| Feature on instance type level      | FT*t*          |
| Feature broadcast                   | BC FEAT        |
| Feature on instance broadcast level | BC FEAT INST   |
| Instance broadcast                  | BC INST        |
| Feature on device level             | FEAT DEV       |