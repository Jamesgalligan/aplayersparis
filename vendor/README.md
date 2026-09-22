# vendor

`libphonenumber-max.js` — libphonenumber-js v1.11.20, UMD build with full
metadata (MIT licence, https://github.com/catamphetamine/libphonenumber-js).

Vendored rather than loaded from a CDN so phone validation on the reserve
form has no runtime network dependency. `build.py` inlines it into
`index.html` at the `/*LIBPHONENUMBER*/` marker.

The "max" metadata is used deliberately: the smaller builds cannot
distinguish number types, which the anti-fake checks rely on.
