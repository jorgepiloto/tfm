# A collection of rules for simplifying project's building process

# Project directories and structure
PROJECTDIR = .
ASYDIR = asy
BINDIR = bin
FIGDIR = fig
TEXDIR = tex
SRCDIR = src
CHDIRS = $(SRCDIR)/00_introduction $(SRCDIR)/01_background $(SRCDIR)/02_targeting $(SRCDIR)/03_direct $(SRCDIR)/04_alternate $(SRCDIR)/05_conclusion
STRUCTURE := $(PROJECTDIR) $(CHDIRS) $(TEXDIR)

# Main project file
MAINFILE = $(PROJECTDIR)/main

# Filter files by their type within actual project structure
ASYFILES := $(addsuffix /*.asy, $(ASYDIR))
PYFILES := $(addsuffix /*.py, $(BINDIR))
BAKFILES := $(addsuffix /*.bak0, $(STRUCTURE))
LOGFILES := $(addsuffix /*.log, $(STRUCTURE))
LOTFILES := $(addsuffix /*.lot, $(STRUCTURE))
LOFFILES := $(addsuffix /*.lof, $(STRUCTURE))
TEXFILES := $(addsuffix /*.tex, $(STRUCTURE))
AUXFILES := $(addsuffix /*.aux,$(STRUCTURE))
OUTFILES := $(addsuffix /*.out,$(STRUCTURE))
LOGFILES := $(addsuffix /*.log,$(STRUCTURE))
TOCFILES := $(addsuffix /*.toc,$(STRUCTURE))
GZFILES := $(addsuffix /*.gz,$(STRUCTURE))
BBLFILES := $(addsuffix /*.bbl,$(STRUCTURE))
BCFFILES := $(addsuffix /*.bcf,$(STRUCTURE))
BLGFILES := $(addsuffix /*.blg,$(STRUCTURE))
BLXFILES := $(addsuffix /*blx.bib,$(STRUCTURE))
RUNFILES := $(addsuffix /*run.xml,$(STRUCTURE))
JUNKFILES := $(AUXFILES) $(OUTFILES) $(LOFFILES) $(LOTFILES) $(LOGFILES) $(TOCFILES) $(GZFILES) $(BBLFILES) $(BCFFILES) $(BLGFILES) $(BLXFILES) $(RUNFILES)

# Latex engine and compiling options
LATEXENGINE = xelatex
LATEXOPTS = -interaction=batchmode

# Bibliography engine and options
BIBENGINE = biber
BIBOPTS = -quiet

# Latex indentation engine and options
LATEXINDENT = latexindent
LATEXINDENTOPTS = -s -w -y="defaultIndent: '  '"

# Asymptote options
ASYENGINE = asy
ASYOPTS = -maxtile "(256,256)"

# Default rule
all: clean pdf

# Generates a PDF and cleans all the workspace
pdf: compile clean

# Build auxiliary and PDF files
compile:
	@echo "Building PDF file..."
	@$(LATEXENGINE) $(LATEXOPTS) $(MAINFILE)
	@$(BIBENGINE) $(BIBOPTS) $(MAINFILE)
	# Compiles twice for linking properly the bibliography
	@$(LATEXENGINE) $(LATEXOPTS) $(MAINFILE)
	@rm -f $(FIGDIR)/*.png
	@echo "Done!"

# Compile all Asymptote scripts
drawings:
	@echo "Building Asymptote drawings..."
	@$(ASYENGINE) $(ASYOPTS) $(ASYFILES)
	@echo "Copying all files to $(FIGDIR) directory..."
	@mv *.png $(FIGDIR)
	@echo "Done!"

# Compile all the binaries
binaries:
	@echo "Compiling binaries..."
	@for py_file in $(PYFILES); do\
		echo "$${py_file}";\
		python $${py_file};\
	done
	@echo "Done!"

# Reformat all the required files for good code quality
style:
	@echo "Reformating all TEX files..."
	@for tex_file in $(TEXFILES); do\
		echo "$${tex_file}";\
		$(LATEXINDENT) $(LATEXINDENTOPTS) $${tex_file};\
	done
	@echo "Cleaning log files..."
	@rm -rf $(LOGFILES) $(BAKFILES)
	@echo "Done!"

# Clean workspace by removing junk files
clean:
	@echo "Cleaning workspace..."
	@rm -f $(JUNKFILES)
	@rm -f $(FIGDIR)/*.png
	@echo "Done!"
