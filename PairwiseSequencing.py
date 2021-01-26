import os
from math import log
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
import StandardFunctions as sf


def save(bio_type, output_name, sequencing):
    """Stores matches and their scores w/ appropriate file naming convention.

    :param str bio_type: "dna" or "protein"
    :param str output_name: segment of filename that lists virus names (e.g. "_MERS-MT387202_SARS-CoV-JQ316196")
    :param list sequencing: stores all possible matches and scores them
    """
    # Save Pairwise Sequencing
    path_filename = os.path.join('data\\Pairwise Sequencing',
                                 bio_type + output_name + '.txt')  # Defines path and filename
    output = open(path_filename, 'w')
    for a in sequencing:
        output.write(format_alignment(*a))  # Standardised format for output
    output.close()

    return


def gap_function(x, y):
    """Deducts points for gaps when matching up sequencing, using a logarithmic scale.

    :param int x: index to start of gap
    :param int y: length of gap instance
    :return: log() producing negative decimal number
    """
    if y == 0:  # Asks if there's a gap
        return 0
    elif y == 1:  # Gap
        return -2
    return -((log(y) / 2) + (2 + (y / 4)))  # Penalty


def run(bio_type, *genomes):
    """Performes Pairwise Sequencing task.
    Matches subsequences of similarity that may indicate evolutionary, functional and structural relationships.
    Higher the score, higher the relationship.

    :param bio_type: "dna" or "protein"
    :param ndarray genomes: array holds genome dictionaries, to be plotted ('*' >=1 genomes)
    """
    if bio_type.lower() == "dna":
        prefix = ""  # none
        directory = 'src/'
    elif bio_type.lower() == "protein":
        prefix = "protein_"
        directory = 'data/Syntheses/'
    else:
        print("Warning in PairwiseSequencing.py: biotype \"" + bio_type + "\" not recongnised. \nEnter \"DNA\" or \"Protein\"")
        return  # Exception Handling

    # Capture all filenames of 'bio_type'
    filenames = sf.capture_filenames(bio_type)
    # filenames = [f.split(".")[0] for f in filenames if bio_type.lower() == "dna"]  # DNA - remove .fasta/.fna and/or .<num> in name

    # Captures two 'bio_type' sequences of interest
    sequences = []  # Virus name, complete protein sequence
    for f in range(len(filenames)):
        for g in range(len(genomes)):
            if set(genomes[g]['name']).issubset(filenames[f]):
                with open(directory + filenames[f]) as s:
                    # DNA, remove top/ description line
                    seq = ''.join([sf.remove_firstline(directory + filenames[f]) if bio_type.lower() == "dna" else s.read()])  # else, protein
                    seq = seq.strip()  # removes any spacing surrounding sequence
                    # Store seqeunces of interest
                    seq_dict = {'name': genomes[g]['name'], 'sequence': seq}
                    sequences.append(seq_dict)

    # Concatenates char members of genome as a string object
    seq1 = sequences[0]['sequence']  # Target seq
    seq2 = sequences[1]['sequence']  # Query seq

    # Print Global Sequencing of our pair
    # Match Score - matched sequence chars found; otherwise - Mismatch Score
    # 5 pts, for identical characters
    # -1 pts, for non-identical character
    # -0.5 pts, when there's a new/ separate gap in the sequence
    # -0.1 pts, if when there's a next gap, right after an existing gap
    sequencing = pairwise2.align.globalmc(seq1[1:100], seq2[1:100], 5, -1, gap_function, gap_function,
                                          penalize_end_gaps=False)

    output_name = sf.output_name(genomes)  # Appended to 'path_filename', in 'save()'
    save(bio_type, output_name, sequencing)

    return