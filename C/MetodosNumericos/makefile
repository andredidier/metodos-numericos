CC=gcc
CFLAGS=-I.
DEPS = metodos.h 
OBJ = main.o metodos.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main: $(OBJ)
	gcc -o metodos $^ $(CFLAGS)

clear:
	rm *.o *.exe

debug: clear
debug: CFLAGS += -DDEBUG 
debug: main

release: clear
release: CFLAGS += -UDEBUG
release: main