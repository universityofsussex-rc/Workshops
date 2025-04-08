EXECS=basic_mpi
MPICC?=mpicc

all: ${EXECS}

basic_mpi: basic_mpi.c
	${MPICC} -o basic_mpi basic_mpi.c

clean:
	rm ${EXECS}"