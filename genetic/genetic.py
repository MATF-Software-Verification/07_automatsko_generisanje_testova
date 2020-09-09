
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

		#print(self.GENES)



	def initilization_of_population(self, pop_size, c_size):
		population = []
		for i in range(pop_size):
			# ----------------- With bytes -----------------
			# chromosome = bytearray('\x00' + ''.join(chr(random.randint(0,255)) for _ in range(c_size)) + '\x00', 'utf-8').decode('utf8')
			# chromosome = np.random.bytes(c_size)



			chromosome = ''.join(random.choices(self.GENES, k = c_size))

			print('[' + chromosome + ']')

			population.append(chromosome)


		return population

	def fitness_score(self, population):
		scores = []
		for chromosome in population:
			# Here we get accuracy score, tricky messy part

			score = self.executor.get_score(chromosome);

			print('Score for input', chromosome, score)

			scores.append(score)
		population = [x for _,x in sorted(zip(scores,population))]
		scores.sort()
		#print(population, scores)
		return scores, population  #reverse list

	def selection(self, pop_after_fit, n_parents):
		population_nextgen = []
		for i in range(n_parents):
			population_nextgen.append(pop_after_fit[i])
		return population_nextgen

	def crossover(self, pop_after_sel):
		population_nextgen=pop_after_sel
		for i in range(len(pop_after_sel)):
			child = pop_after_sel[i][:len(pop_after_sel[i])//2]

			child += pop_after_sel[(i+1)%len(pop_after_sel)][len(pop_after_sel[i])//2:]
			# child.append(pop_after_sel[(i+1)%len(pop_after_sel)])


			# child[3:5] = pop_after_sel[(i+1)%len(pop_after_sel)][3:7]
			population_nextgen.append(child)
		return population_nextgen



	def mutation(self, pop_after_cross, mutation_rate):
		population_nextgen = []
		for i in range(0,len(pop_after_cross)):
			chromosome = pop_after_cross[i]
			# for j in range(len(chromosome)):
					# if random.random() < mutation_rate:
					# 	global GENES

					# 	# --- With bytes ---
					# 	# chromosome[j] =  random.randint(0,255)
					# 	# ------------------

					# 	chromosome += random.choice(GENES)
					# 	# chromosome.replace(chromosome[j],random.choice(GENES))

					# 	# print(chromosome)
			if random.random() < mutation_rate:
				# Had trouble to escape local min
					# clist = list(chromosome)
					# clist[random.randrange(len(clist))] = random.choice(self.GENES)
					# chromosome = "".join(clist)
				chromosome = ''.join(random.choices(self.GENES, k = len(chromosome)))

			population_nextgen.append(chromosome)
		#print(population_nextgen)
		return population_nextgen

	def start_evolution(self):
		best_chromo = []
		best_score = []
		population_nextgen = self.initilization_of_population(self.pop_size, self.c_size)
		for i in range(self.n_gen):
			print('Generation no. :',i)
			scores, pop_after_fit = self.fitness_score(population_nextgen)
			pop_after_sel = self.selection(pop_after_fit,self.n_parents)
			pop_after_cross = self.crossover(pop_after_sel)
			population_nextgen = self.mutation(pop_after_cross,self.mutation_rate)
			best_chromo.append(str(pop_after_fit[-1]))
			best_score.append(scores[-1])

			#print(best_score)
			print("best chromosome so far:", str(best_chromo[-1]), best_score[-1])


			#print('Total coverage: ', len(E.executed_lines)/E.total_number_of_lines);
			self.executor.pretty_progress(len(self.executor.executed_lines), self.executor.total_number_of_lines)
		return best_chromo, best_score
