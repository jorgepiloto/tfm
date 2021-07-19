import graph;
import geometry;

/* Define the settings for the script */
settings.outformat="png";
settings.render=6;
size(7cm,0);

/* Markers definition */
marker croix=marker(scale(2)*cross(4));

/* Interesting points */
pair F = (0.50, 0.00),
     r1 = (0.42136, 0.16313),
     r2 = (0.04405, 0.24783);

/* Additional points */
pair r3 = (0.3275, 0.20135),
     r4 = (0.24704, 0.22295),
     r5 = (0.13094, 0.24167);

/* Angle between the two position vectors */
real nu_value_0 = 115.73697;
real nu_value_f = 151.47421;

/* Coefficients for the conic section equation: ax^2+bxy+cy^2+dx+ey+f=0 */
real a = 0.98883,
     b = 0.00,
     c = 4.98883,
     d = 0,
     e = 0,
     f = -0.30832;

/* Define the Bivariate Quadratic Equation and the conic instance */
bqe conic_equation = bqe(a,b,c,d,e,f);
conic orbit = conic(conic_equation);


/* Draw all the elements */
draw(orbit, 1bp+black);
filldraw(F -- r1 .. r3 .. r4 .. r5 .. r2 -- cycle, palered+opacity(0.45));
filldraw(circle(r1, 0.0075), black);
filldraw(circle(r2, 0.0075), black);
draw("$\vec{r_1}$", F -- r1, Arrow());
draw("$\vec{r_2}$", F -- r2, SW, Arrow());
// draw("$\nu$",arc(F,0.1,nu_value_0,nu_value_f),LeftSide,Arrows);

/* Draw the interesting points */
dot("$F$", F, SW);

/* Draw the angle between the vectors */
draw("$\Delta \theta$", arc(F, 0.1, 115.7373, 151.47387));

/* Crop the figure to desired limits */
limits((0,-0.1),(0.6,0.3),Crop);
