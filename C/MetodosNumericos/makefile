CC=gcc
#CFLAGS=-I. -DDEBUG
CFLAGS= -UDEBUG -I.
DEPS = metodos.h 
OBJ = main.o metodos.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main: $(OBJ)
	gcc -o metodos $^ $(CFLAGS)