import graph;
import geometry;

/* Define the settings for the script */
settings.outformat="png";
settings.render=6;
size(10cm,0);

/* Declare all available ellipse focus */
pair F0 = (0, 0),
     F1 = (0.1, 0.2);

/* Declare the initial and final position vectors */
pair r1 = (0.22062, 0.12735),
     r2 = (-0.01005, 0.26668);

/* The radius for the circles centered at r1 and r2 vectors */
real R1 = 0.14081,
     R2 = 0.1286;

/* Declare the two transfer orbits */
real a1 = 1.17166,
     b1 = -0.32,
     c1 = 0.93166,
     d1 = -0.08517,
     e1 = -0.17033,
     f1 = -0.02267;
bqe conic1 = bqe(a1,b1,c1,d1,e1,f1);
conic orbit1 = conic(conic1);

/* Draw the initial and final position vectors */
draw("$\vec{r_1}$", F0 -- r1, Arrow());
draw("$\vec{r_2}$", F0 -- r2, SW, Arrow());

/* Draw the knwon focus */
dot("$F$", F0, SW);

/* Draw the circles centered at r1 and r2 vectors together with the new focus */
draw(circle(r1, R1), dashed);
draw(circle(r2, R2), dashed);
dot("$F'$", F1, NW, red);

/* Draw both transfer orbits */
draw(orbit1, 1bp+red);

dot(r1);
dot(r2);
