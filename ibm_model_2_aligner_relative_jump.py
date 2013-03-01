#!/usr/bin/env python
import sys, random
from collections import defaultdict

def align(train, english, chinese, num_sents, num_iterations, num_outputs, reverse_output):
    alpha = 0.5
        
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
        i_count = defaultdict(int)
        
        # Expectation step
        for (k, (c, e)) in enumerate(bitext):
            l = len(e)
            
            for (i, c_i) in enumerate(c):
                
                delta_denom = 0.0
                for (j, e_j) in enumerate(e):
                    if (iteration == 0):
                        t[(c_i, e_j)] = random.random()
                        q[(j - i, l)] = random.random()
                                            
                    delta_denom += t[(c_i, e_j)] * (alpha / float(l) + (1.0 - alpha) * q[(j - i, l)])  
                
                for e_j in e:
                    delta = t[(c_i, e_j)] * (alpha / float(l) + (1.0 - alpha) * q[(j - i, l)]) / delta_denom
                    
                    ec_count[(e_j, c_i)] += delta
                    e_count[e_j] += delta
                    ji_count[(j - i, l)] += delta
                    i_count[l] += delta

            if k % 500 == 0:
                sys.stderr.write("%d-%d\n" % (iteration, k))
    
        # Maximization step
        for (e, c) in ec_count:
           
            t[(c, e)] = ec_count[(e, c)] / e_count[e]
            
        for (i, l) in ji_count:
            q[(i, l)] = ji_count[(i, l)] / i_count[l] 

    sys.stderr.write("E-M training finished.\nOutputting aligned pairs...\n")
    
    for (c, e) in bitext[:num_outputs]:
        l = len(e)
                
        for (i, c_i) in enumerate(c):
                        
            max_prob = 0.0
            best_alignment = "0-0"
            
            for (j, e_j) in enumerate(e):
                prob = t[(c_i, e_j)] * (alpha / float(l) + (1.0 - alpha) * q[(j - i, l)])
                
                if prob >= max_prob:
                    max_prob = prob
                    best_alignment = "%i-%i " % ((i, j) if not reverse_output else (j, i))
                    
            sys.stdout.write(best_alignment)
            
        sys.stdout.write("\n")
    
    sys.stderr.write("Done.\n")
