import sys, aligner, score_calculator, combinator, converter

number_of_sentences = 300000
number_of_em_iterations = 10
number_of_outputs = 3265

forward_file = "forward.dice"
backward_file = "reverse.dice"
combined_file = "train.dice"

aligner.align(True, forward_file, number_of_sentences, number_of_em_iterations, number_of_outputs)
aligner.align(False, backward_file, number_of_sentences, number_of_em_iterations, number_of_outputs)

score_calculator.print_score("train.alignment", forward_file)
score_calculator.print_score("train.alignment", backward_file)

stdout = sys.stdout
sys.stdout = open(combined_file, "w")

combinator.symmetrize(forward_file, backward_file)#

# Restore stdout redirection
sys.stdout.close()
sys.stdout = stdout

score_calculator.print_score("train.alignment", combined_file)
