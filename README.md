# Interstellar Interceptors. Mission design for rendezvous with objects in hyperbolic orbits.

<div align="center">
     <img width="256px" src="https://github.com/jorgepiloto/tfm/blob/main/fig/static/shots/2.png" />
     <img width="256px" src="https://github.com/jorgepiloto/tfm/blob/main/fig/static/shots/3.png" />
     <img width="256px" src="https://github.com/jorgepiloto/tfm/blob/main/fig/static/shots/4.png" />
</div>

## About

This repository contains all the files required to generate my master's thesis
in astronomy and astrophysics. The report is titled **Interstellar Interceptors.
Mission design for rendezvous with objects in hyperbolic orbits.**

## Requirements

The following requirements apply for building this project:


- Make: https://www.gnu.org/software/make/
- LaTeX: https://www.latex-project.org/
- XeLaTeX: https://tug.org/xetex/

## About project structure

The project is divided into different directories, each one devoted to store a
particular type of information:

```
.
├── asy
├── bib
├── bin
├── dat
├── fig
│   └── static
├── main.tex
├── Makefile
├── README.md
├── src
└── tex
```

Within the `asy/` folder, all the scripts used for building the Asymptote based
figures are located. Their output will be temporary stored in the `fig/`
directory and removed after the PDF file has been successfully compiled. Notice
that the `static/` sub-directory holds figures which are not supposed to be
deleted after the cleaning process has been executed.

Regarding `bib/`, `src/` and `tex/` locations, they host all necessary style,
bibliography and work content files. The `main.tex` file is the one used to
control the rest of LaTeX files.

The `bin/` and `dat/` directories is where all binaries and databases used by
them are saved.

Finally the `Makefile` is where all auxiliary rules for automation are
described.


## Required dependencies for building the project

Several programs are required to compile the project. The versions listed here
are the ones originally used to build all files. It might be possible that with
newer version, some of tools presented in the following lines are not able to
produce expected results.

**latexindent: a tool for formatting LaTeX files**

```
3.8.3, 2020-11-06
```

**XeLaTeX: the LaTeX engine used to compile the files**

```
XeTeX 3.14159265-2.6-0.999992 (TeX Live 2020/Arch Linux)
kpathsea version 6.3.2
Compiled with ICU version 68.2; using 68.2
Compiled with zlib version 1.2.11; using 1.2.11
Compiled with FreeType2 version 2.10.4; using 2.10.4
Compiled with Graphite2 version 1.3.14; using 1.3.14
Compiled with HarfBuzz version 2.7.4; using 2.7.4
Compiled with libpng version 1.6.37; using 1.6.37
Compiled with poppler version 21.02.0
Compiled with fontconfig version 2.13.91; using 2.13.91
```

**biber: it is used for building the project bibliography**

```
biber version: 2.15
```

**pdfTeX: the program used to render the output PDF file**

```
pdfTeX 3.14159265-2.6-1.40.21 (TeX Live 2020/Arch Linux)
kpathsea version 6.3.2
Compiled with libpng 1.6.37; using libpng 1.6.37
Compiled with zlib 1.2.11; using zlib 1.2.11
Compiled with poppler version 21.02.0
```

**asymptote: it is used for building all technical figures and drawings**

```
Asymptote version 2.69 [(C) 2004 Andy Hammerlindl, John C. Bowman, Tom Prince]
```

**ghostscript: the tool acting as PostScript interpreter, related with
drawings**

```
GPL Ghostscript 9.53.3 (2020-10-01)
```

**Python: the programming language under which binaries are implemented**

```
Python: 3.8.5
```

**make: an utomatition for simplifying project building process**

```
GNU Make 4.3
Built x86_64-pc-linux-gnu
```
