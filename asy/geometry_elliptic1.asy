import graph;
import geometry;

/* Define the settings for the script */
settings.outformat="png";
settings.render=6;
size(10cm,0);

/* Declare all available ellipse focus */
pair F0 = (0, 0),
     F1 = (0.1, 0.2),
     F2  = (0.04038, 0.1369);

/* Declare the initial and final position vectors */
pair r1 = (0.14043, 0.10209),
     r2 = (0.02965, 0.20676);

/* The radius for the circles centered at r1 and r2 vectors */
real R1 = 0.10593,
     R2 = 0.07067;

/* Declare the two transfer orbits */
real a1 = 1.09032,
     b1 = -0.64,
     c1 = 0.61032,
     d1 = -0.04503,
     e1 = -0.09006,
     f1 = -0.00317;
bqe conic1 = bqe(a1,b1,c1,d1,e1,f1);
conic orbit1 = conic(conic1);

real a2 = 1.22423,
     b2 = -0.17692,
     c2 = 0.95044,
     d2 = -0.03733,
     e2 = -0.12655,
     f2 = -0.01335;
bqe conic2 = bqe(a2,b2,c2,d2,e2,f2);
conic orbit2 = conic(conic2);

/* Draw the initial and final position vectors */
draw("$\vec{r_1}$", F0 -- r1, Arrow());
draw("$\vec{r_2}$", F0 -- r2, SW, Arrow());

/* Draw the knwon focus */
dot("$F$", F0, SW);

/* Draw the circles centered at r1 and r2 vectors together with the new focus */
draw(circle(r1, R1), dashed);
draw(circle(r2, R2), dashed);
dot("$F'$", F1, NW, red);
dot("$F''$", F2, SE, blue);

/* Draw both transfer orbits */
draw(orbit1, 1bp+red);
draw(orbit2, 1bp+blue);

dot(r1);
dot(r2);
