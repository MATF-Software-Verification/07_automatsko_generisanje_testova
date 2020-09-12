import random
import string


class Genetic:

	GENES = ''
	shuffleBool = True;
	debugger = None;

	def __init__(self, populationSize=10, chromosomeSize=5, parentsNumber=2, mutationRate=0.5, generationsCount=10, geneTypeList=['digits'], executor=None, debugger=None):
		self.pop_size = populationSize;
		self.c_size = chromosomeSize;
		self.n_parents = parentsNumber;
		self.mutation_rate = mutationRate;
		self.n_gen = generationsCount;
		self.executor = executor;
		self.debugger = debugger;

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



	def __initialize_population(self, pop_size, c_size):

		self.debugger.write('Initializing population of size:' + str(pop_size) + ', and chromosome size:' + str(c_size));
		population = random.sample(range(0,pop_size), pop_size);
		populationList = list(map(lambda _: ''.join(random.choices(self.GENES, k=c_size)), population));
		return populationList;

	def __get_fitness_values(self, population):

		scores = list(map(self.executor.get_score, population))

		result = list(zip (population,scores));
		result = sorted(result, key= lambda x: x[1]);

		self.debugger.log('Current fitness table:', result, color='green')


		return [e[0] for e in result], [e[1] for e in result]

	def __selection(self, pop_after_fit, n_parents):
		return pop_after_fit[len(pop_after_fit) - n_parents:]

	def __crossover(self, pop_after_sel,mutation_rate):
		population_nextgen=[]

		for i in range(self.pop_size):
			xPosition = random.randint(0, self.c_size-1);

			[first,second] = random.sample(range(0,self.n_parents),2);
			child = pop_after_sel[first][:xPosition]

			child += pop_after_sel[second][xPosition:]

			population_nextgen.append(self.__mutation(child, mutation_rate=mutation_rate))

		return population_nextgen

	def __mutation(self, chromosome, mutation_rate):
		if random.random() < mutation_rate:
			randPosition = random.randint(0, len(chromosome)-1);
			listTmp = list(chromosome)
			listTmp[randPosition] = random.choice(self.GENES)
			return ''.join(listTmp)
		else:
			return chromosome

	#public member functions
	def start_evolution(self):
		population_nextgen = self.__initialize_population(self.pop_size, self.c_size)
		for i in range(self.n_gen):
			self.debugger.log(str(i+1) + '. generation:')

			pop_after_fit, scores = self.__get_fitness_values(population_nextgen)

			pop_after_sel = self.__selection(pop_after_fit,self.n_parents)

			self.debugger.log('Selected chromosomes:', pop_after_sel, color="green")

			population_nextgen = self.__crossover(pop_after_sel, self.mutation_rate)


			self.executor.pretty_progress(len(self.executor.executed_lines), self.executor.total_number_of_lines)
			#self.executor.pretty_progress(len(self.executor.executed_functions), self.executor.total_number_of_functions)
		return 0