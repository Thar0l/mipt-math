#include <iostream>
#include <eigen3/Eigen/Dense>
#include <cmath>

using Eigen::MatrixXd;


struct Maxitem
{
		int x;
		int y;
		double value;
};


double ABS(double i)
{
		if (i > 0) return i;
		return -i;
}


MatrixXd createRotationMatrix(int size, int x, int y, double angle);
MatrixXd createMatrix(int size);
MatrixXd Rotate(MatrixXd U, MatrixXd T);
Maxitem getMax(MatrixXd M, int size);
MatrixXd Iterate(MatrixXd A, int size);
double getEps(MatrixXd oldm, MatrixXd newm, int size);



int main()
{
		int size = 3;	
		std::cin >> size;
		MatrixXd A(size, size);
//		A << 1,2,0, 2,1,3, 0,3,1;

		for (int i = 0; i < size; i++) 
				for (int j = 0; j < size; j++)
						std::cin >> A(i,j);
		//		std::cout << "A" << std::endl << A << std::endl;
		bool square = false;
		if (A != A.transpose()) 
		{
				A = A*A.transpose();
				square = true;
//				std::cout << "A" << std::endl << A << std::endl;
		}
		double e = 0.00001;
		std::cin >> e;
		//for (int i = 0; i < 10; i++)
		int i =0;
		double eps = 0.0;
		

		MatrixXd B = A;
		do
		{
				i++;
//				std::cout << "_________________________________________________" << std::endl;
//				std::cout << "Iteration " << i << std::endl;
				B = Iterate(A, size);
				eps = getEps(A, B, size);
				A = B;
//				std::cout << "Eps = " << eps << std::endl;
		} while (eps > e);
		for (int i = 0; i< size; i++)
		{
				if (!square) 
						std::cout << A(i,i);
				else
						std::cout << sqrt(A(i,i));
				std::cout << std::endl;
		}
}

MatrixXd Iterate(MatrixXd A, int size)
{
		Maxitem max = getMax(A, size);
//		std::cout << "Max: A[" <<  max.x << "][" << max.y << "] = " << max.value << std::endl;
		double alpha = std::atan(2*A(max.x, max.y)/(A(max.x, max.x) - A(max.y, max.y)))/2;
//		std::cout << "Alpha = " << alpha << std::endl;
		MatrixXd T = createRotationMatrix(size, max.x, max.y, alpha);
//		std::cout << "T" << T << std::endl;
		MatrixXd B = Rotate(A, T);
//		std::cout << "A" << std::endl << B << std::endl;
		return B;
}



MatrixXd createMatrix(int size)
{
		MatrixXd m = MatrixXd::Random(size, size);
		return m; 
}



MatrixXd createRotationMatrix(int size, int x, int y, double angle)
{
		MatrixXd R = MatrixXd::Identity(size, size);
		R(x,x) =  cos(angle);
  R(x,y) = -sin(angle);
  R(y,x) =  sin(angle);
  R(y,y) =  cos(angle);
		return R;
}



MatrixXd Rotate(MatrixXd U, MatrixXd T)
{
		return (T.transpose()*U)*T;
}



Maxitem getMax(MatrixXd M, int size)
{
		Maxitem max;
		max.x = 0;
		max.y = 0;
		max.value = -1.0;
		for (int i = 0; i < size; i++)
		{
				for (int j = 0; j < size; j++)
				{
//						std::cout << "! " << i << " : " << j << "A(i,j) = " << M(i,j) << std::endl;
						if (i != j)
						if (ABS(M(i,j)) > max.value)
						{
								max.value = ABS(M(i,j));
								max.x = i;
								max.y = j;
//								std::cout << " !!! " << max.value << std::endl;
						}
				}
		}
		return max;
}



double getEps(MatrixXd oldm, MatrixXd newm, int size)
{
		double eps = 0.0;
		for (int i = 0; i < size; i++)
		{
//				std::cout << (double)(ABS(newm(i,i))) << " _ " << ABS(oldm(i,i)) << std::endl;
				if (eps < ABS(ABS(newm(i,i)) - ABS(oldm(i,i)))) 
						eps = ABS(ABS(newm(i,i)) - ABS(oldm(i,i)));
		}
		return eps;
}
