#!/usr/bin/env python
import sys, random
from collections import defaultdict

# Default threshold: 0.5, num_sents = sys.maxint
def align(train, english, chinese, num_sents, num_iterations, num_outputs, reverse_output):
    f_data = "%s.%s" % (train, chinese)
    e_data = "%s.%s" % (train, english)
    
    sys.stderr.write("Training using IBM Model 2 (with relative jumps)...\n")
    bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:num_sents]]
    
    t = {} # t(c|e)    
    q = {} # q(j - i|l)
    for iteration in range(num_iterations):       
        # Translation counts (for MLE estimates)
        e_count = defaultdict(int)
        ec_count = defaultdict(int)
        
        # Alignment counts (for MLE estimates)
        ji_count = defaultdict(int)    
        i_total = 0    
        
        # Expectation step
        for (k, (c, e)) in enumerate(bitext):
            for (i, c_i) in enumerate(c):
                
                delta_denom = 0.0
                for (j, e_j) in enumerate(e):
                    if (iteration == 0):
                        t[(c_i, e_j)] = random.random()
                        q[j - i] = random.random()
                                            
                    delta_denom += t[(c_i, e_j)] * q[j - i]  
                
                for e_j in e:
                    delta = t[(c_i, e_j)] * q[j - i] / delta_denom
                    
                    ec_count[(e_j, c_i)] += delta
                    e_count[e_j] += delta
                    ji_count[j - i] += delta
                    i_total += delta

            if k % 500 == 0:
                sys.stderr.write("%d-%d\n" % (iteration, k))
    
        # Maximization step
        for (e, c) in ec_count:
            t[(c, e)] = ec_count[(e, c)] / e_count[e]
            
        for i in ji_count:
            q[i] = ji_count[i] / i_total 

    sys.stderr.write("E-M training finished.\nOutputting aligned pairs...\n")
    
    alpha = 0.1
    for (c, e) in bitext[:num_outputs]:
        l = len(e)
                
        for (i, c_i) in enumerate(c):
                        
            max_prob = 0.0
            best_alignment = "0-0"
            
            for (j, e_j) in enumerate(e):
                prob = t[(c_i, e_j)] * (alpha / float(l) + (1.0 - alpha) * q[j - i])
                
                if prob >= max_prob:
                    max_prob = prob
                    best_alignment = "%i-%i " % ((i, j) if not reverse_output else (j, i))
                    
            sys.stdout.write(best_alignment)
            
        sys.stdout.write("\n")
    
    sys.stderr.write("Done.\n")
