import graph;
import geometry;

/* Load astronomy symbols */
usepackage("wasysym");

/* Define the settings for the script */
settings.outformat="png";
settings.render=6;
size(12cm,0);

/* Markers definition */
marker croix=marker(scale(3)*cross(4),1bp+black);

/* Main points and trajectory ones */
pair OO = (0.00, 0.00),
     r0 = (-0.25, 0),
     r1 = (0, 0.25),
     r2 = (0.10095, 0.22871),
     r3 = (0.21, 0.16037),
     r4 = (0.265, -0.08013),
     r5 = (0.12151, -0.27429);

/* Build the LM trajecotry */
path trajectory = r2 .. r3 .. r4 .. r5;

/* Radius for the Earth and Moon */
real R_Moon = 0.15,
     R_LM = 0.25,
     R_CSM = 0.30,
     r_dot = 0.0075;

/* Launch location */
pair r_launch = (R_Moon * Cos(200), R_Moon * Sin(200));
pair r_mid = (1.25 * R_Moon * Cos(198), 1.25 * R_Moon * Sin(198));

/* Draw the initial and final desired vectors */
filldraw(OO -- r2 .. r3 ..r4 .. r5 -- cycle, palered+opacity(0.5));
draw(OO -- r2, Arrow);
draw(OO -- r5, Arrow);

/* Draw the moon */
filldraw(circle(OO, R_Moon), mediumgray);
label("Moon", OO, N);
label("\rightmoon", OO, S);

/* Draw the LM and CSM orbits */
draw(circle(OO, R_LM), dashed+1bp);
draw(circle(OO, R_CSM), dashed+1bp);

/* Paint the trajectory followed by LM */
draw(arc(00,R_LM,180,66.1838), 1bp+red, Arrow(8pt));
draw(trajectory, 1bp+red, Arrow(8pt));
draw(r_launch .. r_mid .. r0, 1bp+red, Arrow(8pt));

/* Draw the particular maneuver points */
filldraw(circle(r2, r_dot));
filldraw(circle(r3, r_dot));
filldraw(circle(r4, r_dot));
filldraw(circle(r0, r_dot));
filldraw(circle(r2, r_dot));
filldraw(circle(r5, r_dot));
filldraw(circle(r_launch, r_dot));

/* Add information labels */
draw(Label("Launch",W,fontsize(10pt)),(-.35,-0.15) -- r_launch);
draw(Label("CHD burn",W,fontsize(10pt)),(-.35,0.15) -- r0);
draw(Label("Lambert's maneuver starts",W,fontsize(10pt)),(.12, 0.33) -- r2);
draw(Label("Correction burn I",W,fontsize(10pt)),(0.35, 0.2) -- r3);
draw(Label("Correction burn II",W,fontsize(10pt)),(0.35, -0.1) -- r4);
draw(Label("Docking with CSM",W,fontsize(10pt)),(0.35, -0.3) -- r5);
