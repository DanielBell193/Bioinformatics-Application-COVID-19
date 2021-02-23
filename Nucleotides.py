import matplotlib.pyplot as plt
import numpy as np
import StandardFunctions as sf

# Constants - appropriate referencing (e.g. iteration, print, file name, visual)
BASE = ['A', 'C', 'G', 'T']  # Nitrogenous Bases
BASE_NAME = {"A": "Adenine", "C": "Cytosine", "G": "Guanine", "T": "Thymine"}
POLYNUCLEOTIDE = {1: "Nucleotide", 2: "Dinucleotide", 3: "Trinucleotide", 4: "Tetranucleotide", 5: "Pentanucleotide"}
POLYMER = {1: "monomers", 2: "dimers", 3: "trimers", 4: "tetramers", 5: "pentamers"}  # lower-case for file names
COLOUR_MAP = ["red", "green", "blue", "yellow", "purple"]


def base_combinations(polymer_length):
    """Accumulator method for invoking recursive method (memory efficiency).
    Exception Handling: ensures at least dimers are passed.

    :param int polymer_length: length of all polymer instances (e.g. 2 - dimers)
    :return list combinations: all possible polymers, each of a given 'polymer_length'
    """
    if polymer_length <= 1 or not (isinstance(polymer_length, int)):  # checks whole number is above 1
        print("Warning in Nucleotides.py: must pass a positive whole number >= 2")
        return  # Excepton Handling

    combinations = []  # Appended to by bases_combination_recursive(), externally
    base_combinations_recursive("", polymer_length, combinations)

    return combinations


def base_combinations_recursive(polymer, polymer_length, combinations):
    """Generates all possible polymers possible, each of a 'polymer_length'.
    Each recursion, we append a complete 'polymer' to 'combinations'.
    We pass 'combinations' back to 'base_combinations()' and drop the Stack.
    Stack does not need to be unravelled, once threshold is met, per iteration.

    :param str polymer: an instance of a base combination passed to next recursion and appended to 'combinations'; initially blank ("")
    :param int polymer_length: length of all polymer instances (e.g. 2 - dimers)
    :param list combinations: all possible polymers, each of a given 'polymer_length'
    :return list combinations
    """
    # Base case - run out of character space for each 'polymer'
    if polymer_length == 0:
        combinations.append(polymer)
        # print(polymer)  # Complete polymer instance
        return  # continue back to previous recursion's active for loop iteration

    # Starting with all that begin with 'A' ...
    for i in range(len(BASE)):
        # Next Base appended
        new_polymer = polymer + BASE[i]  # we build upon a new instance
        base_combinations_recursive(new_polymer, (polymer_length - 1), combinations)

    return combinations


def base_content(genome):
    """Calculates the composition of each polymer, from 'base_combination', in a given genome as a %.

    :param dict genome: dictionary containing: 'name', 'description' & 'sequence' of genome (Coronaviridae.py - .fasta/.fna file)
    """
    print("\n-- " + genome['name'] + " --")  # name
    print(genome['description'])
    print(genome['sequence'])

    for n in BASE:
        n_count = genome['sequence'].count(n)
        n_comp = round(n_count / len(genome['sequence']) * 100, 2)
        print(BASE_NAME[n] + " Composition: " + str(n_comp) + "%")

    bases_content_plot(genome['name'], genome['sequence'])


def bases_content_plot(name, sequence):
    """Nitrogenous Bases - AT/GC Ratio:
    Guanine & Cytosine as % of DNA (always paired together),
    Adenine & Thymine as % of DNA (always paired together).

    :param str name: official viral name
    :param list sequence: genome broken down as individual monomer bases
    """
    # Data
    gc = ((sequence.count("G") + sequence.count("C")) / len(sequence)) * 100  # GC Content (%)
    at = ((sequence.count("A") + sequence.count("T")) / len(sequence)) * 100  # AT Content (%)
    # ratio = (sequence.count("A") + sequence.count("T")) / (sequence.count("G") + sequence.count("C"))

    # Plot
    plt.title(name + " Nitrogenous Base Pairs")
    plt.ylabel("Content as Percentage (%)")
    x = ["G-C Content", "A-T Content"]
    y = [gc, at]
    plt.bar(x, y, color='blue')

    # Display & Save
    fig = plt.gcf()
    plt.show()
    plt.draw()
    fig.savefig('data\\Content\\content_' + name + '.png', format='png')


def composition_comparison(base_combinations, *genomes):
    """Plots a chart - Normalised polynucleotide frequences of bases composition, for n genomes of interest.

    :param list base_combinations: holds 'base_combinations()' output array, x axis
    :param ndarray genomes: array holds genome dictionaries, to be plotted ('*' >=1 genomes)
    """
    # To display relevant labels
    n = len(base_combinations[0])  # no. bases in each polymer
    n_coronavirus = "Coronaviridae" if len(genomes) > 1 else "Coronavirus"  # plural or singular

    # Plot
    plt.figure(figsize=(50, 25))
    plt.title(POLYNUCLEOTIDE[n] + " Composition of " + n_coronavirus, fontsize=15)

    # X axis
    plt.xlabel(POLYNUCLEOTIDE[n], fontsize=10)
    plt.xticks(rotation=45)

    # Y axis
    plt.ylabel("Normalised " + POLYNUCLEOTIDE[n] + " Frequency", fontsize=10)
    plt.yticks(np.arange(0, 0.25, 0.01))
    plt.ylim(0, 0.25)

    for g, c in zip(genomes, COLOUR_MAP):
        # Parallel iteration - g (dictionaries in 'genomes') & c (colours in 'COLOUR_MAP')
        nf = normalised_frequencies(base_combinations, g)
        plt.plot(base_combinations, nf, linewidth=2, color=c, label=g['name'])
    plt.legend()

    plt.grid(True)

    # Display & Save
    fig = plt.gcf()
    plt.show()
    plt.draw()

    output_name = sf.output_name(genomes)  # Appended to output filename
    fig.savefig('data\\Composition\\' + POLYNUCLEOTIDE[n] + output_name + '.png', format='png')


def normalised_frequencies(base_combinations, genome):
    """Calculates no. appearances each polymer, as a subsequence, appears in a given genome, as a %.
    Stores .csv - headers = polymers, nf = content (filename "nf_[polymers]_[coronavirus].csv").

    :param list base_combinations: holds 'base_combinations()' output array, x axis
    :param dict genome: dictionary containing: 'name', 'description', 'sequence' of genome (Coronaviridae.py - .fasta/.fna file)
    :return ndarray normalised_freq: infinitesimals, for each polymer, to be plotted in 'composition_comparison()'
    """
    n = len(base_combinations[0])  # no. nucleotide units in polymer
    sequence = ''.join(genome['sequence'])  # concatenates char members of genome as a string object

    normalised_freq = []
    for p in base_combinations:
        count = sequence.count(p)
        nf = (count * n) / len(sequence)
        normalised_freq.append(nf)

    # Store file - list of polymers & normalised frequency scores
    np.savetxt('data\\Normalised Frequency\\nf_' + POLYMER[n] + '_' + genome['name'] + '.csv', normalised_freq,
               delimiter=',')

    return normalised_freq
