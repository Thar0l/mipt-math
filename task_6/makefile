THREADS = 1
generate: parallel_diffusion_equation.cpp
	mpiCC parallel_diffusion_equation.cpp -o generate
graph: parallel_diffusion_equation_graph.cpp
	g++ parallel_diffusion_equation_graph.cpp -lsfml-graphics -lsfml-window -lsfml-system -o graph
run: generate graph
	mpirun -n $(THREADS) ./generate
	./graph
clean:
	rm generate graph