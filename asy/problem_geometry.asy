/*
/ Returns a three-dimensional representation of the Lambert's problem geometry
*/

import three;
import math;
import graph3;
import grid3;
import geometry;

/* Load astronomy symbols */
usepackage("wasysym");

/* Settings and configuration */
size(12cm,0);
settings.outformat="png";
settings.render=8;

/* Define scene settings */
currentprojection=orthographic(2,1,1);
currentlight=nolight;

/* Define the focus of the orbit */
triple F = (-0.5, 0, 0), F_prime = (0, 0, -0.5);

/* Define the right ascension of the ascending and descending nodes */
triple raan_up = (1.37853, 1.70499, 0), raan_down = (-2.10874, -1.46012, 0);

/* Define more points which belong to the orbit */
triple r0 = (0.51674, 1.84635, 1.01754),
       r1 = (-0.23341, 1.60339, 1.5),
       r2 = (-1.66962, 0.41691, 1.62896);

/* Auxiliary points */
triple ax1 = (-1.52803, -1.8444, -1.0041),
       ax2 = (-0.54115, -1.72057, -1.85454),
       ax3 = (1.03803, -0.58088, -2.17803),
       ax4 = (1.72422, 1.08953, -1.02399);

/* Build the path for the orbit */
path3 orbit = raan_up .. r0 .. r1 .. r2 ..raan_down; 
path3 before_raan_up = ax4 .. raan_up .. r0 .. r1 .. r2 ..raan_down; 
path3 after_raan_down = raan_up .. r0 .. r1 .. r2 ..raan_down .. ax1; 

/* Draw the fundamental reference plane with origin at focus */
real r_plane = 2.55;
draw(shift(F) * scale3(r_plane) * unitcircle3, black);
draw(shift(F) * scale3(r_plane) * surface(unitcircle3), gray+opacity(0.5));

/* Draw the orbit */
draw(before_raan_up, red);
draw(after_raan_down, dashed+red);
draw(orbit, red);

/* Draw the area of the sector of observation */
draw(surface(F -- r0 .. r1 .. r2 -- cycle), palered+opacity(0.45));

/* Draw interesting points */
draw(shift(raan_up) * scale3(0.025) * unitsphere, black);
draw(shift(raan_down) * scale3(0.025) * unitsphere, black);
draw(shift(r0) * scale3(0.025) * unitsphere, black);
draw(shift(r2) * scale3(0.025) * unitsphere, black);

/* Draw the radius of observations */
draw(Label("$\vec{r_{1}}$", fontsize(10pt)), F -- r0, black, Arrow3(DefaultHead2));
draw(Label("$\vec{r_{2}}$", align=W, fontsize(10pt)), F -- r2, black, Arrow3(DefaultHead2));

/* Properly display the label of the RAAN */
draw(raan_down -- raan_up, dashed+black);
draw(Label("$\ascnode$", position=EndPoint,fontsize(10pt)), F -- 1.1 * raan_up, opacity(0));
draw(Label("$\descnode$", align=W, position=EndPoint,fontsize(10pt)), F -- 1.05 * raan_down, opacity(0));

/* This function draws an angle dimension in a three-dimensional figure
 * A: the lower point
 * B: the center or common point
 * C: the upper point
 */ 
path3 anglearc(real radius, triple A, triple B, triple C)
{
triple center = B;
triple start = B + radius * unit(A-B);
return arc(center, start, C,cross(A-B, C-B),CCW);
}


/* Draw the inlcination angle of the orbit */
triple A = (0.74772, 2.4868, 0),
       B = raan_up,
       C = (1.04306, 1.84142, 0.48579);
draw(anglearc(0.5, 0.95 * A, B, C), L=Label("$i$", align=NE, fontsize(10pt)), Arrow3);

/* Draw the difference in true anomaly and make label is in front of sector surface  */
draw(anglearc(0.5, r0, F, r2));
label("$\Delta \theta$", align=E, position=(-0.2, 0.45, 0.6), fontsize(10pt));


/* Draw the RAAN angle */
draw(anglearc(r_plane, (r_plane, 0, 0), F, raan_up), L=Label("$\Omega$",
align=NE, fontsize(10pt)), Arrow3);

/* Draw reference frame with origin at focus */
real r = 3.5;
draw(Label("$x$", position=EndPoint, fontsize(10pt)), (F--(r, F.y, F.z)), Arrow3);
draw(Label("$y$", position=EndPoint, fontsize(10pt)), (F--(F.x, r, F.z)), Arrow3);
draw(Label("$z$", position=EndPoint, fontsize(10pt)), (F--(F.x, F.y, r)), Arrow3);
draw(shift(F) * scale3(0.1) * unitsphere, black);
