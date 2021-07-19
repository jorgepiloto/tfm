import graph;
import geometry;

/* Define the settings for the script */
settings.outformat="png";
settings.render=6;
size(10cm,0);

/* Declare all available ellipse focus */
pair F = (0, 0);

/* Declare the initial and final position vectors */
pair r1 = (0.2, 0.1),
     r2 = (-0.1, 0.3);

/* Declare the two tangent lines */
pair x1 = (-0.14599, 0.83007),
     y1 = (0.59283, -0.00672);
line directrice1 = line(x1, y1);
pair x2 = (0.39868, -0.20387),
     y2 = (-0.77361, 0.19532);
line directrice2 = line(x2, y2);

/* The radius for the circles centered at r1 and r2 vectors */
real R1 = 0.22361,
     R2 = 0.31623;

/* Declare the two transfer orbits */
conic orbit1 = conic(F, directrice1, 1.00);
conic orbit2 = conic(F, directrice2, 1.00);

/* Draw the initial and final position vectors */
draw("$\vec{r_1}$", F -- r1, NW, Arrow());
draw("$\vec{r_2}$", F -- r2, SW, Arrow());

/* Draw the knwon focus */
dot("$F$", F, N);

/* Draw the circles centered at r1 and r2 vectors together with the new focus */
draw(circle(r1, R1), dashed);
draw(circle(r2, R2), dashed);

/* Draw the tangent lines */
draw(directrice1, red);
draw(directrice2, blue);

/* Draw both transfer orbits */
draw(orbit1, 1bp+red);
draw(orbit2, 1bp+blue);

dot(r1);
dot(r2);
