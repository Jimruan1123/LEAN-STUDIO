// SPDX-License-Identifier: GPL-3.0-or-later
// Adapted for square profiles from NopSCADlib, Copyright Chris Palmer 2020.
// https://github.com/nophead/NopSCADlib/blob/master/vitamins/extrusion.scad
// https://github.com/nophead/NopSCADlib/blob/master/vitamins/extrusions.scad
// Changes: standalone square-only section, removed BOM/visual dependencies, zero-based extrusion.
series=40; length=500; $fn=96;
// width, center hole (-diameter), corner hole (-diameter), center square, slot, inner slot, tab, spar, fillet
p=series==20?[20,-4.2,0,8,6,12,2,2,1]:series==30?[30,-6.8,-4.2,12,8,16.5,2,2,1]:[40,-10.5,-6,15,10,20,5.5,3,1];
module hole(d){if(d>0)square(d,center=true);else if(d<0)circle(d=-d);}
module section(p){
 w=p[0]; cs=p[3]; cw=p[4]; corner=(w-p[5])/2; tab=p[6]; spar=p[7]; f=p[8];
 union(){
  difference(){union(){hole(cs);for(j=[0:3])rotate(45+90*j)translate([cs/2-spar/2,-spar/2])square([w/sqrt(2)-corner*sqrt(2)-cs/2+spar*(1+tan(22.5)),spar]);}hole(p[1]);}
  for(a=[0:90:270])rotate(a)translate([-w/2,-w/2])difference(){union(){translate([f,0])square([(w-cw)/2-f,tab]);translate([0,f])square([tab,(w-cw)/2-f]);translate([f,f])circle(f);translate([f,f])square([corner-f,corner-f]);}translate([corner/2,corner/2])hole(p[2]);}
 }
}
assert(series==20||series==30||series==40);assert(length>0);
linear_extrude(height=length,convexity=8)section(p);
