import colorsys

def rgb_to_decimal( r:int, g:int, b:int ):
    return round(r/255, 1), round(g/255, 1), round(b/255, 1)

def sv_num_fix(n: float):
    return int(round(n*254, 0))

def hue_num_fix(n: float):
    return int(round(n*65535, 0))

def rgb_to_hsv( r:int, g:int, b:int ):
    R, G, B = rgb_to_decimal(r, g, b)
    H, S, V = colorsys.rgb_to_hsv(R, G, B)
    return hue_num_fix(H), sv_num_fix(S), sv_num_fix(V)
