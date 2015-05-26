#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <iostream>
#include <fstream>
#include <math.h>


class Tab 
{
private:
    double* matrix;
    int M, N;
public:
    Tab (){}

    ~Tab()
    {
        delete (matrix);
    }

    void init(int m, int n)
    {
        M = m;
        N = n;
        matrix = new double[m*n];
    }

    void set(int m, int n, double x)
    {
        matrix[N*m + n] = x;
    }

    double get(int m, int n)
    {
        return matrix[N*m + n];
    }

    int getm()
    {
        return M;
    }

    int getn()
    {
        return N;
    }

    double* getmatrix()
    {
        return matrix;
    }

    double* get_addr_for_add(int to_add){
        matrix = (double*)  realloc(matrix, (M + to_add - 1)*N*sizeof(double));
        double* ptr = (matrix + (M-1)*(N) );
        M += to_add - 1;
        return ptr;
    }

    void print()
    {
        std::ofstream file;
        file.open ("example.txt");
        file << getn() << std::endl << getm() << std::endl;
        for (int n = 0; n < N; n++)
        {
            for (int m = 0; m < M; m++ )
            {
                file << (this->get(m, n)) << " ";
            }
            file << std::endl;
        }
        file << std::endl;
        file.close();
    }

};

double f_right(int m, int n)
{
    return 0.0;
}

double scheme(int m, int n, double h, double t, class Tab& matrix)
{
    return ( f_right(m, n) - (matrix.get(m, n) - matrix.get(m-1, n)) / h )*t + matrix.get(m, n);
}


int main(int argc, char **argv)
{
    MPI::Init(argc, argv);
    int size = MPI::COMM_WORLD.Get_size();
    int rank = MPI::COMM_WORLD.Get_rank();

    double XMIN = 0.0;
    double XMAX = 1.0;
    double tmin = 0.0;
    double tmax = 1.0;

    double h = 0.004;
    double t = 0.00014;

    int Nx = (int)((XMAX - XMIN)/h);
    int Nt = (int)((tmax - tmin)/h);

    double xmin = 0;
    double xmax = 0;

    xmin = Nx / size * (rank);

    if (rank == size -1)
        xmax = Nx;
    else
        xmax = (Nx / size)*(rank + 1);

    int r = size-1;

    for (int i = (Nx % size-1); i > 0; i--)
    {
        if (rank >= r)
            xmin++;
        if (rank >= r-1 && rank != size - 1)
            xmax++;
        r--;
    }

    Tab tab;

    if (rank == 0)
    {
        tab.init((xmax - xmin + 1),(int)((tmax - tmin)/t));
        
        double s = 0.2;
        for(int i = 0; i < (xmax - xmin + 1); i++)
            tab.set(i, 0, 1.0/sqrt(2.0*3.14159*s)*exp(-((i*h-0.5)*(i*h-0.5)/2.0/s/s)));
    }
    else
    {
        tab.init((xmax - xmin + 1),(int)((tmax - tmin)/t));
        double s = 0.2;
        for(int j = 0; j < (xmax - xmin + 1); j++)
        {
            int i = j+xmin;
            tab.set(j, 0, 1.0/sqrt(2.0*3.14159*s)*exp(-((i*h-0.5)*(i*h-0.5)/2.0/s/s)));
        }
    }

    double starttime = 0;
    double endtime = 0;

    if (rank == 0)
        starttime = MPI_Wtime();

    for (int n = 0; n < tab.getn()-1; n++)
    {
        double buf = 0;

        if (n > 0 && rank > 0)
        {
            MPI::COMM_WORLD.Recv(&buf, 1, MPI_DOUBLE, rank - 1, 0);
            tab.set(0, n, buf);
        }
        for (int m = 1; m < tab.getm(); m++)
        {
            tab.set(m, n +1, scheme(m, n, h, t, tab));
        }

        buf = tab.get(tab.getm()-1, n+1);

        if (rank < size-1)
        {
            MPI::COMM_WORLD.Isend(&buf, 1, MPI_DOUBLE, rank + 1, 0);
        }

    }
        endtime = MPI_Wtime();
    if (rank > 0)
    {
        int M = tab.getm();
        MPI::COMM_WORLD.Send(&M, 1, MPI_INT, 0, 0);
        MPI::COMM_WORLD.Send(tab.getmatrix(), tab.getn()*tab.getm(), MPI_DOUBLE, 0, 0);
    }
    if (rank == 0 & size > 1)
    {
        MPI_Status status;
        int matrixM = 0;
        for (int i = 1; i < size; i++)
        {
            MPI::COMM_WORLD.Recv(&matrixM, 1, MPI_INT, i, 0);
            MPI::COMM_WORLD.Recv(tab.get_addr_for_add(matrixM), tab.getn()*matrixM, MPI_DOUBLE, i, 0);
        }
    }

    if (rank == 0)
        endtime = MPI_Wtime();

    if (rank == 0){
        std::cout << "Time = " << endtime - starttime << std::endl;
        tab.print();
    }

    MPI::Finalize();
    return 0;
}