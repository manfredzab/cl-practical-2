#!/usr/bin/env python
import sys, random
from collections import defaultdict

# Default threshold: 0.5, num_sents = sys.maxint
def align(train, english, chinese, num_sents, num_iterations, num_outputs):
    f_data = "%s.%s" % (train, chinese)
    e_data = "%s.%s" % (train, english)
    
    sys.stderr.write("Training using IBM Model 2...\n")
    bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:num_sents]]
    
    t = {} # t(c|e)    
    q = {} # q(j|i,l,m)
    for iteration in range(num_iterations):       
        # Translation counts (for MLE estimates)
        e_count = defaultdict(int)
        ec_count = defaultdict(int)
        
        # Alignment counts (for MLE estimates)
        i_count = defaultdict(int)
        ji_count = defaultdict(int)        
        
        # Expectation step
        for (k, (c, e)) in enumerate(bitext):
            m = len(c)
            l = len(e)
                        
            for (i, c_i) in enumerate(c):
                
                delta_denom = 0.0
                for (j, e_j) in enumerate(e):
                    if (iteration == 0):
                        t[(c_i, e_j)] = random.random()
                        q[(j, i, l, m)] = random.random()
                                            
                    delta_denom += t[(c_i, e_j)] * q[(j, i, l, m)]  
                
                for e_j in e:
                    delta = t[(c_i, e_j)] * q[(j, i, l, m)] / delta_denom
                    
                    ec_count[(e_j, c_i)] += delta
                    e_count[e_j] += delta
                    ji_count[(j, i, l, m)] += delta
                    i_count[(i, l, m)] += delta

            if k % 500 == 0:
                sys.stderr.write("%d-%d\n" % (iteration, k))
    
        # Maximization step
        for (e, c) in ec_count:
            t[(c, e)] = ec_count[(e, c)] / e_count[e]
            
        for (j, i, l, m) in ji_count:
            q[(j, i, l, m)] = ji_count[(j, i, l, m)] / i_count[(i, l, m)] 

    sys.stderr.write("E-M training finished.\nOutputting aligned pairs...\n")
    
    alpha = 0.4
    for (c, e) in bitext[:num_outputs]:
        m = len(c)
        l = len(e)
                
        for (i, c_i) in enumerate(c):
                        
            max_prob = 0.0
            best_alignment = "0-0"
            
            for (j, e_j) in enumerate(e):
                prob = t[(c_i, e_j)] * (alpha / float(l) + (1.0 - alpha) * q[(j, i, l, m)])
                
                if prob >= max_prob:
                    max_prob = prob
                    best_alignment = "%i-%i " % (i, j)
                    
            sys.stdout.write(best_alignment)
            
        sys.stdout.write("\n")
    
    sys.stderr.write("Done.\n")
