import sys, dice_aligner, ibm_model_1_aligner, ibm_model_2_aligner, ibm_model_2_aligner_relative_jump

def align(forward, output_file, number_of_sentences, number_of_em_iterations, number_of_outputs):
    # Redirect stdout to output file
    stdout = sys.stdout
    sys.stdout = open(output_file, "w")

    if (forward):
        target = "english"
        source = "chinese"
    else:
        target = "chinese"
        source = "english"

    ibm_model_2_aligner.align("train", target, source, number_of_sentences, number_of_em_iterations, number_of_outputs, not forward)

    # Restore stdout redirection
    sys.stdout.close()
    sys.stdout = stdout
