import sys, dice_aligner, ibm_model_1_aligner, score_calculator, converter

output_file = "train.dice"

# Redirect stdout to output file
stdout = sys.stdout
sys.stdout = open(output_file, "w")

#dice_aligner.align("train", "english", "chinese", 0.5, sys.maxint)
#dice_aligner.align("train", "english", "chinese", 0.5, 100)
ibm_model_1_aligner.align("train", "english", "chinese", 200000, 20, 1000)

# Restore stdout redirection
sys.stdout.close()
sys.stdout = stdout

score_calculator.print_score("train.alignment", output_file)
