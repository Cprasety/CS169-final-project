import time
import sudokum
import numpy
import matplotlib.pyplot as plot
import copy
from Backtracking import backtracking
from GA import genetic_algorithm, get_fitness
from SA import simulated_annealing


def generate_rand_N(num, difficulty) -> list:
    lst = []
    for i in range(num):
        puzzle = sudokum.generate(mask_rate=difficulty)
        # easy = .5, med = .6, hard = .7, expert = .8, impossible = .9
        # be careful not to set mask_rate too high if testing GA! (will take hours)
        lst.append(puzzle)
    return lst

def test_backtracking(grids):
    time_list, iter_list = [], []
    for i in grids:
        tic = time.time()
        x, iterations = backtracking(i)
        toc = time.time()
        time_list.append(toc - tic)
        print("Time taken: ", toc - tic)
        print("Number of iterations: ", iterations)
        iter_list.append(iterations)
    return time_list, iter_list

def test_simulated_annealing(grids):
    time_list, iter_list = [], []
    for i in grids:
        tic = time.time()
        err, iterations = simulated_annealing(numpy.array(i))
        toc = time.time()
        time_list.append(toc - tic)
        iter_list.append(iterations)
        print("Time taken: ", toc - tic)
        print("Number of iterations: ", iterations)
    return time_list, iter_list

def test_genetic_algorithms(grids):
    time_list, iter_list = [], []
    for i in grids:
        tic = time.time()
        r, iterations = genetic_algorithm(i)
        m = max([get_fitness(c) for c in r])
        for c in r:
            if get_fitness(c) == m:
                toc = time.time()
                # print(c)
                time_list.append(toc - tic)
                iter_list.append(iterations)
                print("Time taken: ", toc - tic)
                print("Number of iterations: ", iterations)
                break
    return time_list, iter_list



def plot_data(num, difficulty):
    bt_time, bt_iter, ga_time, ga_iter, sa_time, sa_iter = [], [], [], [], [], []
    for diff in difficulty:
        N = generate_rand_N(num, diff)
        p1, p2, p3 = copy.deepcopy(N), copy.deepcopy(N[0:1]), copy.deepcopy(N)
        t1, i1 = test_backtracking(p1)
        bt_time.append(numpy.mean(t1))
        bt_iter.append(numpy.mean(i1))
        t2, i2 = test_genetic_algorithms(p2)
        ga_time.append(numpy.mean(t2))
        ga_iter.append(numpy.mean(i2))
        t3, i3 = test_simulated_annealing(p3)
        sa_time.append(numpy.mean(t3))
        sa_iter.append(numpy.mean(i3))
    plot.plot(difficulty, bt_time, label="backtracking")
    plot.plot(difficulty, ga_time, label="genetic_algorithm")
    plot.plot(difficulty, sa_time, label="simulated_annealing")
    plot.xlabel("difficulty")
    plot.ylabel("time")
    plot.legend()
    plot.show()

    plot.plot(difficulty, bt_iter, label="backtracking")
    plot.plot(difficulty, ga_iter, label="genetic_algorithm")
    plot.plot(difficulty, sa_iter, label="simulated_annealing")
    plot.xlabel("difficulty")
    plot.ylabel("iterations")
    plot.legend()
    plot.show()

    # test_genetic_algorithms(N)
    # test_simulated_annealing(N)

def main():
    num = 5 # input
    difficulty = [.4, .45, .5, .55, .6]  # input (lower diff numbers = more clues: 0 - solved < 1 - impossible)
    for diff in difficulty:
    #     diff -= .25
          diff /= 2
    plot_data(num, difficulty)

if __name__ == "__main__":
    main()