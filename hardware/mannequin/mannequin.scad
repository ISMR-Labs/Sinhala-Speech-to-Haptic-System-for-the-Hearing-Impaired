// Stylised mannequin wearing the 18 vibration modules (9 chest, 9 upper back),
// the sleeved leads and the hip-mounted controller box. Used for the turntable
// animation in the README (tools/render_mannequin.py) and for checking the pod pitch.
// Units: mm. spin = turntable angle in degrees.

spin = 0;
pitch = 80;              // module pitch, both grids
pod = [32.5, 40.5, 10.1]; // module pod outer size (x width, z height, y depth)
chest_z = 1320;          // height of the middle row of the chest grid
back_z  = 1360;          // middle row of the back grid (slightly higher, between the shoulder blades)
show_leads = true;

$fn = 48;

skin   = [0.86, 0.79, 0.71];   // mannequin beige
podcol = [0.16, 0.42, 0.85];
leadcl = [0.12, 0.12, 0.12];
boxcol = [0.95, 0.95, 0.95];

module ell(rx, ry, rz) scale([rx, ry, rz]) sphere(1, $fn = 64);

// torso profile: elliptical slices (z, rx, ry), joined by linear tapers so the radii at any
// height are exact and the pods can be placed on the surface
// control points (z, rx, ry); the profile is a Catmull-Rom curve through them, sampled every 20 mm
ctrl = [[960, 170, 118], [1000, 178, 122], [1060, 182, 124], [1170, 152, 100], [1330, 186, 118], [1430, 198, 108], [1460, 170, 92]];
function cr(p0, p1, p2, p3, t) = 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t);
function seg_pt(i, t) = let(p0 = ctrl[max(i - 1, 0)], p1 = ctrl[i], p2 = ctrl[i + 1], p3 = ctrl[min(i + 2, len(ctrl) - 1)])
  [p1[0] + (p2[0] - p1[0]) * t, cr(p0[1], p1[1], p2[1], p3[1], t), cr(p0[2], p1[2], p2[2], p3[2], t)];
profile = [for (i = [0 : len(ctrl) - 2], k = [0 : 4]) seg_pt(i, k / 5)];
function lerp(a, b, t) = a + (b - a) * t;
function torso_r(z, k) =
  z <= profile[0][0] ? profile[0][k] :
  z >= profile[len(profile) - 1][0] ? profile[len(profile) - 1][k] :
  [for (i = [0 : len(profile) - 2]) if (z >= profile[i][0] && z < profile[i + 1][0])
     lerp(profile[i][k], profile[i + 1][k], (z - profile[i][0]) / (profile[i + 1][0] - profile[i][0]))][0];
function torso_rx(z) = torso_r(z, 1);
function torso_ry(z) = torso_r(z, 2);

