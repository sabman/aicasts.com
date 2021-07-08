# for a signal s
def norm_me(s):
    s_norm = (s - s_min) / (s_max - s_min)

def norm_transform(s_norm)
    t = s_norm * (t_max - t_min) + t_min
