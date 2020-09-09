
import random
import string


class Genetic:

	GENES = ''
	shuffleBool = True;

	def __init__(self, populationSize=10, chromosomeSize=5, parentsNumber=2, mutationRate=0.5, generationsCount=10, geneTypeList=['digits'], executor=None):
		self.pop_size = populationSize;
		self.c_size = chromosomeSize;
		self.n_parents = parentsNumber;
		self.mutation_rate = mutationRate;
		self.n_gen = generationsCount;
		self.executor = executor;

		for type_of_gene in geneTypeList:
			if type_of_gene == 'alpha':
				self.GENES += string.ascii_lowercase;
			if type_of_gene == 'digits':
				self.GENES += string.digits
			if type_of_gene == 'punctuation':
				self.GENES += string.punctuation
			if type_of_gene == 'ALPHA':
				self.GENES += string.ascii_uppercase
			if type_of_gene == 'whitespace':
				self.GENES += string.whitespace

		if self.shuffleBool:
			genesList = list(self.GENES);
			random.shuffle(genesList);
			self.GENES = ''.join(genesList);



	def initilization_of_population(self, pop_size, c_size):

		popilation = random.sample(range(0,pop_size), pop_size);
		print(popilation);
		populationList = list(map(lambda _: ''.join(random.choices(self.GENES, k=c_size)), popilation));

		return populationList;

	#return value: list of tuples
	def fitness_score(self, population):
		scores = []

		scores = list(map(self.executor.get_score, population))

		result = list(zip (population,scores));
		result = sorted(result, key= lambda x: x[1]);
		print(result)
		return scores, population

	def selection(self, pop_after_fit, n_parents):
		return pop_after_fit[:n_parents]

	def crossover(self, pop_after_sel,mutation_rate):
		population_nextgen=[]

		for i in range(self.pop_size):
			xPosition = random.randint(0, self.c_size-1);

			[first,second] = random.sample(range(0,self.n_parents),2);
			child = pop_after_sel[first][:xPosition]

			child += pop_after_sel[second][xPosition:]

			population_nextgen.append(self.mutation2(child, mutation_rate=mutation_rate))

		print('population after xover', population_nextgen)
		return population_nextgen

	def mutation2(self, chromosome, mutation_rate):
		if random.random() < mutation_rate:
			randPosition = random.randint(0, len(chromosome)-1);
			listTmp = list(chromosome)
			listTmp[randPosition] = random.choice(self.GENES)
			return ''.join(listTmp)
		else:
			return chromosome


	def start_evolution(self):
		best_chromo = []
		best_score = []
		population_nextgen = self.initilization_of_population(self.pop_size, self.c_size)
		for i in range(self.n_gen):
			print('Iteration :',i+1)
			scores, pop_after_fit = self.fitness_score(population_nextgen)

			pop_after_sel = self.selection(pop_after_fit,self.n_parents)

			population_nextgen = self.crossover(pop_after_sel, self.mutation_rate)

			self.executor.pretty_progress(len(self.executor.executed_lines), self.executor.total_number_of_lines)
		return best_chromo, best_score
