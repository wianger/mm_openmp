CXX = g++
CXXFLAGS = -fopenmp
LIBS = -lopenblas
SRCDIR = src
TARGETDIR = build
SRCS = $(wildcard $(SRCDIR)/*.cc)
TARGET = $(patsubst $(SRCDIR)/%.cc,$(TARGETDIR)/%,$(SRCS))

all: $(TARGET)

$(TARGETDIR)/%: $(SRCDIR)/%.cc
	@mkdir -p $(TARGETDIR)
	$(CXX) $(CXXFLAGS) $< -o $@ $(LIBS)

clean:
	rm -rf $(TARGETDIR)
	rm -f result/*.png result*.pdf

.PHONY: all clean