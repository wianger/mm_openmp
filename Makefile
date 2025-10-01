CXX = g++
CXXFLAGS = -fopenmp
SRCDIR = src
TARGETDIR = build
SRCS = $(wildcard $(SRCDIR)/*.cc)
TARGET = $(patsubst $(SRCDIR)/%.cc,$(TARGETDIR)/%,$(SRCS))

all: $(TARGET)

$(TARGETDIR)/%: $(SRCDIR)/%.cc
	$(CXX) $(CXXFLAGS) $< -o $@
	g++ -I"C:\Scoop\apps\msys2\current\mingw64\include\openblas" -L"C:\Scoop\apps\msys2\current\mingw64\lib" -O3 -o build/openblas_gemm.exe src/openblas_gemm.cpp -lopenblas

clean:
	rm $(TARGETDIR)
	rm ./result/*.png ./result/*.pdf

.PHONY: all clean