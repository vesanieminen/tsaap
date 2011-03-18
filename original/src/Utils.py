from pandac.PandaModules import Vec3

def tupleToVec3(tuple):
  return Vec3( tuple[0], tuple[1], 0 )
  
def vec3ToTuple(vec3):
  return ( vec3[0], vec3[1] )

def tripleToVec3(triple):
  return Vec3( triple[0], triple[1], triple[2] )

def vec3ToTriple(vec3):
  return ( vec3[0], vec3[1], vec3[2] )

def point3ToTuple(point):
  return ( point[0], point[1] )
  
def addTuples(tuple1, tuple2):
  return ( tuple1[0] + tuple2[0], tuple1[1] + tuple2[1] )
  
def scaleTuple(tuple, scale):
  return ( tuple[0]*scale, tuple[1]*scale )
  
def tupleMiddle(tuple1, tuple2):
  return ( (tuple1[0] + tuple2[0])/2., (tuple1[1] + tuple2[1])/2. )
  
def tupleSegment(tuple1, tuple2):
  return ( tuple2[0] - tuple1[0], tuple2[1] - tuple1[1] )
  
def tupleLength(tuple):
  return ( tuple[0]**2 + tuple[1]**2 )**(1/2.)
  
def tupleLengthSquared(tuple):
  return tuple[0]**2 + tuple[1]**2
  
def tupleDistance(tuple1, tuple2):
  return ( ( tuple2[0] - tuple1[0] )**2 + ( tuple2[1] - tuple1[1] )**2 )**(1/2.)
  
def tupleDistanceSquared(tuple1, tuple2):
  return ( tuple2[0] - tuple1[0] )**2 + ( tuple2[1] - tuple1[1] )**2
  
def tupleNormalize(tuple):
  length = tupleLength(tuple)
  if length == 0: return 1.0
  return ( tuple[0]/length, tuple[1]/length )
  
def dotProduct(tuple1, tuple2):
  return tuple1[0]*tuple2[0] + tuple1[1]*tuple2[1]
  
def normalizedDotProduct(tuple1, tuple2):
  lengths = tupleLength(tuple1)*tupleLength(tuple2)
  if lengths == 0: return 1.0
  return ( tuple1[0]*tuple2[0] + tuple1[1]*tuple2[1] ) / lengths

def tupleFurthestDistance(target, sources):
  # First we mark the distance as None
  dist = None
  # Same for source, which is the variable we'll be returning at the end
  source = None
  # Then we iterate through all the sources that are given
  for s in sources:
    # If dist is None then set it to the distance from s in sources to target
    # and set source (the one to be returned) to s
    if dist == None:
      dist = tupleDistanceSquared( s, target )
      source = s
    # Otherwise compare the distance from s to target and see if it is more
    # than dist
    else:
      d = tupleDistanceSquared( s, target )
      # If it is more than dist, then set dist to the new distance and source
      # to s
      if d > dist:
        dist = d
        source = s
  # Finally we return the source with the greatest distance to target
  return source
