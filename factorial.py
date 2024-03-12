from enum import Enum
Strategy = Enum("Strategy", ["Recursion", "Loop", "DivideAndConquer", "DivideAndConquerThreaded"])
import concurrent.futures
import time

def __FactorialRecursion(n: int) -> int:
	if n == 0:
		return 1
	return n * __FactorialRecursion(n - 1)

def __FactorialLoop(n: int) -> int:
	result = 1
	for i in range(1, n + 1):
		result *= i
	return result

def __FactorialDivideAndConquerThreaded(start: int, end: int) -> int:
	if end < start:
		raise ValueError("end must be greater than or equal to start")
	if start == end:
		return start
	if start + 1 == end:
		return start * end
	else:
		with concurrent.futures.ThreadPoolExecutor() as executor:
			future1 = executor.submit(__FactorialDivideAndConquerThreaded, start, (start + end) // 2)
			future2 = executor.submit(__FactorialDivideAndConquerThreaded, (start + end) // 2 + 1, end)
		return future1.result() * future2.result()
def __FactorialDivideAndConquer(start: int, end: int) -> int:
	if end < start:
		raise ValueError("end must be greater than or equal to start")
	if start == end:
		return start
	if start + 1 == end:
		return start * end
	else:
		return __FactorialDivideAndConquer(start, (start + end) // 2) * __FactorialDivideAndConquer((start + end) // 2 + 1, end)

def Factorial(n: int, strategy: Strategy = Strategy.Loop) -> int:
	if strategy == Strategy.Recursion:
		return __FactorialRecursion(n)
	elif strategy == Strategy.Loop:
		return __FactorialLoop(n)
	elif strategy == Strategy.DivideAndConquer:
		return __FactorialDivideAndConquer(1, n)
	elif strategy == Strategy.DivideAndConquerThreaded:
		return __FactorialDivideAndConquerThreaded(1, n)
	
def _runTest(n: int) -> None:
	allMatch = True
	expect = 0
	times = []
	# toTest = Strategy
	toTest = [Strategy.Loop, Strategy.Recursion, Strategy.DivideAndConquer]
	for s in toTest:
		start = time.time()
		r = Factorial(n, s)
		times.append(time.time() - start)
		if expect == 0:
			expect = r
		elif expect != r:
			allMatch = False
		print(f"Factorial({n}, {s}) = {str(r)[:100]}...")
	print(f"Results match: {allMatch}")
	for i, s in enumerate(toTest):
		print(f"Time for {s}: {times[i]}")
if __name__ == "__main__":
	def Help():
		print("Usage: factorial.py [OPTIONS] <number>")
		print("OPTIONS:")
		print("  -d: use divide and conquer")
		print("  -r: use recursion instead of loop")
		print("  -t: use threaded divide and conquer")
		print("  -o: override recursion limit")
		print("  -n: override max str digits")
		print("  -D: show duration")
		print("  -T: run tests")
	import sys
	if len(sys.argv) < 2:
		Help()
		# sys.set_int_max_str_digits(10 ** 9)
		# sys.setrecursionlimit(10 ** 9)
		# _runTest(1000)
		sys.exit(1)
	# defaults
	strategy: Strategy = Strategy.Loop
	runTests = False
	timeCalc = False
	for arg in sys.argv[1:-1]:
		if arg == "-d":
			strategy = Strategy.DivideAndConquer
		elif arg == "-r":
			strategy = Strategy.Recursion
		elif arg == "-t":
			strategy = Strategy.DivideAndConquerThreaded
			print("Using threaded divide and conquer is not recommended")
		elif arg == "-o":
			sys.setrecursionlimit(10 ** 9)
		elif arg == "-T":
			runTests = True
		elif arg == "-n":
			sys.set_int_max_str_digits(10 ** 9)
		elif arg == "-D":
			timeCalc = True
		else:
			print(f"Unknown option: {arg}")
			exit(1)
	try:
		if runTests:
			_runTest(int(sys.argv[-1]))
		else:
			if timeCalc:
				start = time.time()
				r = Factorial(int(sys.argv[-1]), strategy)
				print(f"Duration: {time.time() - start}")
			else:
				print(Factorial(int(sys.argv[-1]), strategy))
	except ValueError as e:
		print(e)
		Help()
		exit(1)
