# Interpolation
# Takes start/end RGB and number of steps to interpolate
def interpolateColors(startColor,endColor,totalBlocks):
    startR,startG,startB = startColor
    endR,endG,endB = endColor
    diffR,diffG,diffB = endR-startR,endG-startG,endB-startB
    colors = []

    for i in range(0, totalBlocks+1):
        r = startR+i*diffR/totalBlocks
        g = startG+i*diffG/totalBlocks
        b = startB+i*diffB/totalBlocks
        colors.append((r,g,b))

    return colors
