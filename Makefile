CXX = g++
CXXFLAGS = -fopenmp
SRCDIR = src
TARGETDIR = build
SRCS = $(wildcard $(SRCDIR)/*.cc)
TARGET = $(patsubst $(SRCDIR)/%.cc,$(TARGETDIR)/%,$(SRCS))

all: $(TARGET)

$(TARGETDIR)/%: $(SRCDIR)/%.cc
	@mkdir -p $(TARGETDIR)
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -rf $(TARGETDIR)
	rm -f result/*.png result*.pdf

.PHONY: all clean