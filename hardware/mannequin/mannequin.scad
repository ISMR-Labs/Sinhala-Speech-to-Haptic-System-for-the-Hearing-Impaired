// Stylised mannequin wearing the 18 vibration modules (9 chest, 9 upper back),
// the sleeved leads and the hip-mounted controller box. Used for the turntable
// animation in the README (tools/render_mannequin.py) and for checking the pod pitch.
// Units: mm. spin = turntable angle in degrees.

spin = 0;
pitch = 80;              // module pitch, both grids
pod = [32.5, 40.5, 10.1]; // module pod outer size (x width, z height, y depth)
chest_z = 1330;          // height of the middle row of the chest grid
back_z  = 1360;          // middle row of the back grid (slightly higher, between the shoulder blades)
show_leads = true;

$fn = 48;

skin   = [0.82, 0.82, 0.84];
podcol = [0.16, 0.42, 0.85];
leadcl = [0.12, 0.12, 0.12];
boxcol = [0.95, 0.95, 0.95];

module ell(rx, ry, rz) scale([rx, ry, rz]) sphere(1, $fn = 56);

// torso: an elliptical taper from the hips to the shoulders (exact radii, so pods sit on the surface)
hip_z = 1060; sh_z = 1440;
hip_r = [185, 125]; sh_r = [205, 112];
function torso_rx(z) = hip_r[0] + (sh_r[0] - hip_r[0]) * (z - hip_z) / (sh_z - hip_z);
function torso_ry(z) = hip_r[1] + (sh_r[1] - hip_r[1]) * (z - hip_z) / (sh_z - hip_z);
module torso() {
  translate([0, 0, hip_z])
    linear_extrude(height = sh_z - hip_z, scale = [sh_r[0] / hip_r[0], sh_r[1] / hip_r[1]], slices = 8)
      scale([hip_r[0], hip_r[1]]) circle(1, $fn = 72);
  translate([0, 0, sh_z]) ell(sh_r[0], sh_r[1], 38);   // rounded shoulders
  translate([0, 0, hip_z]) ell(hip_r[0], hip_r[1], 50); // rounded hips
}
module neck_head() {
  translate([0, 0, 1470]) cylinder(h = 90, r1 = 62, r2 = 55);
  translate([0, 0, 1660]) ell(95, 105, 118);
}
module arms() {
  for (s = [-1, 1]) {
    translate([s * 215, 0, 1420]) sphere(52);                         // shoulder
    hull() {                                                          // upper arm
      translate([s * 220, 0, 1400]) sphere(48);
      translate([s * 240, 20, 1130]) sphere(42);
    }
    hull() {                                                          // forearm
      translate([s * 240, 20, 1130]) sphere(40);
      translate([s * 250, 60, 900]) sphere(34);
    }
  }
}
module legs() {
  for (s = [-1, 1]) hull() {
    translate([s * 95, 0, 1040]) sphere(85);
    translate([s * 95, 0, 520]) sphere(62);
    translate([s * 95, 0, 60]) ell(60, 110, 55);
  }
}
module stand() {
  color([0.35, 0.35, 0.38]) {
    translate([0, 0, 0]) cylinder(h = 12, r = 420);     // turntable disc keeps the bounding box constant
  }
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