module torso() {
  for (i = [0 : len(profile) - 2]) {
    a = profile[i]; b = profile[i + 1];
    if (b[0] > a[0])
      translate([0, 0, a[0]])
        linear_extrude(height = b[0] - a[0] + 0.3, scale = [b[1] / a[1], b[2] / a[2]], slices = 2)
          scale([a[1], a[2]]) circle(1, $fn = 96);
  }
  // sloping shoulders and trapezius
  hull() {
    translate([0, 0, 1460]) ell(166, 90, 16);         // flat top of the torso
    translate([0, 0, 1462]) ell(80, 60, 30);          // trapezius rise at the neck
    for (s = [-1, 1]) translate([s * 182, 0, 1428]) sphere(42);
  }
  translate([0, 0, 960]) ell(170, 118, 40);          // seat
}
module neck_head() {
  translate([0, 0, 1440]) cylinder(h = 110, r1 = 60, r2 = 54);
  hull() {
    translate([0, 0, 1665]) ell(84, 96, 112);        // cranium
    translate([0, -12, 1590]) sphere(52);            // jaw
  }
}
module arms() {
  for (s = [-1, 1]) {
    translate([s * 215, 0, 1410]) sphere(50);                             // deltoid
    hull() { translate([s * 222, 0, 1395]) sphere(44); translate([s * 250, -15, 1150]) sphere(38); }   // upper arm
    translate([s * 250, -15, 1150]) sphere(38);                           // elbow
    hull() { translate([s * 250, -15, 1150]) sphere(38); translate([s * 268, -75, 905]) sphere(28); }  // forearm
    translate([s * 272, -90, 860]) rotate([10, s * 8, 0]) ell(26, 18, 52); // hand
  }
}
module legs() {
  for (s = [-1, 1]) {
    hull() { translate([s * 92, 0, 1010]) sphere(88); translate([s * 98, 0, 520]) sphere(64); }    // thigh
    translate([s * 98, 0, 520]) sphere(64);                                                          // knee
    hull() { translate([s * 98, 0, 520]) sphere(58); translate([s * 100, 0, 95]) sphere(42); }       // shin
    translate([s * 100, -45, 32]) ell(52, 118, 32);                                                  // foot
  }
}
module stand() {
  color([0.35, 0.35, 0.38]) cylinder(h = 12, r = 420);   // turntable disc keeps the bounding box constant
}

module pod_at(x, z, side) {   // side = +1 front (-y is the face), -1 back
  rx = torso_rx(z); ry = torso_ry(z);
  y = ry * sqrt(max(0, 1 - pow(x / rx, 2)));
  ang = atan2(x / (rx * rx), y / (ry * ry));          // surface normal angle from +y
  translate([x, -side * (y + pod[2] / 2 + 3), z])
    rotate([0, 0, side * ang])
      color(podcol) hull() for (sx = [-1, 1], sz = [-1, 1])
        translate([sx * (pod[0] / 2 - 4), 0, sz * (pod[1] / 2 - 4)])
          rotate([90, 0, 0]) cylinder(h = pod[2], r = 4, center = true);
}

module lead(x, z, side) {
  rx = torso_rx(z); ry = torso_ry(z);
    // down the torso surface to the hip box
  pts = [for (zz = [z : -40 : 1060]) let(r = torso_ry(zz) * sqrt(max(0, 1 - pow(x / torso_rx(zz), 2))) + 5)
           [x, -side * r, zz]];
  color(leadcl) for (i = [0 : len(pts) - 2]) hull() {
    translate(pts[i]) sphere(2.2, $fn = 12);
    translate(pts[i + 1]) sphere(2.2, $fn = 12);
  }
  color(leadcl) hull() {
    translate(pts[len(pts) - 1]) sphere(2.2, $fn = 12);
    translate(side > 0 ? [-torso_rx(1050) - 6, 20, 1045] : [-110 + x * 0.25, torso_ry(1050) + 4, 1050]) sphere(2.2, $fn = 12);
  }
}

module controller_box() {   // on the lower back, left of the spine, lying flat against the body
  translate([-110, torso_ry(1050) + 20, 1050]) rotate([0, 0, 0]) {
    color(boxcol) hull() for (sx = [-1, 1], sz = [-1, 1])
      translate([sx * 44, 0, sz * 28]) rotate([90, 0, 0]) cylinder(h = 36, r = 6, center = true);
    translate([30, 20, 0]) color([0.1, 0.6, 0.2]) rotate([-90, 0, 0]) cylinder(h = 6, r = 7);  // push button
  }
}

module figure() {
  color(skin) { torso(); neck_head(); arms(); legs(); }
  for (c = [-1, 0, 1], r = [-1, 0, 1]) {
    pod_at(c * pitch, chest_z - r * pitch, 1);
    pod_at(c * pitch, back_z - r * pitch, -1);
    if (show_leads) { lead(c * pitch, chest_z - r * pitch, 1); lead(c * pitch, back_z - r * pitch, -1); }
  }
  controller_box();
}

stand();
rotate([0, 0, spin]) figure();
