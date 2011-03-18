from unittest import TestCase

from pandac.PandaModules import Vec3, Point3

from Utils import (
  tupleToVec3,
  vec3ToTuple,
  tripleToVec3,
  vec3ToTriple,
  point3ToTuple,
  addTuples,
  scaleTuple,
  tupleMiddle,
  tupleSegment,
  tupleLength,
  tupleLengthSquared,
  tupleDistance,
  tupleDistanceSquared,
  tupleNormalize,
  dotProduct,
  normalizedDotProduct
)

class TestUtils(TestCase):

  def setUp(self):
    pass

  def testTupleToVec3(self):
    self.failUnlessEqual( tupleToVec3( (2, 4) ), Vec3(2, 4, 0) )
    
  def testVec3ToTuple(self):
    self.failUnlessEqual( vec3ToTuple( Vec3(3, 7, 0) ), (3, 7) )

  def testTripleToVec3(self):
    self.failUnlessEqual( tripleToVec3( (1, 2, 3) ), Vec3(1, 2, 3) )

  def testVec3ToTriple(self):
    self.failUnlessEqual( vec3ToTriple( Vec3(1, 2, 3) ), (1, 2, 3) )

  def testPoint3ToTuple(self):
    self.failUnlessEqual( point3ToTuple( Point3(2, 4, 0) ), (2, 4) )
    
  def testAddTuples(self):
    self.failUnlessEqual( addTuples( (1, 4), (2, -7) ), (3, -3) )
    
  def testScaleTuple(self):
    self.failUnlessEqual( scaleTuple( (1, -4), 3 ), (3, -12) )
    
  def testTupleMiddle(self):
    self.failUnlessEqual( tupleMiddle( (2, -3), (-4, -7) ), (-1, -5) )
    
  def testTupleSegment(self):
    tuple1 = (1, 2)
    tuple2 = (-2, 3)
    segment12 = (-3, 1)
    segment21 = (3, -1)
    self.failUnlessEqual( tupleSegment( tuple1, tuple2 ), segment12 )
    self.failUnlessEqual( tupleSegment( tuple2, tuple1 ), segment21 )
  
  def testTupleLength(self):
    self.failUnlessEqual( tupleLength( (3, 4) ), 5)
    
  def testTupleLengthSquared(self):
    self.failUnlessEqual( tupleLengthSquared( (3, 4) ), 25)
    
  def testTupleDistance(self):
    tuple1 = (1, 2)
    tuple2 = (4, 6)
    distance = ( ( tuple2[0] - tuple1[0] )**2 + ( tuple2[1] - tuple1[1] )**2 )**(1/2.)
    self.failUnlessEqual( tupleDistance( tuple1, tuple2 ), distance )
    
  def testTupleDistanceSquared(self):
    tuple1 = (4, -2)
    tuple2 = (8, 0)
    distanceSquared = ( tuple2[0] - tuple1[0] )**2 + ( tuple2[1] - tuple1[1] )**2
    self.failUnlessEqual( tupleDistanceSquared( tuple1, tuple2 ), distanceSquared )
    
  def testTupleNormalize(self):
    tuple = (3, 4)
    unitTuple = (3/5., 4/5.)
    self.failUnlessEqual( tupleNormalize( tuple ), unitTuple )
    
  def testDotProduct(self):
    tuple1 = (1, 2)
    tuple2 = (2, -1)
    self.failIf( dotProduct( tuple1, tuple2 ) )
    
  def testNormalizedDotProduct(self):
    tuples = [
      ( (5.0, 5.0), (5.0, -5.0) ),
      ( (5.0, 5.0), (5.0, 5.0) ),
      ( (5.0, 5.0), (-5.0, -5.0) ),
      ( (234, 174), (1737, 2461) ),
      ( (-1, 5), (12, -5) ),
      ( (90, 0), (0, -5) ),
      ( (-10, -1), (-1, -7) )
    ]
    self.failIf( normalizedDotProduct( tuples[0][0], tuples[0][1] ) )
    self.failIf( normalizedDotProduct( tuples[1][0], tuples[1][1] ) < .999999 )
    self.failIf( normalizedDotProduct( tuples[1][0], tuples[1][1] ) > 1.000001 )
    self.failIf( normalizedDotProduct( tuples[2][0], tuples[2][1] ) > -.999999 )
    self.failIf( normalizedDotProduct( tuples[2][0], tuples[2][1] ) < -1.000001 )
    for t in tuples:
      self.failIf( normalizedDotProduct(t[0], t[1]) > 1.0 )
      self.failIf( normalizedDotProduct(t[0], t[1]) < -1.0 )
    