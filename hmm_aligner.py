#!/usr/bin/env python
import sys#, random
from collections import defaultdict

# Default threshold: 0.5, num_sents = sys.maxint
def align(train, english, chinese, num_sents, num_iterations, num_outputs):
    f_data = "%s.%s" % (train, chinese)
    e_data = "%s.%s" % (train, english)
    
    sys.stderr.write("Training using IBM Model 1...\n")
    bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:num_sents]]
    
    t = {} # Probabilities    
    for iteration in range(num_iterations):       
        e_count = defaultdict(int)
        ec_count = defaultdict(int)         
        
        # Expectation step
        for (k, (c, e)) in enumerate(bitext):
            #e.insert(0, "<NULL>")
            for c_i in c:
                
                delta_denom = 0.0
                for e_j in e:
                    if (iteration == 0):
                        t[(c_i, e_j)] = 1.0#random.random()
                                            
                    delta_denom += t[(c_i, e_j)] 
                
                for e_j in e:                    
                    delta = t[(c_i, e_j)] / delta_denom
                    
                    ec_count[(e_j, c_i)] += delta
                    e_count[e_j] += delta

            if k % 500 == 0:
                sys.stderr.write("%d-%d\n" % (iteration, k))
    
        # Maximization step
        for (e, c) in ec_count:
            t[(c, e)] = ec_count[(e, c)] / e_count[e]

    sys.stderr.write("E-M training finished.\nOutputting aligned pairs...\n")    
    for (c, e) in bitext[:num_outputs]:
        for (i, c_i) in enumerate(c):
            #e.insert(0, "<NULL>")
            
            max_prob = 0.0
            best_alignment = "0-0"
            for (j, e_j) in enumerate(e):
                if t[(c_i, e_j)] >= max_prob:
                    max_prob = t[(c_i, e_j)]
                    best_alignment = "%i-%i " % (i, j)
                    
            sys.stdout.write(best_alignment)
            
        sys.stdout.write("\n")
    
    sys.stderr.write("Done.\n")
