CC=gcc
CFLAGS=-I. -lm
DEPS = metodos.h 
OBJ = $(wildcard *.o)

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

all: $(OBJ)
	gcc -o metodos $^ $(CFLAGS)

clear:
	rm *.o *.exe

debug: clear
debug: CFLAGS += -DDEBUG 
debug: main

release: clear
release: CFLAGS += -UDEBUG
release: main
