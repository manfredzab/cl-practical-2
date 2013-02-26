import sys

def symmetrize(forward_file, backward_file):
    neighboring_points = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
    for (forward_alignment, backward_alignment) in zip(open(forward_file), open(backward_file)):                       
        forward_set = set(forward_alignment.strip().split())
        backward_set = set(backward_alignment.strip().split())
        
        union = forward_set.union(backward_set)

        # grow-diag
        current_points = forward_set.intersection(backward_set)        
        
        while True: # iterate until no new points are added
            new_points_added = False
            
            for ce in current_points.copy():
                (c, e) = ce.split('-')
                
                for (delta_c, delta_e) in neighboring_points:                    
                    (c_new, e_new) = (str(int(c) + delta_c), str(int(e) + delta_e))                     
                    
                    if (c_new, e_new) in union:
                        if (not is_c_covered(current_points, c_new)) or (not is_e_covered(current_points, e_new)):
                            current_points.add("%s-%s" % (c_new, e_new))
                            new_points_added = True
                            
            if not new_points_added:
                break
        
        # final-and
        for ce in union:
            (c, e) = ce.split('-')

            if (not is_c_covered(current_points, c)) and (not is_e_covered(current_points, e)): # for "final" change the "and" in this line to "or"
                current_points.add("%s-%s" % (c, e))
                        
        sys.stdout.write(' '.join(current_points) + '\n')
        
        
def is_c_covered(point_set, c):
    for ce in point_set:
        if (ce.split('-')[0] == c):
            return True
    
    return False


def is_e_covered(point_set, e):
    for ce in point_set:
        if (ce.split('-')[1] == e):
            return True
    
    return False